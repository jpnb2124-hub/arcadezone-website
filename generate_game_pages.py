import csv
import re
from pathlib import Path

BASE_URL = "https://pxlrush.com"
ROOT = Path(__file__).parent
CSV_PATH = ROOT / "games.csv"
TEMPLATE_PATH = ROOT / "game-template.html"
OUTPUT_DIR = ROOT

CATEGORY_SENTENCES = {
    "featured": "This featured pick highlights a top browser game with strong replay value and easy access.",
    "action": "Action games on ArcadeZone are designed for fast reflexes, clear goals, and browser-friendly controls.",
    "puzzle": "Puzzle games are chosen for their thoughtful challenge, relaxing gameplay, and smart problem-solving.",
    "racing": "Racing games deliver quick circuits, responsive steering, and easy-to-learn mechanics for instant fun.",
    "sports": "Sports games bring favorite athletics into the browser with intuitive controls and competitive action.",
    "classics": "Classic arcade games are included for nostalgic play and simple, addictive gameplay that works everywhere.",
}

TIP_TEMPLATES = {
    "featured": [
        "Take your time as you learn the pace and find the right rhythm for each level.",
        "Use the game’s strengths to your advantage — every free browser title has its own pattern.",
        "Build confidence by practicing the same move sequence until it becomes second nature."
    ],
    "action": [
        "Focus on movement first, then add aiming once the controls feel comfortable.",
        "Small adjustments are often better than fast, risky maneuvers in browser action games.",
        "Watch the game environment and use cover, speed, or space to manage pressure."
    ],
    "puzzle": [
        "Slow down and look for the best move rather than the first move that seems possible.",
        "Many puzzle games reward planning ahead more than fast clicking.",
        "If a level feels difficult, step back and re-evaluate the objective before replaying."
    ],
    "racing": [
        "Smooth steering and controlled acceleration beat aggressive driving in browser races.",
        "Learn the curves and braking points to keep each track clean and fast.",
        "Use the camera, if available, to see the next turn and choose the safest racing line."
    ],
    "sports": [
        "Master the timing for shots, passes, or swings to stay in control of the play.",
        "Keep an eye on the entire field so you can react to opponent movement quickly.",
        "Use the game’s practice mode or warm-up to get a feel for the controls before competing."
    ],
    "classics": [
        "Classic games often reward consistency and timing more than quick reactions.",
        "Focus on the core rule set first — then begin trying higher scores or faster completion.",
        "Remember that many classic browser games are all about pattern recognition."
    ],
}

CONTROL_TEMPLATES = {
    "Action": "Use keyboard and mouse combinations for movement, aiming, and special actions.",
    "Puzzle": "Click or tap to move pieces, and use keyboard arrows when the game supports them.",
    "Racing": "Use arrow keys or WASD for driving controls and respond to each turn carefully.",
    "Sports": "Most sports games use mouse control or simple key presses to manage moves and shots.",
    "Classic": "Classic games usually use arrow keys or a single action button for simple play.",
    "Strategy": "Use precise clicks and slow, thoughtful decisions to stay in control of the board.",
    "Shooter": "Use the mouse to aim and fire, and keyboard keys to move around the map.",
    "Arcade": "Enjoy quick, reactive controls that keep you focused on score and timing.",
    "Multiplayer": "Stay aware of other players while controlling your character with keyboard and mouse input.",
    "Battle Royale": "Rely on movement, cover, and a careful approach while you compete against many opponents.",
    "Platformer": "Jump, move, and time your actions precisely to cross each obstacle cleanly.",
    "Bike": "Use throttle and steering controls to manage speed and stay on the track.",
    "Drift": "Focus on timing and smooth turns to keep your vehicle drifting through each bend.",
    "Pool": "Use mouse drag and release or arrow controls to aim and hit the cue ball with precise force.",
    "Baseball": "Aim carefully and time each swing to hit the ball toward the open field.",
    "Bowling": "Line up your shot and roll with steady control to keep the ball in the strike lane.",
    "Ping Pong": "Use quick reflexes and short movements to return each shot and keep the rally going.",
    "Word": "Type letters carefully and focus on clues to solve each word challenge quickly.",
    "Endless": "Keep moving without pausing and adapt to new obstacles as the game speeds up.",
    "Match-3": "Swap tiles or pieces to create matches and clear the board efficiently.",
    "Logic": "Think through each move, then act with patience to solve the puzzle steadily.",
}

