import os
from datetime import datetime

import torch.distributed as dist
from cprint import cprint


def dprint(text):
    pid = os.getpid()
    now = datetime.now().strftime("%m-%d %I:%M:%S:%f %p")
    rank = dist.get_rank() if dist.is_available() and dist.is_initialized() else -1
    cprint(rank, f"[{rank}]({pid}){now} - {text}")
