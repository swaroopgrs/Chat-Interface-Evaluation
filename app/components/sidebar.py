import reflex as rx


def sidebar_item(icon: str, label: str, url: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 mr-3"),
            rx.el.span(label, class_name="font-medium"),
            class_name="flex items-center",
        ),
        href=url,
        class_name="flex items-center px-3 py-2.5 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-blue-600 transition-colors group",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.icon("bot", class_name="h-8 w-8 text-blue-600"),
            rx.el.span("LangSmith Clone", class_name="text-xl font-bold text-gray-900"),
            class_name="flex items-center gap-3 px-2 py-6 mb-4",
        ),
        rx.el.nav(
            sidebar_item("message-square", "Chat Playground", "/"),
            sidebar_item("bar-chart-2", "Evaluations", "/evaluations"),
            class_name="space-y-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="h-4 w-4 text-gray-600"),
                    class_name="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p(
                        "Admin User", class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p("admin@example.com", class_name="text-xs text-gray-500"),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="mt-auto pt-6 border-t",
        ),
        class_name="flex flex-col w-64 bg-white border-r border-gray-200 h-screen p-4 sticky top-0",
    )


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(content, class_name="flex-1 bg-gray-50 h-screen overflow-auto"),
        class_name="flex h-screen w-full overflow-hidden font-['Inter']",
    )