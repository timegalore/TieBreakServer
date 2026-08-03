# -*- coding: utf-8 -*-
"""Shared fixtures for TieBreakServer unit tests."""
from decimal import Decimal

from chessjson import chessjson


DEFAULT_GAME_SCORE = {
    "W": Decimal("1.0"),
    "D": Decimal("0.5"),
    "L": Decimal("0.0"),
    "F": "W",
    "H": "D",
    "Z": Decimal("0.0"),
    "P": "W",
    "A": "D",
    "U": "Z",
}

DEFAULT_MATCH_SCORE = {
    "W": Decimal("2.0"),
    "D": Decimal("1.0"),
    "L": Decimal("0.0"),
    "F": "W",
    "H": "D",
    "Z": Decimal("0.0"),
    "P": "D",
    "A": "D",
    "U": "Z",
}


def make_game(rnd, white, black, w_result, played=True, rated=True, game_id=None):
    game = {
        "id": game_id if game_id is not None else rnd * 100 + white,
        "round": rnd,
        "white": white,
        "black": black,
        "played": played,
        "rated": rated,
        "wResult": w_result,
    }
    reverse = {"W": "L", "D": "D", "L": "W", "Z": "W", "P": "L", "H": "H", "U": "U", "A": "A"}
    if black > 0 and w_result in reverse:
        game["bResult"] = reverse[w_result]
    elif black == 0:
        game["bResult"] = "Z"
    return game


def make_competitor(cid, rating=2000, rank=0, present=True, points=None):
    cmp = {
        "cid": cid,
        "profileId": cid,
        "present": present,
        "rank": rank if rank else cid,
        "rating": rating,
        "random": cid,
    }
    if points is not None:
        cmp["gamePoints"] = points
    return cmp


def make_individual_tournament(
    num_rounds=3,
    competitors=None,
    games=None,
    tournament_type="Swiss",
    start_date="2025-06-01",
):
    """Build a minimal individual tournament usable by tiebreak/pairing."""
    if competitors is None:
        competitors = [make_competitor(i, rating=2100 - i * 10) for i in range(1, 5)]
    if games is None:
        # Round 1: 1W-2, 3W-4 ; Round 2: 1W-3, 2W-4 ; Round 3: 1W-4, 2W-3
        games = [
            make_game(1, 1, 2, "W"),
            make_game(1, 3, 4, "D"),
            make_game(2, 1, 3, "W"),
            make_game(2, 2, 4, "W"),
            make_game(3, 1, 4, "D"),
            make_game(3, 2, 3, "L"),
        ]
    return {
        "tournamentNo": 1,
        "tournamentType": tournament_type,
        "ratingList": "TRF",
        "numRounds": num_rounds,
        "currentRound": num_rounds,
        "teamTournament": False,
        "teamSize": 1,
        "rankOrder": ["PTS"],
        "competitors": competitors,
        "scoreSystem": {
            "game": dict(DEFAULT_GAME_SCORE),
            "match": dict(DEFAULT_MATCH_SCORE),
            "primary": "game",
        },
        "gameList": games,
        "matchList": [],
        "maxMeets": 1,
        "accelerated": None,
        "tournamentInfo": {"startDate": start_date},
        "topColor": "w",
    }


def make_event_with_tournament(tournament=None):
    cj = chessjson()
    if tournament is None:
        tournament = make_individual_tournament()
    cj.chessjson["event"]["tournaments"] = [tournament]
    for cmp in tournament["competitors"]:
        cj.append_profile(
            {
                "id": 0,
                "fideId": cmp["cid"],
                "firstName": "P%d" % cmp["cid"],
                "lastName": "Player",
                "sex": "m",
                "federation": "NOR",
                "rating": [cmp.get("rating") or 0],
            }
        )
        cmp["profileId"] = cj.chessjson["event"]["profiles"][-1]["id"]
    return cj


def minimal_trf_four_players():
    """Minimal TRF-16 style file with 4 players and 3 rounds."""

    def player(startno, name, rating, points, rank, games):
        line = [" "] * 91
        line[0:3] = list("001")
        line[4:8] = list("%4d" % startno)
        line[9] = "m"
        line[10:13] = list("%-3s" % "")
        line[14:47] = list(("%-33s" % name)[:33])
        line[48:52] = list("%4d" % rating)
        line[53:56] = list("%-3s" % "NOR")
        line[57:68] = list("%11d" % startno)
        line[69:79] = list("%-10s" % "1990/01/01")
        line[80:84] = list("%4.1f" % points)
        line[85:89] = list("%4d" % rank)
        out = "".join(line)
        for opp, color, result in games:
            chunk = "%4d %s %s  " % (opp, color, result)
            out += chunk[:10].ljust(10)
        return out

    lines = [
        "012 Unit Test Swiss",
        "022 Test City",
        "032 2025/06/01",
        "042 2025/06/03",
        "062 4",
        "092 Swiss System",
        player(1, "Alpha, Ada", 2100, 2.5, 1, [(2, "w", "1"), (3, "w", "1"), (4, "w", "=")]),
        player(2, "Beta, Bob", 2000, 1.0, 3, [(1, "b", "0"), (4, "w", "1"), (3, "w", "0")]),
        player(3, "Gamma, Gus", 1900, 1.5, 2, [(4, "w", "="), (1, "b", "0"), (2, "b", "1")]),
        player(4, "Delta, Dee", 1800, 1.0, 4, [(3, "b", "="), (2, "b", "0"), (1, "b", "=")]),
    ]
    return "\n".join(lines) + "\n"


def tiebreak_params(tiebreaks=None, current_round=-1, check=False, swiss=True):
    return {
        "tiebreak": tiebreaks or ["PTS", "BH", "SNO"],
        "current_round": current_round,
        "check": check,
        "pre_determined": False,
        "swiss": swiss,
        "is_rr": False if swiss else True,
        "unrated": None,
        "rank": True,
        "verbose": 0,
        "experimental": [],
    }
