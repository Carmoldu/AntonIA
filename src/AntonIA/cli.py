# src/AntonIA/cli.py
import argparse
import logging
from AntonIA.pipeline import main as run_pipeline

def main():
    parser = argparse.ArgumentParser(
        description="AntonIA - Morning image and caption generator ☕🐓"
    )

    parser.add_argument(
        "--persona",
        type=str,
        default="default",
        help="Name of the persona configuration to use (without .yaml extension)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug logging output",
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
    )

    # Run the pipeline
    run_pipeline(persona=args.persona, config_dir=args.config_dir)

if __name__ == "__main__":
    main()
