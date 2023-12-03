import lgpio
from time import sleep
#Connor Pietrasik 015126007

ADDRESS_MAG = 0x1E
ADDRESS_ACCEL = 0x19

REG_MAG_WHO = 0x4F
REG_MAG_CFG_A = 0x60

REG_MAG_X_L = 0x68
REG_MAG_Y_L = 0x6A
REG_MAG_Z_L = 0x6C

h = lgpio.i2c_open(1, ADDRESS_MAG)

#0 = 10Hz continuous mode
lgpio.i2c_write_byte_data(h, REG_MAG_CFG_A, 0)


while True:
    try:
        x = lgpio.i2c_read_byte_data(h, REG_MAG_X_L)
        y = lgpio.i2c_read_byte_data(h, REG_MAG_Y_L)
        z = lgpio.i2c_read_byte_data(h, REG_MAG_Z_L)
        print(f"X: { x }\tY: { y }\tZ: { z }")
        sleep(0.2)
    except KeyboardInterrupt:
        lgpio.i2c_close(h)
        exit(1)