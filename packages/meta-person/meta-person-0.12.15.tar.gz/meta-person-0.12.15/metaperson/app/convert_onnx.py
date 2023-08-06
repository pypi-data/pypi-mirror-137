import torch
import torch.nn as nn
from ..model_zoo import YOLOPAFPN, YOLOX, YOLOXHead, SiLU
from ..utils import get_exp_by_file, replace_module


class ConvertOnnx:
    def __init__(self,
                 model_file='models/bytetrack_s_mot17.pth.tar',
                 exp_file='configs/yolox_s_mix_det.py'):
        exp = get_exp_by_file(exp_file)
        self.test_size = exp.test_size
        self.model = self.get_model(exp)
        self.model.eval()

        ckpt = torch.load(model_file, map_location="cpu")
        self.model.load_state_dict(ckpt["model"])
        self.model = replace_module(self.model, nn.SiLU, SiLU)
        self.model.head.decode_in_inference = False

    def get_model(self, exp):
        def init_yolo(M):
            for m in M.modules():
                if isinstance(m, nn.BatchNorm2d):
                    m.eps = 1e-3
                    m.momentum = 0.03

        if getattr(self, "model", None) is None:
            in_channels = [256, 512, 1024]
            backbone = YOLOPAFPN(exp.depth, exp.width, in_channels=in_channels)
            head = YOLOXHead(exp.num_classes, exp.width, in_channels=in_channels)
            model = YOLOX(backbone, head)

        model.apply(init_yolo)
        model.head.initialize_biases(1e-2)
        return model

    def convert(self, output_name="bytetrack_s.onnx"):
        import onnx
        from onnxsim import simplify

        x = torch.randn(1, 3, self.test_size[0], self.test_size[1])
        torch.onnx._export(
            self.model,
            x,
            output_name,
            input_names=["images"],
            output_names=["output"],
            opset_version=11,
        )
        onnx_model = onnx.load(output_name)
        model_simp, check = simplify(onnx_model)
        onnx.save(model_simp, output_name)
