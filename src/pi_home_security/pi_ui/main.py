try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import pi_home_security.pi_ui.dashboard as GPIO



GPIO.setmode(GPIO.BCM)

for pin in range(1,101):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.run_ui()
