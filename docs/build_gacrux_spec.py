# -*- coding: utf-8 -*-
"""Build GacruxSoftware.pdf aligned to TieBreakServer v1.9.57."""
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).with_name("GacruxSoftware.pdf")
OUT_FALLBACK = Path(__file__).with_name("GacruxSoftware-1.9.pdf")

PAGE_W, PAGE_H = A4


def styles():
    base = getSampleStyleSheet()
    s = {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            spaceAfter=6,
            alignment=TA_LEFT,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#444444"),
            spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            spaceBefore=10,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12,
            leftIndent=12,
            spaceAfter=2,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8,
            leading=10,
            backColor=colors.HexColor("#F5F5F5"),
            spaceBefore=4,
            spaceAfter=8,
            leftIndent=4,
            rightIndent=4,
        ),
        "tablecell": ParagraphStyle(
            "TCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
        ),
        "tablehead": ParagraphStyle(
            "THead",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=colors.HexColor("#555555"),
            spaceAfter=8,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            alignment=TA_CENTER,
        ),
    }
    return s


def P(text, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


def code_block(text, s):
    return Preformatted(text.rstrip() + "\n", s["code"])


def simple_table(headers, rows, s, col_widths=None):
    data = [[P(h, s["tablehead"]) for h in headers]]
    for row in rows:
        data.append([P(str(c), s["tablecell"]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#AAAAAA")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def add_page_number(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W / 2, 12 * mm, str(page))
    canvas.restoreState()


def build():
    s = styles()
    story = []

    # ----- Title / intro -----
    story.append(P("Gacrux software", s["title"]))
    story.append(
        P(
            "Ver. 1.9, aligned to TieBreakServer 1.9.57 (2026-07-21)<br/>"
            "Original author: Otto Milvang<br/>"
            "Ver. 1.9 update (August 3, 2026): Paul Hampton - aligned this specification to the "
            "implementation (code is authoritative)",
            s["meta"],
        )
    )
    story.append(P("Introduction", s["h1"]))
    story.append(
        P(
            "The Gacrux software is a collection of tools and shared data structures designed to "
            "support Tournament Handler Programs (THPs) for chess events. Its core purpose is to "
            "provide a consistent, transparent, and verifiable representation of tournament data-"
            "covering players, rounds, pairings, results, rankings, and tiebreaks-throughout the "
            "lifecycle of an event.",
            s["body"],
        )
    )
    story.append(
        P(
            "At the heart of Gacrux is a unified internal structure that can be serialized to and "
            "from JSON. In this document that structure is called the <b>Json Chess</b> representation. "
            "On the command line and in file I/O the format name is <b>JSON</b> (file extensions "
            "<font face='Courier'>.jch</font> and <font face='Courier'>.json</font> both map to "
            "JSON). The structure is designed to be human-readable, machine-processable, and easy "
            "to extend.",
            s["body"],
        )
    )
    story.append(
        P(
            "Gacrux includes command-line programs for pairing generation and verification, "
            "tiebreak calculation, ranking checks, and synthetic tournament generation. These tools "
            "operate on JSON files or import and export common tournament formats, including "
            "FIDE TRF and TournamentService (TS) files.",
            s["body"],
        )
    )
    story.append(
        P(
            "Every operation produces structured output that includes status codes, diagnostics, "
            "and-when requested-detailed explanations of pairing and tiebreak decisions.",
            s["body"],
        )
    )

    story.append(P("Json Chess (JSON)", s["h1"]))
    story.append(
        P(
            "The Json Chess file defines the canonical data structure used by the Gacrux software. "
            "A file encapsulates the complete state of a tournament, including identifiers, player "
            "and team data, rounds, pairings, results, rankings, and tiebreak information.",
            s["body"],
        )
    )
    story.append(
        P(
            "CLI and API format identifiers are <b>JSON</b>, <b>TRF</b>, and <b>TS</b>. The string "
            "<font face='Courier'>JCH</font> is not accepted as an <font face='Courier'>-f</font> / "
            "<font face='Courier'>-F</font> value; use <font face='Courier'>JSON</font>.",
            s["body"],
        )
    )
    story.append(
        P(
            "Each program records origin, options, status, and results in a consistent JSON "
            "envelope so transformations can be inspected, validated, and reproduced. The "
            "definition is versioned; backward-compatible extensions may be introduced as needed.",
            s["body"],
        )
    )

    # ----- Common CLI -----
    story.append(P("Programs", s["h1"]))
    story.append(P("Common program syntax", s["h2"]))
    story.append(
        P(
            "Command-line options are divided into common options (I/O, encoding, verbosity, "
            "tournament selection) and program-specific options.",
            s["body"],
        )
    )
    story.append(code_block("python programname.py [options]", s))

    story.append(
        simple_table(
            ["Option", "Description", "Default"],
            [
                [
                    "-i, --input-file &lt;filename&gt;",
                    'Path to input file. "-" = stdin.',
                    "stdin (-)",
                ],
                [
                    "-o, --output-file &lt;filename&gt;",
                    'Path to output file. "-" = stdout.',
                    "stdout (-)",
                ],
                [
                    "-f, --input-format &lt;format&gt;",
                    "JSON - TRF - TS. Other values are rejected (status 403).",
                    "TRF",
                ],
                [
                    "-F, --output-format &lt;format&gt;",
                    "JSON - TRF - TXT. If -d is set, text output is used regardless of -F. "
                    "TS output is not implemented.",
                    "JSON",
                ],
                [
                    "-b, --encoding &lt;encoding&gt;",
                    "Python codec name (ascii, utf-8, cp1252, ...).",
                    "JSON->utf-8; TRF->latin1; TS->ascii",
                ],
                [
                    "-e, --tournament-number &lt;n&gt;",
                    "Tournament index in multi-event files (1-based). 0 = all / passthrough where supported.",
                    "1",
                ],
                [
                    "-n, --current-round &lt;n&gt;",
                    "Round override; meaning depends on the program (-1 = use file / program default).",
                    "-1",
                ],
                [
                    "-N, --number-of-rounds &lt;n&gt;",
                    "Overrides tournament numRounds when &gt; 0.",
                    "0",
                ],
                [
                    "-G, --game-score &lt;key:val ...&gt;",
                    "Override game point system (KEY:val or KEY=val, comma-separated groups).",
                    "see score table",
                ],
                [
                    "-M, --match-score &lt;key:val ...&gt;",
                    "Override match point system.",
                    "see score table",
                ],
                ["-c, --check", "Check mode (count flag). Meaning is program-specific.", "off"],
                ["-r, --rank", "Sort text output in rank order (tiebreakchecker).", "off"],
                [
                    "-d, --delimiter &lt;text&gt;",
                    'Force text output. T=tab, B=blank, S=semicolon, C=comma, @=status line, or literal text.',
                    "unset -> JSON",
                ],
                [
                    "-D, --decimal-point &lt;text&gt;",
                    "Decimal mark in text output. C=comma, P=point, or literal.",
                    "unset",
                ],
                [
                    "-x, --experimental &lt;list&gt;",
                    'Experimental keywords (e.g. "weighted", "time", "DUMP").',
                    "[]",
                ],
                ["-v, --verbose", "Progress / debug (count: -v, -vv, ...).", "0"],
                ["-V, --version", "Print version string and exit.", "off"],
            ],
            s,
            col_widths=[4.2 * cm, 9.0 * cm, 3.8 * cm],
        )
    )
    story.append(
        P(
            "Note: argparse default for -f is always TRF. Extension-based detection via "
            "helpers.getFileFormat() is used by chessserver when resolving input_filename, "
            "not by the standalone CLI parsers.",
            s["caption"],
        )
    )

    story.append(P("Score system defaults (-G / -M)", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Meaning", "Default game (-G)", "Default match (-M)"],
            [
                ["W", "Win", "1.0", "2.0"],
                ["D", "Draw", "0.5", "1.0"],
                ["L", "Loss", "0.0", "0.0"],
                ["Z", "Zero point bye", "0.0", "0.0"],
                ["P", "Pairing allocated bye", "W", "D"],
                ["A", "Adjourned", "D", "D"],
                ["F", "Full point bye", "W", "W"],
                ["H", "Half point bye", "D", "D"],
                ["U", "Unknown", "Z", "Z"],
                ["FG / HG / ZG / PG", "Match game-points for F/H/Z/P", "-", "W* / D* / Z* / P*"],
            ],
            s,
            col_widths=[3.5 * cm, 4.5 * cm, 4.5 * cm, 4.5 * cm],
        )
    )
    story.append(
        P(
            "Example (individual PAB as draw): <font face='Courier'>-G P:D</font>. "
            "X* means game points for X times team size.",
            s["caption"],
        )
    )

    story.append(P("JSON output envelope", s["h2"]))
    story.append(
        P(
            "Common JSON output has a header, status, and a result object keyed by program "
            "(pairingResult, tiebreakResult, ...). Mandatory fields are shown in bold in spirit; "
            "all of the following are always present on success paths.",
            s["body"],
        )
    )
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["filetype", "String", "Pairing - Tiebreak - Event - ..."],
                ["version", "String", "Envelope schema version (currently 1.0)"],
                ["published", "String", "Creation date-time (YYYY-MM-DD HH:MM:SS)"],
                ["origin", "String", "Program name and version"],
                ["options", "Object", "Parsed CLI / request options"],
                ["status", "Object", "code, info[], error[]"],
                ["&lt;filetype&gt;Result", "Object", "Operation result (not always an array)"],
            ],
            s,
            col_widths=[3.5 * cm, 2.5 * cm, 11 * cm],
        )
    )
    story.append(P("Status object", s["h3"]))
    story.append(
        simple_table(
            ["code", "Meaning"],
            [
                ["0", "OK; with -c, check passed"],
                ["1", "OK path with check failed"],
                ["2", "OK but no legal pairing (empty pairs)"],
                ["200-202", "Same semantics as 0-2 for web contexts where used"],
                ["400-499", "Client / input errors (e.g. 401 read, 403 format, 405 empty)"],
                ["500-599", "Internal / program errors"],
            ],
            s,
            col_widths=[3 * cm, 14 * cm],
        )
    )
    story.append(code_block(
        """{
  "filetype": "Pairing",
  "version": "1.0",
  "published": "2026-04-06 16:30:57",
  "origin": "pairingchecker ver. 1.9.57",
  "options": { "input_file": "test1315.trf", "input_format": "TRF", ... },
  "status": { "code": 0, "info": [], "error": [] },
  "pairingResult": { "rules": "2026-03-01", "round": 3, "pairs": [[1,6], ...] }
}""",
        s,
    ))

    # ----- pairingchecker -----
    story.append(PageBreak())
    story.append(P("pairingchecker.py", s["h1"]))
    story.append(code_block("python pairingchecker.py [options]", s))
    story.append(
        P(
            "Generate, analyse, and verify pairings according to the applicable pairing rules. "
            "In analysis mode the program explains the pairing already present for a round. "
            "In pairing mode it computes the best pairing. In check mode it compares the "
            "computed pairing to the tournament file.",
            s["body"],
        )
    )
    story.append(P("Options (in addition to common options)", s["h2"]))
    story.append(
        simple_table(
            ["Option", "Description", "Default"],
            [
                [
                    "-m, --method &lt;name&gt;",
                    "Pairing system. Legal engines: dutch, berger. "
                    "Suffixes after '-' set primary score: dutch-mp / dutch-gp "
                    "(also match/game). Token double raises maxMeets.",
                    "[] -> tournament pairingSystem, else dutch",
                ],
                [
                    "-n, --current-round &lt;n&gt;",
                    "Round to pair/analyse/check. "
                    "Defaults: -p -> next round; -a -> last paired; -c -> all played rounds.",
                    "-1",
                ],
                ["-p, --pairing", "Compute pairing (count flag).", "off"],
                ["-a, --analysis", "Analyse existing pairing (count flag).", "off"],
                [
                    "-c, --check",
                    "Compare pairing to analysis / file. With -p/-a adds detail; alone summaries rounds.",
                    "off",
                ],
                [
                    "-t, --top-color &lt;w|b&gt;",
                    "Colour for top competitor in round 1.",
                    "blank -> derived / random path",
                ],
                [
                    "-u, --unpaired &lt;cid ...&gt;",
                    "Competitors not to be paired (marked absent) for the run.",
                    "[]",
                ],
                [
                    "-K, --maxmeets &lt;n&gt;",
                    "Maximum meetings between the same pair. Effective value is at least 1.",
                    "0 -> clamped to >=1",
                ],
                [
                    "-T, --exchange &lt;a-b ...&gt;",
                    "Test mode: rewrite pairs then re-analyse (use with -c -a -p -n).",
                    "[]",
                ],
                [
                    "-x, --experimental &lt;...&gt;",
                    'weighted (reference algorithm), time, fakerank, TPN, QMM, DUMP, ...',
                    "[]",
                ],
            ],
            s,
            col_widths=[4.2 * cm, 9.5 * cm, 3.3 * cm],
        )
    )

    story.append(P("Json output - pairingResult", s["h2"]))
    story.append(
        P(
            "The top-level result key is <font face='Courier'>pairingResult</font>. It is a "
            "<b>single object</b> (not an array).",
            s["body"],
        )
    )
    story.append(P("Pairing / analysis mode (without -c)", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["rules", "String", "Rule date string used by the engine"],
                ["round", "Int", "Round paired or analysed"],
                ["pairs", "Array of [w,b]", "Computed pairs; b=0 is pairing-allocated bye"],
            ],
            s,
            col_widths=[3 * cm, 3.5 * cm, 10.5 * cm],
        )
    )
    story.append(code_block(
        """"pairingResult": {
  "rules": "2026-03-01",
  "round": 3,
  "pairs": [[1,6],[11,2],[5,10],[17,15],[7,3],[4,9],[12,16],[8,13],[14,0]]
}""",
        s,
    ))
    story.append(
        P(
            "Status code 0 if pairs is non-empty, else 2.",
            s["caption"],
        )
    )

    story.append(P("Check mode (-c)", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["rules", "String", "Rule date"],
                ["check", "Boolean", "True if all round checks passed"],
                ["roundpairing", "Array", "Per-round detail objects"],
            ],
            s,
            col_widths=[3.5 * cm, 2.5 * cm, 11 * cm],
        )
    )
    story.append(P("roundpairing element", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["round", "Int", "Round number"],
                ["pairs", "Array", "Checker pairing"],
                ["current", "Array", "Pairing from tournament file"],
                ["check", "Boolean", "pairs == current"],
                ["pairing", "Array", "Per-scorebracket pairing information"],
                ["analysis", "Array", "Per-scorebracket analysis of file pairing"],
                ["competitors", "Array", "Competitor snapshots used by the engine"],
                ["level2score", "Array", "Scorelevel -> points; PAB is -1.0 at level 0"],
            ],
            s,
            col_widths=[3.5 * cm, 2.5 * cm, 11 * cm],
        )
    )

    story.append(P("Pairing information (score bracket)", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["scorelevel", "Int", "Internal bracket index"],
                ["competitors", "Array of int", "Competitor ids in bracket"],
                ["pairs", "Array of objects", "Pair details"],
                ["downfloaters", "Array of int", "Downfloated competitors"],
                ["remaining", "Array of int", "Remaining competitors"],
                ["quality", "Object", "Named quality weights (QC6...HO5, ...); lower is better"],
                ["bsne / bsno", "Array", "BSN lists when present"],
                ["pab", "Boolean", "True if PAB level"],
            ],
            s,
            col_widths=[3.5 * cm, 3.5 * cm, 10 * cm],
        )
    )

    story.append(P("Pair details (dutch)", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["ca / cb", "Int", "Colour-independent competitor ids (cb >= ca)"],
                ["sa / sb", "Int", "Scorelevels"],
                ["w / b", "Int", "White / black ids; b=0 for PAB"],
                ["canmeet", "Boolean", "Legal meeting"],
                ["played", "Int", "Prior meetings"],
                ["quality", "Object", "Per-pair quality weights"],
                ["colorrule", "String", "Colour assignment rule id"],
                ["board", "Int/String", "Board number"],
                ["mode", "String", "Pairing mode marker"],
            ],
            s,
            col_widths=[3.5 * cm, 3 * cm, 10.5 * cm],
        )
    )

    story.append(P("Competitors (pairing snapshot)", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["cid", "Int", "Competitor id"],
                ["pts / acc", "Float", "Points / points + acceleration"],
                ["rfp", "Boolean", "Ready for pairing (present)"],
                ["hst / met", "Object", "History / opponents met"],
                ["num / rip", "Int", "Played games / rounds paired"],
                ["cod / cop / csq", "...", "Colour difference / preference / sequence"],
                ["flt", "Int", "Float bits (8=df, 4=uf previous; 2/1 two rounds earlier)"],
                ["top", "Boolean", "Top scorer"],
                ["scorelevel", "Int", "Score level"],
            ],
            s,
            col_widths=[3.5 * cm, 2.5 * cm, 11 * cm],
        )
    )

    story.append(P("Text output", s["h2"]))
    story.append(
        P(
            "<font face='Courier'>python pairingchecker.py -i &lt;input&gt; -o &lt;output&gt; -p -dT</font> "
            "prints the number of pairs, then lines <font face='Courier'>w b</font> "
            "(compatible with JaVaFo / bbpPairings style). "
            "<font face='Courier'>-c -dT</font> prints per-round headers and differences; "
            "<font face='Courier'>-c -d@</font> prints status code 0 or 1.",
            s["body"],
        )
    )

    # ----- tiebreakchecker -----
    story.append(PageBreak())
    story.append(P("tiebreakchecker.py", s["h1"]))
    story.append(code_block("python tiebreakchecker.py [options]", s))
    story.append(
        P(
            "Calculate and verify tiebreak values and ranking order. Calculate mode computes "
            "tiebreaks and ranks; check mode also compares ranks to the tournament file.",
            s["body"],
        )
    )
    story.append(P("Options (in addition to common options)", s["h2"]))
    story.append(
        simple_table(
            ["Option", "Description", "Default"],
            [
                [
                    "-n, --current-round &lt;n&gt;",
                    "Rounds included in the calculation.",
                    "-1 -> all rounds in file",
                ],
                [
                    "-t, --tiebreak &lt;list&gt;",
                    "Rank-order specifiers. If empty and the tournament has rankOrder, that list is used.",
                    "[]",
                ],
                [
                    "-p, --pre-determined",
                    "Treat as pre-determined (round-robin) pairing for unplayed-game rules.",
                    "off -> params.pre_determined",
                ],
                ["-s, --swiss", "Force Swiss unplayed-game rules.", "off"],
                ["-u, --unrated &lt;rating&gt;", "Rating for unrated players in rating TBs.", "unset"],
            ],
            s,
            col_widths=[4.5 * cm, 9.0 * cm, 3.5 * cm],
        )
    )

    story.append(P("Tiebreak list syntax", s["h2"]))
    story.append(
        P(
            "<font face='Courier'>TB :pp /Mn /opt</font> - TB name; optional "
            "<font face='Courier'>:MP</font>/<font face='Courier'>:GP</font> (and ESB "
            "<font face='Courier'>:MM|:MG|:GM|:GG</font>); modifiers "
            "<font face='Courier'>/C1 /C2 /M1 /M2 /L±n /Kx /P /F /U1400 /V1 /V2024 /V2 /V2026 /R /S</font>.",
            s["body"],
        )
    )

    story.append(P("Point systems and main tiebreaks", s["h3"]))
    story.append(
        simple_table(
            ["Name", "Modifiers", "Notes"],
            [
                ["PTS / MPTS / GPTS / MPVGP", ":MP :GP", "Points / match / game / primary flip"],
                ["DE", "/P", "Direct encounter"],
                ["WIN / WON / BPG / BWG", ":MP", "Wins / games won / black played / black won"],
                ["PS", ":MP :GP /C...", "Progressive score"],
                ["REP (GE deprecated alias)", "", "Rounds elected to play"],
                ["STD", "", "Standard score helper"],
                ["BH / FB / SB / AOB", ":MP :GP /C /M /P /F", "Buchholz family; FB == BH/F"],
                ["KS", ":MP :GP /L...", "Koya"],
                ["ARO / TPR / PTP / APRO / APPO", "/C /M /U...", "Rating performance family"],
                ["BC / TBR / BBE", "", "Board-count family (teams)"],
                ["ESB / EMMSB / EMGSB / EGMSB / EGGSB", ":MM... /C /P", "Extended Sonneborn-Berger"],
                ["EDE", "/P", "Extended direct encounter"],
                ["SSSC", "/Kx /P /F", "Score strength combination"],
                ["SNO / RANK / RTG / RND / VUR / ABH / AFB", "/P /R", "Helpers / order keys"],
                ["NUM / COP / COD / CSQ / ACC / FLT / RFP / TOP", "", "Pairing diagnostics helpers"],
            ],
            s,
            col_widths=[5.5 * cm, 4 * cm, 7.5 * cm],
        )
    )

    story.append(P("Version modifiers (/V...)", s["h3"]))
    story.append(
        simple_table(
            ["Modifier", "Internal ver", "Rules date"],
            [
                ["/V0 or /V2022", "0", "2022-01-01"],
                ["/V1 or /V2024", "1", "2024-08-01"],
                ["/V2, /V2026, or other", "2", "2026-03-01"],
                ["/V (bare)", "2", "latest (max key)"],
            ],
            s,
            col_widths=[5 * cm, 4 * cm, 8 * cm],
        )
    )

    story.append(P("tiebreakResult", s["h2"]))
    story.append(
        P(
            "The result key is <font face='Courier'>tiebreakResult</font>, a single object:",
            s["body"],
        )
    )
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["rules", "String", "Rule date (from ver)"],
                ["round", "Int", "Rounds used"],
                ["tiebreaks", "Array", "Parsed TB descriptors (order, name, pointtype, modifiers, precision)"],
                ["competitors", "Array", "Per-competitor results"],
                ["check", "Boolean", "Present when -c"],
            ],
            s,
            col_widths=[3.5 * cm, 2.5 * cm, 11 * cm],
        )
    )
    story.append(P("TB modifiers object (typical keys)", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["ver", "Int", "0/1/2 rule set"],
                ["rev", "Boolean", "Sort direction flip relative to TB default"],
                ["cutlow / cuthigh", "Int", "Cut / median cuts"],
                ["plim / nlim", "Number", "KS limits (percent / score)"],
                ["unrated", "Int", "Substitute rating"],
                ["predetermined", "Boolean", "Unplayed treated as played"],
                ["swiss", "Boolean", "Swiss unplayed rules"],
                ["foremode", "Boolean", "Fore Buchholz"],
                ["urd / exchange / vun", "Boolean", "Experimental / special flags"],
            ],
            s,
            col_widths=[4 * cm, 2.5 * cm, 10.5 * cm],
        )
    )
    story.append(P("competitor object", s["h3"]))
    story.append(
        simple_table(
            ["Key", "Type", "Description"],
            [
                ["cid", "Int", "Competitor id"],
                ["rank", "Int", "Computed rank"],
                ["tiebreakScore", "Array", "Values aligned with tiebreaks[]"],
                ["tiebreakDetails", "Array", "Present with -c; per-TB contribution detail"],
                ["boardPoints", "Object", "Team + -c only: board number -> points"],
            ],
            s,
            col_widths=[3.5 * cm, 2.5 * cm, 11 * cm],
        )
    )
    story.append(
        P(
            "There is no separate boardCount field in JSON; BC is a tiebreak whose score is "
            "derived from boardPoints.",
            s["caption"],
        )
    )

    story.append(P("Text output", s["h2"]))
    story.append(
        P(
            "<font face='Courier'>-d T</font> (or S/C/B) prints a header row "
            "StartNo/Rank (or Rank/StartNo with -r) plus each -t token, then one row per "
            "competitor. With -c an extra <font face='Courier'>Check: True/False</font> line "
            "is written. <font face='Courier'>-d@</font> prints the status code only.",
            s["body"],
        )
    )

    # ----- tournamentgenerator -----
    story.append(PageBreak())
    story.append(P("tournamentgenerator.py", s["h1"]))
    story.append(code_block("python tournamentgenerator.py [options]", s))
    story.append(
        P(
            "Supporting tool for testing and development. Generates synthetic tournaments with "
            "controlled statistics using the same pairing engines as pairingchecker, exported as TRF.",
            s["body"],
        )
    )
    story.append(
        simple_table(
            ["Option", "Description", "Default"],
            [
                [
                    "-g, --generate ...",
                    "1-3 ints: [count] or [start count] or [start count step]. "
                    "Two-arg form: range(start, start+count).",
                    "0 1000",
                ],
                ["-o, --output-file", "%d in the path -> zero-padded tournament number.", "required for files"],
                ["-p, --players", "Number of competitors.", "40"],
                ["-T, --members", "Players per team (playing).", "1"],
                ["-m, --method", "dutch or berger (and -suffixes as in pairingchecker).", "dutch"],
                ["-t, --top-color", "Accepted; generator currently alternates by file number.", "blank"],
                ["-R, --rating [top step sigma]", "Rating model; omitted -> heuristics by field size.", "[]"],
                [
                    "-S, --statistics [zpb hpb forfeited]",
                    "Rates of ZPB, HPB, forfeits. RR forces zpb=hpb=0.",
                    "0.01 0.05 0.02",
                ],
                ["-a, --acceleration", "Baku acceleration.", "off"],
                ["-K, --maxmeets", "Max meetings (clamped like pairing).", "0"],
                ["-n / -N", "Round count via common options.", "see common"],
            ],
            s,
            col_widths=[4.8 * cm, 8.7 * cm, 3.5 * cm],
        )
    )
    story.append(code_block(
        "python tournamentgenerator.py -g 500 -n 9 -p 300 -o c:\\files\\myfilename%d.trf",
        s,
    ))

    # ----- chessserver -----
    story.append(P("chessserver.py", s["h1"]))
    story.append(code_block("python chessserver.py", s))
    story.append(
        P(
            "Stdin/stdout JSON service for web deployment. Services: "
            "<font face='Courier'>convert</font>, "
            "<font face='Courier'>pairing</font>, "
            "<font face='Courier'>tiebreak</font>. "
            "Unknown service falls back to convert. No authentication; put a reverse proxy in front. "
            "Host paths from the client are ignored; only in-memory payloads are accepted "
            "(max request/payload 10 MiB).",
            s["body"],
        )
    )
    story.append(P("Request", s["h2"]))
    story.append(
        P(
            "The body is a JSON object with a <b>command</b> property holding the options:",
            s["body"],
        )
    )
    story.append(code_block(
        """{
  "command": {
    "service": "convert" | "pairing" | "tiebreak",
    "input_format": "TRF" | "TS" | "JSON",
    "input_filetype": "TRF" | "TS" | "JSON",
    "input_filename": "optional name for extension sniffing",
    "base64": "<base64 tournament file>" | ["..."],
    "jch": "<raw Json Chess text>",
    "data": "<base64>" | ["<base64 lines>"],
    "encoding": "ascii",
    "tournament_number": 1,
    "current_round": -1,
    "number_of_rounds": 0,
    "check": false,
    "tiebreak": ["PTS", "DE", "BH/C1"],
    "pre-determined": false,
    "swiss": false,
    "unrated": null,
    "pairing": true,
    "analysis": false,
    "method": "dutch",
    "top_color": "w",
    "maxmeets": 1,
    "unpaired": [],
    "rank": false,
    "game_score": {},
    "match_score": {},
    "experimental": [],
    "verbose": 0
  }
}""",
        s,
    ))
    story.append(
        P(
            "At least one of base64, jch, or data is required. If input_format is omitted, "
            "input_filetype is used, else getFileFormat(input_filename), else TRF. "
            "Server default encoding is ascii (so TRF over the server defaults to ascii, not latin1). "
            "Allowlisted option names use underscores except <font face='Courier'>pre-determined</font> "
            "(hyphen), matching the CLI long option spelling.",
            s["body"],
        )
    )
    story.append(P("Response", s["h2"]))
    story.append(
        P(
            "JSON envelope identical in shape to the corresponding CLI program output "
            "(convert -> event JSON; pairing -> pairingResult; tiebreak -> tiebreakResult). "
            "When base64 or jch was used, stdout may be prefixed with a "
            "<font face='Courier'>Content-Type: application/json</font> header.",
            s["body"],
        )
    )

    # ----- File extension helper -----
    story.append(P("helpers.getFileFormat", s["h2"]))
    story.append(
        simple_table(
            ["Extension", "Format id"],
            [
                [".jch, .json", "JSON"],
                [".trf, .trfx, .txt", "TRF"],
                [".trx", "TS"],
                ["other / missing", "JSON"],
            ],
            s,
            col_widths=[6 * cm, 6 * cm],
        )
    )

    story.append(Spacer(1, 12))
    story.append(
        P(
            "This document describes the behaviour of TieBreakServer 1.9.57. "
            "Where earlier drafts differed (for example format name JCH as a CLI token, "
            "pairingResult as an array, or chessserver top-level options without a command wrapper), "
            "the implementation is authoritative. "
            "The Ver. 1.9 alignment of this specification to the code was made by Paul Hampton.",
            s["body"],
        )
    )

    import tempfile
    import shutil

    fd, tmp_path = tempfile.mkstemp(suffix=".pdf", dir=str(OUT.parent))
    os.close(fd)
    tmp = Path(tmp_path)
    try:
        doc = SimpleDocTemplate(
            str(tmp),
            pagesize=A4,
            leftMargin=1.8 * cm,
            rightMargin=1.8 * cm,
            topMargin=1.6 * cm,
            bottomMargin=1.8 * cm,
            title="Gacrux software",
            author="Otto Milvang; Ver. 1.9 update by Paul Hampton",
        )
        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
        try:
            shutil.move(str(tmp), str(OUT))
            target = OUT
        except OSError:
            shutil.move(str(tmp), str(OUT_FALLBACK))
            target = OUT_FALLBACK
            print(f"NOTE: {OUT.name} is locked; wrote {target.name} instead. Close the PDF and re-run.")
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)

    print(f"Wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
