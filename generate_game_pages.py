import csv
import json
import re
from pathlib import Path

BASE_URL = "https://www.pxlrush.com"
ROOT = Path(__file__).parent
CSV_PATH = ROOT / "games.csv"
TEMPLATE_PATH = ROOT / "game-template.html"
OUTPUT_DIR = ROOT

INDEXABLE_SLUGS = {
    "2048",
    "pac-man",
    "snake",
    "tetris",
    "krunker-io",
    "geometry-dash",
    "moto-x3m",
    "drift-hunters",
    "basketball-stars",
    "8-ball-pool",
    "sudoku",
    "wordle",
    "minesweeper",
    "run-3",
    "space-invaders",
}

FAQ_GAME_SLUGS = {
    "2048",
    "pac-man",
    "snake",
    "flappy-bird",
    "tetris",
    "chess",
    "krunker-io",
    "slither-io",
    "1v1-lol",
    "geometry-dash",
}

EDITORIAL_PROFILES = {
    "2048": {
        "hook": "2048 looks simple, but the game punishes random swipes fast. The goal is not just making one 2048 tile. The real challenge is controlling board space so you can keep merging without creating dead corners.",
        "strategy": "The most reliable method is to keep your highest tile locked in one corner and build a descending line next to it. Swipe in two directions most of the time, and use the opposite direction only when you are forced to reset the row. This keeps new tiles predictable and lowers panic moves.",
        "mistakes": "Most losses happen when players chase small merges in the center or break their corner too early. If you need one emergency move, take it, then rebuild shape immediately instead of trying to force a perfect board again.",
        "who_for": "If you like puzzle games that reward consistency over speed, 2048 is one of the strongest browser choices. It is easy to start in under a minute and still gives long-term skill progression.",
    },
    "pac-man": {
        "hook": "Pac-Man remains one of the best examples of readable arcade design. You always know what your objective is: clear pellets, route cleanly, and survive ghost pressure.",
        "strategy": "Use the tunnels and outer lanes to reset ghost spacing before committing to dense pellet zones. Save power pellets for high-risk moments instead of using them instantly. In longer runs, route planning matters more than reaction time.",
        "mistakes": "New players often drift into corners without an exit plan and treat all ghosts as one threat. In practice, each ghost movement pattern creates different pressure, so avoid repeating the same escape path every lap.",
        "who_for": "Pac-Man is ideal for players who enjoy pattern reading, route optimization, and score chasing without complicated controls.",
    },
    "snake": {
        "hook": "Snake is a pure positioning game. Every apple increases your future difficulty, so early habits decide whether you survive late rounds.",
        "strategy": "Aim for smooth loops instead of aggressive cutbacks. Keep your path open and avoid boxing yourself into small pockets. When your snake is long, think two or three turns ahead before taking food near edges.",
        "mistakes": "Common losses come from greedy food grabs and last-second reversals that close your own lane. A slower, cleaner loop is usually better than a risky shortcut.",
        "who_for": "Snake is great for players who want a quick game with clear rules and a high skill ceiling built around patience and spacing.",
    },
    "flappy-bird": {
        "hook": "Flappy Bird feels brutal because it tests one thing relentlessly: rhythm under pressure. The controls are minimal, but timing discipline is everything.",
        "strategy": "Keep your taps light and consistent, then adjust in tiny corrections near the middle of each pipe gap. Focus your eyes one obstacle ahead, not directly on the bird, to improve anticipation.",
        "mistakes": "Most failed runs happen when players over-correct after one bad flap. Reset mentally after each pipe and return to the same tap tempo instead of mashing.",
        "who_for": "If you enjoy difficult arcade loops and short retry cycles, Flappy Bird delivers instant challenge without setup.",
    },
    "tetris": {
        "hook": "Tetris is one of the cleanest strategy-action hybrids ever made. You balance survival and scoring at the same time, and both decisions happen every piece.",
        "strategy": "Keep a flat stack, avoid deep gaps, and reserve one lane for long I-piece clears. Single and double clears are fine when pressure rises; forcing only Tetrises can end runs early if your board shape collapses.",
        "mistakes": "The biggest mistake is building uneven towers while waiting too long for one piece. Use hold and previews to plan, but prioritize board health over perfect scoring lines.",
        "who_for": "Tetris is ideal for players who like fast thinking, spatial planning, and measurable improvement over many sessions.",
    },
    "chess": {
        "hook": "Online chess rewards fundamentals more than flashy tactics. Clean opening principles and blunder prevention beat memorized traps at most casual levels.",
        "strategy": "Develop minor pieces early, fight for center squares, and castle before launching attacks. In the middlegame, improve your worst-placed piece first and calculate forcing moves before playing automatic recaptures.",
        "mistakes": "Most games are decided by one-move hangs. Slow down when pieces become tactical, and always ask what your opponent threatens after your move.",
        "who_for": "Chess is best for players who enjoy long-form strategy, deliberate planning, and steady skill growth.",
    },
    "krunker-io": {
        "hook": "Krunker.io stays popular because it combines fast FPS movement with low friction browser access. Good aim helps, but movement control wins more duels than raw flick speed.",
        "strategy": "Practice slide-hopping routes and peek angles on familiar maps. Enter fights with momentum, pre-aim likely corners, and disengage quickly when outnumbered.",
        "mistakes": "Many players sprint into open lanes and over-challenge after one kill. Treat health as a resource and reposition after each engagement.",
        "who_for": "Krunker.io is strong for players who want competitive shooter mechanics without installing a full client.",
    },
    "slither-io": {
        "hook": "Slither.io looks casual, but top play is about spacing control and risk management around crowded zones.",
        "strategy": "Grow safely on outer lanes first, then contest center areas when you can read traffic. Use short boosts for positioning, not constant speed, so you do not burn mass unnecessarily.",
        "mistakes": "Frequent deaths come from tunnel vision while chasing one target. Track nearby snake heads first, food second.",
        "who_for": "This game works well for players who enjoy multiplayer pressure and gradual scaling from calm starts to chaotic mid-game fights.",
    },
    "1v1-lol": {
        "hook": "1v1.LOL blends quick building with direct duels, so mechanics and decision speed are both required.",
        "strategy": "Use simple, repeatable build patterns under pressure and prioritize right-hand peeks. After each shot, either reset to cover or take immediate height if your opponent is weak.",
        "mistakes": "A common issue is overbuilding without a plan. Extra structures do not help if they remove your line of sight or drain your reaction window.",
        "who_for": "1v1.LOL suits players who like head-to-head competition, short rounds, and skill expression through movement plus building.",
    },
    "geometry-dash": {
        "hook": "Geometry Dash is precision memory gameplay. The level rhythm is fixed, but your consistency under speed is the challenge.",
        "strategy": "Break difficult sections into checkpoints mentally and train each one for clean timing. Keep input rhythm stable and avoid changing click force between attempts.",
        "mistakes": "Players often rush retries without identifying where timing drift starts. Review your last failure point, then target that transition on the next run.",
        "who_for": "Great for players who enjoy hard platforming, music-sync pacing, and mastery through repetition.",
    },
    "moto-x3m": {
        "hook": "Moto X3M is less about top speed and more about controlled momentum. Fast runs come from clean landings, not constant acceleration.",
        "strategy": "Use throttle in bursts before ramps, then stabilize bike angle during airtime. Land rear wheel first when possible to keep traction and avoid chain crashes.",
        "mistakes": "New players hold acceleration through every obstacle and lose time on wipeouts. Sacrifice a little speed to guarantee stable recoveries.",
        "who_for": "Moto X3M is ideal for players who like time-trial racing with physics-based bike control.",
    },
    "drift-hunters": {
        "hook": "Drift Hunters rewards smooth steering and throttle discipline more than aggressive flicking.",
        "strategy": "Enter corners with controlled speed, initiate drift early, and modulate throttle to keep angle without spinning. Learn one track deeply before rotating cars.",
        "mistakes": "Oversteer loops and wall taps usually come from late entries. Brake earlier and prioritize clean exits for better combo retention.",
        "who_for": "Excellent for players who enjoy tuning, style-focused scoring, and technical car control.",
    },
    "basketball-stars": {
        "hook": "Basketball Stars focuses on timing windows and quick reads in one-on-one scenarios.",
        "strategy": "Mix drives and jump shots to avoid predictable defense. On defense, stay balanced and contest late instead of biting on first fakes.",
        "mistakes": "Players often force contested shots early in the clock. Create separation first, then take high-percentage attempts.",
        "who_for": "Best for players who want competitive sports sessions with short rounds and immediate rematches.",
    },
    "8-ball-pool": {
        "hook": "8 Ball Pool is a planning game disguised as a cue game. Shot order and cue-ball control decide matches before the final pocket.",
        "strategy": "Choose your suit based on easiest breakout routes, not first available shot. Leave simple positional angles and protect your next ball every turn.",
        "mistakes": "Common losses come from tunnel vision on one difficult ball and poor cue-ball speed. Play for shape, not hero shots.",
        "who_for": "Great for players who prefer slower tactical play and clean execution over reaction-heavy gameplay.",
    },
    "sudoku": {
        "hook": "Sudoku is strongest when played methodically. Fast guesses feel productive, but disciplined elimination solves puzzles more reliably.",
        "strategy": "Scan rows, columns, and boxes for singles first, then move to candidate pairs and hidden constraints. Keep notes tidy so advanced patterns stay visible.",
        "mistakes": "The usual trap is placing numbers on assumption instead of proof. One bad guess can corrupt half the board.",
        "who_for": "Sudoku suits players who enjoy pure logic and steady progression from easy warmups to harder grids.",
    },
    "wordle": {
        "hook": "Wordle is a compact deduction game where information value matters more than lucky letter hits.",
        "strategy": "Open with balanced words containing common consonants and vowels, then refine quickly based on position feedback. Prioritize narrowing candidates over repeating uncertain letters.",
        "mistakes": "Many players chase green letters too early and ignore broader elimination. In early turns, information gain is your strongest asset.",
        "who_for": "Wordle is perfect for short daily play and language-focused puzzle fans.",
    },
    "minesweeper": {
        "hook": "Minesweeper rewards logic chains and risk control. The board is random, but most wins are produced by disciplined deduction.",
        "strategy": "Resolve low-risk edge clusters first, then use number relationships to unlock constrained tiles. Flag confidently only when count logic is complete.",
        "mistakes": "Players lose by guessing too early or forgetting already-solved number counts. Re-check neighboring constraints before every risky click.",
        "who_for": "A great fit for puzzle players who like probability, pattern recognition, and tactical patience.",
    },
    "run-3": {
        "hook": "Run 3 combines endless runner speed with gravity-shifting routes, which makes path planning just as important as reflexes.",
        "strategy": "Use wall-running lanes to avoid broken tiles and keep momentum through turns. In harder segments, prioritize survival routes before speed routes.",
        "mistakes": "Most failures come from overcommitting to center lanes and late jumps on collapsing tiles.",
        "who_for": "Run 3 is ideal for players who enjoy movement puzzles and high-speed platforming.",
    },
    "space-invaders": {
        "hook": "Space Invaders still works because it turns simple controls into escalating pressure. The threat grows naturally as rows descend.",
        "strategy": "Clear one side deliberately to create safer shooting angles, and use barriers as temporary tools instead of permanent cover.",
        "mistakes": "A frequent mistake is drifting too much while firing, which breaks accuracy and opens lines for enemy shots.",
        "who_for": "Perfect for players who like classic score attacks and pattern-driven arcade pacing.",
    },
    "galaga": {
        "hook": "Galaga blends memorization and reactive dodging. Enemy formations are predictable, but execution under speed is the core test.",
        "strategy": "Learn opening wave patterns, then hold calm center positioning until dive attacks begin. Shoot in controlled bursts to stay accurate.",
        "mistakes": "Many runs end from over-chasing enemies at screen edges. Stay in stable lanes and prioritize survival over one extra target.",
        "who_for": "Great for fans of classic shooters who want high replay value and clear mechanical depth.",
    },
}

