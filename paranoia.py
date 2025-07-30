#!/usr/bin/env python

from core.mud_game import MudGame

DB_PATH = "data/mud.db"

if __name__ == "__main__":
    game = MudGame(DB_PATH)
    game.run()

