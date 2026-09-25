from typing import List
from sqlalchemy.orm import Session
from app.models import Lead, Deal, Client, Audit, DeliveryPlan, Ticket
from app.agents import LeadHunterAgent, OutreachAgent, AuditAgent, DeliveryAgent, CEOAgent

class Workflow:
    def __init__(self, db: Session):
        self.db = db
        self.lead_agent = LeadHunterAgent()
        self.outreach_agent = OutreachAgent()
        self.audit_agent = AuditAgent()
        self.delivery_agent = DeliveryAgent()
        self.ceo_agent = CEOAgent()
    
    def generate_leads(self, city: str, category: str, limit: int = 10):
        """Generate and store leads"""
        leads_data = self.lead_agent.generate_leads(city, category, limit)
        created_leads = []
        
        for lead_data in leads_data:
            lead = Lead(
                business_name=lead_data["business_name"],
                city=lead_data["city"],
                category=lead_data["category"],
                website=lead_data.get("website"),
                phone=lead_data.get("phone"),
                email=lead_data.get("email"),
                rating=lead_data.get("rating", 0.0),
                score=lead_data.get("score", 0.0),
                notes=lead_data.get("notes", "")
            )
            self.db.add(lead)
            created_leads.append(lead)
        
        self.db.commit()
        return created_leads
    
    def approve_leads(self, lead_ids: List[int]):
        """Approve leads for outreach"""
        for lead_id in lead_ids:
            lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
            if lead:
                lead.status = "approved"
        self.db.commit()
    
    def create_deal(self, lead_id: int, price: float) -> Deal:
        """Create a deal for a lead"""
        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError("Lead not found")
        
        deal = Deal(lead_id=lead.id, price=price, status="negotiating")
        self.db.add(deal)
        lead.status = "deal_created"
        self.db.commit()
        return deal
    
    def approve_deal(self, deal_id: int) -> Client:
        """Approve a deal and create client"""
        deal = self.db.query(Deal).filter(Deal.id == deal_id).first()
        if not deal:
            raise ValueError("Deal not found")
        
        deal.owner_approved = True
        client = Client(
            deal_id=deal.id,
            business_name=deal.lead.business_name,
            city=deal.lead.city,
            contact_email=deal.lead.email
        )
        self.db.add(client)
        self.db.commit()
        return client
    
    def create_audit(self, client_id: int) -> Audit:
        """Create growth audit for client"""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError("Client not found")
        
        audit_data = self.audit_agent.create_audit(client.business_name, client.city)
        audit = Audit(
            client_id=client.id,
            title=audit_data["title"],
            content=audit_data["content"]
        )
        self.db.add(audit)
        self.db.commit()
        return audit
    
    def approve_audit(self, audit_id: int) -> Audit:
        """Approve audit for delivery"""
        audit = self.db.query(Audit).filter(Audit.id == audit_id).first()
        if not audit:
            raise ValueError("Audit not found")
        
        audit.owner_approved = True
        self.db.commit()
        return audit
    
    def create_delivery(self, client_id: int) -> DeliveryPlan:
        """Create delivery plan"""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError("Client not found")
        
        plan_data = self.delivery_agent.create_delivery_plan(client.business_name)
        plan = DeliveryPlan(
            client_id=client.id,
            title=plan_data["title"],
            content=plan_data["content"]
        )
        self.db.add(plan)
        self.db.commit()
        return plan
    
    def approve_delivery(self, plan_id: int) -> DeliveryPlan:
        """Approve delivery plan"""
        plan = self.db.query(DeliveryPlan).filter(DeliveryPlan.id == plan_id).first()
        if not plan:
            raise ValueError("Plan not found")
        
        plan.owner_approved = True
        self.db.commit()
        return plan
    
    def create_ticket(self, client_id: int, title: str, description: str) -> Ticket:
        """Create support ticket"""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError("Client not found")
        
        ticket = Ticket(
            client_id=client.id,
            title=title,
            description=description
        )
        self.db.add(ticket)
        self.db.commit()
        return ticket
    
    def get_ceo_summary(self):
        """Get CEO summary"""
        leads = self.db.query(Lead).count()
        deals = self.db.query(Deal).count()
        audits = self.db.query(Audit).count()
        tickets = self.db.query(Ticket).count()
        
        return self.ceo_agent.get_summary(leads, deals, audits, tickets)