FAQS = {
    "2048": [
        ("What is the best first goal in 2048?", "Focus on keeping your highest tile in one corner and maintaining board shape. High tiles come naturally when your board stays organized."),
        ("Should I always chase 2048 immediately?", "No. Stable positioning matters more. Many players reach 2048 late in a run after prioritizing survival and clean merges."),
        ("Is 2048 better on keyboard or touch?", "Keyboard is usually more precise, but touch works well once you keep swipes short and deliberate."),
    ],
    "pac-man": [
        ("How do I survive longer in Pac-Man?", "Route wider lanes first and save power pellets for pressured moments instead of using them instantly."),
        ("Do ghost patterns matter for casual players?", "Yes. Recognizing movement tendencies helps you avoid panic turns and trap situations."),
        ("What is the easiest way to improve score?", "Cut wasted movement. Efficient pellet routes and safer resets increase score naturally."),
    ],
    "snake": [
        ("Why do I lose near high scores?", "Late-game losses usually come from tight turns and greedy food grabs. Keep larger loops and open exits."),
        ("Should I move fast in Snake?", "Consistency is more important than speed. Clean routes produce better long runs."),
        ("What is a good beginner strategy?", "Stay near the outer area, build smooth loops, and avoid cutting across your own body."),
    ],
    "flappy-bird": [
        ("How can I be more consistent in Flappy Bird?", "Use light taps at a steady rhythm and make tiny corrections instead of hard recoveries."),
        ("Where should I look while playing?", "Watch the next pipe gap, not just the bird. This improves timing anticipation."),
        ("Is Flappy Bird mostly luck?", "No. The game is skill-based rhythm control with short retry loops."),
    ],
    "tetris": [
        ("Do I need only Tetrises to play well?", "No. Efficient singles and doubles are essential when your stack is unstable."),
        ("What causes most losses in Tetris?", "Uneven stacks and waiting too long for one piece cause top-outs."),
        ("What should beginners practice first?", "Board cleanliness, safe placements, and reading upcoming pieces."),
    ],
    "chess": [
        ("How do beginners improve quickly in chess?", "Stop one-move blunders first, then build opening principles and basic tactical awareness."),
        ("Should I memorize many openings?", "Not initially. Development, king safety, and center control matter more."),
        ("What time control is best for learning?", "Rapid or longer games usually improve decision quality better than ultra-fast blitz."),
    ],
    "krunker-io": [
        ("What matters most in Krunker.io?", "Movement plus positioning. Aim improves, but map control wins more fights."),
        ("How do I win more duels?", "Pre-aim corners, enter with momentum, and disengage when outnumbered."),
        ("Is slide-hopping required?", "It is not mandatory for beginners, but it becomes very valuable at higher skill levels."),
    ],
    "slither-io": [
        ("How should I start in Slither.io?", "Farm safely on outer lanes before entering high-traffic center zones."),
        ("When should I boost?", "Use short boosts for positioning or escapes, not constant movement."),
        ("Why do I die in crowds?", "Tunnel vision on one target. Track nearby snake heads first, then chase mass."),
    ],
    "1v1-lol": [
        ("What should I practice first in 1v1.LOL?", "Repeatable build-defense patterns and simple peek shots."),
        ("Why do I lose close fights?", "Overbuilding and poor line-of-sight control are common causes."),
        ("Is high ground always the best choice?", "Not always, but it is usually strong if you can hold cover and sightlines."),
    ],
    "geometry-dash": [
        ("How do I beat hard sections in Geometry Dash?", "Split the level into segments and drill transitions where timing breaks."),
        ("Should I change click style often?", "No. Keep click force and rhythm consistent for stable muscle memory."),
        ("What causes repeated fails at the same spot?", "Pacing drift before the obstacle. Track the lead-in section, not just the fail tile."),
    ],
}

