try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import mock_gpio_ui as GPIO

from rpi_home_security.pi_board import PiBoard

pi = PiBoard()

GPIO.setmode(GPIO.BCM)

for pin in range(1,100):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.run_ui()
