# src/AntonIA/cli.py
"""Thin wrapper that exposes the Hydra-backed pipeline entrypoint.

Hydra already provides a rich CLI for selecting configurations, so there is no
need to maintain custom argparse logic here.  Users can simply invoke
``python -m AntonIA.cli`` or ``python -m AntonIA.pipeline`` directly.
"""

from AntonIA.pipeline import main

# the function imported above is decorated with ``@hydra.main``; invoking it
# will launch the Hydra CLI.

if __name__ == "__main__":
    main()
