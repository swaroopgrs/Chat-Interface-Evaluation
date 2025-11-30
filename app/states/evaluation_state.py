import reflex as rx
from typing import Any
import datetime
import random
import json


class Run(rx.Base):
    id: str
    timestamp: str
    status: str
    duration: int
    tokens: int
    cost: float
    model: str
    input_text: str
    output_text: str
    tags: list[str]
    transcript: list[dict[str, str]] = []
    feedback_thumb: str = "none"
    rating: int = 0
    feedback_comment: str = ""


class EvaluationState(rx.State):
    runs: list[Run] = []
    search_query: str = ""
    status_filter: str = "All"
    model_filter: str = "All"
    expanded_run_id: str = ""
    selected_run_ids: list[str] = []
    is_comparison_open: bool = False
    new_tag_input: str = ""
    temp_comment: str = ""

    def _generate_mock_data(self):
        models = ["gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus"]
        statuses = ["success", "success", "success", "error", "success"]
        prompts = [
            "Explain quantum computing",
            "Write a python script for scraping",
            "Summarize this article",
            "Translate to Spanish",
            "Debug this code snippet",
        ]
        mock_runs = []
        for i in range(15):
            status = random.choice(statuses)
            model = random.choice(models)
            tokens = random.randint(150, 2000)
            duration = random.randint(500, 5000)
            cost = tokens / 1000 * (0.03 if "gpt-4" in model else 0.002)
            prompt_text = prompts[i % len(prompts)]
            response_text = "This is a simulated response content for the run..." * 3
            transcript = [
                {"role": "user", "content": prompt_text, "created_at": "10:00"},
                {"role": "assistant", "content": response_text, "created_at": "10:01"},
            ]
            mock_runs.append(
                Run(
                    id=f"run_{1000 + i}",
                    timestamp=(
                        datetime.datetime.now() - datetime.timedelta(hours=i * 2)
                    ).strftime("%Y-%m-%d %H:%M"),
                    status=status,
                    duration=duration,
                    tokens=tokens,
                    cost=round(cost, 4),
                    model=model,
                    input_text=prompt_text,
                    output_text=response_text,
                    tags=["production"] if i % 2 == 0 else ["test"],
                    transcript=transcript,
                    feedback_thumb=random.choice(["up", "down", "none"]),
                    rating=random.randint(0, 5),
                )
            )
        return sorted(mock_runs, key=lambda x: x.timestamp, reverse=True)

    @rx.event
    def on_load(self):
        if not self.runs:
            self.runs = self._generate_mock_data()

    @rx.var
    def filtered_runs(self) -> list[Run]:
        filtered = self.runs
        if self.search_query:
            q = self.search_query.lower()
            filtered = [
                r for r in filtered if q in r.id.lower() or q in r.input_text.lower()
            ]
        if self.status_filter != "All":
            filtered = [
                r for r in filtered if r.status.lower() == self.status_filter.lower()
            ]
        if self.model_filter != "All":
            filtered = [r for r in filtered if r.model == self.model_filter]
        return filtered

    @rx.var
    def total_runs(self) -> int:
        return len(self.runs)

    @rx.var
    def average_latency(self) -> int:
        if not self.runs:
            return 0
        return int(sum((r.duration for r in self.runs)) / len(self.runs))

    @rx.var
    def total_tokens(self) -> int:
        return sum((r.tokens for r in self.runs))

    @rx.var
    def total_cost(self) -> float:
        return round(sum((r.cost for r in self.runs)), 4)

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status

    @rx.event
    def set_model_filter(self, model: str):
        self.model_filter = model

    @rx.event
    def toggle_detail(self, run_id: str):
        if self.expanded_run_id == run_id:
            self.expanded_run_id = ""
        else:
            self.expanded_run_id = run_id

    @rx.event
    def export_data(self):
        data = [
            {
                "id": r.id,
                "timestamp": r.timestamp,
                "status": r.status,
                "model": r.model,
                "tokens": r.tokens,
                "cost": r.cost,
                "input": r.input_text,
                "output": r.output_text,
                "rating": r.rating,
                "feedback": r.feedback_comment,
                "tags": r.tags,
            }
            for r in self.runs
        ]
        json_str = json.dumps(data, indent=2)
        return rx.download(data=json_str, filename="evaluation_runs.json")

    @rx.var
    def chart_data_latency(self) -> list[dict[str, str | int | float]]:
        data = []
        runs = self.filtered_runs
        if not runs:
            return []
        sorted_runs = sorted(runs, key=lambda x: x.timestamp)
        recent_runs = sorted_runs[-20:]
        for r in recent_runs:
            data.append({"name": r.id, "latency": r.duration, "tokens": r.tokens})
        return data

    @rx.var
    def chart_data_daily_volume(self) -> list[dict[str, str | int | float]]:
        counts = {}
        for r in self.runs:
            date_key = r.timestamp.split(" ")[0]
            counts[date_key] = counts.get(date_key, 0) + 1
        sorted_dates = sorted(counts.keys())
        return [{"date": d, "runs": counts[d]} for d in sorted_dates]

    @rx.event
    def toggle_run_selection(self, run_id: str, checked: bool):
        if checked:
            if run_id not in self.selected_run_ids:
                self.selected_run_ids.append(run_id)
        elif run_id in self.selected_run_ids:
            self.selected_run_ids.remove(run_id)

    @rx.event
    def set_comparison_open(self, is_open: bool):
        self.is_comparison_open = is_open

    @rx.var
    def selected_runs_data(self) -> list[Run]:
        return [r for r in self.runs if r.id in self.selected_run_ids]

    @rx.event
    def set_thumb_feedback(self, run_id: str, value: str):
        for r in self.runs:
            if r.id == run_id:
                r.feedback_thumb = value
                break
        self.runs = self.runs

    @rx.event
    def set_rating(self, run_id: str, rating: int):
        for r in self.runs:
            if r.id == run_id:
                r.rating = rating
                break
        self.runs = self.runs

    @rx.event
    def update_comment(self, run_id: str, comment: str):
        for r in self.runs:
            if r.id == run_id:
                r.feedback_comment = comment
                break
        self.runs = self.runs
        yield rx.toast("Feedback updated")

    @rx.event
    def add_tag(self, run_id: str, tag: str):
        if not tag.strip():
            return
        for r in self.runs:
            if r.id == run_id:
                if tag not in r.tags:
                    r.tags.append(tag)
                break
        self.runs = self.runs

    @rx.event
    def remove_tag(self, run_id: str, tag: str):
        for r in self.runs:
            if r.id == run_id:
                if tag in r.tags:
                    r.tags.remove(tag)
                break
        self.runs = self.runs

    @rx.event
    def add_run_from_chat(self, transcript: list[dict], model: str):
        input_text = transcript[0]["content"] if transcript else ""
        output_text = transcript[-1]["content"] if transcript else ""
        full_text = " ".join([m["content"] for m in transcript])
        tokens = len(full_text.split()) * 1.3
        cost = tokens / 1000 * 0.002
        new_run = Run(
            id=f"run_{random.randint(10000, 99999)}",
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            status="success",
            duration=random.randint(800, 2500),
            tokens=int(tokens),
            cost=round(cost, 5),
            model=model,
            input_text=input_text,
            output_text=output_text,
            tags=["chat-session"],
            transcript=transcript,
            feedback_thumb="none",
            rating=0,
            feedback_comment="",
        )
        self.runs.insert(0, new_run)
        self.runs = self.runs