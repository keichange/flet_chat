import flet as ft
import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

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

async def main(page: ft.Page):

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.Colors.BLACK45, size=12)
        elif message.message_type == "error_message":
            m = ft.Text(message.text, color=ft.Colors.ERROR)
        chat.controls.append(m)
        page.update()

    async def send_text(e):
        if not new_text.value.strip():
            return
        page.pubsub.send_all(Message(user=user_name.value, text=new_text.value, message_type="chat_message"))
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, ai_response, new_text.value)
        new_text.value = ""
        page.update()
    
    def ai_response(message_to_ai):
        try:
            response = ai_chat.send_message(message_to_ai)
            if response and response.text:
                page.pubsub.send_all(Message(user="AI", text=response.text, message_type="chat_message"))
            else:
                page.pubsub.send_all(Message(
                    user="System",
                    text="AI response was empty",
                    message_type="error_message"
                ))
        except Exception as e:
            page.pubsub.send_all(Message(
                user="System",
                text=f"Error getting AI response: {str(e)}",
                message_type="error_message"
            ))

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

    # AIの初期化
    GOOGLE_API_KEY=os.environ['API_KEY']
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    ai_chat = model.start_chat(history=[])

    # pubsubでイベントが発行されるとon_messageが呼ばれる
    page.pubsub.subscribe(on_message)
        
    # --- 入室時のダイアログ ---
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
    # ------

    # メインのチャットページ
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
