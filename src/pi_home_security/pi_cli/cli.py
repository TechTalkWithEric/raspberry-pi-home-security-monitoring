import argparse
from pi_home_security.pi_service.service import get_gpio_service

def main():
    gpio = get_gpio_service()

    parser = argparse.ArgumentParser(description="Control GPIO via CLI")
    parser.add_argument("action", choices=["read", "write", "setup_input", "setup_output", "cleanup"])
    parser.add_argument("--pin", type=int, required=True, help="GPIO pin number")
    parser.add_argument("--value", type=int, choices=[0, 1], help="Value for write (0 or 1)")

    args = parser.parse_args()

    if args.action == "setup_input":
        gpio.setup_input(args.pin)
    elif args.action == "setup_output":
        gpio.setup_output(args.pin)
    elif args.action == "read":
        val = gpio.read(args.pin)
        print(f"Pin {args.pin} is {'HIGH' if val else 'LOW'}")
    elif args.action == "write":
        gpio.write(args.pin, bool(args.value))
        print(f"Wrote {'HIGH' if args.value else 'LOW'} to pin {args.pin}")
    elif args.action == "cleanup":
        gpio.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()
