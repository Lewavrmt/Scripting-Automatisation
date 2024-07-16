from fastapi import APIRouter, HTTPException
from app.dependencies import get_subdomains
from app.models import DomainRequest

router = APIRouter()

@router.post("/scan_subdomains/")
async def scan_subdomains(request: DomainRequest):
    subdomains = get_subdomains(request.domain)
    if not subdomains:
        raise HTTPException(status_code=404, detail="No subdomains found")
    return {"subdomains": list(subdomains)}
