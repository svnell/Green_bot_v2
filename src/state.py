from dataclasses import dataclass, field
import asyncio
import httpx
from typing import Dict, Any


@dataclass
class ChatState:
    statuses: Dict[str, bool] = field(default_factory=dict)
    await_dump_date: bool = False


@dataclass
class Tracking:
    day: str
    data: Dict[str, Dict[str, Any]]
    rollover_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    last_exported_day: str | None = None


@dataclass
class BotState:
    client: httpx.AsyncClient | None = None
    tasks: Dict[int, Dict[str, Any]] = field(default_factory=dict)       # chat_id -> {"task": Task, "stop": Event}
    chat_states: Dict[int, ChatState] = field(default_factory=dict)      # chat_id -> ChatState
    tracking: Tracking | None = None


def get_chat_state(bot_state: BotState, chat_id: int) -> ChatState:
    return bot_state.chat_states.setdefault(chat_id, ChatState())
