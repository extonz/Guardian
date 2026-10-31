namespace Guardian.Models
{
    public class UserSettings
    {
        public int Id { get; set; }
        public bool StartOnBoot { get; set; } = true;
        public bool NotificationsEnabled { get; set; } = true;
        public int DataRetentionDays { get; set; } = 30;
    }
}
