from overrides import overrides
from ...trainer import NWTrainer

class FeedForwardTrainer(NWTrainer):
    @overrides
    def train_step(self, x, gt, is_optimizing: bool):
        y = self.model.train_step(x)
        loss = self.model.criterion(y, gt)
        if is_optimizing:
            NWTrainer.do_optimizer_step(self.model, loss)
        return y, loss
