#!/usr/bin/env python

import sys
from core.mud_game import MudGame

DB_PATH = "data/mud.db"

def main():
    game = MudGame(DB_PATH)
    game.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
