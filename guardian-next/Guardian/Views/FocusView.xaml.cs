using System.Windows.Controls;
using Guardian.ViewModels;

namespace Guardian.Views
{
    public partial class FocusView : UserControl
    {
        public FocusView()
        {
            InitializeComponent();
            Loaded += async (s, e) =>
            {
                if (DataContext is FocusViewModel vm)
                {
                    await vm.LoadRecentSessionsAsync();
                }
            };
        }
    }
}
