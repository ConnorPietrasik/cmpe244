import lgpio
from time import sleep
#Connor Pietrasik 015126007

ADDRESS_MAG = 0x1E
ADDRESS_ACCEL = 0x19

REG_WHO_M = 0x4F

REG_MAG_X_H = 0x69
REG_MAG_Y_H = 0x6B
REG_MAG_Z_H = 0x6D

h = lgpio.i2c_open(1, 0x1E)


while True:
    try:
        x = lgpio.i2c_read_byte_data(h, REG_MAG_X_H)
        y = lgpio.i2c_read_byte_data(h, REG_MAG_Y_H)
        z = lgpio.i2c_read_byte_data(h, REG_MAG_Z_H)
        print(f"X: { x }\tY: { y }\tZ: { z }")
        sleep(0.5)
    except KeyboardInterrupt:
        lgpio.i2c_close(h)
        exit(1)