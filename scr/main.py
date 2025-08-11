from detect import Detect
from check_same_person import Check
import cv2 
def run():
    detect = Detect()
    check = Check()
    INPUT_SIZE = 640
    cap = cv2.VideoCapture(0)
    while True:

        ret, frame = cap.read()

        if not ret:
            break
        
        boxes = detect.detect(frame)
        mnDist = -1
        ownerBox = (0,0,0,0)
        for box in boxes:
            x,y,w,h = box[:4]
            x1 = int((x - w/2) * frame.shape[1] / INPUT_SIZE*2)
            y1 = int((y - h/2) * frame.shape[0] / INPUT_SIZE*2)
            x2 = int((x + w/2) * frame.shape[1] / INPUT_SIZE*2)
            y2 = int((y + h/2) * frame.shape[0] / INPUT_SIZE*2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            if x1 < x2 or y1 < y2:
                continue
            dist = check.is_same_person(frame[y1:y2][x1:x2])
            if mnDist == -1:
                mnDist = dist
            elif mnDist > dist:
                mnDist = dist
                ownerBox = (x1,x2,y1,y2)
        if mnDist < 0.55:
            cv2.rectangle(frame, (ownerBox[0], ownerBox[1]), (ownerBox[2], ownerBox[3]), (255,0,0), 2)
            cv2.putText(frame, "Owner", (ownerBox[0], ownerBox[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        cv2.imshow("Camera",frame)
        if cv2.waitKey(1) == ord('q'):
            break

run()
                
            
