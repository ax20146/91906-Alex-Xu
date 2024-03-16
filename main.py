# /main.py


from source import Window, create_window


def main() -> None:
    window: Window = create_window()
    window.run()


if __name__ == "__main__":
    main()
