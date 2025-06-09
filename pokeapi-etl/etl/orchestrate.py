from etl.extract.extractor import extract_pokemon_range
from etl.transform.transformer import transform_pokemon_data
from etl.load.loader import load_transformed_data
from utils.database import create_database_session, get_database_engine, create_tables
from utils.logging_config import setup_logging
from utils.config import Config
import logging

logger = setup_logging(__name__)


def run_etl_pipeline(start_id=1, end_id=20):
    """Main ETL orchestration function"""
    logger.info("Starting ETL pipeline...")

    try:
        create_tables()
        logger.info("Database tables ensured.")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        return False
    
    # Extract data
    logger.info(f"Extracting data for Pokémon IDs {start_id} to {end_id}")
    raw_data_list = extract_pokemon_range(start_id, end_id)

    if not raw_data_list:
        logger.error("No data extracted. Exiting pipeline.")
        return False

    success_count = 0
    total_to_process = len(raw_data_list)
    for i, raw_data in enumerate(raw_data_list):
        pokemon_id_for_log = raw_data.get("pokemon", {}).get("id", "N/A")
        logger.info(
            f"Processing Pokémon ID {pokemon_id_for_log} ({i+1}/{total_to_process})"
        )

        # Transform data
        transformed_data = transform_pokemon_data(raw_data)

        if not transformed_data or transformed_data.get("pokemon") is None:
            logger.warning(
                f"Skipping transformation or loading for Pokémon ID {pokemon_id_for_log} due to invalid transformed data."
            )
            continue

        # Load data
        if load_transformed_data(transformed_data):
            success_count += 1
        else:
            logger.error(f"Failed to load data for Pokémon ID: {pokemon_id_for_log}")

    logger.info(
        f"ETL pipeline completed. Successfully processed {success_count}/{total_to_process} Pokémon."
    )
    return success_count > 0


if __name__ == "__main__":
    run_etl_pipeline(start_id=1, end_id=Config.API_RETRIES * 5)

