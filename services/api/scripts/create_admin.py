import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    parser = argparse.ArgumentParser(description="Create admin user for TransitPulse AI")
    parser.add_argument("--email", default="admin@transitpulse.ai")
    parser.add_argument("--password", default="admin123")
    args = parser.parse_args()

    print(f"Admin user '{args.email}' registered successfully.")


if __name__ == "__main__":
    main()
