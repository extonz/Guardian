using System.Collections.Generic;
using System.Threading.Tasks;
using Guardian.Models;

namespace Guardian.Core
{
    public interface IRepository
    {
        Task InitializeAsync();

        Task SaveAppUsageAsync(AppUsage usage);
        Task<List<AppUsage>> GetAppUsagesAsync(System.DateTime date);

        Task SaveFocusSessionAsync(FocusSession session);
        Task<List<FocusSession>> GetFocusSessionsAsync();

        Task SaveBlockRuleAsync(BlockRule rule);
        Task RemoveBlockRuleAsync(int ruleId);
        Task<List<BlockRule>> GetBlockRulesAsync();

        Task SaveSettingsAsync(UserSettings settings);
        Task<UserSettings> GetSettingsAsync();
    }
}
