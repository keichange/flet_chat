import flet as ft
from models.message import Message

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment=ft.CrossAxisAlignment.START
        self.controls=[
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user)),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message.user),
            ),
            ft.Column(
                [
                    ft.Text(message.user, weight="bold"),
                    ft.Markdown(
                        message.text,
                        code_style_sheet=ft.MarkdownStyleSheet.codeblock_alignment,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        ),
                ],
                tight=True,
                spacing=5
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()
    
    def get_avatar_color(self, user_name: str):
        colors_lookup = [
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
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
