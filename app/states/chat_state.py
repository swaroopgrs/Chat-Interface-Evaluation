import reflex as rx
import asyncio
import datetime


class Message(rx.Base):
    role: str
    content: str
    created_at: str


class ChatState(rx.State):
    messages: list[Message] = []

    @rx.event
    async def send_message(self, form_data: dict):
        message_content = form_data.get("message", "").strip()
        if not message_content:
            return
        current_time = datetime.datetime.now().strftime("%H:%M")
        user_msg = Message(
            role="user", content=message_content, created_at=current_time
        )
        self.messages.append(user_msg)
        yield rx.call_script(
            "var el = document.getElementById('chat-scroll-area'); if(el) el.scrollTop = el.scrollHeight;"
        )
        yield
        await asyncio.sleep(0.8)
        bot_time = datetime.datetime.now().strftime("%H:%M")
        bot_msg = Message(
            role="assistant",
            content=f"I received your message: '{user_msg.content}'. This is a simulated response from the ChatState.",
            created_at=bot_time,
        )
        self.messages.append(bot_msg)
        from app.states.evaluation_state import EvaluationState

        eval_state = await self.get_state(EvaluationState)
        transcript = [
            {"role": m.role, "content": m.content, "created_at": m.created_at}
            for m in self.messages
        ]
        eval_state.add_run_from_chat(transcript, model="gpt-3.5-turbo-sim")
        yield rx.call_script(
            "var el = document.getElementById('chat-scroll-area'); if(el) el.scrollTop = el.scrollHeight;"
        )

    @rx.event
    def clear_chat(self):
        self.messages = []