from AntonIA.common.logger_setup import setup_logging
from AntonIA.services.llm_client import OpenAIClient, MockAIClient
from AntonIA.services.storage_client import LocalStorageClient
from AntonIA.services.image_generation_client import ImageGenerationClient
from AntonIA.core import image_saver, prompt_generator, image_generator


def main():
    logger = setup_logging()
    llm_client = OpenAIClient(
        system_prompt="""
            You are a grandma obsessed with good-morning images. 
            Since you discovered AI image generators, you have mastered the 
            art of creating good morning images with it, becoming a master 
            of AI image generation prompting.
            """
    )
    image_generator_client = ImageGenerationClient(model="gpt-image-1")
    storage_client = LocalStorageClient(base_dir="./outputs/images")

    prompt_for_image_generation, response_details = prompt_generator.generate(llm_client)
    image_bytes = image_generator.generate(image_generator_client, prompt_for_image_generation, size="1024x1024")
    saved_image_path = image_saver.save(image_bytes, storage_client)

    

if __name__ == "__main__":
    main()