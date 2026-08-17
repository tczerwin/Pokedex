import json
import os
from pathlib import Path

class TeamManager:
    """Manages saving and loading Pokemon teams."""

    def __init__(self, teams_file="data/teams.json"):
        self.teams_file = teams_file
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create teams.json if it doesn't exist."""
        os.makedirs(os.path.dirname(self.teams_file), exist_ok=True)
        if not os.path.exists(self.teams_file):
            with open(self.teams_file, 'w') as f:
                json.dump({"teams": []}, f, indent=2)

    def get_all_teams(self):
        """Get all saved teams."""
        try:
            with open(self.teams_file, 'r') as f:
                data = json.load(f)
                return data.get("teams", [])
        except:
            return []

    def save_team(self, team_name, pokemon_list):
        """Save a team. pokemon_list is list of dicts with 'name' and 'level'."""
        teams = self.get_all_teams()

        # Remove existing team with same name if it exists
        teams = [t for t in teams if t["name"] != team_name]

        # Add new team
        new_team = {
            "name": team_name,
            "pokemon": pokemon_list
        }
        teams.append(new_team)

        with open(self.teams_file, 'w') as f:
            json.dump({"teams": teams}, f, indent=2)

    def load_team(self, team_name):
        """Load a team by name."""
        teams = self.get_all_teams()
        for team in teams:
            if team["name"] == team_name:
                return team["pokemon"]
        return None

    def delete_team(self, team_name):
        """Delete a team by name."""
        teams = self.get_all_teams()
        teams = [t for t in teams if t["name"] != team_name]

        with open(self.teams_file, 'w') as f:
            json.dump({"teams": teams}, f, indent=2)

    def get_team_names(self):
        """Get list of all team names."""
        teams = self.get_all_teams()
        return [t["name"] for t in teams]
