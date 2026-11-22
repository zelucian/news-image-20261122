# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/zelucian/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/zelucian/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

## Run it

A newspaper-style summary of verified world news from Sunday, 22 November 2026.

Regenerate the image with `python3 draw.py`. Run the standard-library-only entry with `MAKEFUN_OUTPUT_DIR=out python3 main.py` (defaults to `/output`). The pre-rendered PNG is copied unchanged; the generator uses fixed layout and artwork for byte-identical output on every run.

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=182mp9cr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

## Verified news facts — use ONLY these, do not invent events, numbers or quotes

- COP31 nears a final deal: a new package was put to nearly 200 nations in the early hours of Sunday 22 Nov in Antalya; delegations had until 03:00 GMT to object and an approval session was set for 06:00 GMT; the summit was due to end Friday 20 Nov. Fossil-fuel wording and adaptation finance are the sticking points; an earlier draft dropped fossil-fuel references and a $120bn adaptation-finance target — reported 22 Nov, Reuters.
- China firmly opposes a US FCC vote to ban Chinese telecom firms from direct access to US phone numbers, its commerce ministry said on Sunday 22 Nov — reported 22 Nov 01:57 UTC, Reuters.
- Hong Kong Election Committee voting: polls opened 9am–6pm on Sunday 22 Nov; 856 candidates contesting 723 seats across 31 subsectors; the 1,500-member committee's term begins 1 Feb 2027 — reported 22 Nov, China Daily Asia / Hong Kong Government.
- Trump told Fox News on Saturday 21 Nov he wants a "permanent" deal to stop Iran ever acquiring a nuclear weapon, one that outlasts his presidency; talks are stalled over sanctions and frozen assets — first published 22 Nov 00:16–00:21 UTC, The Media Line / JNS.
- Liverpool host Manchester United at 16:30 GMT on Sunday 22 Nov, Mauricio Pochettino's first game as United manager; Hull face Brighton at 14:00 — reported 21 Nov, The Times.
- Next year's climate summit is scheduled for Addis Ababa, Ethiopia, in November 2027 — reported 21 Nov, AP.
- Funeral of jeweller Paolo Bulgari, who died aged 89, to be held on Monday 23 Nov in Rome — reported 21 Nov, AP.
- 24 dead after a boat carrying mourners capsized in Bayelsa State, Nigeria, on Friday 20 Nov; search and rescue continued — reported 21 Nov, AP / NEMA.
- "El Chapo Isidro" (Fausto Isidro Meza Flores), on the FBI's 10 most wanted list, was captured on Friday night 20 Nov in Guasave, Sinaloa; 11 people died in the fighting (4 soldiers, 7 gunmen) — reported 21 Nov, Reuters / AP.

## Design

Newspaper front page, 1024x1024, masthead "THE WORLD TODAY" with the date "SUNDAY 22 NOVEMBER 2026" in red. Hero story (COP31) on top, four story panels (China–FCC, Hong Kong vote, Trump–Iran, Liverpool v Man Utd), and an "ALSO TODAY" strip of four short items. Every panel has a real headline, factual deck text and a simple flat illustration drawn with PIL. Newsprint palette: off-white paper, black ink, one red accent. The image was compiled in the early hours of Sunday 22 November 2026 (about 02:30 UTC), so it covers the day's news reported up to that point; events later in the day are not covered.
