import lgpio
import time
#Connor Pietrasik 015126007

h = lgpio.i2c_open(1, 0x1E)
while True:
    try:
        print(lgpio.i2c_read_byte_data(h, 0))
    except KeyboardInterrupt:
        lgpio.i2c_close(h)
        exit(1)