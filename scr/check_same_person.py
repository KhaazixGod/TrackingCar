import cv2
import numpy as np
import onnxruntime as ort
from scipy.spatial.distance import cosine

# Khởi tạo session cho ReID model (chỉ cần chạy 1 lần)
class Check:
    def __init__(self):
        
        self.reid_sess = ort.InferenceSession(r"C:\Users\ADMIN\Documents\TrackCar\model\osnet_x0_25_msmt17.onnx", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
        
        img1 = cv2.imread(r'C:\Users\ADMIN\Documents\TrackCar\data\Du1.jpg')
        img2 = cv2.imread(r'C:\Users\ADMIN\Documents\TrackCar\data\Du2.jpg')
        # img3 = cv2.imread(r'C:\Users\ADMIN\Documents\TrackCar\data\Du3.jpg')
        self.feature1 = self.extract_feature(img1)
        self.feature2 = self.extract_feature(img2)
        # self.feature3 = self.extract_feature(img3)
        

    def extract_feature(self,img_crop):
        img = cv2.resize(img_crop, (128, 256))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.
        img = img.transpose(2, 0, 1)

        # Pad thành 16 ảnh (batch size 16) nếu model yêu cầu
        input_batch = np.zeros((16, 3, 256, 128), dtype=np.float32)
        input_batch[0] = img  # chỉ dùng ảnh đầu tiên

        out = self.reid_sess.run(None, {self.reid_sess.get_inputs()[0].name: input_batch})[0]
        feat = out[0] / np.linalg.norm(out[0])  # chỉ lấy feature ảnh đầu tiên
        return feat


    def is_same_person(self,img):
        """So sánh 2 ảnh người, trả về True nếu là cùng người."""
        feat = self.extract_feature(img)

        dist = cosine(feat,self.feature1) + cosine(feat,self.feature2)
        print(f"Cosine distance: {dist:.4f}")
        return dist

