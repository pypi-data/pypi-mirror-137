from pydantic import BaseModel

class Logger(BaseModel):
    level: str = 'INFO'
    retention: str = '7 days'
    compression: str = 'zip'
    rotation: str = '00:00'
    log_path: str = "/var/log"

