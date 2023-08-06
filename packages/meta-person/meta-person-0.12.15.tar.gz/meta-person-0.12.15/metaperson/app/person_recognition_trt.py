import cv2, time
from .person_detection_trt import PersonDetectionTrt
from ..model_zoo import BYTETracker


class PersonTrackerTrt:
    def __init__(self,
                 model_file='models/bytetrack_s_fp16.trt',
                 track_thresh=0.5,
                 match_thresh=0.8,
                 track_buffer=30,
                 frame_rate=30):
        self.detector = PersonDetectionTrt(model_file)
        self.tracker = BYTETracker(track_thresh, match_thresh, track_buffer, frame_rate)

    def predict(self, image, min_box_area=10, aspect_ratio_thresh=1.6):
        img_info = image.shape[:2]
        results = []
        outputs = self.detector.predict(image)
        if outputs is not None:
            targets = self.tracker.update(outputs, img_info, img_info)
            for t in targets:
                vertical = t.tlwh[2] / t.tlwh[3] > aspect_ratio_thresh
                if t.tlwh[2] * t.tlwh[3] > min_box_area and not vertical:
                    results.append(dict(box=list(t.tlwh.astype(int)),
                                        id=t.track_id,
                                        score=t.score))
        return results

    def show(self, image, results):
        h, w = image.shape[:2]
        for result in results:
            box = result['box']
            l, t, r, b = max(box[0], 0), max(box[1], 0), min(box[0] + box[2] - 1, w - 1), min(box[1] + box[3] - 1,
                                                                                              h - 1)
            cv2.rectangle(image, (l, t), (r, b), (255, 0, 255), 2)
            cv2.putText(image, 'id: %d, score: %.2f' % (result['id'], result['score']),
                        (l, max(t - 4, 0)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), thickness=2)
        return image

    def predict_video(self, file_path=0, test_size=(608, 1088), min_box_area=10):
        cap = cv2.VideoCapture(file_path)
        frame_id = 0
        while True:
            ret, frame = cap.read()
            if ret:
                s = time.time()
                results = self.predict(frame, test_size, min_box_area)
                print("person nums: ", len(results), time.time() - s)
                # if len(results) > 0:
                #     frame = self.show(frame, results)
                #     cv2.imwrite('/home/cash/WorkSpace/online_data/results/' + str(frame_id) + '.jpg', frame)
            else:
                break
            frame_id += 1


if __name__ == '__main__':
    import glob, time, os

    detector = PersonTrackerTrt(model_file='models/bytetrack_s_fp16.trt')

    # img_paths = glob.glob('images/*.jpg')
    # for img_path in img_paths:
    #     img = cv2.imread(img_path)
    #     s = time.time()
    #     outputs = detector.predict(img)
    #     print("person recognition: ", time.time() - s)
    #     rimg = detector.show(img, outputs)
    #     filename = os.path.basename(img_path)
    #     cv2.imwrite('outputs/%s' % filename, rimg)

    file_path = 'rtsp://admin:dahua123456@113.31.167.129:8893/cam/realmonitor?channel=1&subtype=1'
    file_path = 'images/palace.mp4'
    detector.predict_video(file_path)
