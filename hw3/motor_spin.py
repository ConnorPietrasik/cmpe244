import lgpio
import time
#Connor Pietrasik 015126007

OUT1 = 17
OUT2 = 27
OUT3 = 22
OUT4 = 23

delay = 0.2

step_max = 50
clockwise = True

pins = [OUT1, OUT2, OUT3, OUT4]

#Half-step sequence
# steps = [
#     [1,0,0,1],
#     [1,0,0,0],
#     [1,1,0,0],
#     [0,1,0,0],
#     [0,1,1,0],
#     [0,0,1,0],
#     [0,0,1,1],
#     [0,0,0,1]
# ]

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
lgpio.group_claim_output(h, [OUT1, OUT2, OUT3, OUT4])

def cleanup():
    lgpio.group_write(h, OUT1, 0)
    lgpio.group_free(h, OUT1)
    lgpio.gpiochip_close(h)

try:
    step = 0
    for i in range(step_max):
        lgpio.group_write(h, OUT1, steps[step])
        step = (step - 1) % 8 if clockwise else (step + 1) % 8
        time.sleep(delay)
except KeyboardInterrupt:
     cleanup()

cleanup()


#Can't use GPIO group because that sets them all the same, unfortunately
# for pin in pins:
#     lgpio.gpio_claim_output(h, pin)

# def cleanup():
#     for pin in pins:
#         lgpio.gpio_write(h, pin, 0)
#         lgpio.gpio_free(h, pin)
#     lgpio.gpiochip_close(h)

# try:
#     step = 0
#     for i in range(step_max):
#         lgpio.group_write(h, OUT1, steps[step])
#         step = (step - 1) % 8 if clockwise else (step + 1) % 8
#         time.sleep(delay)
# except KeyboardInterrupt:
#      cleanup()

# cleanup()