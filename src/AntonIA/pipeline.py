from AntonIA.common.logger_setup import setup_logging
from AntonIA.services.llm_client import OpenAIClient, MockAIClient
from AntonIA.core import prompt_generator, image_generator


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
    prompt_for_image_generation, response_details = prompt_generator.generate(llm_client)
    image_path = image_generator.generate(prompt_for_image_generation, size="1024x1024")

    

if __name__ == "__main__":
    main()