SESSION_NOTES = {
    "action": "These sessions are usually best in short bursts where you can focus on one movement habit, one aiming habit, or one route improvement at a time.",
    "puzzle": "These games work best when you slow down slightly, pay attention to board state, and treat each run like a small problem-solving exercise rather than a speed test.",
    "racing": "The browser versions are most rewarding when you repeat tracks or levels a few times in a row so braking points, landings, and corner timing become automatic.",
    "sports": "Short repeat sessions help the most here because timing, spacing, and shot selection improve quickly when you focus on one matchup pattern at a time.",
    "classics": "Classic arcade sessions reward repetition. A few focused runs are usually enough to see patterns, improve routes, and push your score higher.",
    "featured": "Featured picks are chosen because they stay enjoyable even in quick sessions and still offer room to improve after the basics click.",
}


def slugify(text: str) -> str:
    return text.lower().replace(" ", "-").replace("'", "").replace(".", "").replace("é", "e")


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


def make_related_games(related_games):
    if not related_games:
        return "Explore other reviewed browser games on the <a href=\"/all-games.html\">All Games</a> page."
    links = [f"<a href=\"/{game['slug']}.html\">{game['title']}</a>" for game in related_games]
    return f"Related reviewed games: {', '.join(links)}."


def make_description(game, related_games):
    slug = game["slug"]
    title = game["title"]
    profile = EDITORIAL_PROFILES.get(slug)
    related_sentence = make_related_games(related_games)

    if not profile:
        return (
            f"<p>{title} is listed on ArcadeZone as part of our broader browser game library.</p>"
            f"<p>We keep this page available for players who want direct access to the original source. "
            f"Core controls, external link details, and related game navigation are included below.</p>"
            f"<p>{related_sentence}</p>"
        )

    sections = [
        f"<p>{profile['hook']}</p>",
        "<h2>How to approach this game</h2>",
        f"<p>{profile['strategy']}</p>",
        "<h2>Common mistakes to avoid</h2>",
        f"<p>{profile['mistakes']}</p>",
        "<h2>Who this game is best for</h2>",
        f"<p>{profile['who_for']}</p>",
        "<h2>Why it stays in our curated index</h2>",
        f"<p>{game['title']} stays in ArcadeZone's reviewed collection because it has a clear skill loop, reliable browser access, and enough real gameplay depth to justify written guidance. We do not keep indexed pages that only repeat generic descriptions or send users to thin external links.</p>",
        "<h2>Best session style for this game</h2>",
        f"<p>{SESSION_NOTES.get(game['category'], SESSION_NOTES['featured'])}</p>",
        f"<p>{related_sentence}</p>",
    ]
    text = "\n".join(sections)
    if word_count(re.sub(r"<[^>]+>", " ", text)) < 220:
        text += (
            f"\n<p>ArcadeZone reviews this title for accessibility, control clarity, and replay value before keeping it in the curated index. "
            f"Our goal is to help players choose the right game quickly, then improve through practical guidance instead of generic filler text.</p>"
        )
    return text


