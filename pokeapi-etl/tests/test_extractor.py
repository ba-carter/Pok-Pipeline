import pytest
from unittest.mock import patch

from etl.extract.extractor import (
    fetch_data,
    fetch_pokemon_data,
    fetch_species_data,
    fetch_evolution_chain,
)

from utils.config import Config


@patch("etl.extract.extractor.requests.Session")
def test_fetch_data_success(mock_session):
    mock_response = mock_session.return_value.get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "bulbasaur"}

    result = fetch_data("https://pokeapi.co/api/v2/pokemon/1")
    assert result == {"id": 1, "name": "bulbasaur"}


@pytest.fixture
def mock_fetch_data(mocker):
    """Fixture to mock the internal fetch_data call within extractor."""
    return mocker.patch("etl.extract.extractor.fetch_data")


def test_fetch_pokemon_data_calls_fetch_data(mock_fetch_data):
    """Verifies fetch_pokemon_data correctly calls fetch_data with correct URL."""
    pokemon_id = 1
    expected_url = f"{Config.POKEAPI_BASE_URL}pokemon/{pokemon_id}"
    mock_fetch_data.return_value = {"id": pokemon_id, "name": "Bulbasaur"}

    result = fetch_pokemon_data(pokemon_id)

    mock_fetch_data.assert_called_once_with(expected_url)
    assert result == {"id": pokemon_id, "name": "Bulbasaur"}


def test_fetch_species_data_calls_fetch_data(mock_fetch_data):
    """Verifies fetch_species_data correctly calls fetch_data with correct URL."""
    species_url = "https://pokeapi.co/api/v2/pokemon-species/1/"
    mock_fetch_data.return_value = {"id": 1, "name": "bulbasaur-species"}

    result = fetch_species_data(species_url)

    mock_fetch_data.assert_called_once_with(species_url)
    assert result == {"id": 1, "name": "bulbasaur-species"}


def test_fetch_evolution_chain_calls_fetch_data(mock_fetch_data):
    """Verifies fetch_evolution_chain correctly calls fetch_data with correct URL."""
    evolution_url = "https://pokeapi.co/api/v2/evolution-chain/1/"
    mock_fetch_data.return_value = {"id": 1, "chain": {}}

    result = fetch_evolution_chain(evolution_url)

    mock_fetch_data.assert_called_once_with(evolution_url)
    assert result == {"id": 1, "chain": {}}
