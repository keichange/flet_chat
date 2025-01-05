import flet as ft
import os
import asyncio
from dotenv import load_dotenv

from models.message import Message
from services.ai_chat_service import AiSrevice
from components.chat_message import ChatMessage
from config import Config

load_dotenv()
config = Config()


async def main(page: ft.Page):
    GOOGLE_API_KEY=os.environ['API_KEY']
    ai_service = AiSrevice(GOOGLE_API_KEY, 'gemini-1.5-flash')
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
        if not new_text.value.strip() or page.session.get("is_loading"):
            return
        if len(new_text.value) > config.max_message_length:
            page.pubsub.send_all(
                Message("System",
                        text="The text is too long. Please keep each message under 1000 characters.",
                        message_type="error_message"
                        )
                        )
            return
        page.pubsub.send_all(Message(user=user_name.value, text=new_text.value, message_type="chat_message"))
        ai_task = asyncio.create_task(get_ai_response(new_text.value))
        new_text.value = ""
        page.update()

    async def get_ai_response(message_to_ai):
        try:
            progress_start()
            response = await ai_service.send_message(message_to_ai)
            progress_end()

            if response:
                page.pubsub.send_all(response)

        except Exception as e:
            progress_end()
            page.pubsub.send_all(Message(
                user="System",
                text=f"Error getting AI response: {str(e)}",
                message_type="error_message"
            ))

    def progress_start():
        page.session.set("is_loading", True)
        update_loading_state()
    
    def progress_end():
        page.session.set("is_loading", False)
        update_loading_state()

    def update_loading_state():
        is_loading = page.session.get("is_loading")
        send_button.visible = not is_loading
        progress_ring.visible = is_loading
        page.update()

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

    send_button = ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_text,
                    visible=True)
    
    progress_ring = ft.ProgressRing(
                    visible=False
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
                send_button,
                progress_ring])
    )
    page.title = config.app_title
    page.update()

ft.app(main)
