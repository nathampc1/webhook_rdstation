from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TARGET_URL: str
    DEBUG: bool = False

    class Config:
        env_file = "var.env" 
        env_file_encoding = 'utf-8'
        extra = 'allow'

class LastConversion(BaseModel):
    content: Optional[Dict[str, Any]] = None 
    class Config:
        extra = "allow"

class Lead(BaseModel):
    name: str
    personal_phone: Optional[str] = None
    last_conversion: LastConversion
    
    custom_fields: Optional[Dict[str, Any]] = None 

    class Config:
        extra = "allow"

class RDStationWebhook(BaseModel):
    leads: List[Lead]
    class Config:
        extra = "allow"

class NewRequestData(BaseModel):
    nome: str
    telefone: str
    produto_interesse: str