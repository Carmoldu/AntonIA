from AntonIA.common.logger_setup import setup_logging
from AntonIA.common.config import config
from AntonIA.services import (
    OpenAIClient, MockAIClient,
    LocalStorageClient, MockStorageClient,
    OpenAIimageGenerationClient, MockImageGenerationClient,
    LocalFileDatabaseClient, MockDatabaseClient,
)
from AntonIA.core import (
    image_saver,
    prompt_generator,
    image_generator,
    instagram_caption_generator,
    run_info_saver,
    retrieve_past_records,
)
from AntonIA.utils.image_utils import add_watermark_fn_factory

def main():
    logger = setup_logging()

    # Set up clients
    llm_client_1 = OpenAIClient(
        system_prompt="""
            You are a grandma obsessed with good-morning images. 
            Since you discovered AI image generators, you have mastered the 
            art of creating good morning images with it, becoming a master 
            of AI image generation prompting.
            """
    )
    llm_client_2 = llm_client_1  # Using the same LLM client for both tasks, set up like this for easy swapping with MockAIClient
    image_generator_client = OpenAIimageGenerationClient(model="gpt-image-1")
    storage_client = LocalStorageClient(base_dir="./outputs/images")
    database_client = LocalFileDatabaseClient(db_path="./outputs/database")

    # llm_client_1 = MockAIClient(response='{"phrase": "Good Morning", "topic": "Nice sunset", "style": "Aquarela", "font": "Comic Sans"}')
    # llm_client_2 = MockAIClient(response="This is a caption")
    # image_generator_client = MockImageGenerationClient()
    # storage_client = MockStorageClient()
    # database_client = MockDatabaseClient()


    # Pipeline execution
    past_records = retrieve_past_records.retrieve_past_n_days(database_client, "antonIA_runs", n_days=10)

    prompt_for_image_generation, response_details = prompt_generator.generate(llm_client_1, past_records, temperature=0.1)
    
    caption = instagram_caption_generator.generate(
        llm_client_2, 
        phrase=response_details["phrase"], 
        topic=response_details["topic"], 
        style=response_details["style"], 
    )
    image_bytes = image_generator.generate(
        image_generator_client, 
        prompt_for_image_generation, 
        size="1024x1024", 
        postprocess_fn=add_watermark_fn_factory(config.watermark_path, opacity=0.8, scale=0.2)
        )
    saved_image_path = image_saver.save(image_bytes, storage_client)

    run_info = run_info_saver.RunInfo.from_generation_details(
        prompt=prompt_for_image_generation,
        response_details=response_details,
        caption=caption,
        image_path=saved_image_path,
    )

    run_info_saver.save(database_client, "antonIA_runs", run_info)



    

if __name__ == "__main__":
    main()