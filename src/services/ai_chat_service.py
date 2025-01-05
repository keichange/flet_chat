import google.generativeai as genai
import asyncio

from models.message import Message, MessageType



class AiSrevice:
    def __init__(
            self,
            api_key: str,
            model: str,
            ):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model)
            self.ai_chat = model.start_chat(history=[])

    async def send_message(self,message_to_ai):
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, self._get_ai_response, message_to_ai)
            if response and response.text:
                return Message(user="AI", text=response.text, message_type=MessageType.CHAT_MESSAGE)
            else:
                return Message(
                    user="System",
                    text="AI response was empty",
                    message_type=MessageType.ERROR_MESSAGE
                )
            
        except Exception as e:
            return Message(
                user="System",
                text=f"Error getting AI response: {str(e)}",
                message_type=MessageType.ERROR_MESSAGE
            )
    
    def _get_ai_response(self, message_to_ai):
         return self.ai_chat.send_message(message_to_ai)