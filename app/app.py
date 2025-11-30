import reflex as rx
from app.components.chat import chat_interface
from app.components.evaluation import evaluation_dashboard
from app.components.sidebar import layout
from app.states.evaluation_state import EvaluationState


def index() -> rx.Component:
    return layout(chat_interface())


def evaluations() -> rx.Component:
    return layout(evaluation_dashboard())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(evaluations, route="/evaluations", on_load=EvaluationState.on_load)