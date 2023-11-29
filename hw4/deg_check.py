import lgpio
from time import sleep
from math import atan2, degrees
#Connor Pietrasik 015126007

#step_max overrides spin_time if set, otherwise calculated based on spin_time and delay
def spin_motor(clockwise = True, delay = 0.004, step_max = 4096, con0 = 17, con1 = 27, con2 = 22, con3 = 23):
    #half-step, so step_max = 4096 for full rotation
    steps = [
        0b1001,
        0b1000,
        0b1100,
        0b0100,
        0b0110,
        0b0010,
        0b0011,
        0b0001
    ]

    h = lgpio.gpiochip_open(0)
    lgpio.group_claim_output(h, [con0, con1, con2, con3])

    try:
        step = 0
        for i in range(step_max):
            lgpio.group_write(h, con0, steps[step])
            step = (step - 1) % 8 if clockwise else (step + 1) % 8
            sleep(delay)
    except KeyboardInterrupt:
        lgpio.group_write(h, con0, 0)
        lgpio.group_free(h, con0)
        lgpio.gpiochip_close(h)
        exit(1)

    lgpio.group_write(h, con0, 0)
    lgpio.group_free(h, con0)
    lgpio.gpiochip_close(h)

#From what I can find on Google, pwm control of a stepper motor seems to be locking duty_cycle at 50 and control by frequency
#One pulse = one step
def pwm_spin_motor(f_pwm = 250, clockwise = True, spin_time = 5, con0 = 17, con1 = 27, con2 = 22, con3 = 23):
    #Hz to S
    delay = 1 / f_pwm
    spin_motor(clockwise, spin_time, delay, None, con0, con1, con2, con3)



def spin_check_deg(degree, clockwise = True):
    ADDRESS_MAG = 0x1E

    REG_MAG_CFG_A = 0x60

    REG_MAG_X_L = 0x68
    REG_MAG_Y_L = 0x6A
    REG_MAG_Z_L = 0x6C

    h = lgpio.i2c_open(1, ADDRESS_MAG)

    #0 = 10Hz continuous mode
    lgpio.i2c_write_byte_data(h, REG_MAG_CFG_A, 0)

    start_x = lgpio.i2c_read_byte_data(h, REG_MAG_X_L)
    start_y = lgpio.i2c_read_byte_data(h, REG_MAG_Y_L)
    start_z = lgpio.i2c_read_byte_data(h, REG_MAG_Z_L)
    print(f"Start X: { start_x }\tStart Y: { start_y }\tStart Z: { start_z }")

    steps = int(degree * 4096 / 360)
    print(f"{degree} degrees = {steps} steps")

    spin_motor(clockwise, 0.004, steps)
    sleep(0.2) #let the sensor settle

    x = lgpio.i2c_read_byte_data(h, REG_MAG_X_L)
    y = lgpio.i2c_read_byte_data(h, REG_MAG_Y_L)
    z = lgpio.i2c_read_byte_data(h, REG_MAG_Z_L)
    print(f"End X: { x }\tEnd Y: { y }\tEnd Z: { z }")

    print(f"Calculated angle: {degrees(atan2(y, x))}")

    lgpio.i2c_close(h)


spin_check_deg(15)
print()
sleep(0.2)
spin_check_deg(15, False)