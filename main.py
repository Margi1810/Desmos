"""Launch the Desmos-style graphing application."""
def main():
    from app.ui.window import DesmosWindow
    window = DesmosWindow()
    window.run()

if __name__ == "__main__":
    main()
