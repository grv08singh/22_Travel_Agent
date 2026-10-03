import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field, SecretStr
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

class ConfigLoader:
    def __init__(self) -> None:
        print('Loaded Config...')
        self.config = load_config()
        
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai", "google"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)
    
    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        assert self.config is not None
        print('LLM Loading...')
        print(f'Loading Model from provider: {self.model_provider}')
        
        if self.model_provider == 'groq':
            groq_api_key = SecretStr(os.getenv("GROQ_API_KEY") or "")
            model_name = self.config['llm']['groq']['model_name']
            llm = ChatGroq(api_key=groq_api_key, model=model_name)
        elif self.model_provider == 'openai':
            openai_api_key = SecretStr(os.getenv("OPENAI_API_KEY") or "")
            model_name = self.config['llm']['openai']['model_name']
            llm = ChatOpenAI(api_key=openai_api_key, model=model_name)
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
        return llm