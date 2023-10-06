import lgpio
import time

LED = 17
INPIN = 22

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, INPIN)
lgpio.gpio_claim_output(h, LED)

try:
	while True:
		if lgpio.gpio_read(h, INPIN) > 0:
			print("1")
			lgpio.gpio_write(h, LED, 1)
		else:
			print("0")
			lgpio.gpio_write(h, LED, 0)
		time.sleep(0.5)
		
except KeyboardInterrupt:
	lgpio.gpio_write(h, LED, 0)
	lgpio.gpio_free(h, LED)
	lgpio.gpio_free(h, INPIN)
	lgpio.gpiochip_close(h)