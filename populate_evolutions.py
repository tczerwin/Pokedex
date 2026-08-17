"""
Run this once to populate evolution chains in your database.
It will fetch evolution data from PokeAPI for all 1000+ pokemon.
"""
from PokemonDatabase import PokemonDatabase

if __name__ == "__main__":
    pokedex = PokemonDatabase()
    pokedex.add_evolution_chains_to_database()
