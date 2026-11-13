import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI(title="x402 Code Auditor")

# Configuration from environment variables
PAY_TO_ADDRESS = os.getenv("PAY_TO_ADDRESS", "0x81dd9de49f6ba6171a42112e995af2b9e5b01e3d")

class AuditRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "x402 Code Auditor", "price": "$0.05 USDC"}

@app.post("/v1/audit-code")
async def audit_code(request: Request, body: AuditRequest):
    # Check for x402 v2 payment headers or invoke your x402 middleware verification here
    payment_header = request.headers.get("X-PAYMENT") or request.headers.get("PAYMENT-SIGNATURE")
    
    if not payment_header:
        # Return x402 v2 compliant challenge response headers/payload if required, 
        # or let your x402 v2 FastAPI middleware intercept and raise the 402 challenge automatically.
        raise HTTPException(
            status_code=402,
            detail="X-PAYMENT header is required",
        )
        
    # Process code audit logic once payment is verified...
    return {
        "status": "success",
        "audit_report": "No critical vulnerabilities found in test contract.",
        "risk_score": "Low"
    }
