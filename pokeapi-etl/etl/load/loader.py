from sqlalchemy.exc import SQLAlchemyError
from data_models.models import (
    Pokemon,
    Type,
    Ability,
    PokemonType,
    PokemonAbility,
    PokemonStat,
)
from utils.database import create_database_session
import logging
from utils.logging_config import setup_logging

logger = setup_logging(__name__)

def load_transformed_data(transformed_data, session=None):
    """Load transformed data into the database"""
    if not transformed_data or transformed_data.get('pokemon') is None:
        logger.warning("No valid transformed data to load.")
        return False

    own_session = False
    if session is None:
        session = create_database_session()
        own_session = True

    try:
        pokemon_data = transformed_data["pokemon"]
        pokemon_id = pokemon_data.get('pokemon_id')

        if pokemon_id is None:
            logger.error("Attempted to load Pokémon with missing pokemon_id.")
            return False

        pokemon = Pokemon(**pokemon_data)
        session.merge(pokemon)

        # Types
        for type_data in transformed_data.get('types', []):
            type_name = type_data.get('type_name')
            if not type_name:
                logger.warning(f"Skipping type for Pokémon {pokemon_id}.")
                continue

            type_record = session.query(Type).filter_by(type_name=type_name).first()
            if not type_record:
                type_record = Type(type_name=type_name)
                session.add(type_record)
                session.flush()

            session.merge(PokemonType(pokemon_id=pokemon_id, type_id=type_record.type_id))

        # Abilities
        for ability_data in transformed_data.get('abilities', []):
            ability_name = ability_data.get('ability_name')
            if not ability_name:
                logger.warning(f"Skipping ability for Pokémon {pokemon_id}.")
                continue

            ability_record = session.query(Ability).filter_by(ability_name=ability_name).first()
            if not ability_record:
                ability_record = Ability(ability_name=ability_name)
                session.add(ability_record)
                session.flush()

            session.merge(PokemonAbility(pokemon_id=pokemon_id, ability_id=ability_record.ability_id))

        # Stats
        for stat_data in transformed_data.get('stats', []):
            if not stat_data.get('stat_name') or stat_data.get('base_stat') is None:
                logger.warning(f"Skipping stat for Pokémon {pokemon_id}: {stat_data}")
                continue

            stat_data['pokemon_id'] = pokemon_id
            session.merge(PokemonStat(**stat_data))

        session.commit()
        logger.info(f"Successfully loaded Pokémon {pokemon_id}")
        return True

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error for Pokémon {pokemon_id}: {e}")
        return False

    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error for Pokémon {pokemon_id}: {e}")
        return False

    finally:
        if own_session:
            session.close()

def load_transformation(transformed_data):
    """Load transformed data into the database"""
    if not transformed_data or transformed_data.get('pokemon') is None:
        logger.warning("No valid transformed data to load.")
        return False

    session = create_database_session()

    try:
        pokemon_data = transformed_data["pokemon"]
        
        pokemon_id = pokemon_data.get('pokemon_id')
        if pokemon_id is None:
            logger.error("Attempted to load Pokémon with missing pokemon_id.")
            return False

        pokemon = Pokemon(**pokemon_data)
        session.merge(pokemon)

        for type_data in transformed_data.get('types', []):
            type_name = type_data.get('type_name')
            if not type_name:
                logger.warning(f"Skipping type association for Pokémon {pokemon_id} due to missing type name.")
                continue

            type_record = session.query(Type).filter_by(type_name=type_name).first()
            if not type_record:
                type_record = Type(type_name=type_name)
                session.add(type_record)
                session.flush()

            association = PokemonType(
                pokemon_id=pokemon_id, type_id=type_record.type_id
            )
            session.merge(association)

        for ability_data in transformed_data.get('abilities', []):
            ability_name = ability_data.get('ability_name')
            if not ability_name:
                logger.warning(f"Skipping ability association for Pokémon {pokemon_id} due to missing ability name.")
                continue

            ability_record = (
                session.query(Ability).filter_by(ability_name=ability_name).first()
            )
            if not ability_record:
                ability_record = Ability(ability_name=ability_name)
                session.add(ability_record)
                session.flush()

            association = PokemonAbility(
                pokemon_id=pokemon_id, ability_id=ability_record.ability_id
            )
            session.merge(association)

        for stat_data in transformed_data.get('stats', []):
            if stat_data.get('stat_name') is None or stat_data.get('base_stat') is None:
                logger.warning(f"Skipping malformed stat entry for Pokémon {pokemon_id}: {stat_data}")
                continue

            stat_data['pokemon_id'] = pokemon_id
            stat = PokemonStat(**stat_data)
            session.merge(stat)

        session.commit()
        logger.info(
            f"Successfully loaded data for Pokémon ID: {pokemon_id}"
        )
        return True

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error occurred during load for Pokémon ID {pokemon_id}: {e}")
        return False
    except Exception as e:
        session.rollback()
        logger.error(f"An unexpected error occurred during load for Pokémon ID {pokemon_id}: {e}")
        return False
    finally:
        session.close()

