import logging
from utils.logging_config import setup_logging

logger = setup_logging(__name__)


def transform_pokemon_data(raw_data):
    """Transform raw API data into structured relational format"""
    transformed = {
        "pokemon": None,
        "types": [],
        "abilities": [],
        "stats": [],
        "species_id": None,
        "evolution_chain_id": None,
    }
    if not raw_data or "pokemon" not in raw_data or raw_data["pokemon"] is None:
        logger.warning("No valid 'pokemon' data found in raw_data for transformation.")
        return transformed

    pokemon = raw_data["pokemon"]

    transformed["pokemon"] = {
        "pokemon_id": pokemon.get("id"),
        "name": pokemon.get("name"),
        "height": pokemon.get("height"),
        "weight": pokemon.get("weight"),
        "base_experience": pokemon.get("base_experience"),
        "is_default": pokemon.get("is_default", False),
    }

    if raw_data.get("species") and raw_data["species"].get("url"):
        try:
            transformed["species_id"] = int(
                raw_data["species"]["url"].rstrip("/").split("/")[-1]
            )
        except (ValueError, IndexError):
            logger.warning(
                f"Could not parse species_id from URL: {raw_data['species']['url']}"
            )

    if raw_data.get("evolution_chain") and raw_data["evolution_chain"].get("url"):
        try:
            transformed["evolution_chain_id"] = int(
                raw_data["evolution_chain"]["url"].rstrip("/").split("/")[-1]
            )
        except (ValueError, IndexError):
            logger.warning(
                f"Could not parse evolution_chain_id from URL: {raw_data['evolution_chain']['url']}"
            )

    # Types
    if "types" in pokemon and isinstance(pokemon["types"], list):
        for type_entry in pokemon["types"]:
            type_data = type_entry.get("type")
            if type_data and type_data.get("name"):
                transformed["types"].append(
                    {"type_name": type_data["name"], "pokemon_id": pokemon["id"]}
                )
            else:
                logger.warning(
                    f"Malformed type entry for Pokémon ID {pokemon.get('id')}: {type_entry}"
                )
    else:
        logger.info(f"No 'types' data found for Pokémon ID {pokemon.get('id')}.")

    # Abilities
    if "abilities" in pokemon and isinstance(pokemon["abilities"], list):
        for ability_entry in pokemon["abilities"]:
            ability_data = ability_entry.get("ability")
            if ability_data and ability_data.get("name"):
                transformed["abilities"].append(
                    {"ability_name": ability_data["name"], "pokemon_id": pokemon["id"]}
                )
            else:
                logger.warning(
                    f"Malformed ability entry for Pokémon ID {pokemon.get('id')}: {ability_entry}"
                )
    else:
        logger.info(f"No 'abilities' data found for Pokémon ID {pokemon.get('id')}.")

    # Stats
    if "stats" in pokemon and isinstance(pokemon["stats"], list):
        for stat_entry in pokemon["stats"]:
            stat_data = stat_entry.get("stat")
            if (
                stat_data
                and stat_data.get("name")
                and stat_entry.get("base_stat") is not None
            ):
                transformed["stats"].append(
                    {
                        "stat_name": stat_data["name"],
                        "base_stat": stat_entry["base_stat"],
                        "effort": stat_entry.get("effort", 0),
                        "pokemon_id": pokemon["id"],
                    }
                )
            else:
                logger.warning(
                    f"Malformed stat entry for Pokémon ID {pokemon.get('id')}: {stat_entry}"
                )
    else:
        logger.info(f"No 'stats' data found for Pokémon ID {pokemon.get('id')}.")

    return transformed
