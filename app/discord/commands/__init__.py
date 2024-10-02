from app.discord.objects import Command

from app.discord.commands.test import Ping
from typing import List

all: List[Command] = list()
all.append(Ping())
