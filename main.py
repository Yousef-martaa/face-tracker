# filename: main.py

from MANAGER.manager import Manager


def main():
    """Application entry point.

    Creates the system manager and starts the application.
    This function contains no business logic.
    """
    system = Manager()
    system.run()


if __name__ == "__main__":
    main()