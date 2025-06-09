import pytest
from etl.load.loader import load_transformed_data
from data_models.models import Pokemon


def test_load_transformed_data(db_session):
    test_data = {
        "pokemon": {
            "pokemon_id": 999,
            "name": "testmon",
            "height": 1,
            "weight": 1,
            "base_experience": 1,
            "is_default": True,
        },
        "types": [{"type_name": "test-type"}],
        "abilities": [{"ability_name": "test-ability"}],
        "stats": [{"stat_name": "test-stat", "base_stat": 50, "effort": 0}],
    }

    result = load_transformed_data(test_data, session=db_session)
    assert result is True

    pokemon = db_session.query(Pokemon).filter_by(pokemon_id=999).first()
    assert pokemon.name == "testmon"
