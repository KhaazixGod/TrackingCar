import cv2
import numpy as np
import onnxruntime as ort

class Detect:
    def __init__(self):
        MODEL_PATH = r'C:\Users\ADMIN\Documents\TrackCar\model\yolov8n.onnx'  
        self.INPUT_SIZE = 640  

        # === LOAD MODEL ===
        self.session = ort.InferenceSession(MODEL_PATH)
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [o.name for o in self.session.get_outputs()]

    def nms_boxes(self,boxes, scores, iou_threshold=0.5, score_threshold=0.0):
        if not boxes or not scores:
            return []

        indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold, iou_threshold)
        
        if len(indices) == 0:
            return []

        # Chuyển từ index về box gốc
        selected_boxes = [boxes[i[0]] if isinstance(i, (list, tuple, np.ndarray)) else boxes[i] for i in indices]
        
        return selected_boxes

    def detect(self,rgb):
        orig_shape = rgb.shape
        img_height, img_width = rgb.shape[:2]

        # Resize ảnh về 320x320 cho input model
        rgb_resized = cv2.resize(rgb, (320, 320))

        # Tiền xử lý ảnh
        img_input = rgb_resized.transpose(2, 0, 1) / 255.0  # HWC → CHW, scale về 0–1
        img_input = np.expand_dims(img_input, axis=0).astype(np.float32)  # [1, 3, 320, 320]

        # Chạy inference ONNX
        output = self.session.run(None, {self.input_name: img_input})[0]  # output: [1, 5, N] hoặc [5, N]
        output = np.squeeze(output).T
        ans_boxes = []
        ans_conf = []
        for det in output:
            x, y, w, h,conf = det[:5]
            if(conf<0.7):
                continue
            ans_boxes.append([x,y,w,h])
            ans_conf.append(conf)
            
        ans = self.nms_boxes(ans_boxes,ans_conf)
        return ans
