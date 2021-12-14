import pioneer_sdk
import cv2
import numpy as np
from lobe import ImageModel
from PIL import Image

pioneer = pioneer_sdk.Pioneer()

model = ImageModel.load('./Helicopter_Place_TensorFlow')

command_x = float(0)
command_y = float(0)
command_z = float(1)
command_yaw = np.radians(float(0))
increment_xy = float(0.2)
increment_z = float(0.1)
increment_deg = np.radians(float(10))

new_command = False

leds_sent = False
old_prediction = None

while True:
    raw = pioneer.get_raw_video_frame()
    frame = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    model_frame = Image.fromarray(frame_rgb)

    predictions = model.predict(model_frame)

    key = cv2.waitKey(1)
    if key == 32:
        print('space pressed')
        pioneer.arm()
        print('point')
        pioneer.takeoff()
    if key == 27:  # esc
        print('esc pressed')
        pioneer.land()
    if key == ord('w'):
        print('w')
        command_y += increment_xy
        new_command = True
    elif key == ord('s'):
        print('s')
        command_y -= increment_xy
        new_command = True
    elif key == ord('a'):
        print('a')
        command_x -= increment_xy
        new_command = True
    elif key == ord('d'):
        print('d')
        command_x += increment_xy
        new_command = True
    elif key == ord('q'):
        print('q')
        command_yaw += increment_deg
        new_command = True
    elif key == ord('e'):
        print('e')
        command_yaw -= increment_deg
        new_command = True
    elif key == ord('h'):
        print('h')
        command_z += increment_z
        new_command = True
    elif key == ord('l'):
        print('l')
        command_z -= increment_z
        new_command = True
    elif key == ord('k'):
        break

    if new_command:
        pioneer.go_to_local_point(x=command_x, y=command_y, z=command_z, yaw=command_yaw)
        new_command = False

    cv2.putText(frame, f'Predicted class is {predictions.prediction}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(0, 0, 255))

    if predictions.prediction == 'Class_Place' and not leds_sent:
        pioneer.led_control(0, 255, 0, 0)
        pioneer.led_control(1, 255, 0, 0)
        pioneer.led_control(2, 255, 0, 0)
        pioneer.led_control(3, 255, 0, 0)
        leds_sent = True
    elif predictions.prediction == 'Class_NoPlace' and not leds_sent:
        pioneer.led_control(0, 0, 0, 0)
        pioneer.led_control(1, 0, 0, 0)
        pioneer.led_control(2, 0, 0, 0)
        pioneer.led_control(3, 0, 0, 0)
        leds_sent = True

    if predictions.prediction != old_prediction:
        leds_sent = False

    old_prediction = predictions.prediction

    cv2.imshow("Frame", frame)

cv2.destroyAllWindows()

