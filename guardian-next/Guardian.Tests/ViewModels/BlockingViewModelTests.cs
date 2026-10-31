using System.Collections.Generic;
using System.Threading.Tasks;
using Guardian.Core;
using Guardian.Models;
using Guardian.ViewModels;
using Moq;
using Xunit;

namespace Guardian.Tests.ViewModels
{
    public class BlockingViewModelTests
    {
        [Fact]
        public async Task LoadRulesAsync_PopulatesRulesCollection()
        {
            var mockRepo = new Mock<IRepository>();
            var mockBlocker = new Mock<IAppBlocker>();

            mockRepo.Setup(r => r.GetBlockRulesAsync()).ReturnsAsync(new List<BlockRule>
            {
                new BlockRule { Id = 1, ProcessName = "notepad", IsActive = true },
                new BlockRule { Id = 2, ProcessName = "calc", IsActive = false }
            });

            var vm = new BlockingViewModel(mockRepo.Object, mockBlocker.Object);

            await vm.LoadRulesAsync();

            Assert.Equal(2, vm.Rules.Count);
            Assert.Equal("notepad", vm.Rules[0].ProcessName);
        }
    }
}
