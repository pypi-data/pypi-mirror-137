import os
import tensorrt as trt

trt_logger = trt.Logger(trt.Logger.VERBOSE)
explicit_batch = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)


class Onnx2Trt:
    def __init__(self,
                 onnx_file,
                 batch_size=1,
                 fp16_on=True):
        self.onnx_file = onnx_file
        self.batch_size = batch_size
        self.fp16_on = fp16_on

    def simplify(self):
        import onnx
        from onnxsim import simplify

        onnx_model = onnx.load(self.onnx_file)
        model_simp, check = simplify(onnx_model)
        onnx.save(model_simp, self.onnx_file)

    def convert(self):
        engine_file = self.onnx_file.replace('.onnx', '_fp16.trt' if self.fp16_on else '_fp32.trt')
        with trt.Builder(trt_logger) as builder:
            with builder.create_network(explicit_batch) as network:
                with trt.OnnxParser(network, trt_logger) as parser:
                    builder.max_workspace_size = 1 << 30
                    builder.max_batch_size = self.batch_size
                    builder.fp16_mode = self.fp16_on
                    if not os.path.exists(self.onnx_file):
                        raise FileNotFoundError('Onnx file not exist')

                    with open(self.onnx_file, 'rb') as model:
                        parser.parse(model.read())

                    for error in range(parser.num_errors):
                        print(parser.get_error(error))

                    print("Test: ", network.num_layers)
                    engine = builder.build_cuda_engine(network)
                    with open(engine_file, "wb") as f:
                        f.write(engine.serialize())


if __name__ == '__main__':
    o2t = Onnx2Trt(onnx_file='models/bytetrack_s.onnx', fp16_on=True)
    o2t.convert()