HISTORY_TEMPLATES = {
    "2048": "First released as a browser puzzle challenge, 2048 became popular for its elegant number-merging mechanic and easy-to-learn rules.",
    "Pac-Man": "Pac-Man is one of the oldest arcade classics, with a simple chase-and-eat objective that defined a generation of games.",
    "Snake": "Snake is a timeless arcade favorite where the goal is to grow as long as possible without running into yourself.",
}


def slugify(title: str) -> str:
    return title.lower().replace(' ', '-').replace("'", '').replace('.', '').replace('é', 'e')


def make_description(game, related_games):
    title = game['title']
    category = game['category']
    tag = game['tag']
    intro = (
        f"{title} is a browser-friendly {tag.lower()} game on ArcadeZone that plays instantly in your web browser. "
        f"This page explains the core rules, the best way to approach each session, and how to enjoy {title} without downloads or extra installs."
    )
    history = HISTORY_TEMPLATES.get(title, f"This browser version of {title} fits the category of {category} games that are built for fast playing and repeat sessions.")
    history += " " + CATEGORY_SENTENCES.get(category, "This game offers a browser-ready play experience.")
    controls = (
        f"Controls are simple enough for quick games and satisfying enough for longer play. "
        f"{CONTROL_TEMPLATES.get(tag, CONTROL_TEMPLATES.get(category.capitalize(), 'Use simple keyboard, mouse, or touch actions to play.'))} "
        f"You can play {title} on desktop or mobile, depending on the browser and the page version."
    )
    strategy = (
        f"To improve in {title}, focus on the most important idea for the genre: {tag.lower()} games often reward good timing, pattern recognition, and steady progress. "
        f"This page also includes practical tips that help you find the right pace and avoid common mistakes while playing."
    )
    related_note = ""
    if related_games:
        links = []
        for related in related_games[:3]:
            links.append(f"<a href=\"/{related['slug']}.html\">{related['title']}</a>")
        related_sentence = ', '.join(links[:2])
        if len(links) > 2:
            related_sentence += f", and {links[2]}"
        related_note = (
            f"If you enjoy {tag.lower()} games, try {related_sentence} next. "
            f"All of these are listed on the <a href=\"/all-games.html\">ArcadeZone All Games</a> page for quick access."
        )
    closing = (
        f"ArcadeZone keeps this {title} page clean and easy to use, with a strong focus on playability and helpful guidance. "
        f"Bookmark this page if you want faster access to {title} and other browser classics from the ArcadeZone collection."
    )
    paragraphs = [intro, history, controls, strategy + ' ' + related_note, closing]
    text = "\n\n".join(paragraphs)
    return ensure_word_count(text, title)


def ensure_word_count(text, title, min_words=320):
    words = re.findall(r"\w+", text)
    if len(words) >= min_words:
        return text

    fillers = [
        f"{title} is featured here because it offers a polished browser experience with fast loading and easy access from any modern device.",
        f"This page also covers what makes {title} work well online and how to get the most out of every session.",
        f"When you want a quick game break, {title} delivers simple play mechanics and satisfying goals without distractions.",
        f"Each section on this page is designed to help you understand the controls, learn good strategy, and avoid common mistakes.",
        f"ArcadeZone keeps the page format clean so the gameplay information is easy to scan and the external play link is right where you need it.",
        f"The content on this page is written to serve players who want clear instructions, better scoring tips, and better browser game choices.",
    ]

    filler_index = 0
    while len(words) < min_words:
        text += "\n\n" + fillers[filler_index % len(fillers)]
        filler_index += 1
        words = re.findall(r"\w+", text)
    return text


