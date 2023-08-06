import os
import cv2
import numpy as np
import tensorrt as trt
from ..utils import allocate_buffers, do_inference, preproc, demo_postprocess, multiclass_nms


class PersonDetectionTrt:
    def __init__(self,
                 engine_file,
                 score_thr=0.1,
                 nms_thr=0.7,
                 with_p6=False):
        self.engine_file = engine_file
        self.score_thr = score_thr
        self.nms_thr = nms_thr
        self.with_p6 = with_p6
        self.rgb_means = (0.485, 0.456, 0.406)
        self.std = (0.229, 0.224, 0.225)
        engine = self.get_model(engine_file)
        self.input_shape = list(engine.get_binding_shape(engine[0]))
        self.output_shape = list(engine.get_binding_shape(engine[-1]))
        self.context = engine.create_execution_context()
        self.inputs, self.outputs, self.bindings, self.stream = allocate_buffers(engine)

    def get_model(self, engine_file):
        if not os.path.exists(engine_file):
            FileNotFoundError('Trt file not exist')

        runtime = trt.Runtime(trt.Logger(trt.Logger.VERBOSE))
        with open(engine_file, "rb") as f:
            return runtime.deserialize_cuda_engine(f.read())

    def predict(self, image):
        image, ratio = preproc(image, self.input_shape[2:], self.rgb_means, self.std)
        image = np.expand_dims(image, axis=0)
        image_batch_ravel = image.ravel()
        np.copyto(dst=self.inputs[0].host, src=image_batch_ravel)
        outputs = do_inference(context=self.context,
                               bindings=self.bindings,
                               inputs=self.inputs,
                               outputs=self.outputs,
                               stream=self.stream,
                               batch_size=self.input_shape[0])
        outputs = [output.reshape(self.output_shape) for output in outputs]
        predictions = demo_postprocess(outputs[0], self.input_shape[2:], p6=self.with_p6)[0]
        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:]
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
        boxes_xyxy /= ratio
        dets = multiclass_nms(boxes_xyxy, scores, nms_thr=self.nms_thr, score_thr=self.score_thr)
        return dets[:, :-1] if dets is not None else None

    def show(self, image, results):
        index = 1
        for (box, score) in zip(list(results[:, :-1].astype(int)), list(results[:, -1])):
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255, 0, 255), 2)
            cv2.putText(image, 'id: %d, score: %.2f' % (index, score),
                        (box[0], box[1] - 4), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), thickness=2)
            index += 1
        return image


if __name__ == '__main__':
    import time

    tp = PersonDetectionTrt(engine_file='bytetrack_s_fp16.trt')

    img = cv2.imread("face.jpg")
    s = time.time()
    trt_out = tp.predict(img)
    print("time: ", time.time() - s)
    print(list(trt_out))