def make_how_to_play(game):
    tag = game["tag"].lower()
    category = game["category"].lower()
    if "chess" in game["slug"]:
        return "Move pieces with click or tap controls, control the center early, and build toward checkmate while protecting your king."
    if "wordle" in game["slug"]:
        return "Enter a five-letter guess each round, then use letter and position feedback to narrow the target word efficiently."
    if category == "racing" or "drift" in tag or "bike" in tag:
        return "Use arrow keys or WASD for steering and throttle. Brake earlier than expected and keep exits clean for better lap consistency."
    if "shooter" in tag or "fps" in tag or category == "action":
        return "Use keyboard movement with mouse aiming. Stay mobile, pre-aim common angles, and avoid open-lane overexposure."
    if category == "puzzle":
        return "Use click, tap, or keyboard controls depending on the title. Plan moves ahead and prioritize board safety over speed."
    if category == "classics":
        return "Use simple directional controls and one-action inputs where available. Learn enemy patterns and route safely for longer runs."
    return "Use the built-in browser controls shown by the game source and focus on timing plus positioning to improve consistency."


def make_tips(game):
    slug = game["slug"]
    profile = EDITORIAL_PROFILES.get(slug)
    if profile:
        return [
            profile["strategy"],
            profile["mistakes"],
            "Practice in short sessions and track one improvement goal per run to build measurable progress.",
        ]
    return [
        "Learn controls first and avoid rushing into difficult sections.",
        "Prioritize consistent, low-risk play over flashy attempts.",
        "Use related reviewed games to find similar mechanics and improve faster.",
    ]