def make_how_to_play(game):
    title = game['title']
    tag = game['tag']
    category = game['category']
    if 'chess' in title.lower():
        return "Move the pieces with the mouse or tap controls, capture the opponent, and aim for checkmate while thinking one step ahead."
    if 'word' in title.lower() or 'wordle' in title.lower():
        return "Type letters or tap the keyboard to guess words. Use clues from previous attempts to solve the daily puzzle."
    if 'pool' in title.lower() or 'billiards' in title.lower():
        return "Aim carefully, then click or tap to hit the cue ball and sink the target balls with steady control."
    if 'racing' in category or 'bike' in tag.lower() or 'drift' in tag.lower():
        return "Use the arrow keys or WASD for steering, and manage speed to stay on the track through each turn."
    if 'puzzle' in category or 'match' in tag.lower() or 'logic' in tag.lower():
        return "Use click or touch controls to move pieces, solve levels, and build the right pattern before time runs out."
    if 'action' in category or 'shoot' in tag.lower() or 'battle' in tag.lower():
        return "Use your mouse to aim and keyboard keys for movement. Stay aware of enemies and stay on the move."
    if 'classic' in category or 'arcade' in tag.lower():
        return "This classic game uses simple controls and quick reflexes. Use arrow keys or one-button input to play."
    return CONTROL_TEMPLATES.get(tag, CONTROL_TEMPLATES.get(category.capitalize(), "Use your mouse, keyboard, or touchscreen to play and enjoy the game in your browser."))


def make_tips(game):
    category = game['category']
    tips = TIP_TEMPLATES.get(category, TIP_TEMPLATES['featured'])
    return tips[:3]


def make_highlights(game):
    title = game['title']
    tag = game['tag']
    category = game['category']
    highlights = [
        f"Instant browser access with no downloads or installations required.",
        f"Designed for {tag.lower()} players who want a quick, reliable game experience.",
        f"A clean, mobile-ready page helps you learn the controls and start playing immediately."
    ]
    if category == 'classics':
        highlights[1] = f"Enjoy a nostalgic arcade experience with a classic {title} play style."
    if category == 'puzzle':
        highlights[1] = f"Practice your logic and pattern skills with a calm, focused puzzle experience."
    if category == 'racing':
        highlights[1] = f"Get into fast races and tight tracks with responsive browser controls."
    if category == 'sports':
        highlights[1] = f"Play competitive sports challenges that fit well in quick browser sessions."
    return "\n".join(f"          <li>{item}</li>" for item in highlights)


def make_essentials(game):
    title = game['title']
    category = game['category']
    tag = game['tag']
    best_for = {
        'featured': 'players looking for top browser game picks',
        'action': 'fast-paced action and quick reflex fun',
        'puzzle': 'brain training and thoughtful challenges',
        'racing': 'speed, timing, and track mastery',
        'sports': 'competitive sports mini-games',
        'classics': 'nostalgic arcade gameplay'
    }.get(category, 'browser game sessions')
    controls = {
        'Strategy': 'mouse clicks and keyboard movement for thoughtful play',
        'Puzzle': 'click and tap controls, with keyboard support where available',
        'Racing': 'arrow keys or WASD for steering and speed control',
        'Sports': 'mouse aiming and quick key presses for shots and movement',
        'Shooter': 'mouse aiming plus keyboard movement for fast action',
        'Arcade': 'simple, responsive controls for classic gameplay',
        'Multiplayer': 'fast reactions, movement, and careful spacing',
        'Battle Royale': 'strategic movement and defense while competing with others',
        'Platformer': 'timed jumps and smooth navigation',
        'Bike': 'steering and speed control on dynamic tracks',
        'Match-3': 'swipe or click to match tiles and clear the board',
        'Logic': 'planning moves before clicking or tapping'
    }.get(tag, 'use your keyboard, mouse, or touchscreen to play')
    return "\n".join([
        f"          <li><strong>Category:</strong> {category.title()}</li>",
        f"          <li><strong>Game type:</strong> {tag}</li>",
        f"          <li><strong>Best for:</strong> {best_for}</li>",
        f"          <li><strong>Controls:</strong> {controls}</li>"
    ])


def make_developer_info(game):
    title = game['title']
    return (
        f"ArcadeZone provides this page as a guide to {title}. Wherever possible, we link directly to the game’s browser-ready version and credit the original creators. "
        f"If you want more browser game recommendations, visit the <a href=\"/all-games.html\">All Games</a> page."
    )


def make_related_games(related_games):
    if not related_games:
        return "Explore other browser games on the <a href=\"/all-games.html\">All Games</a> page."
    links = [f"<a href=\"/{game['slug']}.html\">{game['title']}</a>" for game in related_games]
    return f"Related browser games you may enjoy: {', '.join(links)}."


