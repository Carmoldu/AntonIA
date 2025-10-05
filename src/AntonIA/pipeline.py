from AntonIA.common.logger_setup import setup_logging
from AntonIA.services import (
    OpenAIClient,
    MockAIClient,
    LocalStorageClient,
    ImageGenerationClient,
)
from AntonIA.core import image_saver, prompt_generator, image_generator, instagram_caption_generator


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

    prompt_for_image_generation, response_details = prompt_generator.generate(llm_client, temperature=0.4)
    
    caption = instagram_caption_generator.generate(
        llm_client, 
        phrase=response_details["phrase"], 
        topic=response_details["topic"], 
        style=response_details["style"], 
    )
    image_bytes = image_generator.generate(image_generator_client, prompt_for_image_generation, size="1024x1024")
    saved_image_path = image_saver.save(image_bytes, storage_client)

    

if __name__ == "__main__":
    main()