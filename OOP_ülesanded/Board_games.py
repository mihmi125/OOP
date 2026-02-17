"""Board games."""
from collections import Counter


class Player:
    """Represents a player and tracks their overall match history."""

    def __init__(self, name):
        """Initialize a new Player instance."""
        self.name = name
        self.play_count = 0
        self.win_count = 0
        self.played_games = []

    def add_play(self, game_name, is_winner):
        """Add a game play to player history."""
        self.play_count += 1
        self.played_games.append(game_name)
        if is_winner:
            self.win_count += 1

    def get_favourite_game(self):
        """Return the game name played most frequently by this player."""
        if not self.played_games:
            return None
        # Safely handle the Counter result
        common = Counter(self.played_games).most_common(1)
        return common[0][0] if common else None


class Game:
    """Represents a specific board game and its statistics."""

    def __init__(self, name):
        """Initialize a new Game instance."""
        self.name = name
        self.plays = []
        self.record_score = -float('inf')
        self.record_holder = None

    def add_play(self, play_data):
        """Add session data to the game statistics."""
        self.plays.append(play_data)

        if play_data['type'] == 'points':
            for p_name, score in play_data['points'].items():
                if score > self.record_score:
                    self.record_score = score
                    self.record_holder = p_name

    def get_most_frequent_player_count(self):
        """Find the most common number of players in a session."""
        if not self.plays:
            return None
        counts = [len(p['players']) for p in self.plays]
        common = Counter(counts).most_common(1)
        return common[0][0] if common else None

    def get_stat_leader(self, key):
        """Return the player with the most occurrences of a key."""
        stats = [p[key] for p in self.plays if p.get(key) is not None]
        if not stats:
            return None
        common = Counter(stats).most_common(1)
        return common[0][0] if common else None

    def get_rate_leader(self, target_type='winner'):
        """Calculate win/loss percentage per player for this specific game."""
        player_stats = {}

        for p in self.plays:
            if target_type == 'loser' and p['type'] == 'winner':
                continue

            for player_name in p['players']:
                if player_name not in player_stats:
                    player_stats[player_name] = [0, 0]

                player_stats[player_name][1] += 1
                if p.get(target_type) == player_name:
                    player_stats[player_name][0] += 1

        if not player_stats:
            return None

        return max(player_stats, key=lambda k: player_stats[k][0] / player_stats[k][1])


class Statistics:
    """Handles the loading and querying of board game data."""

    def __init__(self, filename):
        """Initialize Statistics by loading data from a file."""
        self.games = {}
        self.players = {}
        self.all_plays = []
        self._load_data(filename)

    def _process_result(self, r_type, results, player_list):
        """Parse the result string based on the result type."""
        winner, loser, points_map = None, None, {}
        if r_type == 'points':
            scores = list(map(int, results.split(',')))
            points_map = dict(zip(player_list, scores))
            winner = max(points_map, key=points_map.get)
            loser = min(points_map, key=points_map.get)
        elif r_type == 'places':
            ranking = results.split(',')
            winner, loser = ranking[0], ranking[-1]
        elif r_type == 'winner':
            winner = results
        return winner, loser, points_map

    def _load_data(self, filename):
        """Parse the semicolon-separated text file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    parts = clean_line.split(';')
                    if len(parts) != 4:
                        continue

                    g_name, p_names, r_type, results = parts
                    player_list = p_names.split(',')

                    if g_name not in self.games:
                        self.games[g_name] = Game(g_name)

                    winner, loser, points_map = self._process_result(r_type, results, player_list)
                    play_info = {
                        'game': g_name, 'players': player_list, 'type': r_type,
                        'winner': winner, 'loser': loser, 'points': points_map
                    }

                    self.all_plays.append(play_info)
                    self.games[g_name].add_play(play_info)
                    for p_name in player_list:
                        if p_name not in self.players:
                            self.players[p_name] = Player(p_name)
                        self.players[p_name].add_play(g_name, p_name == winner)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")

    def _get_player_stat(self, name, action):
        """Handle player-specific queries."""
        player = self.players.get(name)
        if not player:
            return None
        if action == "amount":
            return player.play_count
        if action == "favourite":
            return player.get_favourite_game()
        if action == "won":
            return player.win_count
        return None

    def _get_game_stat(self, name, action):
        """Handle game-specific queries."""
        game = self.games.get(name)
        if not game:
            return None
        actions = {
            "amount": lambda: len(game.plays),
            "player-amount": game.get_most_frequent_player_count,
            "most-wins": lambda: game.get_stat_leader('winner'),
            "most-frequent-winner": lambda: game.get_rate_leader('winner'),
            "most-losses": lambda: game.get_stat_leader('loser'),
            "most-frequent-loser": lambda: game.get_rate_leader('loser'),
            "record-holder": lambda: game.record_holder
        }
        query = actions.get(action)
        return query() if query else None

    def get(self, path: str):
        """Act as an API Router for path-based queries."""
        p = path.strip("/").split("/")
        if not p or p[0] == "":
            return "Invalid Path"

        if p[0] == "players":
            return list(self.players.keys())
        if p[0] == "games":
            return list(self.games.keys())
        if p[0] == "total":
            return len(self.all_plays) if len(p) == 1 else sum(1 for pl in self.all_plays if pl['type'] == p[1])
        if p[0] == "player" and len(p) > 2:
            return self._get_player_stat(p[1], p[2])
        if p[0] == "game" and len(p) > 2:
            return self._get_game_stat(p[1], p[2])
        return "Invalid Path"