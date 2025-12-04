import requests
import models
from fastapi import HTTPException
import logging
from typing import Optional
import re

CAMPO_SOLUCAO_DESEJADA = "[LM] [F] Solução desejada"

def padronizar_telefone(numero: Optional[str]) -> str:
    if not numero:
        return "Não Informado"
    
    limpo = re.sub(r'\D', '', numero)
    
    if 8 <= len(limpo) <= 11:
        if not limpo.startswith('55'):
            return f"+55{limpo}"
        else:
            return f"+{limpo}"

    return "Não Informado"

async def webhook_processor(data: models.RDStationWebhook, TARGET_URL: str, logger: logging.Logger):
    
    logger.info("Webhook recebido. Processando leads...")

    if not data.leads:
        logger.warning("Nenhuma informação de lead encontrada no corpo da requisição.")
        raise HTTPException(status_code=400, detail="Corpo da requisição inválido: Nenhuma informação de lead encontrada.")

    lead = data.leads[0]
    
    nome_lead = lead.name
    
    telefone_bruto = lead.personal_phone
    telefone_padronizado = padronizar_telefone(telefone_bruto)
    
    if lead.custom_fields and lead.custom_fields.get(CAMPO_SOLUCAO_DESEJADA):
        produto_interesse_lead = lead.custom_fields.get(CAMPO_SOLUCAO_DESEJADA)
    else:
        produto_interesse_lead = "Não Informado"

    payload_to_send = models.NewRequestData(
        nome=nome_lead,
        telefone=telefone_padronizado,
        produto_interesse=produto_interesse_lead
    )
    
    json_payload = payload_to_send.model_dump_json(indent=2)
    
    logger.info(f"Payload simplificado preparado para envio: {json_payload}")

    try:
        response = requests.post(
            TARGET_URL, 
            data=json_payload,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            timeout=10
        )
        
        response.raise_for_status() 
        
        logger.info(f"Dados enviados com sucesso para {TARGET_URL}. Status: {response.status_code}")
        
        return payload_to_send
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Falha ao enviar dados para {TARGET_URL}: {e}")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Falha na comunicação com o destino: {e}"
        )