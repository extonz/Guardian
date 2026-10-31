using System.Windows;
using System.Windows.Controls;
using Guardian.ViewModels;

namespace Guardian.Views
{
    public partial class DashboardView : UserControl
    {
        public DashboardView()
        {
            InitializeComponent();
            Loaded += async (s, e) =>
            {
                if (DataContext is DashboardViewModel vm)
                {
                    await vm.LoadDataAsync();
                }
            };
        }
    }
}
