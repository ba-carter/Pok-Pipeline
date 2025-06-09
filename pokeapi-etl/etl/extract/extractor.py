import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.helpers import get_request_delay
from utils.logging_config import setup_logging
from utils.config import Config
import time
import os

logger = setup_logging(__name__)

POKEAPI_BASE_URL = Config.POKEAPI_BASE_URL
API_RETRIES = Config.API_RETRIES
API_BACKOFF_FACTOR = Config.API_BACKOFF_FACTOR


def create_retry_session(retries=API_RETRIES, backoff_factor=API_BACKOFF_FACTOR):
    """Creates a requests session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_data(url):
    """Fetch data with retry logic and timeout"""
    session = create_retry_session()
    request_delay = get_request_delay()

    try:
        response = session.get(url, timeout=(3.05, 10))
        response.raise_for_status()
        time.sleep(request_delay)
        return response.json()
    except requests.exceptions.HTTPError as err:
        logger.error(
            f"HTTP error occurred for {url}: {err.response.status_code} - {err.response.text}"
        )
    except requests.exceptions.Timeout:
        logger.error(f"Request to {url} timed out.")
    except requests.exceptions.ConnectionError as err:
        logger.error(f"Connection error occurred for {url}: {err}")
    except requests.exceptions.RequestException as err:
        logger.error(f"An unexpected request error occurred for {url}: {err}")
    return None


def fetch_pokemon_data(pokemon_id):
    """Fetch Pokémon data from PokeAPI by ID"""
    url = f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}"
    return fetch_data(url)


def fetch_species_data(species_url):
    """Fetch species data from PokeAPI"""
    return fetch_data(species_url)


def fetch_evolution_chain(evolution_chain_url):
    """Fetch evolution chain data from PokeAPI"""
    return fetch_data(evolution_chain_url)


def extract_poke_range(start_id, end_id):
    """Extract data for a range of Pokémon IDs"""
    pokemon_data = []
    for pokemon_id in range(start_id, end_id + 1):
        logger.info(f"Extracting data for Pokémon ID: {pokemon_id}")
        pokemon = fetch_pokemon_data(pokemon_id)
        if not pokemon:
            continue

        # Fetch species data
        species = (
            fetch_species_data(pokemon["species"]["url"])
            if "species" in pokemon
            else None
        )

        # Fetch evolution chain if available
        evolution_chain = None
        if species and species.get("evolution_chain", {}).get("url"):
            evolution_chain = fetch_evolution_chain(species["evolution_chain"]["url"])

        pokemon_data.append(
            {"pokemon": pokemon, "species": species, "evolution_chain": evolution_chain}
        )

    return pokemon_data


def extract_pokemon_range(start_id, end_id):
    """Extract data for a range of Pokémon IDs"""
    pokemon_data = []
    for pokemon_id in range(start_id, end_id + 1):
        logger.info(f"Extracting data for Pokémon ID: {pokemon_id}")

        pokemon = fetch_pokemon_data(pokemon_id)
        if not pokemon:
            logger.warning(
                f"Skipping Pokémon ID {pokemon_id} due to failed main data extraction."
            )
            continue

        species = None
        if "species" in pokemon and "url" in pokemon["species"]:
            species = fetch_species_data(pokemon["species"]["url"])
        else:
            logger.warning(
                f"Species URL not found for Pokémon ID {pokemon_id}. Skipping species data extraction."
            )

        evolution_chain = None
        if species and species.get("evolution_chain", {}).get("url"):
            evolution_chain = fetch_evolution_chain(species["evolution_chain"]["url"])
        else:
            logger.warning(
                f"Evolution chain URL not found for Pokémon ID {pokemon_id}. Skipping evolution chain extraction."
            )

        pokemon_data.append(
            {
                "pokemon": pokemon,
                "species": species,
                "evolution_chain": evolution_chain,
            }
        )

    return pokemon_data
