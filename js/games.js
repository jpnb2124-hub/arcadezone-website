const GAMES = [
  // FEATURED
  { id: 1, title: "2048", category: "featured", tag: "Puzzle", emoji: "🔢", url: "https://play2048.co/" },
  { id: 2, title: "Pac-Man", category: "featured", tag: "Classic", emoji: "👾", url: "https://www.google.com/logos/2010/pacman10-i.html" },
  { id: 3, title: "Snake", category: "featured", tag: "Classic", emoji: "🐍", url: "https://www.google.com/fbx?fbx=snake_arcade" },
  { id: 4, title: "Flappy Bird", category: "featured", tag: "Action", emoji: "🐦", url: "https://flappybird.io/" },
  { id: 5, title: "Tetris", category: "featured", tag: "Puzzle", emoji: "🟦", url: "https://tetris.com/play-tetris" },
  { id: 6, title: "Chess", category: "featured", tag: "Strategy", emoji: "♟️", url: "https://www.chess.com/play/computer" },

  // ACTION
  { id: 7, title: "Bullet Force", category: "action", tag: "Shooter", emoji: "🔫", url: "https://www.crazygames.com/embed/bullet-force-multiplayer" },
  { id: 8, title: "Krunker.io", category: "action", tag: "FPS", emoji: "🎯", url: "https://krunker.io/" },
  { id: 9, title: "Agar.io", category: "action", tag: "Multiplayer", emoji: "🔵", url: "https://agar.io/" },
  { id: 10, title: "Slither.io", category: "action", tag: "Multiplayer", emoji: "🐛", url: "https://slither.io/" },
  { id: 11, title: "Zombs Royale", category: "action", tag: "Battle Royale", emoji: "🧟", url: "https://zombsroyale.io/" },
  { id: 12, title: "Diep.io", category: "action", tag: "Shooter", emoji: "💥", url: "https://diep.io/" },
  { id: 37, title: "Shell Shockers", category: "action", tag: "FPS", emoji: "🥚", url: "https://shellshock.io/" },
{ id: 38, title: "Smash Karts", category: "action", tag: "Battle", emoji: "🏁", url: "https://smashkarts.io/" },
{ id: 39, title: "1v1.LOL", category: "action", tag: "Shooter", emoji: "🏗️", url: "https://1v1.lol/" },
{ id: 40, title: "Surviv.io", category: "action", tag: "Battle Royale", emoji: "🎖️", url: "https://surviv.io/" },
{ id: 41, title: "Venge.io", category: "action", tag: "FPS", emoji: "🔪", url: "https://venge.io/" },
{ id: 42, title: "Wings.io", category: "action", tag: "Arcade", emoji: "✈️", url: "https://wings.io/" },
{ id: 43, title: "Crazy Pixel Apocalypse", category: "action", tag: "Shooter", emoji: "🧟", url: "https://www.crazygames.com/embed/crazy-pixel-apocalypse" },
{ id: 44, title: "Stick Merge", category: "action", tag: "Action", emoji: "🤺", url: "https://www.crazygames.com/embed/stick-merge" },
{ id: 45, title: "Rooftop Snipers", category: "action", tag: "Fighting", emoji: "🎯", url: "https://www.crazygames.com/embed/rooftop-snipers" },
{ id: 46, title: "Getaway Shootout", category: "action", tag: "Action", emoji: "🏃", url: "https://www.crazygames.com/embed/getaway-shootout" },

  // PUZZLE
  { id: 13, title: "Sudoku", category: "puzzle", tag: "Puzzle", emoji: "🔣", url: "https://sudoku.com/" },
  { id: 14, title: "Mahjong", category: "puzzle", tag: "Classic", emoji: "🀄", url: "https://www.mahjong.org/" },
  { id: 15, title: "Cut the Rope", category: "puzzle", tag: "Puzzle", emoji: "🍬", url: "https://www.crazygames.com/embed/cut-the-rope" },
  { id: 16, title: "Wordle", category: "puzzle", tag: "Word", emoji: "📝", url: "https://www.nytimes.com/games/wordle/index.html" },
  { id: 17, title: "Minesweeper", category: "puzzle", tag: "Classic", emoji: "💣", url: "https://minesweeper.online/" },
  { id: 18, title: "Jigsaw Puzzle", category: "puzzle", tag: "Puzzle", emoji: "🧩", url: "https://www.jigsawplanet.com/" },

  // RACING
  { id: 19, title: "Moto X3M", category: "racing", tag: "Bike", emoji: "🏍️", url: "https://www.crazygames.com/embed/moto-x3m" },
  { id: 20, title: "Road Fury", category: "racing", tag: "Racing", emoji: "🚗", url: "https://www.crazygames.com/embed/road-fury" },
  { id: 21, title: "Drift Hunters", category: "racing", tag: "Drift", emoji: "🏎️", url: "https://drifthunters.io/" },
  { id: 22, title: "Burnout Drift", category: "racing", tag: "Racing", emoji: "💨", url: "https://www.crazygames.com/embed/burnout-drift" },
  { id: 23, title: "Traffic Rider", category: "racing", tag: "Bike", emoji: "🛵", url: "https://www.crazygames.com/embed/traffic-rider" },
  { id: 24, title: "Parking Fury", category: "racing", tag: "Parking", emoji: "🅿️", url: "https://www.crazygames.com/embed/parking-fury-3d" },

  // SPORTS
  { id: 25, title: "Basketball Stars", category: "sports", tag: "Basketball", emoji: "🏀", url: "https://www.crazygames.com/embed/basketball-stars" },
  { id: 26, title: "Soccer Random", category: "sports", tag: "Soccer", emoji: "⚽", url: "https://www.crazygames.com/embed/soccer-random" },
  { id: 27, title: "8 Ball Pool", category: "sports", tag: "Pool", emoji: "🎱", url: "https://www.miniclip.com/games/8-ball-pool-multiplayer/" },
  { id: 28, title: "Baseball Pro", category: "sports", tag: "Baseball", emoji: "⚾", url: "https://www.crazygames.com/embed/baseball-pro" },
  { id: 29, title: "Bowling King", category: "sports", tag: "Bowling", emoji: "🎳", url: "https://www.crazygames.com/embed/bowling-king" },
  { id: 30, title: "Table Tennis", category: "sports", tag: "Ping Pong", emoji: "🏓", url: "https://www.crazygames.com/embed/table-tennis-world-tour" },

  // CLASSICS
  { id: 31, title: "Space Invaders", category: "classics", tag: "Arcade", emoji: "👾", url: "https://freeinvaders.org/" },
  { id: 32, title: "Donkey Kong", category: "classics", tag: "Arcade", emoji: "🦍", url: "https://www.crazygames.com/embed/donkey-kong" },
  { id: 33, title: "Breakout", category: "classics", tag: "Arcade", emoji: "🧱", url: "https://www.crazygames.com/embed/block-breaker" },
  { id: 34, title: "Frogger", category: "classics", tag: "Arcade", emoji: "🐸", url: "https://www.crazygames.com/embed/frogger-in-toy-town" },
  { id: 35, title: "Galaga", category: "classics", tag: "Arcade", emoji: "🚀", url: "https://www.crazygames.com/embed/galaxian" },
  { id: 36, title: "Asteroids", category: "classics", tag: "Arcade", emoji: "☄️", url: "https://www.crazygames.com/embed/asteroids" },
  { id: 47, title: "Geometry Dash", category: "action", tag: "Platformer", emoji: "📐", url: "https://geometrydash.io/" },
  { id: 48, title: "Helix Jump", category: "action", tag: "Arcade", emoji: "🌀", url: "https://www.crazygames.com/game/helix-jump" },
  { id: 49, title: "Run 3", category: "action", tag: "Endless", emoji: "🚀", url: "https://www.coolmathgames.com/0-run-3" },
  { id: 50, title: "Candy Crush", category: "puzzle", tag: "Match-3", emoji: "🍭", url: "https://www.crazygames.com/game/candy-crush-saga" },
  { id: 51, title: "Unblock Me", category: "puzzle", tag: "Logic", emoji: "🧠", url: "https://www.unblockmeapp.com/" },
  { id: 52, title: "Flow Free", category: "puzzle", tag: "Flow", emoji: "🔵", url: "https://www.crazygames.com/game/flow-free" },
  { id: 53, title: "Temple Run", category: "racing", tag: "Endless", emoji: "🏃‍♂️", url: "https://www.crazygames.com/game/temple-run" },
  { id: 54, title: "Asphalt 9", category: "racing", tag: "Arcade", emoji: "🏎️", url: "https://www.crazygames.com/game/asphalt-9-legends" },
  { id: 55, title: "Super Soccer Stars", category: "sports", tag: "Soccer", emoji: "🥅", url: "https://www.crazygames.com/game/super-soccer-stars" },
  { id: 56, title: "Wiffle Ball", category: "sports", tag: "Baseball", emoji: "🥎", url: "https://www.crazygames.com/game/wiffle-ball" },
];
