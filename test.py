from djitellopy import Tello   
from time import sleep

me = Tello()
me.connect()
print("Battery percentage:", me.get_battery())
me.takeoff()
try:
        me.send_rc_control(0, 50, 0, 0)  # Điều khiển di chuyển tới trước
        print("Command 1 sent successfully")
        sleep(2)
except Exception as e:
        print(f"Failed to send command 1: {e}")

try:
        me.send_rc_control(30, 0, 0, 0)  # Điều khiển di chuyển sang trái
        print("Command 2 sent successfully")
        sleep(2)
except Exception as e:
        print(f"Failed to send command 2: {e}")

try:
        me.send_rc_control(0, 0, 50, 0)  # Thử điều khiển độ cao
        print("Command 3 sent successfully")
        sleep(2)
except Exception as e:
        print(f"Failed to send command 3: {e}")

try:
        me.send_rc_control(0, 0, 0, 50)  # Thử điều khiển xoay
        print("Command 4 sent successfully")
        sleep(2)
except Exception as e:
        print(f"Failed to send command 4: {e}")

me.land()
