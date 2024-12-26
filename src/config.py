from dataclasses import dataclass, field
from typing import List
import flet as ft

@dataclass
class Config:
    app_title: str = "Flet Chat"
    max_message_length: int = 1000
    avatar_colors: List[str] = field(default_factory=lambda: [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ])