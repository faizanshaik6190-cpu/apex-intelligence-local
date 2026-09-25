from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.workflow import Workflow
from app.models import Lead, Deal, Client, Audit, DeliveryPlan, Ticket

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Apex Intelligence",
    description="AI-Powered Growth Agency",
    version="1.0.0"
)

# Request models
class LeadGenerateRequest(BaseModel):
    city: str
    category: str
    limit: int = 10

class ApproveLeadsRequest(BaseModel):
    lead_ids: List[int]

class CreateDealRequest(BaseModel):
    lead_id: int
    price: float

class CreateTicketRequest(BaseModel):
    client_id: int
    title: str
    description: str

# Routes
@app.get("/")
def root():
    return {
        "message": "Apex Intelligence is running",
        "status": "operational",
        "docs": "http://localhost:8000/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/leads/generate")
def generate_leads(payload: LeadGenerateRequest, db: Session = Depends(get_db)):
    workflow = Workflow(db)
    leads = workflow.generate_leads(payload.city, payload.category, payload.limit)
    return {
        "message": "Leads generated",
        "count": len(leads),
        "leads": [{"id": l.id, "business_name": l.business_name, "score": l.score} for l in leads]
    }

@app.post("/leads/approve")
def approve_leads(payload: ApproveLeadsRequest, db: Session = Depends(get_db)):
    workflow = Workflow(db)
    workflow.approve_leads(payload.lead_ids)
    return {"message": "Leads approved", "count": len(payload.lead_ids)}

@app.get("/leads")
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    return {
        "count": len(leads),
        "leads": [{"id": l.id, "business_name": l.business_name, "city": l.city, "status": l.status} for l in leads]
    }

@app.post("/deals/create")
def create_deal(payload: CreateDealRequest, db: Session = Depends(get_db)):
    try:
        workflow = Workflow(db)
        deal = workflow.create_deal(payload.lead_id, payload.price)
        return {"message": "Deal created", "deal_id": deal.id, "price": deal.price}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/deals/approve")
def approve_deal(deal_id: int, db: Session = Depends(get_db)):
    try:
        workflow = Workflow(db)
        client = workflow.approve_deal(deal_id)
        return {"message": "Deal approved", "client_id": client.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/deals")
def list_deals(db: Session = Depends(get_db)):
    deals = db.query(Deal).all()
    return {
        "count": len(deals),
        "deals": [{"id": d.id, "price": d.price, "status": d.status} for d in deals]
    }

@app.get("/clients")
def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return {
        "count": len(clients),
        "clients": [{"id": c.id, "business_name": c.business_name} for c in clients]
    }

@app.post("/audits/create")
def create_audit(client_id: int, db: Session = Depends(get_db)):
    try:
        workflow = Workflow(db)
        audit = workflow.create_audit(client_id)
        return {"message": "Audit created", "audit_id": audit.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/audits/approve")
def approve_audit(audit_id: int, db: Session = Depends(get_db)):
    try:
        workflow = Workflow(db)
        audit = workflow.approve_audit(audit_id)
        return {"message": "Audit approved", "audit_id": audit.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/audits")
def list_audits(db: Session = Depends(get_db)):
    audits = db.query(Audit).all()
    return {
        "count": len(audits),
        "audits": [{"id": a.id, "title": a.title, "approved": a.owner_approved} for a in audits]
    }

@app.post("/delivery/create")
def create_delivery(client_id: int, db: Session = Depends(get_db)):
    try:
        workflow = Workflow(db)
        plan = workflow.create_delivery(client_id)
        return {"message": "Delivery plan created", "plan_id": plan.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/delivery/approve")
def approve_delivery(plan_id: int, db: Session = Depends(get_db)):
    try:
        workflow = Workflow(db)
        plan = workflow.approve_delivery(plan_id)
        return {"message": "Delivery approved", "plan_id": plan.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/tickets/create")
def create_ticket(payload: CreateTicketRequest, db: Session = Depends(get_db)):
    try:
        workflow = Workflow(db)
        ticket = workflow.create_ticket(payload.client_id, payload.title, payload.description)
        return {"message": "Ticket created", "ticket_id": ticket.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/ceo/summary")
def ceo_summary(db: Session = Depends(get_db)):
    workflow = Workflow(db)
    return workflow.get_ceo_summary()
