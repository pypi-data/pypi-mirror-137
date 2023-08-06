import torch as tr
from overrides import overrides

from ...trainer import NWTrainer
from ...loss import bce

class GANTrainer(NWTrainer):
    @overrides
    def train_step(self, x, gt, is_optimizing: bool):
        device = self.model.getDevice()
        MB = len(x)
        ones = tr.full((MB, ), 1, dtype=tr.float32).to(device)
        zeros = tr.full((MB, ), 0, dtype=tr.float32).to(device)

        # Generate fake data
        g = self.model.generator.inference_step(MB)

        # Discriminator step
        dFakePredict = self.model.discriminator.forward(g.detach())
        dRealPredict = self.model.discriminator.forward(gt)
        dRealLoss = bce(dRealPredict, ones).mean()
        dFakeLoss = bce(dFakePredict, zeros).mean()
        dLoss = (dRealLoss + dFakeLoss) / 2
        if is_optimizing:
            NWTrainer.do_optimizer_step(self.model.discriminator, dLoss)

        # Generator step
        gFakePredict = self.model.discriminator.forward(g)
        gLoss = bce(gFakePredict, ones).mean()
        if is_optimizing:
            NWTrainer.do_optimizer_step(self.model.generator, gLoss)

        trLoss = (dLoss + gLoss) / 2
        trResults = {
            "gLoss" : gLoss.detach(),
            "dLoss" : dLoss.detach(),
            "gSample" : g.detach()
        }
        return trResults, trLoss
