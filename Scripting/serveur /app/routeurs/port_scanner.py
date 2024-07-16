from fastapi import APIRouter
from subprocess import run, PIPE
from app.dependencies import dns_check, is_blacklisted
from app.models import PortScanRequest

router = APIRouter()

def parse_nmap_output(nmap_output):
    open_ports = {}
    for line in nmap_output.splitlines():
        if 'open' in line:
            parts = line.split()
            open_ports[parts[0]] = {'state': 'open', 'service': parts[2] if len(parts) > 2 else 'unknown' }
    return open_ports

@router.post("/scan_ports/")
async def scan_ports(request: PortScanRequest):
    if is_blacklisted(request.domain):
       return {"error": "The domain is blacklisted"}
    if not dns_check(request.domain):
        return {"error": "Invalid domain"}
    args = ["nmap", "-sT", "-p80-443", "-Pn", request.domain]
    result = run(args, stdout=PIPE, stderr=PIPE, text=True)

    if result.returncode != 0:
        return {"error": result.stderr}
    open_ports = parse_nmap_output(result.stdout)

    return {"open_ports": open_ports }
