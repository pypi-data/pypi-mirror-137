from typing import Any, Dict, List
from overrides import overrides
import torch as tr

from ..metrics import Metric, MetricWrapper
from .feed_forward import FeedForwardNetwork
from .generator_network import GeneratorNetwork
from ..nwmodule import NWModule
from ..loss import bce

class VariationalAutoencoderNetwork(FeedForwardNetwork):
    def __init__(self, encoder: NWModule, decoder: GeneratorNetwork, lossWeights = {"latent": 1, "decoder": 1}):
        assert hasattr(encoder, "noise_size")
        assert isinstance(decoder, GeneratorNetwork)
        assert encoder.noise_size == decoder.noise_size, f"{encoder.noise_size} vs. {decoder.noise_size}"
        self.lossWeights = lossWeights
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder

    @overrides
    def train_step(self, x: Any, **kwargs) -> Any:
        MB = len(x)

        # Get the mean/std of this input
        encoder_mean, encoder_std = self.encoder.forward(x)

        # "Reparametrization trick": Sample from N(0, I) and multiply by our distribution's mean/std.
        z_noise = tr.randn(MB, self.encoder.noise_size).to(self.getDevice())
        z_noise = z_noise * encoder_std + encoder_mean

        # Decode the result
        output_decoder = self.decoder.forward(z_noise)

        y = {
            "encoder" : (encoder_mean, encoder_std),
            "decoder" : output_decoder
        }
        return y

    @overrides
    def inference_step(self, x: Any, **kwargs) -> Any:
        return self.decoder.inference_step(x)

    @overrides
    def criterion(self, y: Any, gt: Any) -> tr.Tensor:
        latent_loss = VariationalAutoencoderNetwork.latent_loss_fn(y)
        decoder_loss = VariationalAutoencoderNetwork.decoder_loss_fn(y, gt)
        loss = self.lossWeights["latent"] * latent_loss + self.lossWeights["decoder"] * decoder_loss
        return loss

    @overrides
    def get_default_metrics(self) -> List[Metric]:
        default = super().get_default_metrics()
        vae_metrics = [
            MetricWrapper("Reconstruction Loss", lambda y, gt:
                self.lossWeights["decoder"] * VariationalAutoencoderNetwork.decoder_loss_fn(y, gt), "min"),
            MetricWrapper("Latent Loss", lambda y, gt:
                self.lossWeights["latent"] * VariationalAutoencoderNetwork.latent_loss_fn(y), "min"),
        ]
        return [*default, *vae_metrics]

    @staticmethod
    def latent_loss_fn(y: Dict[str, tr.Tensor]) -> float:
        encoder_mean, encoder_std = y["encoder"]
        # KL-Divergence between two Gaussians: N(0, I) and N(encoderMean, encoderStd) 
        KL = 0.5 * tr.sum((encoder_std**2 + encoder_mean**2 - 1 - tr.log(encoder_std**2)))
        return KL

    @staticmethod
    def decoder_loss_fn(y: Dict[str, tr.Tensor], gt: tr.Tensor) -> float:
        output_decoder = y["decoder"]
        MB = len(y["decoder"])
        output_decoder = output_decoder.view(MB, -1)
        gt = gt.view(MB, -1)
        decoder_loss = bce(output_decoder, gt).mean()
        return decoder_loss
