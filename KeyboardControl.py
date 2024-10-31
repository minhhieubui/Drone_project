import cv2
from djitellopy import tello
import time
import KeyPressModule as kp
import numpy as np

global img_default, img, img_qrcode

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()

def getkeyboardInput():
    lf, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lf = speed
    elif kp.getKey("RIGHT"): lf = -speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = speed
    elif kp.getKey("d"): yv = -speed

    if kp.getKey("q"): me.land() ; time.sleep(3)
    if kp.getKey("e"): me.takeoff()

    if kp.getKey("l"): me.rotate_clockwise(10)
    if kp.getKey("j"): me.rotate_counter_clockwise(10)

    if kp.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img_default)
        time.sleep(0.3)

    return [lf, fb, ud, yv]

def check_qrcode(img):
    try:
        # Chuyển hình ảnh sang grayscale để dễ phát hiện QR code
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Khởi tạo QRCodeDetector
        qr_detector = cv2.QRCodeDetector()

        # Phát hiện và giải mã QR code
        data, bbox, _ = qr_detector.detectAndDecode(gray_img)

        if bbox is not None and data:
            print(f"QR Code detected: {data}")
            n_lines = len(bbox)
            for i in range(n_lines):
                # Vẽ đường viền quanh QR code
                point1 = tuple(bbox[i][0])
                point2 = tuple(bbox[(i+1) % n_lines][0])
                cv2.line(img, point1, point2, (255, 0, 0), 2)
            print("Đã quét được QR Code")
        else:
            print("Không phát hiện QR Code")

        return img
    except Exception as e:
        print(f"Error detecting QR code: {e}")
        return img

while True:
    vals = getkeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    time.sleep(0.05)

    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    img_default = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Gọi hàm kiểm tra QR code
    img_qrcode = check_qrcode(img_default)

    # Hiển thị hình ảnh kèm QR code nếu có
    cv2.imshow("image", img_qrcode)

    # Nhấn ESC để thoát
    if cv2.waitKey(1) == 27:
        break

me.streamoff()
cv2.destroyAllWindows()
