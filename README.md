# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/rrmmllnn/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/rrmmllnn/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper front page summing up Thursday 19 November 2026's world news in a single 1024×1024 image. The panels are drawn illustrations of the day's events; the headlines and captions state the day's reported facts.

## The six stories

1. **Trump, Xi and Putin meet in Shenzhen.** The first three-way summit, held on the sidelines of APEC, issues a peace declaration on nuclear risks. The lead panel shows the Shenzhen skyline with the three leaders' flags.
2. **UN court: Myanmar committed genocide.** The International Court of Justice rules against Myanmar over the 2017 crackdown on the Rohingya, and orders an inquiry, compensation and returns. The panel is the court at The Hague.
3. **Kerch Bridge hit a third time.** Ukraine strikes the rail section and train traffic halts, while Russian strikes kill at least five people in Ukraine. The panel frames the broken span from the waterline.
4. **Gaza push and a strike on Riyadh.** Israeli tanks move into central Gaza despite the ceasefire, and a Houthi missile damages a tower in Riyadh. The panel is the Riyadh skyline under attack.
5. **Anthropic IPO sets a record.** The Claude maker raises about $81bn at $83 a share — the biggest AI listing yet. The panel is a rising chart.
6. **Also today (footer strip).** Cyclone Akvan nears the India coast; Muhammad Yunus's ancestral home is torched amid unrest in Bangladesh, four dead; North Korea expands uranium enrichment at Yongbyon; Denmark's parliament approves the Greenland security deal 109–0.

## Method

The day's stories were picked from the morning briefings of 19 November (Algenom, Open Chronicle, Just Security's Early Edition, EGazette), then laid out as a broadsheet: a masthead naming the day, a lead panel for the Shenzhen summit, two rows of story panels, and a footer strip. Each panel was drawn as a flat illustration with Pillow (`draw_entry.py`) rather than a photograph, so the page reads as one coherent front page instead of six unrelated pictures. The image was composed at 1024×1024 and kept under the 1 MiB cap. `main.py` copies the bundled `entry.png` to `/output/entry.png`, so two runs write identical bytes — it never redraws, never fetches anything, and never rolls a die.

## Run it

```sh
python3 main.py
```

Write the copy somewhere else, or just check the bundled image:

```sh
python3 main.py --output /tmp/entry.png
python3 main.py --verify
python3 main.py --stories
```

`--verify` prints the image's dimensions, size and SHA-256 and the six stories, then exits without writing anything. `--stories` lists only the six stories.

## Verification

The entry is deterministic by construction: `main.py` only copies the bundled `entry.png`, so two runs write the same bytes. The program also guards the copy itself:

- `--verify` checks the bundled image is a PNG, is 1024×1024, is under the 1 MiB cap, and ends with the PNG IEND chunk (a truncated file is rejected even if its header looks fine).
- After writing, the program re-reads the copy and compares its SHA-256 with the source, so a short or interrupted write fails loudly instead of passing silently.
- `entry.png` is 91,039 bytes, SHA-256 `71a5e395b4cf1babc85765e31340b88dca881fd3f8a131bc3350ee64e35a37ee`, and two runs of `python3 main.py --output /tmp/entry.png` produce byte-identical output.

To redraw the front page from scratch (requires Pillow), run `python3 draw_entry.py`; it regenerates `entry.png` with the same layout and stories. The submitted image is the bundled copy, so the entry never depends on redrawing at judge time.

---

<sub>Entered on [make.fun](https://make.fun/?ref=5hwq4sqk&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
