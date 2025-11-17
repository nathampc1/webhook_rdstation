from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    TARGET_URL: str

    class Config:

        env_file = "var.env" 
        env_file_encoding = 'utf-8'

class ConversionContent(BaseModel):
    solucao_desejada: Optional[str] = Field(None, alias="[LM] [F] Solução desejada")
    
class Config:
    populate_by_name = True
    extra = "allow"        

class LastConversion(BaseModel):
    content: ConversionContent
    class Config:
        extra = "allow"

class Lead(BaseModel):
    name: str
    personal_phone: Optional[str] = None
    last_conversion: LastConversion

class Config:
        extra = "allow"

class RDStationWebhook(BaseModel):
    leads: List[Lead]

class NewRequestData(BaseModel):
    nome: str
    telefone: str
    produto_interesse: str