using System.Windows.Controls;
using Guardian.ViewModels;

namespace Guardian.Views
{
    public partial class SettingsView : UserControl
    {
        public SettingsView()
        {
            InitializeComponent();
            Loaded += async (s, e) =>
            {
                if (DataContext is SettingsViewModel vm)
                {
                    await vm.LoadSettingsAsync();
                }
            };
        }
    }
}
