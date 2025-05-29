#!/usr/bin/env python3
"""
Generate ping-pong ladder challenge pairings.

The CSV is assumed to be ranked top-to-bottom by current ladder position.
Each player may challenge someone 1-4 rungs below

Usage:
    python ladder-pairing.py ladder.csv
"""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# how far down the ladder you can challenge
MAX_GAP: int = 4 

def load_players(csv_path: Path) -> List[Dict[str, str]]:
    """Return all non-blank Player rows in ladder order."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row.get("Player")]

# Returns row index of chosen opponent
def choose_opponent(total_players: int, player_index: int, already_matched: Set[int]) -> int | None:
    start, end = player_index + 1, min(player_index + MAX_GAP + 1, total_players)
    available_opponents = [i for i in range(start, end) if i not in already_matched]
    return random.choice(available_opponents) if available_opponents else None


def create_pairings(player_rows: List[Dict[str, str]]) -> List[Tuple[int, int]]:
    already_matched, pairings = set(), []
    total_players = len(player_rows)

    for player_index in range(total_players):
        if player_index in already_matched:
            continue

        opponent_index = choose_opponent(total_players, player_index, already_matched)
        if opponent_index is not None:
            pairings.append((player_index, opponent_index))
            already_matched.update({player_index, opponent_index})
        else:
            already_matched.add(player_index)

    return pairings



def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python ladder-pairing.py ladder.csv")
    
    player_rows = load_players(Path(sys.argv[1]))
    pairings = create_pairings(player_rows)
    
    print("Challenges:")
    for challenger_index, opponent_index in pairings:
        challenger = player_rows[challenger_index]['Player']
        opponent = player_rows[opponent_index]['Player']
        print(f"  {challenger} vs {opponent}")
    
    # Find players without opponents
    players_without_opponents = {
        player_rows[i]["Player"] for i in range(len(player_rows))
        if all(i not in pairing for pairing in pairings)
    }
    
    for player_name in players_without_opponents:
        print(f"  {player_name} has no opponent this round")


if __name__ == "__main__":
    main()