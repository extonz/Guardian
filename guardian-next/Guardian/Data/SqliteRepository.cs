using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Guardian.Core;
using Guardian.Models;
using Microsoft.Data.Sqlite;

namespace Guardian.Data
{
    public class SqliteRepository : IRepository
    {
        private readonly string _connectionString;

        public SqliteRepository()
        {
            var appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            var dbPath = Path.Combine(appData, "Guardian", "guardian.db");

            Directory.CreateDirectory(Path.GetDirectoryName(dbPath)!);
            _connectionString = $"Data Source={dbPath}";
        }

        public async Task InitializeAsync()
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                CREATE TABLE IF NOT EXISTS AppUsages (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ProcessName TEXT NOT NULL,
                    WindowTitle TEXT,
                    StartTime TEXT NOT NULL,
                    EndTime TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS FocusSessions (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    StartTime TEXT NOT NULL,
                    EndTime TEXT,
                    DurationTicks INTEGER NOT NULL,
                    IsCompleted INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS BlockRules (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ProcessName TEXT NOT NULL UNIQUE,
                    IsActive INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Settings (
                    Id INTEGER PRIMARY KEY CHECK (Id = 1),
                    StartOnBoot INTEGER NOT NULL,
                    NotificationsEnabled INTEGER NOT NULL,
                    DataRetentionDays INTEGER NOT NULL
                );
            ";

            await command.ExecuteNonQueryAsync();

            // Insert default settings if not exists
            command.CommandText = "INSERT OR IGNORE INTO Settings (Id, StartOnBoot, NotificationsEnabled, DataRetentionDays) VALUES (1, 1, 1, 30);";
            await command.ExecuteNonQueryAsync();
        }

        public async Task SaveAppUsageAsync(AppUsage usage)
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                INSERT INTO AppUsages (ProcessName, WindowTitle, StartTime, EndTime)
                VALUES ($ProcessName, $WindowTitle, $StartTime, $EndTime);
            ";
            command.Parameters.AddWithValue("$ProcessName", usage.ProcessName);
            command.Parameters.AddWithValue("$WindowTitle", usage.WindowTitle ?? "");
            command.Parameters.AddWithValue("$StartTime", usage.StartTime.ToString("o"));
            command.Parameters.AddWithValue("$EndTime", usage.EndTime.ToString("o"));

            await command.ExecuteNonQueryAsync();
        }

        public async Task<List<AppUsage>> GetAppUsagesAsync(DateTime date)
        {
            var usages = new List<AppUsage>();
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var startOfDay = date.Date.ToString("o");
            var endOfDay = date.Date.AddDays(1).ToString("o");

            var command = connection.CreateCommand();
            command.CommandText = @"
                SELECT Id, ProcessName, WindowTitle, StartTime, EndTime
                FROM AppUsages
                WHERE StartTime >= $StartOfDay AND StartTime < $EndOfDay
            ";
            command.Parameters.AddWithValue("$StartOfDay", startOfDay);
            command.Parameters.AddWithValue("$EndOfDay", endOfDay);

            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                usages.Add(new AppUsage
                {
                    Id = reader.GetInt32(0),
                    ProcessName = reader.GetString(1),
                    WindowTitle = reader.GetString(2),
                    StartTime = DateTime.Parse(reader.GetString(3)),
                    EndTime = DateTime.Parse(reader.GetString(4))
                });
            }

            return usages;
        }

