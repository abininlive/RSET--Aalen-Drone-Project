from RPIO import PWM
import time
servo = PWM.Servo()

#servo.set_servo(17, 200)
#servo.set_servo(19, 200)
#servo.set_servo(26, 200)
#servo.set_servo(27, 200)
servo.set_servo(17, 1000)
servo.set_servo(19, 1000)
servo.set_servo(26, 1000)
servo.set_servo(27, 1000)


#a=float(raw_input("duration: "))
a=1
b=int(raw_input("speed: "))


servo.set_servo(17, b)
#servo.set_servo(19, b)
#servo.set_servo(26, b)
#servo.set_servo(27, b)

time.sleep(a)


servo.stop_servo(17)
servo.stop_servo(19)
servo.stop_servo(26)
servo.stop_servo(27)


