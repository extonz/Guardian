using System.Windows.Controls;
using Guardian.ViewModels;

namespace Guardian.Views
{
    public partial class BlockingView : UserControl
    {
        public BlockingView()
        {
            InitializeComponent();
            Loaded += async (s, e) =>
            {
                if (DataContext is BlockingViewModel vm)
                {
                    await vm.LoadRulesAsync();
                }
            };
        }
    }
}
