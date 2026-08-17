import requests
import pandas as pd
import time
import sqlite3


TYPE_ADVANTAGE = {
    "normal": ["fighting"],
    "water": ["electric", "grass"],
    "fire": ["water", "rock", "ground"],
    "grass": ["fire", "ice", "poison", "flying", "bug"],
    "electric": ["ground"],
    "psychic": ["bug", "ghost", "dark"],
    "dragon": ["ice", "dragon", "fairy"],
    "dark": ["fighting", "bug", "fairy"],
    "fairy": ["poison", "steel"],
    "fighting": ["flying", "psychic", "fairy"],
    "rock": ["water", "grass", "fighting", "ground", "steel"],
    "ground": ["water", "grass", "ice"],
    "ice": ["fire", "fighting", "rock", "steel"],
    "ghost": ["ghost", "dark"],
    "bug": ["fire", "flying", "rock"],
    "poison": ["ground", "psychic"],
    "flying": ["electric", "ice", "rock"],
    "steel": ["fire", "fighting", "ground"]
}

# Create TYPE_RESIST mapping (what resists each type)
TYPE_RESIST = {}
for defend_type, attack_types in TYPE_ADVANTAGE.items():
    for attack_type in attack_types:
        if attack_type not in TYPE_RESIST:
            TYPE_RESIST[attack_type] = []
        TYPE_RESIST[attack_type].append(defend_type)


# Standard Pokemon type colors -- shared by top10.py and look_up.py to
# theme their result cards (border color, type badges) consistently.
TYPE_COLORS = {
    "normal":   "#A8A878",
    "fire":     "#F08030",
    "water":    "#6890F0",
    "electric": "#F8D030",
    "grass":    "#78C850",
    "ice":      "#98D8D8",
    "fighting": "#C03028",
    "poison":   "#A040A0",
    "ground":   "#E0C068",
    "flying":   "#A890F0",
    "psychic":  "#F85888",
    "bug":      "#A8B820",
    "rock":     "#B8A038",
    "ghost":    "#705898",
    "dragon":   "#7038F8",
    "dark":     "#705848",
    "steel":    "#B8B8D0",
    "fairy":    "#EE99AC",
}
DEFAULT_TYPE_COLOR = "#777777"