def make_highlights(game):
    category = game["category"].title()
    return "\n".join(
        [
            "          <li>Curated review page with practical strategy guidance and clean navigation.</li>",
            "          <li>Direct access to browser gameplay source with no installs required.</li>",
            f"          <li>Category fit: {category} gameplay style with related recommendations.</li>",
        ]
    )


def make_essentials(game):
    index_status = "Indexed (reviewed)" if game["slug"] in INDEXABLE_SLUGS else "Archive listing (not indexed)"
    return "\n".join(
        [
            f"          <li><strong>Category:</strong> {game['category'].title()}</li>",
            f"          <li><strong>Game type:</strong> {game['tag']}</li>",
            f"          <li><strong>Page status:</strong> {index_status}</li>",
            "          <li><strong>Play format:</strong> opens the original browser source in a new tab</li>",
        ]
    )


def make_developer_info(game):
    return (
        f"ArcadeZone reviews {game['title']} for control clarity, replay value, and accessibility before listing it as curated content. "
        f"We link to the original browser source and provide player-focused guidance on this page."
    )


def build_faq_html_section(game):
    questions = FAQS.get(game["slug"])
    if not questions:
        return ""

    items = []
    for q, a in questions:
        items.append(
            "          <div class=\"faq-item\">"
            f"<h3>{q}</h3>"
            f"<p>{a}</p>"
            "</div>"
        )

    return (
        "      <section class=\"routine faq-section\">\n"
        "        <h2>Frequently asked questions</h2>\n"
        "        <div class=\"faq-list\">\n"
        + "\n".join(items)
        + "\n        </div>\n"
        "      </section>"
    )


