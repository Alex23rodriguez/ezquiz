from pathlib import Path
from random import choice
from typing import Literal

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ezquiz.ezquiz import Q


class APIGame:
    def __init__(self, title: str, qs: dict[str, Q]) -> None:
        self.title = title
        self.qs = qs
        self.score = 0
        self.mistakes = 0
        self.streak = 0
        self.history = []

    def start(
        self,
        **fastapi_kw,
    ):
        app = FastAPI(**fastapi_kw)

        templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

        @app.get("/", response_class=HTMLResponse)
        async def landing_page(request: Request):
            return templates.TemplateResponse(
                "index.html",
                context={
                    "request": request,
                    "title": self.title,
                    "categories": list(self.qs.keys()),
                },
            )

        @app.post("/api/next", response_class=JSONResponse)
        async def next_question(request: Request):
            """Get the next question in the session."""
            # return a random question from selected categories
            data = await request.json()
            print(data)
            categories = data.get("categories", [])

            # Get all available questions from selected categories
            cat = choice(categories)

            q = self.qs[cat]
            seed = q.get_seed()
            prompt = q.ask(seed)

            return JSONResponse(
                {
                    "complete": False,
                    "question": {"category": cat, "seed": seed, "text": prompt},
                }
            )

        @app.post("/api/submit", response_class=JSONResponse)
        async def submit_answer(request: Request):
            data = await request.json()
            print(data)
            cat = data["category"]
            seed = data["seed"]
            submitted_ans = data["answer"]

            q = self.qs[cat]
            correct_ans = q.correct(seed)
            correct = q.check(correct_ans, submitted_ans)
            explain = q.explain(seed)

            return JSONResponse(
                {
                    "correct": correct,
                    "submitted_answer": submitted_ans,
                    "correct_answer": correct_ans,
                    "explanation": explain,
                }
            )

        uvicorn.run(app)
