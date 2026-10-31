using System.Collections.ObjectModel;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Guardian.Core;
using Guardian.Models;

namespace Guardian.ViewModels
{
    public partial class BlockingViewModel : ObservableObject
    {
        private readonly IRepository _repository;
        private readonly IAppBlocker _blocker;

        [ObservableProperty]
        private ObservableCollection<BlockRule> _rules = new();

        [ObservableProperty]
        private string _newProcessName = string.Empty;

        public BlockingViewModel(IRepository repository, IAppBlocker blocker)
        {
            _repository = repository;
            _blocker = blocker;
        }

        [RelayCommand]
        public async Task LoadRulesAsync()
        {
            var rules = await _repository.GetBlockRulesAsync();
            Rules.Clear();
            foreach (var rule in rules)
            {
                Rules.Add(rule);
            }
        }

        [RelayCommand]
        private async Task AddRuleAsync()
        {
            if (string.IsNullOrWhiteSpace(NewProcessName)) return;

            var rule = new BlockRule
            {
                ProcessName = NewProcessName.Trim(),
                IsActive = true
            };

            await _repository.SaveBlockRuleAsync(rule);
            _blocker.AddRule(rule);

            NewProcessName = string.Empty;
            await LoadRulesAsync();
        }

        [RelayCommand]
        private async Task RemoveRuleAsync(BlockRule rule)
        {
            if (rule != null)
            {
                await _repository.RemoveBlockRuleAsync(rule.Id);
                _blocker.RemoveRule(rule);
                await LoadRulesAsync();
            }
        }

        [RelayCommand]
        private async Task ToggleRuleAsync(BlockRule rule)
        {
            if (rule != null)
            {
                rule.IsActive = !rule.IsActive;
                await _repository.SaveBlockRuleAsync(rule);

                if (rule.IsActive)
                    _blocker.AddRule(rule);
                else
                    _blocker.RemoveRule(rule);
            }
        }
    }
}
