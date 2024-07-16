from fastapi import APIRouter, HTTPException
import requests
import socket
from app.models import DomainRequest

router = APIRouter()

@router.post("/get_provider/")
async def get_hosting_provider(request: DomainRequest):
    try:
        ip = socket.gethostbyname(request.domain)
        url = f"https://ipinfo.io/{ip}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching hosting provider info")
        data = response.json()
        provider_info = data.get('org', '')
        provider = " ".join(provider_info.split(' ')[1:] if ' ' in provider_info else ["Unknown Provider"])
        return {"provider": provider}
    except socket.gaierror:
        raise HTTPException(status_code=404, detail="Domain not found")
