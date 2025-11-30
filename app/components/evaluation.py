import reflex as rx
from app.states.evaluation_state import EvaluationState, Run


def metric_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 {color}"),
            class_name="p-3 bg-gray-50 rounded-xl",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start justify-between",
    )


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.cond(
            status.lower() == "success",
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
        ),
    )


def tag_badge(run: Run, tag: str) -> rx.Component:
    return rx.el.span(
        tag,
        rx.el.button(
            rx.icon("x", class_name="h-3 w-3 ml-1.5 hover:text-gray-900"),
            on_click=EvaluationState.remove_tag(run.id, tag),
        ),
        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-700 border border-gray-200 mr-2 mb-2",
    )


def feedback_section(run: Run) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "Quality Rating:", class_name="text-sm font-medium text-gray-700 mr-3"
            ),
            rx.foreach(
                [1, 2, 3, 4, 5],
                lambda i: rx.el.button(
                    rx.icon(
                        "star",
                        class_name=rx.cond(
                            run.rating >= i,
                            "h-5 w-5 fill-yellow-400 text-yellow-400",
                            "h-5 w-5 text-gray-300",
                        ),
                    ),
                    on_click=EvaluationState.set_rating(run.id, i),
                    class_name="focus:outline-none transition-transform hover:scale-110",
                ),
            ),
            class_name="flex items-center mb-4",
        ),
        rx.el.div(
            rx.el.span(
                "Sentiment:", class_name="text-sm font-medium text-gray-700 mr-3"
            ),
            rx.el.button(
                rx.icon(
                    "thumbs-up",
                    class_name=rx.cond(
                        run.feedback_thumb == "up",
                        "h-5 w-5 fill-green-500 text-green-500",
                        "h-5 w-5 text-gray-400",
                    ),
                ),
                on_click=EvaluationState.set_thumb_feedback(run.id, "up"),
                class_name="p-2 hover:bg-gray-100 rounded-full mr-2",
            ),
            rx.el.button(
                rx.icon(
                    "thumbs-down",
                    class_name=rx.cond(
                        run.feedback_thumb == "down",
                        "h-5 w-5 fill-red-500 text-red-500",
                        "h-5 w-5 text-gray-400",
                    ),
                ),
                on_click=EvaluationState.set_thumb_feedback(run.id, "down"),
                class_name="p-2 hover:bg-gray-100 rounded-full",
            ),
            class_name="flex items-center mb-4",
        ),
        rx.el.div(
            rx.el.textarea(
                placeholder="Add specific feedback comments...",
                default_value=run.feedback_comment,
                on_blur=lambda val: EvaluationState.update_comment(run.id, val),
                class_name="w-full p-3 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none h-24 bg-white",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.span(
                "Tags:", class_name="text-sm font-medium text-gray-700 block mb-2"
            ),
            rx.el.div(
                rx.foreach(run.tags, lambda t: tag_badge(run, t)),
                class_name="flex flex-wrap",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Add tag...",
                    id=f"tag-input-{run.id}",
                    class_name="text-xs border rounded px-2 py-1 w-24 focus:outline-none focus:border-blue-500",
                    on_blur=lambda val: EvaluationState.add_tag(run.id, val),
                ),
                class_name="mt-1",
            ),
        ),
        class_name="bg-white p-4 rounded-lg border border-gray-200 h-full",
    )


def transcript_message(msg: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                msg["role"],
                class_name="text-xs font-bold uppercase text-gray-500 mb-1 block",
            ),
            rx.el.div(
                msg["content"], class_name="text-sm whitespace-pre-wrap text-gray-800"
            ),
            class_name=f"p-3 rounded-lg {rx.cond(msg['role'] == 'user', 'bg-gray-100', 'bg-blue-50')}",
        ),
        class_name="mb-3",
    )


def transcript_view(run: Run) -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            "Conversation Transcript",
            class_name="text-sm font-semibold text-gray-900 mb-4 flex items-center gap-2",
        ),
        rx.cond(
            run.transcript,
            rx.el.div(
                rx.foreach(run.transcript, transcript_message), class_name="space-y-2"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "INPUT",
                        class_name="text-xs font-bold uppercase text-gray-500 mb-1 block",
                    ),
                    rx.el.div(
                        run.input_text,
                        class_name="text-sm whitespace-pre-wrap bg-gray-100 p-3 rounded-lg",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.span(
                        "OUTPUT",
                        class_name="text-xs font-bold uppercase text-gray-500 mb-1 block",
                    ),
                    rx.el.div(
                        run.output_text,
                        class_name="text-sm whitespace-pre-wrap bg-blue-50 p-3 rounded-lg",
                    ),
                ),
            ),
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200",
    )


