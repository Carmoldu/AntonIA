import os
from dataclasses import dataclass
from dotenv import load_dotenv



@dataclass
class Config:
    openai_api_key: str = ''
    model_name: str = "gpt-4"

    def __post_init__(self):
        load_dotenv()  # Load environment variables from a .env file
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment.")
        
config = Config()
