import logging
import os
from datetime import datetime, timezone, UTC
from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('incidentflow')

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    severity: str = Field(pattern='^(low|medium|high)$')

class Incident(IncidentCreate):
    id: int
    status: str
    created_at: datetime

store: dict[int, Incident] = {}
ids = count(1)
lock = Lock()

app = FastAPI(title='IncidentFlow', version='1.0.0')

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'incidentflow', 'environment': os.getenv('APP_ENV', 'development')}

@app.get('/incidents', response_model=list[Incident])
def list_incidents():
    with lock:
        return list(store.values())

@app.post('/incidents', response_model=Incident, status_code=201)
def create_incident(payload: IncidentCreate):
    with lock:
        item = Incident(id=next(ids), title=payload.title, severity=payload.severity,
                        status='open', created_at=datetime.now(UTC))
        store[item.id] = item
    logger.info('incident_created id=%s severity=%s', item.id, item.severity)
    return item

@app.patch('/incidents/{incident_id}/resolve', response_model=Incident)
def resolve_incident(incident_id: int):
    with lock:
        item = store.get(incident_id)
        if item is None:
            raise HTTPException(status_code=404, detail='Incident not found')
        updated = item.model_copy(update={'status': 'resolved'})
        store[incident_id] = updated
    logger.info('incident_resolved id=%s', incident_id)
    return updated