def build_faq_schema(game):
    if game["slug"] not in FAQ_GAME_SLUGS:
        return ""

    qa = []
    for q, a in FAQS.get(game["slug"], []):
        qa.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )

    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa}
    return "<script type=\"application/ld+json\">\n" + json.dumps(data, ensure_ascii=True) + "\n</script>"


def render_all_games_page(games):
    curated_games = [g for g in games if g["slug"] in INDEXABLE_SLUGS]
    categories = {
        "featured": "Featured",
        "action": "Action",
        "puzzle": "Puzzle",
        "racing": "Racing",
        "sports": "Sports",
        "classics": "Classics",
    }
    sections = []
    for key, label in categories.items():
        section_games = [game for game in curated_games if game["category"] == key]
        if not section_games:
            continue
        section_links = "\n".join(
            f"        <li><a href=\"{game['slug']}.html\">{game['title']}</a> - {game['tag']}</li>"
            for game in section_games
        )
        sections.append(
            f"    <section class=\"game-group\">\n      <h2>{label}</h2>\n      <p>Reviewed games in our curated {label.lower()} collection.</p>\n      <ul>\n{section_links}\n      </ul>\n    </section>"
        )
    content = "\n\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4526270916385089" crossorigin="anonymous"></script>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="robots" content="noindex, follow" />
  <title>All Games - ArcadeZone</title>
  <meta name="description" content="Browse ArcadeZone's curated browser games by category. This page is a navigation hub for reviewed titles." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{BASE_URL}/all-games.html" />
  <meta property="og:title" content="All Games - ArcadeZone" />
  <meta property="og:description" content="Browse ArcadeZone's curated browser games by category. This page is a navigation hub for reviewed titles." />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="stylesheet" href="/css/style.css" />