def run_row(run: Run) -> rx.Component:
    return rx.fragment(
        rx.el.tr(
            rx.el.td(
                rx.el.input(
                    type="checkbox",
                    on_change=lambda checked: EvaluationState.toggle_run_selection(
                        run.id, checked
                    ),
                    checked=EvaluationState.selected_run_ids.contains(run.id),
                    class_name="rounded border-gray-300 text-blue-600 focus:ring-blue-500",
                ),
                class_name="pl-6 pr-2 py-4",
            ),
            rx.el.td(
                rx.el.span(run.id, class_name="font-mono text-xs text-gray-500"),
                class_name="px-2 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
            ),
            rx.el.td(
                run.timestamp,
                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
            ),
            rx.el.td(
                status_badge(run.status), class_name="px-6 py-4 whitespace-nowrap"
            ),
            rx.el.td(
                f"{run.duration}ms",
                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
            ),
            rx.el.td(
                run.model,
                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
            ),
            rx.el.td(
                f"{run.tokens}",
                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
            ),
            rx.el.td(
                f"${run.cost:.4f}",
                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
            ),
            rx.el.td(
                rx.el.button(
                    rx.cond(
                        EvaluationState.expanded_run_id == run.id,
                        rx.icon("chevron-up", class_name="h-4 w-4 text-gray-500"),
                        rx.icon("chevron-down", class_name="h-4 w-4 text-gray-500"),
                    ),
                    on_click=lambda: EvaluationState.toggle_detail(run.id),
                    class_name="p-1 hover:bg-gray-100 rounded-md transition-colors",
                ),
                class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
            ),
            class_name=rx.cond(
                EvaluationState.expanded_run_id == run.id,
                "bg-blue-50/30",
                "hover:bg-gray-50 transition-colors",
            ),
        ),
        rx.cond(
            EvaluationState.expanded_run_id == run.id,
            rx.el.tr(
                rx.el.td(
                    rx.el.div(
                        rx.el.div(transcript_view(run), class_name="col-span-2"),
                        rx.el.div(feedback_section(run), class_name="col-span-1"),
                        class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 bg-gray-50/50 shadow-inner",
                    ),
                    col_span=9,
                    class_name="p-0",
                )
            ),
        ),
    )


def analytics_charts() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Run Volume (Last 30 Days)",
                class_name="text-sm font-semibold text-gray-700 mb-4",
            ),
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                rx.recharts.x_axis(
                    data_key="date", font_size=10, tick_line=False, axis_line=False
                ),
                rx.recharts.y_axis(font_size=10, tick_line=False, axis_line=False),
                rx.recharts.tooltip(),
                rx.recharts.bar(
                    data_key="runs", fill="#3b82f6", radius=[4, 4, 0, 0], bar_size=20
                ),
                data=EvaluationState.chart_data_daily_volume,
                height=200,
                width="100%",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h3(
                "Recent Latency & Tokens",
                class_name="text-sm font-semibold text-gray-700 mb-4",
            ),
            rx.recharts.composed_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                rx.recharts.x_axis(data_key="name", hide=True),
                rx.recharts.y_axis(
                    y_axis_id="left",
                    orientation="left",
                    font_size=10,
                    tick_line=False,
                    axis_line=False,
                    label={"value": "ms", "angle": -90, "position": "insideLeft"},
                ),
                rx.recharts.y_axis(
                    y_axis_id="right",
                    orientation="right",
                    font_size=10,
                    tick_line=False,
                    axis_line=False,
                    label={"value": "tok", "angle": 90, "position": "insideRight"},
                ),
                rx.recharts.tooltip(),
                rx.recharts.bar(
                    data_key="latency",
                    y_axis_id="left",
                    fill="#f97316",
                    radius=[4, 4, 0, 0],
                    bar_size=10,
                    name="Latency (ms)",
                ),
                rx.recharts.line(
                    data_key="tokens",
                    y_axis_id="right",
                    stroke="#8b5cf6",
                    stroke_width=2,
                    dot=False,
                    name="Tokens",
                ),
                data=EvaluationState.chart_data_latency,
                height=200,
                width="100%",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8",
    )


