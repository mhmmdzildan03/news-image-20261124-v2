# news-image-20261124-v2

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/mhmmdzildan03/news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/mhmmdzildan03/news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# 24 November 2026 in one image — the broadsheet

A single 1024x1024 broadsheet front page that sums up the world news of
Tuesday 24 November 2026, built for make.fun's "Sum up 24 November's
world news in one image" bounty.

**Design:** a disciplined broadsheet — the date as the biggest type on
the page, a region-count ticker, a day-in-numbers strip, three
illustrated lead stories, a grid of five more plus a "Where it
happened" dot map pinned to stories 1–9, and an "Also on Tuesday"
list of nineteen one-line stories: 27 stories in all, every one dated
Tuesday 24 November 2026 and verified against that day's reporting
(Reuters, AP, the BBC, the Kyiv Independent and others). Every story
carries a status chip (CONFIRMED / OFFICIAL / REPORTED / CLAIM) and
its source by name, and a date-check box names the Monday stories
deliberately left out. Organized density, kept legible — headlines
stay readable at thumbnail size. (Earlier designs are kept in the
repo as generate.py, broadsheet.py and broadsheet2.py.)

- **Hero:** COP31 in Antalya ended with no deal and the world reacted
  in anger on day two — Guterres "deeply disappointed", the EU calling
  the summit hijacked by oil states, island nations refusing to sign.
- **Factory fire:** the Cikande candy-factory fire in Banten — toll
  confirmed at 24 dead, about 30 workers still missing.
- **Oil slides:** Brent crude fell to $89.37, its lowest since August,
  as oil kept flowing past the Hormuz attacks.
- **Kyiv struck:** fresh drone and missile strikes hit Ukraine's Kyiv
  region.
- **Chess final:** the World Chess Championship title match opened in
  Geneva — champion D Gukesh of India vs Javokhir Sindarov of
  Uzbekistan.
- **Also today:** Modi + Shah flagged off the Ayodhya–Janakpur
  Saryu-Kamala Express; Alcaraz won his first ATP Finals title in
  Turin; Pant hit 128 in the drawn Wellington Test.

## Run it

```sh
python3 main.py            # writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR)
```

`main.py` is standard-library only and copies the bundled `entry.png`
byte for byte. The page itself is rendered by `broadsheet3.py`
(Pillow), kept here so the whole build is inspectable.
