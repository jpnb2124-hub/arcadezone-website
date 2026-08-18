const ALL_GAMES = typeof GAMES !== 'undefined' ? GAMES : [];

function slugifyTitle(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

const CURATED_GAME_SLUGS = new Set([
  '2048',
  'pac-man',
  'snake',
  'flappy-bird',
  'tetris',
  'chess',
  'krunker-io',
  'slither-io',
  '1v1-lol',
  'geometry-dash',
  'moto-x3m',
  'drift-hunters',
  'basketball-stars',
  '8-ball-pool',
  'sudoku',
  'wordle',
  'minesweeper',
  'run-3',
  'space-invaders',
  'galaga'
]);

const CURATED_GAMES = ALL_GAMES.filter(game => CURATED_GAME_SLUGS.has(slugifyTitle(game.title)));

function renderGames() {
  const categories = ['featured', 'action', 'puzzle', 'racing', 'sports', 'classics'];
  const gridIds = {
    featured: 'featuredGrid',
    action: 'actionGrid',
    puzzle: 'puzzleGrid',
    racing: 'racingGrid',
    sports: 'sportsGrid',
    classics: 'classicsGrid'
  };

  categories.forEach(cat => {
    const grid = document.getElementById(gridIds[cat]);
    if (!grid) return;
    const games = CURATED_GAMES.filter(g => g.category === cat);
    grid.innerHTML = games.map(game => createGameCard(game)).join('');
  });
}

function createGameCard(game) {
  const page = `${slugifyTitle(game.title)}.html`;
  return `
    <a class="game-card" href="${page}">
      <div class="game-thumb">${game.emoji}</div>
      <div class="play-overlay">▶</div>
      <div class="game-info">
        <div class="game-title">${game.title}</div>
        <span class="game-tag">${game.tag}</span>
      </div>
    </a>
  `;
}

function searchGames() {
  const query = document.getElementById('searchInput').value.toLowerCase().trim();
  if (!query) return;

  const existing = document.getElementById('searchResults');
  if (existing) existing.remove();

  const results = CURATED_GAMES.filter(g =>
    g.title.toLowerCase().includes(query) ||
    g.tag.toLowerCase().includes(query) ||
    g.category.toLowerCase().includes(query)
  );

  const container = document.createElement('div');
  container.id = 'searchResults';

  if (results.length === 0) {
    container.innerHTML = `<h2>No games found for "${query}"</h2>`;
  } else {
    container.innerHTML = `
      <h2>🔍 Results for "${query}" (${results.length} games)</h2>
      <div class="games-grid">${results.map(createGameCard).join('')}</div>
    `;
  }

  document.querySelector('.hero').insertAdjacentElement('afterend', container);
  container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

const searchInput = document.getElementById('searchInput');
if (searchInput) {
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') searchGames();
  });
}

function initCookieNotice() {
  const notice = document.getElementById('cookieNotice');
  const acceptBtn = document.getElementById('cookieNoticeAccept');
  if (!notice || !acceptBtn) return;

  if (localStorage.getItem('arcadezone_cookie_notice_accepted') === '1') {
    return;
  }

  notice.hidden = false;
  acceptBtn.addEventListener('click', () => {
    localStorage.setItem('arcadezone_cookie_notice_accepted', '1');
    notice.hidden = true;
  });
}

if (ALL_GAMES.length > 0) {
  renderGames();
}

initCookieNotice();