class PokemonDatabase:

    def __init__(self, database="data/pokemon.db"):
        self.database = database


    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    def get_connection(self):
        return sqlite3.connect(self.database)


    # ==========================================
    # POKEAPI
    # ==========================================

    def get_pokemon_count(self):

        url = "https://pokeapi.co/api/v2/pokemon-species/"

        try:
            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            return data["count"]

        except requests.exceptions.RequestException as e:

            print(f"API request failed: {e}")

            return 0


    def get_pokemon_stats(self, pokemon_id):

        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            stats = {}

            stats["pokemon"] = data["name"]
            stats["pokedex_no"] = data["id"]

            for stat in data["stats"]:

                stat_name = (
                    stat["stat"]["name"]
                    .replace("-", "_")
                )

                stats[stat_name] = stat["base_stat"]

            return pd.DataFrame(
                stats,
                index=[0]
            )

        except requests.exceptions.RequestException as e:

            print(
                f"Error getting Pokemon {pokemon_id}: {e}"
            )

            return None


    def get_pokemon_details(self, pokemon_id):

        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            details = {}

            details["pokemon"] = data["name"]
            details["pokedex_no"] = data["id"]

            # PokeAPI uses decimeters
            details["height"] = data["height"] / 10

            # PokeAPI uses hectograms
            details["weight"] = data["weight"] / 10

            types = []

            for pokemon_type in data["types"]:

                types.append(
                    pokemon_type["type"]["name"]
                )

            details["type_1"] = types[0]

            if len(types) > 1:
                details["type_2"] = types[1]
            else:
                details["type_2"] = None

            return pd.DataFrame(
                details,
                index=[0]
            )

        except requests.exceptions.RequestException as e:

            print(
                f"Error getting Pokemon {pokemon_id}: {e}"
            )

            return None


    # ==========================================
    # CREATE POKEDEX
    # ==========================================

    def create_pokedex(self, number_of_pokemon):

        pokemon_list = []

        for pokemon_id in range(
            1,
            number_of_pokemon + 1
        ):

            pokemon = self.get_pokemon_stats(
                pokemon_id
            )

            if pokemon is not None:
                pokemon_list.append(pokemon)

            print(
                f"Pokemon no. {pokemon_id} added to pokedex"
            )

        return pd.concat(
            pokemon_list,
            ignore_index=True
        )


    def create_pokemon_details(self, number_of_pokemon):

        details_list = []

        for pokemon_id in range(
            1,
            number_of_pokemon + 1
        ):

            details = self.get_pokemon_details(
                pokemon_id
            )

            if details is not None:
                details_list.append(details)

            print(
                f"Details added for Pokemon {pokemon_id}"
            )

            time.sleep(0.05)

        return pd.concat(
            details_list,
            ignore_index=True
        )


    # ==========================================
    # STORE DATA
    # ==========================================

    def store_pokedex_sqlite(self, df):

        conn = self.get_connection()

        df.to_sql(
            "pokedex",
            conn,
            if_exists="replace",
            index=False
        )

        conn.close()

        print(
            "Pokédex stored in SQLite database"
        )


    # ==========================================
    # GET POKEMON
    # ==========================================

    def get_pokemon_by_number(self, pokedex_no):

        conn = self.get_connection()

        query = """
        SELECT *
        FROM pokedex
        WHERE pokedex_no = ?
        """

        pokemon = pd.read_sql(
            query,
            conn,
            params=(pokedex_no,)
        )

        conn.close()

        if pokemon.empty:

            print(
                f"No Pokemon found with "
                f"Pokédex number {pokedex_no}"
            )

            return None

        return pokemon


    def get_pokemon_by_name(self, pokemon_name):

        conn = self.get_connection()

        query = """
        SELECT *
        FROM pokedex
        WHERE LOWER(pokemon) = LOWER(?)
        """

        pokemon = pd.read_sql(
            query,
            conn,
            params=(pokemon_name,)
        )

        conn.close()

        if pokemon.empty:

            print("Pokemon not found")

            return None

        return pokemon.iloc[0].to_dict()


    # ==========================================
    # TOP 10
    # ==========================================

    def get_top_10(self, pokemon_type):

        conn = self.get_connection()

        query = """
        SELECT
            pokemon,
            type_1,
            type_2,
            hp,
            attack,
            defense,
            special_attack,
            special_defense,
            speed,
            hp + attack + defense +
            special_attack +
            special_defense +
            speed AS total_stats
        FROM pokedex
        WHERE LOWER(type_1) = LOWER(?)
           OR LOWER(type_2) = LOWER(?)
        ORDER BY total_stats DESC
        LIMIT 10
        """

        strongest = pd.read_sql(
            query,
            conn,
            params=(pokemon_type, pokemon_type)
        )

        conn.close()
        if strongest.empty:

            print("Type not found")

            return None

        return strongest


    # ==========================================
    # RAID COUNTERS
    # ==========================================

    def get_raid_counters(self, raid_boss):

        conn = self.get_connection()

        # Try to parse as a number first
        boss = None
        try:
            boss_num = int(raid_boss)
            query = """
            SELECT *
            FROM pokedex
            WHERE pokedex_no = ?
            """
            boss = pd.read_sql(
                query,
                conn,
                params=(boss_num,)
            )
        except (ValueError, TypeError):
            # If not a number, try by name
            query = """
            SELECT *
            FROM pokedex
            WHERE LOWER(pokemon) = LOWER(?)
            """
            boss = pd.read_sql(
                query,
                conn,
                params=(raid_boss,)
            )

        if boss.empty:

            conn.close()

            print("Raid boss not found")

            return None

        boss_types = [
            boss.iloc[0]["type_1"],
            boss.iloc[0]["type_2"]
        ]

        boss_types = [
            pokemon_type
            for pokemon_type in boss_types
            if pd.notna(pokemon_type)
        ]

        # Find weaknesses (types strong against boss)

        weaknesses = []

        for pokemon_type in boss_types:

            if pokemon_type in TYPE_ADVANTAGE:

                weaknesses.extend(
                    TYPE_ADVANTAGE[pokemon_type]
                )

        # Get Pokemon

        counters_query = """
        SELECT
            pokemon,
            attack,
            special_attack,
            defense,
            special_defense,
            speed,
            type_1,
            type_2,
            hp + attack + defense +
            special_attack +
            special_defense +
            speed AS total_stats
        FROM pokedex
        """

        pokemon = pd.read_sql(
            counters_query,
            conn
        )

        conn.close()

        # Find counters with type advantage

        counters = pokemon[
            (
                pokemon["type_1"]
                .isin(weaknesses)
            )
            |
            (
                pokemon["type_2"]
                .isin(weaknesses)
            )
        ].copy()

        # Calculate counter score
        def calculate_counter_score(row):
            # Base score heavily weighted toward attack (most important for DPS)
            offensive_score = (row['attack'] + row['special_attack']) / 2
            defensive_score = (row['defense'] + row['special_defense']) / 2

            # Check if counter's type_1 is strong against boss
            counter_type1 = str(row['type_1']).lower() if pd.notna(row['type_1']) else None
            counter_type2 = str(row['type_2']).lower() if pd.notna(row['type_2']) else None

            # Apply type advantage multiplier (1.5x if has type advantage)
            type_multiplier = 1.0
            for boss_type in boss_types:
                boss_type_lower = str(boss_type).lower()
                if boss_type_lower in TYPE_ADVANTAGE:
                    if counter_type1 in TYPE_ADVANTAGE[boss_type_lower] or counter_type2 in TYPE_ADVANTAGE[boss_type_lower]:
                        type_multiplier = 1.5
                        break

            # Apply type resistance multiplier for defense (1.25x if resists)
            resist_multiplier = 1.0
            for boss_type in boss_types:
                boss_type_lower = str(boss_type).lower()
                if boss_type_lower in TYPE_RESIST:
                    if counter_type1 in TYPE_RESIST[boss_type_lower] or counter_type2 in TYPE_RESIST[boss_type_lower]:
                        resist_multiplier = 1.25
                        break

            # Score: heavily favor attack (70%), defense (20%), speed (10%)
            speed = row['speed']
            score = (offensive_score * type_multiplier * 0.7) + (defensive_score * resist_multiplier * 0.2) + (speed * 0.1)

            return score

        counters['counter_score'] = counters.apply(calculate_counter_score, axis=1)

        counters = counters.sort_values(
            by='counter_score',
            ascending=False
        )

        return counters.head(5)


    # ==========================================
    # SPRITES
    # ==========================================

    def add_sprites_to_database(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                ALTER TABLE pokedex
                ADD COLUMN sprite BLOB
                """
            )

            print("Added sprite column")

        except sqlite3.OperationalError:

            print(
                "Sprite column already exists"
            )

        number_of_pokemon = (
            self.get_pokemon_count()
        )

        for pokemon_id in range(
            1,
            number_of_pokemon + 1
        ):

            try:

                url = (
                    "https://pokeapi.co/api/v2/"
                    f"pokemon/{pokemon_id}"
                )

                response = requests.get(
                    url,
                    timeout=10
                )

                response.raise_for_status()

                data = response.json()

                sprite_url = (
                    data["sprites"]["front_default"]
                )

                if sprite_url is None:

                    print(
                        f"No sprite found for "
                        f"Pokemon {pokemon_id}"
                    )

                    continue

                sprite_response = requests.get(
                    sprite_url,
                    timeout=10
                )

                sprite_response.raise_for_status()

                sprite = sprite_response.content

                cursor.execute(
                    """
                    UPDATE pokedex
                    SET sprite = ?
                    WHERE pokedex_no = ?
                    """,
                    (
                        sprite,
                        pokemon_id
                    )
                )

                print(
                    f"Added sprite for Pokemon "
                    f"{pokemon_id}"
                )

                time.sleep(0.05)

            except requests.exceptions.RequestException as e:

                print(
                    f"Error downloading Pokemon "
                    f"{pokemon_id}: {e}"
                )

        conn.commit()

        conn.close()

        print(
            "All sprites added to database!"
        )


    # ==========================================
    # EVOLUTION CHAINS
    # ==========================================

    def add_evolution_chains_to_database(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                ALTER TABLE pokedex
                ADD COLUMN evolution_chain TEXT
                """
            )

            print("Added evolution_chain column")

        except sqlite3.OperationalError:

            print(
                "Evolution_chain column already exists"
            )

        number_of_pokemon = (
            self.get_pokemon_count()
        )

        for pokemon_id in range(
            1,
            number_of_pokemon + 1
        ):

            try:

                # Get species data to find evolution chain URL
                species_url = (
                    "https://pokeapi.co/api/v2/"
                    f"pokemon-species/{pokemon_id}"
                )

                species_response = requests.get(
                    species_url,
                    timeout=10
                )

                species_response.raise_for_status()

                species_data = species_response.json()

                evolution_chain_url = (
                    species_data["evolution_chain"]["url"]
                )

                # Get evolution chain data
                chain_response = requests.get(
                    evolution_chain_url,
                    timeout=10
                )

                chain_response.raise_for_status()

                chain_data = chain_response.json()

                # Parse evolution chain into readable format
                evolution_text = (
                    self._parse_evolution_chain(
                        chain_data["chain"]
                    )
                )

                cursor.execute(
                    """
                    UPDATE pokedex
                    SET evolution_chain = ?
                    WHERE pokedex_no = ?
                    """,
                    (
                        evolution_text,
                        pokemon_id
                    )
                )

                print(
                    f"Added evolution chain for "
                    f"Pokemon {pokemon_id}"
                )

                time.sleep(0.05)

            except requests.exceptions.RequestException as e:

                print(
                    f"Error getting evolution data for "
                    f"Pokemon {pokemon_id}: {e}"
                )

        conn.commit()

        conn.close()

        print(
            "All evolution chains added to database!"
        )

    def _parse_evolution_chain(self, chain_node, parent_name=None):
        """
        Recursively parse PokeAPI evolution chain into readable format.
        Returns a string like: "Bulbasaur → Ivysaur (Level 16) → Venusaur (Level 32)"
        """
        current_name = chain_node["species"]["name"].title()

        # Build evolution text for current node
        if parent_name is None:
            current_text = current_name
        else:
            # Get evolution details
            details = chain_node.get("evolution_details", [])
            if details:
                detail = details[0]
                condition = self._get_evolution_condition(detail)
                current_text = f"{current_name} ({condition})"
            else:
                current_text = current_name

        # Recursively process evolutions
        if chain_node["evolves_to"]:
            evolution_strings = []
            for evolution in chain_node["evolves_to"]:
                evolution_strings.append(
                    self._parse_evolution_chain(
                        evolution,
                        current_name
                    )
                )
            return f"{current_text} → {' → '.join(evolution_strings)}"
        else:
            return current_text

    def _get_evolution_condition(self, detail):
        """Extract human-readable evolution condition."""
        if detail.get("min_level"):
            return f"Level {detail['min_level']}"
        elif detail.get("item"):
            return detail["item"]["name"].title()
        elif detail.get("trade"):
            return "Trade"
        elif detail.get("held_item"):
            return f"Hold {detail['held_item']['name'].title()}"
        elif detail.get("trigger", {}).get("name") == "level-up":
            return "Level Up"
        else:
            return "Special"

    def get_evolution_chain(self, pokemon_name):
        """Get evolution chain for a pokemon."""
        conn = self.get_connection()

        query = """
        SELECT evolution_chain
        FROM pokedex
        WHERE LOWER(pokemon) = LOWER(?)
        """

        result = pd.read_sql(
            query,
            conn,
            params=(pokemon_name,)
        )

        conn.close()

        if result.empty or result.iloc[0]["evolution_chain"] is None:
            return None

        return result.iloc[0]["evolution_chain"]


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    pokedex = PokemonDatabase()

    # pokemon = pokedex.get_top_10("fire")

    # print(pokemon)
