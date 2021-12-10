import pioneer_sdk
import cv2
import numpy as np

pioneer = pioneer_sdk.Pioneer()

while True:
    raw = pioneer.get_raw_video_frame()
    frame = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)

    if k == ord('q'):
        break

cv2.destroyAllWindows()

