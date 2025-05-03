import sys

def main():
    if "--cli" in sys.argv:
        from pi_home_security.pi_cli.cli import main as cli_main
        cli_main()
    else:
        from pi_home_security.pi_ui.dashboard import main as ui_main
        ui_main()

if __name__ == "__main__":
    main()
