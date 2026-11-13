import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi_x402 import init_x402, pay

app = FastAPI(title="x402 Code Security Auditor")

# 1. Initialize x402 Payment Gateway (Base Mainnet USDC)
# Reads PAY_TO_ADDRESS, CDP_API_KEY_ID, and CDP_API_KEY_SECRET from environment variables
init_x402(
    app,
    pay_to=os.getenv("PAY_TO_ADDRESS"),
    network="base",
)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.get("/")
async def health_check():
    return {"status": "online", "service": "x402 Code Auditor", "price": "$0.05 USDC"}

# 2. Protected Paid Endpoint ($0.05 USDC per call)
@app.post("/v1/audit-code")
@pay("$0.05")
async def audit_code(payload: dict):
    code_snippet = payload.get("code", "")
    if not code_snippet:
        raise HTTPException(status_code=400, detail="Missing 'code' field in JSON body")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a concise security auditor. List critical vulnerabilities in under 100 words.",
                    },
                    {"role": "user", "content": code_snippet},
                ],
                "max_tokens": 150,
            },
            timeout=15.0,
        )

    if res.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream LLM inference failed")

    audit_report = res.json()["choices"][0]["message"]["content"]

    return {
        "status": "success",
        "paid_usdc": "0.05",
        "audit_report": audit_report,
    }