def comparison_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Run Comparison",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="h-5 w-5"),
                                class_name="text-gray-400 hover:text-gray-500",
                            )
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            EvaluationState.selected_runs_data,
                            lambda r: rx.el.div(
                                rx.el.div(
                                    rx.el.h4(
                                        r.id,
                                        class_name="font-mono text-xs text-gray-500 mb-1",
                                    ),
                                    rx.el.div(
                                        status_badge(r.status), class_name="mb-2"
                                    ),
                                    class_name="border-b pb-3 mb-3",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Duration", class_name="text-xs text-gray-500"
                                    ),
                                    rx.el.p(
                                        f"{r.duration}ms",
                                        class_name="text-sm font-medium mb-2",
                                    ),
                                    rx.el.p("Cost", class_name="text-xs text-gray-500"),
                                    rx.el.p(
                                        f"${r.cost:.4f}",
                                        class_name="text-sm font-medium mb-2",
                                    ),
                                    rx.el.p(
                                        "Model", class_name="text-xs text-gray-500"
                                    ),
                                    rx.el.p(
                                        r.model, class_name="text-sm font-medium mb-2"
                                    ),
                                    rx.el.p(
                                        "Rating", class_name="text-xs text-gray-500"
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "star",
                                            class_name="h-4 w-4 text-yellow-400 inline mr-1",
                                        ),
                                        f"{r.rating}/5",
                                        class_name="text-sm font-medium mb-2 flex items-center",
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Output Snippet",
                                        class_name="text-xs text-gray-500 mt-2 mb-1",
                                    ),
                                    rx.el.div(
                                        r.output_text,
                                        class_name="text-xs bg-gray-50 p-2 rounded h-32 overflow-y-auto whitespace-pre-wrap",
                                    ),
                                ),
                                class_name="flex-1 min-w-[250px] border-r last:border-r-0 px-4",
                            ),
                        ),
                        class_name="flex overflow-x-auto pb-4",
                    ),
                    class_name="bg-white p-6 rounded-xl max-w-[90vw] w-fit mx-auto max-h-[80vh] overflow-hidden flex flex-col shadow-xl",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 outline-none",
            ),
        ),
        open=EvaluationState.is_comparison_open,
        on_open_change=EvaluationState.set_comparison_open,
    )


def evaluation_dashboard() -> rx.Component:
    return rx.el.div(
        comparison_modal(),
        rx.el.div(
            rx.el.h1(
                "Evaluation Dashboard", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Track and analyze your AI model performance",
                class_name="text-sm text-gray-500 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            metric_card(
                "Total Runs",
                EvaluationState.total_runs.to_string(),
                "activity",
                "text-blue-600",
            ),
            metric_card(
                "Avg. Latency",
                f"{EvaluationState.average_latency}ms",
                "clock",
                "text-orange-600",
            ),
            metric_card(
                "Total Tokens",
                EvaluationState.total_tokens.to_string(),
                "cpu",
                "text-purple-600",
            ),
            metric_card(
                "Total Cost",
                f"${EvaluationState.total_cost}",
                "dollar-sign",
                "text-green-600",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        analytics_charts(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search by ID or content...",
                        on_change=EvaluationState.set_search_query.debounce(500),
                        class_name="pl-10 pr-4 py-2 w-full border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm",
                    ),
                    class_name="relative w-full md:w-96",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("All Status", value="All"),
                        rx.el.option("Success", value="Success"),
                        rx.el.option("Error", value="Error"),
                        on_change=EvaluationState.set_status_filter,
                        class_name="px-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none bg-white",
                    ),
                    rx.el.select(
                        rx.el.option("All Models", value="All"),
                        rx.el.option("gpt-4-turbo", value="gpt-4-turbo"),
                        rx.el.option("gpt-3.5-turbo", value="gpt-3.5-turbo"),
                        rx.el.option("claude-3-opus", value="claude-3-opus"),
                        on_change=EvaluationState.set_model_filter,
                        class_name="px-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none bg-white",
                    ),
                    class_name="flex gap-3",
                ),
                class_name="flex flex-col md:flex-row gap-4 justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.cond(
                    EvaluationState.selected_run_ids.length() > 0,
                    rx.el.button(
                        rx.icon("columns_3", class_name="h-4 w-4 mr-2"),
                        f"Compare ({EvaluationState.selected_run_ids.length()})",
                        on_click=EvaluationState.set_comparison_open(True),
                        class_name="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm",
                    ),
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4 mr-2"),
                    "Export JSON",
                    on_click=EvaluationState.export_data,
                    class_name="flex items-center px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors",
                ),
                class_name="flex gap-3 items-center",
            ),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50 w-4",
                        ),
                        rx.el.th(
                            "Run ID",
                            class_name="px-2 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Timestamp",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Duration",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Model",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Tokens",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Cost",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th("", class_name="px-6 py-3 bg-gray-50"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(EvaluationState.filtered_runs, run_row),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm overflow-x-auto",
        ),
        class_name="p-8 max-w-[1600px] mx-auto",
    )