        public async Task SaveFocusSessionAsync(FocusSession session)
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            if (session.Id == 0)
            {
                command.CommandText = @"
                    INSERT INTO FocusSessions (StartTime, EndTime, DurationTicks, IsCompleted)
                    VALUES ($StartTime, $EndTime, $DurationTicks, $IsCompleted);
                    SELECT last_insert_rowid();
                ";
                command.Parameters.AddWithValue("$StartTime", session.StartTime.ToString("o"));
                command.Parameters.AddWithValue("$EndTime", session.EndTime?.ToString("o") ?? (object)DBNull.Value);
                command.Parameters.AddWithValue("$DurationTicks", session.Duration.Ticks);
                command.Parameters.AddWithValue("$IsCompleted", session.IsCompleted ? 1 : 0);

                session.Id = Convert.ToInt32(await command.ExecuteScalarAsync());
            }
            else
            {
                command.CommandText = @"
                    UPDATE FocusSessions
                    SET EndTime = $EndTime, DurationTicks = $DurationTicks, IsCompleted = $IsCompleted
                    WHERE Id = $Id;
                ";
                command.Parameters.AddWithValue("$Id", session.Id);
                command.Parameters.AddWithValue("$EndTime", session.EndTime?.ToString("o") ?? (object)DBNull.Value);
                command.Parameters.AddWithValue("$DurationTicks", session.Duration.Ticks);
                command.Parameters.AddWithValue("$IsCompleted", session.IsCompleted ? 1 : 0);

                await command.ExecuteNonQueryAsync();
            }
        }

        public async Task<List<FocusSession>> GetFocusSessionsAsync()
        {
            var sessions = new List<FocusSession>();
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "SELECT Id, StartTime, EndTime, DurationTicks, IsCompleted FROM FocusSessions";

            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                sessions.Add(new FocusSession
                {
                    Id = reader.GetInt32(0),
                    StartTime = DateTime.Parse(reader.GetString(1)),
                    EndTime = reader.IsDBNull(2) ? null : DateTime.Parse(reader.GetString(2)),
                    Duration = TimeSpan.FromTicks(reader.GetInt64(3)),
                    IsCompleted = reader.GetInt32(4) == 1
                });
            }

            return sessions;
        }

        public async Task SaveBlockRuleAsync(BlockRule rule)
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                INSERT INTO BlockRules (ProcessName, IsActive)
                VALUES ($ProcessName, $IsActive)
                ON CONFLICT(ProcessName) DO UPDATE SET IsActive = $IsActive;
            ";
            command.Parameters.AddWithValue("$ProcessName", rule.ProcessName);
            command.Parameters.AddWithValue("$IsActive", rule.IsActive ? 1 : 0);

            await command.ExecuteNonQueryAsync();
        }

        public async Task RemoveBlockRuleAsync(int ruleId)
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "DELETE FROM BlockRules WHERE Id = $Id";
            command.Parameters.AddWithValue("$Id", ruleId);

            await command.ExecuteNonQueryAsync();
        }

        public async Task<List<BlockRule>> GetBlockRulesAsync()
        {
            var rules = new List<BlockRule>();
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "SELECT Id, ProcessName, IsActive FROM BlockRules";

            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                rules.Add(new BlockRule
                {
                    Id = reader.GetInt32(0),
                    ProcessName = reader.GetString(1),
                    IsActive = reader.GetInt32(2) == 1
                });
            }

            return rules;
        }

        public async Task SaveSettingsAsync(UserSettings settings)
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = @"
                UPDATE Settings
                SET StartOnBoot = $StartOnBoot, NotificationsEnabled = $NotificationsEnabled, DataRetentionDays = $DataRetentionDays
                WHERE Id = 1;
            ";
            command.Parameters.AddWithValue("$StartOnBoot", settings.StartOnBoot ? 1 : 0);
            command.Parameters.AddWithValue("$NotificationsEnabled", settings.NotificationsEnabled ? 1 : 0);
            command.Parameters.AddWithValue("$DataRetentionDays", settings.DataRetentionDays);

            await command.ExecuteNonQueryAsync();
        }

        public async Task<UserSettings> GetSettingsAsync()
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            var command = connection.CreateCommand();
            command.CommandText = "SELECT StartOnBoot, NotificationsEnabled, DataRetentionDays FROM Settings WHERE Id = 1";

            using var reader = await command.ExecuteReaderAsync();
            if (await reader.ReadAsync())
            {
                return new UserSettings
                {
                    Id = 1,
                    StartOnBoot = reader.GetInt32(0) == 1,
                    NotificationsEnabled = reader.GetInt32(1) == 1,
                    DataRetentionDays = reader.GetInt32(2)
                };
            }

            return new UserSettings(); // Default
        }
    }
}
