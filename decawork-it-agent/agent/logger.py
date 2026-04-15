from datetime import datetime

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def _ts():
    return datetime.now().strftime("%H:%M:%S")

def log_info(msg: str):
    print(f"{BLUE}[{_ts()}] INFO  {RESET}{msg}")

def log_success(msg: str):
    print(f"{GREEN}[{_ts()}] OK    {RESET}{msg}")

def log_error(msg: str):
    print(f"{RED}[{_ts()}] ERROR {RESET}{msg}")

def log_warn(msg: str):
    print(f"{YELLOW}[{_ts()}] WARN  {RESET}{msg}")