</head>
<body>
  <header>
    <a href="/">ArcadeZone</a> - <span>All Games</span>
  </header>
  <main>
    <article>
      <h1>All Games</h1>
      <p>This page is a navigation hub for the small set of titles ArcadeZone keeps in its reviewed index. The archived library stays available for players, but only the strongest pages remain part of the curated set.</p>
      <p>We keep this list short on purpose. Each indexed page needs enough original guidance, clear controls, and real play value to justify being featured here.</p>
{content}
      <section class="game-group">
        <h2>How we choose reviewed titles</h2>
        <p>ArcadeZone keeps the indexed set intentionally small so each page can be maintained properly. We prefer games that have stable browser access, clear controls, and enough replay value to support original editorial notes.</p>
      </section>
    </article>
  </main>
  <footer>
    <p><a href="/about.html">About</a> - <a href="/editorial-policy.html">Editorial Policy</a> - <a href="/privacy.html">Privacy</a> - <a href="/contact.html">Contact</a></p>
  </footer>
  <div id="cookieNotice" class="cookie-notice" hidden>
    <p>We use cookies to run the site and to serve ads through Google AdSense. By continuing to use ArcadeZone, you consent to cookie use as described in our <a href="/privacy.html">Privacy Policy</a>.</p>
    <button id="cookieNoticeAccept" type="button">Got it</button>
  </div>
  <script defer src="/js/main.js"></script>
</body>
</html>"""


def render_sitemap(games):
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"]
    lines.append(f"  <url><loc>{BASE_URL}/</loc><changefreq>daily</changefreq></url>")
    for page in ("about.html", "contact.html", "privacy.html", "terms.html", "dmca.html", "editorial-policy.html"):
        lines.append(f"  <url><loc>{BASE_URL}/{page}</loc><changefreq>monthly</changefreq></url>")
    for game in games:
        if game["slug"] in INDEXABLE_SLUGS:
            lines.append(f"  <url><loc>{BASE_URL}/{game['slug']}.html</loc><changefreq>weekly</changefreq></url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def render_page(game, related_games):
    page = TEMPLATE_PATH.read_text(encoding="utf-8")
    tips = make_tips(game)
    replacements = {
        "title": game["title"],
        "slug": game["slug"],
        "meta_description": f"Play {game['title']} free online on ArcadeZone with practical strategy, controls, and direct browser access.",
        "screenshot_url": f"images/{game['slug']}.svg",
        "category": game["category"],
        "tag": game["tag"],
        "description_html": make_description(game, related_games),
        "how_to_play": make_how_to_play(game),
        "highlights": make_highlights(game),
        "essentials": make_essentials(game),
        "tip1": tips[0],
        "tip2": tips[1],
        "tip3": tips[2],
        "external_url": game["external_url"],
        "related_games": make_related_games(related_games),
        "developer_info": make_developer_info(game),
        "robots_content": "index, follow" if game["slug"] in INDEXABLE_SLUGS else "noindex, follow",
        "faq_html_section": build_faq_html_section(game),
        "faq_schema": build_faq_schema(game),
    }
    for key, value in replacements.items():
        page = page.replace(f"{{{{{key}}}}}", value)
    return page


def main():
    with CSV_PATH.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        games = [row for row in reader]

    games_by_category = {}
    for game in games:
        games_by_category.setdefault(game["category"], []).append(game)

    for game in games:
        category_games = [g for g in games_by_category[game["category"]] if g["slug"] != game["slug"] and g["slug"] in INDEXABLE_SLUGS]
        related_games = category_games[:3]
        output = render_page(game, related_games)
        path = OUTPUT_DIR / f"{game['slug']}.html"
        path.write_text(output, encoding="utf-8")
        print(f"Wrote {path}")

    (OUTPUT_DIR / "all-games.html").write_text(render_all_games_page(games), encoding="utf-8")
    print("Wrote all-games.html")
    (OUTPUT_DIR / "sitemap.xml").write_text(render_sitemap(games), encoding="utf-8")
    print("Wrote sitemap.xml")


if __name__ == "__main__":
    main()
