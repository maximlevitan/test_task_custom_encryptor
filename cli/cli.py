import argparse
from engine.engine import EncryptionEngine


def main():
    parser = argparse.ArgumentParser(description="Custom Encryption CLI")
    parser.add_argument("mode", choices=["encrypt","decrypt"], help="Mode")
    parser.add_argument("text", type=str, help="Text to process")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    engine = EncryptionEngine()

    if args.mode == "encrypt":
        result = engine.encrypt(args.text, verbose=args.verbose)
    else:
        result = engine.decrypt(args.text, verbose=args.verbose)

    print(result)


if __name__ == "__main__":
    main()
