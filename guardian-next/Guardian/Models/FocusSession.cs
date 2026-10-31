using System;

namespace Guardian.Models
{
    public class FocusSession
    {
        public int Id { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime? EndTime { get; set; }
        public TimeSpan Duration { get; set; }
        public bool IsCompleted { get; set; }
    }
}
