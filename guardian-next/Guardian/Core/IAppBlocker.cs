using Guardian.Models;

namespace Guardian.Core
{
    public interface IAppBlocker
    {
        void Start();
        void Stop();
        void AddRule(BlockRule rule);
        void RemoveRule(BlockRule rule);
    }
}
