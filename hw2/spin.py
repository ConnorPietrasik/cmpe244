import lgpio
import sys
#Connor Pietrasik 015126007

PWM_OUT = 18

#f_pwm expected as first argument, 1-10000
f_pwm = 10000
if (len(sys.argv) > 1):
    f_pwm = int(sys.argv[1])
	
#duty_cycle expected as second argument, 0-100 int for percentage
duty_cycle = 90
if (len(sys.argv) > 2):
    f_pwm = int(sys.argv[2])

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, PWM_OUT)

try:
    while True:
        lgpio.tx_pwm(h, 0, f_pwm, duty_cycle)
        duty_cycle = int(input())

except KeyboardInterrupt:
	lgpio.tx_pwm(h, 0, 0)
	lgpio.gpio_free(h, PWM_OUT)
	lgpio.gpiochip_close(h)
