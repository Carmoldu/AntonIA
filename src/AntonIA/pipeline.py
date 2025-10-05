from AntonIA.common.logger_setup import setup_logging
from AntonIA.services.llm_client import OpenAIClient, MockAIClient
from AntonIA.core import phrase_generator


def main():
    logger = setup_logging()
    llm_client = MockAIClient()
    phrase = phrase_generator.generate(llm_client)
    

if __name__ == "__main__":
    main()