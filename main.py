#!/usr/bin/env python3
"""
RedBall – Arcade Futuristic Platform Game
Entry point.

Usage:
    pip install -r requirements.txt
    python main.py
"""
import sys
import os

# Ensure the project root is on the path regardless of CWD
sys.path.insert(0, os.path.dirname(__file__))

from core import GameLoop


def main():
    game = GameLoop()
    game.run()


if __name__ == "__main__":
    main()
