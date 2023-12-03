import lgpio
from time import sleep
from threading import Thread

def spin_motor():
    con = [17, 27, 22, 23]

    #Half-step, so step_max = 4096 for full rotation
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
    lgpio.group_claim_output(h, con)

    try:
        step = 0
        while enable:
            lgpio.group_write(h, con[0], steps[step])
            step = (step - 1) % 8 if clockwise else (step + 1) % 8
            sleep(delay)
    except Exception:
        lgpio.group_write(h, con[0], 0)
        lgpio.group_free(h, con[0])
        lgpio.gpiochip_close(h)
        exit(1)

def start():
    global enable, pwm_thread, clockwise
    enable = True
    clockwise = True
    pwm_thread = Thread(target=spin_motor)
    pwm_thread.start()

def stop():
    global enable
    enable = False

def write(h, pin, val):
    global clockwise
    clockwise = True if val else False

def pwm(h, pwm_pin, f_pwm, duty = 0):
    if duty and duty != 50:
        lgpio.tx_pwm(h, pwm_pin, f_pwm, duty)
    else:
        global enable, delay
        if f_pwm:
            delay = 1 / f_pwm
            if not enable:
                start()
        else:
            enable = False