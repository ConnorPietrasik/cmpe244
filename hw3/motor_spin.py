import lgpio
import time
#Connor Pietrasik 015126007

def spin_motor(clockwise = True, spin_time = 5, delay = 0.008, con1 = 17, con2 = 27, con3 = 22, con4 = 23):
    step_max = spin_time / delay
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
    lgpio.group_claim_output(h, [con1, con2, con3, con4])

    try:
        step = 0
        for i in range(step_max):
            lgpio.group_write(h, con1, steps[step])
            step = (step - 1) % 8 if clockwise else (step + 1) % 8
            time.sleep(delay)
    except KeyboardInterrupt:
        lgpio.group_write(h, con1, 0)
        lgpio.group_free(h, con1)
        lgpio.gpiochip_close(h)
        exit(1)

    lgpio.group_write(h, con1, 0)
    lgpio.group_free(h, con1)
    lgpio.gpiochip_close(h)


spin_motor()
spin_motor(False)