using System;

namespace Guardian.Models
{
    public class BlockRule
    {
        public int Id { get; set; }
        public string ProcessName { get; set; } = string.Empty;
        public bool IsActive { get; set; }
    }
}
