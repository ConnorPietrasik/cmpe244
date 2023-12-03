import lgpio
import lgpiopwm
from time import sleep
from math import degrees
import numpy as np
#Connor Pietrasik 015126007

def spin_check_deg(degree, clockwise = True):
    ADDRESS_MAG = 0x1E

    REG_MAG_CFG_A = 0x60

    REG_MAG_X_L = 0x68
    REG_MAG_Y_L = 0x6A
    REG_MAG_Z_L = 0x6C

    PWM_PIN = 12
    DIR_PIN = 17

    PWM_FREQ = 250

    h = lgpio.i2c_open(1, ADDRESS_MAG)

    #0 = 10Hz continuous mode
    lgpio.i2c_write_byte_data(h, REG_MAG_CFG_A, 0)

    #The higher byte doesn't seem to change in my tests, so just using the lower one
    start_x = lgpio.i2c_read_byte_data(h, REG_MAG_X_L)
    start_y = lgpio.i2c_read_byte_data(h, REG_MAG_Y_L)
    start_z = lgpio.i2c_read_byte_data(h, REG_MAG_Z_L)
    print(f"Start X: { start_x }\tStart Y: { start_y }\tStart Z: { start_z }")

    steps = int(degree * 4096 / 360)
    print(f"{degree} degrees = {steps} steps")

    #Steps to time before turning pwm off
    delay = steps / PWM_FREQ

    h_pwm = lgpiopwm.init(PWM_PIN)

    lgpiopwm.write(h, DIR_PIN, int(clockwise))

    lgpiopwm.pwm(h_pwm, PWM_FREQ, 50)
    sleep(delay)
    lgpiopwm.pwm(h_pwm, 0, 0)
    sleep(0.2) #Let the sensor settle

    x = lgpio.i2c_read_byte_data(h, REG_MAG_X_L)
    y = lgpio.i2c_read_byte_data(h, REG_MAG_Y_L)
    z = lgpio.i2c_read_byte_data(h, REG_MAG_Z_L)
    print(f"End X: { x }\tEnd Y: { y }\tEnd Z: { z }")

    #Standard formula to get angle between two vectors
    vec1 = [start_x, start_y, start_z]
    vec2 = [x, y, z]
    calc_angle = degrees(np.arccos(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))))

    #This was needed at first, then the sensor went crazy for a while, and now it's no longer needed (but values aren't as consistent)
    #Pretty sure the sensor is cursed
    # #I don't understand why I need this, but found it by looking for patterns in results
    # #It was all 14.9 or so and then 29.9 for these cases
    # a = start_x > x
    # b = start_y > y
    # c = start_z > z

    # #Two greater in a row makes it double the result for some reason
    # c1 = a and b and not c
    # c2 = a and not b and not c
    # c3 = not a and b and c
    # c4 = not a and not b and c

    # if c1 or c2 or c3 or c4:
    #     calc_angle /= 2


    print(f"Calculated angle: {calc_angle} degrees")

    lgpio.i2c_close(h)


spin_check_deg(15)
print()
sleep(0.2)
spin_check_deg(15, False)