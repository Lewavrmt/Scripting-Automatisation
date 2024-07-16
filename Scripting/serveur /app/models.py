from pydantic import BaseModel

class DomainRequest(BaseModel):
    domain: str

class ScreenshotRequest(BaseModel):
    url: str

class PortScanRequest(BaseModel):
    domain: str
