from core.config import Config


def main():
    print("PriceWatcher initialized.")
    print(f"Checking prices every {Config.INTERVAL_MINUTES} minutes.")


if __name__ == "__main__":
    main()
