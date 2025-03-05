import asyncio
import flet as ft
from pyodide.ffi import to_js

class Message():
    def __init__(self, user: str, text: str, message_type: str):
        self.user = user
        self.text = text
        self.message_type = message_type

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
                    ft.Text(message.text, selectable=True),
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

def main(page: ft.Page):
    # Pyodideのイベントループを設定
    loop = asyncio.get_event_loop()
    page.pubsub.loop = to_js(loop)

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.Colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    def send_text(e):
        page.pubsub.send_all(Message(user=user_name.value, text=new_text.value, message_type="chat_message"))
        new_text.value = ""
        page.update()   

    def join_click(e):
        if not user_name.value:
            user_name.error_text = "Name cannot be blank!"
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            join_dialog.open = False
            page.pubsub.send_all(
                Message(
                    user=user_name.value, 
                    text=f"{user_name.value} has joined the chat.", 
                    message_type="login_message")
            )
            page.update()
        print(join_dialog.open)
        
    user_name = ft.TextField(label="Enter your name", autofocus=True, on_submit=join_click)
      
    join_dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_click)],
        actions_alignment="end"
    )

    page.overlay.append(join_dialog)
    new_text = ft.TextField(shift_enter=True, on_submit=send_text)
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_text,
                ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_text)])
    )

    page.title = "Flet Chat"
    page.update()

ft.app(main)
