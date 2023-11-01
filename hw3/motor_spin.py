import lgpio
import time
#Connor Pietrasik 015126007

#step_max overrides spin_time if set, otherwise calculated based on spin_time and delay
def spin_motor(clockwise = True, spin_time = 5, delay = 0.004, step_max = None, con0 = 17, con1 = 27, con2 = 22, con3 = 23):
    #half-step, so step_max = 4096 for full rotation
    if step_max is None:
        step_max = int(spin_time / delay) + 1
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
            time.sleep(delay)
    except KeyboardInterrupt:
        lgpio.group_write(h, con0, 0)
        lgpio.group_free(h, con0)
        lgpio.gpiochip_close(h)
        exit(1)

    lgpio.group_write(h, con0, 0)
    lgpio.group_free(h, con0)
    lgpio.gpiochip_close(h)


spin_motor()
spin_motor(False)