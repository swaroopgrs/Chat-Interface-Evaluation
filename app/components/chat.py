import reflex as rx
from app.states.chat_state import ChatState, Message


def message_bubble(message: Message) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                message.content,
                class_name=rx.cond(
                    message.role == "user",
                    "bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-2",
                    "bg-gray-100 text-gray-800 rounded-2xl rounded-tl-sm px-4 py-2",
                ),
            ),
            rx.el.span(
                message.created_at,
                class_name=rx.cond(
                    message.role == "user",
                    "text-xs text-gray-400 mt-1 mr-1 text-right block",
                    "text-xs text-gray-400 mt-1 ml-1 text-left block",
                ),
            ),
            class_name="max-w-[80%]",
        ),
        class_name=rx.cond(
            message.role == "user",
            "flex justify-end w-full mb-4",
            "flex justify-start w-full mb-4",
        ),
    )


def empty_state() -> rx.Component:
    return rx.el.div(
        rx.icon("message-square", class_name="h-12 w-12 text-gray-300 mb-3"),
        rx.el.h3("No messages yet", class_name="text-lg font-medium text-gray-900"),
        rx.el.p(
            "Start the conversation by typing a message below.",
            class_name="text-sm text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center h-full text-center p-8 opacity-60",
    )


def chat_interface() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("bot", class_name="h-6 w-6 text-blue-600 mr-2"),
                rx.el.h1(
                    "AI Assistant", class_name="text-lg font-semibold text-gray-900"
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4 mr-2"),
                "Clear Chat",
                on_click=ChatState.clear_chat,
                class_name="flex items-center text-sm text-gray-500 hover:text-red-600 transition-colors",
            ),
            class_name="flex items-center justify-between px-6 py-4 border-b bg-white/80 backdrop-blur-md sticky top-0 z-10",
        ),
        rx.el.div(
            rx.cond(
                ChatState.messages.length() > 0,
                rx.el.div(
                    rx.foreach(ChatState.messages, message_bubble),
                    class_name="w-full max-w-3xl mx-auto",
                ),
                empty_state(),
            ),
            id="chat-scroll-area",
            class_name="flex-1 overflow-y-auto p-4 bg-gray-50/50",
        ),
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.input(
                        name="message",
                        placeholder="Type your message...",
                        class_name="flex-1 bg-gray-100 border-0 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all outline-none",
                    ),
                    rx.el.button(
                        rx.icon("send", class_name="h-5 w-5"),
                        type="submit",
                        class_name="bg-blue-600 text-white p-3 rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    class_name="flex gap-3 w-full max-w-3xl mx-auto",
                ),
                on_submit=ChatState.send_message,
                reset_on_submit=True,
                class_name="w-full",
            ),
            class_name="p-4 border-t bg-white",
        ),
        class_name="flex flex-col h-full w-full bg-white",
    )