def render_all_games_page(games):
    categories = {
        'featured': 'Featured',
        'action': 'Action',
        'puzzle': 'Puzzle',
        'racing': 'Racing',
        'sports': 'Sports',
        'classics': 'Classics',
    }
    sections = []
    for key, label in categories.items():
        section_games = [game for game in games if game['category'] == key]
        if not section_games:
            continue
        section_links = "\n".join(
            f"        <li><a href=\"{game['slug']}.html\">{game['title']}</a> — {game['tag']}</li>"
            for game in section_games
        )
        sections.append(
            f"    <section class=\"game-group\">\n      <h2>{label}</h2>\n      <p>Explore {label.lower()} browser games on ArcadeZone with direct play pages, tips, and strategy guidance.</p>\n      <ul>\n{section_links}\n      </ul>\n    </section>"
        )
    content = "\n\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
  <meta name=\"robots\" content=\"index, follow\" />
  <title>All Games — ArcadeZone</title>
  <meta name=\"description\" content=\"Browse all free browser games available on ArcadeZone, organized by category and ready to play.\" />
  <meta property=\"og:type\" content=\"website\" />
  <meta property=\"og:url\" content=\"{BASE_URL}/all-games.html\" />
  <meta property=\"og:title\" content=\"All Games — ArcadeZone\" />
  <meta property=\"og:description\" content=\"Browse all free browser games available on ArcadeZone, organized by category and ready to play.\" />
  <meta name=\"twitter:card\" content=\"summary_large_image\" />
  <link rel=\"stylesheet\" href=\"/css/style.css\" />
</head>
<body>
  <header>
    <a href=\"/\">ArcadeZone</a> › <span>All Games</span>
  </header>
  <main>
    <article>
      <h1>All Games</h1>
      <p>Browse the full ArcadeZone library by category and choose the perfect browser game for your mood.</p>
{content}
    </article>
  </main>
  <footer>
    <p><a href=\"/privacy.html\">Privacy</a> • <a href=\"/contact.html\">Contact</a></p>
  </footer>
</body>
</html>"""


def render_sitemap(games):
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"]
    lines.append(f"  <url><loc>{BASE_URL}/</loc><changefreq>daily</changefreq></url>")
    lines.append(f"  <url><loc>{BASE_URL}/all-games.html</loc><changefreq>monthly</changefreq></url>")
    for page in ("about.html", "contact.html", "privacy.html", "terms.html", "dmca.html"):
        lines.append(f"  <url><loc>{BASE_URL}/{page}</loc><changefreq>yearly</changefreq></url>")
    for game in games:
        lines.append(f"  <url><loc>{BASE_URL}/{game['slug']}.html</loc><changefreq>monthly</changefreq></url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def render_page(game, related_games):
    page = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "title": game['title'],
        "slug": game['slug'],
        "meta_description": f"Play {game['title']} free online on ArcadeZone. Expert tips, controls, and quick access to the browser game.",
        "screenshot_url": f"images/{game['slug']}.svg",
        "category": game['category'],
        "tag": game['tag'],
        "description_300_plus": make_description(game, related_games),
        "how_to_play": make_how_to_play(game),
        "highlights": make_highlights(game),
        "essentials": make_essentials(game),
        "tip1": make_tips(game)[0],
        "tip2": make_tips(game)[1],
        "tip3": make_tips(game)[2],
        "external_url": game['external_url'],
        "related_games": make_related_games(related_games),
        "developer_info": make_developer_info(game),
    }
    for key, value in replacements.items():
        page = page.replace(f"{{{{{key}}}}}", value)
    return page


def main():
    with CSV_PATH.open(newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        games = [row for row in reader]

    games_by_category = {}
    for game in games:
        games_by_category.setdefault(game['category'], []).append(game)

    for game in games:
        category_games = [g for g in games_by_category[game['category']] if g['slug'] != game['slug']]
        related_games = category_games[:3]
        output = render_page(game, related_games)
        path = OUTPUT_DIR / f"{game['slug']}.html"
        path.write_text(output, encoding='utf-8')
        print(f"Wrote {path}")

    (OUTPUT_DIR / "all-games.html").write_text(render_all_games_page(games), encoding='utf-8')
    print("Wrote all-games.html")
    (OUTPUT_DIR / "sitemap.xml").write_text(render_sitemap(games), encoding='utf-8')
    print("Wrote sitemap.xml")


if __name__ == '__main__':
    main()
