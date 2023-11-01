import lgpio
import time
#Connor Pietrasik 015126007

OUT1 = 25
OUT2 = 8
OUT3 = 7
OUT4 = 1

delay = 0.2

step_max = 50
clockwise = True

pins = [OUT1, OUT2, OUT3, OUT4]

#half-step sequence
steps = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

h = lgpio.gpiochip_open(0)
lgpio.group_claim_output(h, pins)

def cleanup():
    lgpio.group_write(h, pins, [0,0,0,0])
    lgpio.group_free(h, pins)
    lgpio.gpiochip_close(h)

try:
    step = 0
    for i in range(step_max):
        lgpio.group_write(h, pins, steps[])
        step = (step - 1) % 8 if clockwise else (step + 1) % 8
        time.sleep(delay)
except KeyboardInterrupt:
     cleanup()

cleanup()