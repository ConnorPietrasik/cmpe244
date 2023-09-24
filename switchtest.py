import lgpio
import time

INPIN = 22

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, INPIN)

try:
	while True:
		if lgpio.gpio_read(h, INPIN) > 0:
			print("1\n")
		else:
			print("0\n")
		
except KeyboardInterrupt:
	lgpio.gpio_free(h, INPIN)
	lgpio.gpiochip_close(h)