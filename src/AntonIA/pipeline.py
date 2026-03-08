from dotenv import load_dotenv
load_dotenv()   # IMPORTANT: load .env at the very beginning so env vars are available for config loading

import truststore
truststore.inject_into_ssl()

import hydra

from AntonIA.common.logger_setup import setup_logging
from AntonIA.common.config import Config

from AntonIA.services import factory

from AntonIA.core import (
    image_saver,
    prompt_generator,
    image_generator,
    instagram_caption_generator,
    run_info_saver,
    retrieve_past_records,
)
from AntonIA.utils.image_utils import add_watermark_fn_factory
from AntonIA.utils.prompts import build_prompt_from_template



def run(cfg: Config):
    """Core pipeline logic; takes a config object (Hydra DictConfig or dataclass).
    Tests can call this directly, and the Hydra entrypoint will pass its config.
    """
    logger = setup_logging()

    # Set up clients via configuration-driven factory
    system_prompt = build_prompt_from_template(
        cfg.grandma.prompts.system,
        {"language": cfg.grandma.language},
    )

    llm_client_1 = factory.create_llm_client(cfg.llm, system_prompt=system_prompt)
    llm_client_2 = llm_client_1  # reuse for simplicity

    image_generator_client = factory.create_image_client(cfg.image)
    storage_client = factory.create_storage_client(cfg.storage)
    database_client = factory.create_database_client(cfg.database)


    # Pipeline execution
    past_records = retrieve_past_records.retrieve_past_n_days(
        database_client=database_client, 
        table=cfg.grandma.runs_table_name, 
        n_days=cfg.past_records_to_retrieve
        )

    prompt_for_image_generation, response_details = prompt_generator.generate(
        llm_client=llm_client_1, 
        prompt_generateion_template=cfg.grandma.prompts.creation_template,
        image_prompt_template=cfg.grandma.prompts.image_template,
        past_records=past_records, 
        temperature=cfg.grandma.temperature_for_image_prompt_generation,
        language=cfg.grandma.language,
        )
    
    caption = instagram_caption_generator.generate(
        llm_client_2, 
        template=cfg.grandma.prompts.instagram_caption_template,
        phrase=response_details["phrase"], 
        topic=response_details["topic"], 
        style=response_details["style"], 
        temperature=cfg.grandma.temperature_for_caption_generation,
        language=cfg.grandma.language,
        hashtags=cfg.grandma.hashtags,
    )

    image_bytes = image_generator.generate(
        image_generator_client, 
        prompt_for_image_generation, 
        size=cfg.image.size, 
        postprocess_fn=add_watermark_fn_factory(
            cfg.grandma.watermark_path, 
            opacity=0.8, 
            scale=0.2,
            ),
        )
    
    saved_image_path = image_saver.save(image_bytes, storage_client)

    run_info = run_info_saver.RunInfo.from_generation_details(
        prompt=prompt_for_image_generation,
        response_details=response_details,
        caption=caption,
        image_path=saved_image_path,
    )

    run_info_saver.save(
        database_client, 
        cfg.grandma.runs_table_name, 
        run_info,
        )


@hydra.main(config_path="../../config", config_name="config", version_base=None)
def main(cfg: Config):
    run(cfg)


if __name__ == "__main__":
    main()