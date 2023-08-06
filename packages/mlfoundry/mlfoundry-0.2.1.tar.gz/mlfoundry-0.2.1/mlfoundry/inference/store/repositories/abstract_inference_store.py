import abc
import typing

from ..inference_packet import InferencePacket


class AbstractInferenceStore(abc.ABC):
    def log_inference(self, inference_packet: InferencePacket):
        self.batch_log_inference([inference_packet])

    @abc.abstractmethod
    def batch_log_inference(self, inference_packets: typing.List[InferencePacket]):
        ...
