# TieBreakServer

Chess tournament tools: Swiss/Berger pairing, tie-break calculation, TRF/JSON/TS I/O, and a stdin/stdout JSON service.

Software version: **1.9.57** (see `version.py`). Behaviour is documented in [`docs/GacruxSoftware.pdf`](docs/GacruxSoftware.pdf) (Ver. 1.9). Regenerate that PDF with `python docs/build_gacrux_spec.py`.

## Install

- Download / clone this project
- Python **3.8+** (3.8 is the last version that runs on Windows 7)
- Install dependencies: see `requirements.txt`

Main entry points:

- `python pairingchecker.py`
- `python tiebreakchecker.py`
- `python tournamentgenerator.py`
- `python chessserver.py` (stdin/stdout service)

## chessserver.py deployment

`chessserver.py` is a local stdin/stdout JSON helper (CGI-style). It has **no authentication**. Do not expose it directly on a network; put it behind a reverse proxy or application that enforces auth, size limits, and an allowlisted request schema. Prefer in-memory payloads (`base64` / `jch` / `data`) over host file paths.

Request body shape: `{"command": { ...options... }}`. See the Gacrux spec for the full allowlist.

## Common command-line parameters

Used by pairingchecker, tiebreakchecker, and tournamentgenerator:

| Option | Description |
|--------|-------------|
| `-i`, `--input-file <file>` | Input path; `-` = stdin (default) |
| `-o`, `--output-file <file>` | Output path; `-` = stdout (default) |
| `-f`, `--input-format <fmt>` | `JSON`, `TRF`, or `TS`. Default: **TRF**. (`JCH` is not a valid `-f` value; use `JSON`. Extensions `.jch`/`.json` map to JSON via helpers when sniffing filenames.) |
| `-F`, `--output-format <fmt>` | `JSON` (default), `TRF`, or `TXT`. If `-d` is set, text output is used regardless of `-F`. |
| `-b`, `--encoding <enc>` | Character encoding ([Python codecs](https://docs.python.org/3/library/codecs.html#standard-encodings)). If omitted: JSON→utf-8, TRF→latin1, TS→ascii. |
| `-e`, `--tournament-number <n>` | Tournament index in multi-event files (1-based). `0` = passthrough / all where supported. Default: `1`. |
| `-n`, `--current-round <n>` | Round override (`-1` = program/file default). |
| `-N`, `--number-of-rounds <n>` | Overrides tournament round count when &gt; 0. |
| `-G`, `--game-score <key:val …>` | Override game point system. |
| `-M`, `--match-score <key:val …>` | Override match point system. |
| `-c`, `--check` | Check mode (program-specific). |
| `-r`, `--rank` | Sort text output in rank order (tiebreakchecker). |
| `-d`, `--delimiter <text>` | Force text output. `T`=tab, `B`=blank, `S`=semicolon, `C`=comma, `@`=status code line, or literal text. Default without `-d`: JSON. |
| `-D`, `--decimal-point <text>` | Decimal mark in text: `P`=point, `C`=comma, or literal. |
| `-x`, `--experimental <list>` | Experimental keywords (e.g. `weighted`). |
| `-v`, `--verbose` | Progress / debug (repeatable). |
| `-V`, `--version` | Print version and exit. |

TRF input follows the FIDE tournament report format (see current FIDE TRF documentation).

## Pairingchecker

### Options

| Option | Description |
|--------|-------------|
| `-p`, `--pairing` | Compute pairing. |
| `-a`, `--analysis` | Analyse existing pairing. |
| `-c`, `--check` | Compare computed pairing to the file. |
| `-m`, `--method <name>` | `dutch` or `berger` (also `dutch-mp` / `dutch-gp` for primary score). Default falls back to tournament / dutch. |
| `-t`, `--top-color <w\|b>` | Colour for top competitor in round 1. |
| `-u`, `--unpaired <cid …>` | Competitors not paired for this run. |
| `-K`, `--maxmeets <n>` | Max meetings between the same pair (effective minimum 1). |
| `-T`, `--exchange <a-b …>` | Test mode: rewrite pairs then re-analyse (use with `-c -a -p -n`). |

Round defaults when `-n` is omitted: `-p` → next round; `-a` → last paired; `-c` → all played rounds.

### Examples

```text
python pairingchecker.py -i infile.trf -o outfile.json -p
python pairingchecker.py -i infile.trf -c -dT
python pairingchecker.py -i infile.trf -c -a -p -n 3 -dT -x weighted
```

## Tiebreakchecker

### Options

| Option | Description |
|--------|-------------|
| `-t`, `--tiebreak <list>` | Rank-order specifiers. If empty and the tournament has `rankOrder`, that list is used. |
| `-p`, `--pre-determined` | Pre-determined (round-robin) unplayed-game rules. |
| `-s`, `--swiss` | Swiss unplayed-game rules. |
| `-r`, `--rank` | Print rows in rank order. |
| `-u`, `--unrated <rating>` | Rating substituted for unrated players. |

### Rank-order syntax

`TB:PS/Mn/opt` — for example `PTS`, `BH/C1`, `DE/P`, `BH:GP/C1`.

- **TB** — tie-break name (required)
- **:PS** — team score selector: `:MP` or `:GP` (ESB also `:MM` / `:MG` / `:GM` / `:GG`)
- **/Mn** — modifiers such as `/C1`, `/M1`, `/L+2`, `/U1400`, `/V2026`, `/P`, `/F`, `/R`
- Full catalogue: [tie-break list](https://fide-tec.gacrux.no:9001/tbs/tiebreaklist.html) and `docs/GacruxSoftware.pdf`

### Examples

```text
python tiebreakchecker.py -i infile.trf -o outfile.json -t PTS DE BH BH/C1 WON
python tiebreakchecker.py -i infile.trf -c -dT -t PTS DE BH/C1 WON
```

## Tournamentgenerator

Generates synthetic TRF tournaments for testing (uses the same pairing engines).

### Options

| Option | Description |
|--------|-------------|
| `-g`, `--generate …` | Count, or `start count`, or `start count step`. Default: `0 1000`. |
| `-o`, `--output-file` | Output path; `%d` → zero-padded tournament number. |
| `-p`, `--players <n>` | Number of competitors. Default: `40`. |
| `-T`, `--members <n>` | Players per team. Default: `1`. |
| `-m`, `--method <name>` | `dutch` or `berger`. Default: `dutch`. |
| `-n` / `-N` | Number of rounds (via common options). |
| `-t`, `--top-color <w\|b>` | Accepted; generator currently alternates by file number. |
| `-R`, `--rating [top step sigma]` | Rating model. |
| `-S`, `--statistics [zpb hpb forfeited]` | Bye / forfeit rates. Default: `0.01 0.05 0.02`. |
| `-a`, `--acceleration` | Baku acceleration. |
| `-K`, `--maxmeets <n>` | Max meetings. |

### Example

```text
python tournamentgenerator.py -n 9 -x weighted -p 15 -R 2200 10 50.0 -S 0.02 0.10 0.04 -o C:/temp/t_n9_p15_d10_s50/T%d.trf -g 10000
```

Creates `C:/temp/t_n9_p15_d10_s50` and writes `T0000.trf` … `T9999.trf`.
