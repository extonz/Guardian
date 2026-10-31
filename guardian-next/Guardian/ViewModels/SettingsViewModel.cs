using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Guardian.Core;
using Guardian.Models;

namespace Guardian.ViewModels
{
    public partial class SettingsViewModel : ObservableObject
    {
        private readonly IRepository _repository;

        [ObservableProperty]
        private UserSettings _settings = new();

        [ObservableProperty]
        private string _saveStatus = string.Empty;

        public SettingsViewModel(IRepository repository)
        {
            _repository = repository;
        }

        [RelayCommand]
        public async Task LoadSettingsAsync()
        {
            Settings = await _repository.GetSettingsAsync();
        }

        [RelayCommand]
        private async Task SaveSettingsAsync()
        {
            await _repository.SaveSettingsAsync(Settings);
            SaveStatus = "Saved successfully!";
            await Task.Delay(2000);
            SaveStatus = string.Empty;
        }
    }
}
