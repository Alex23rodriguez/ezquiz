from pathlib import Path
from random import choice

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ezquiz.ezquiz import Q


class APIGame:
    def __init__(self) -> None:
        self.quizzes = {}  # subpath -> {"title": str, "qs": dict[str, Q]}

    def add_quiz(self, subpath: str, title: str, qs: dict[str, Q]) -> None:
        """Add a quiz at the given subpath.
        
        Args:
            subpath: URL path for this quiz (e.g., "math", "spanish")
            title: Display title for the quiz
            qs: Dictionary of question categories
        """
        # Normalize subpath (remove leading/trailing slashes)
        subpath = subpath.strip("/")
        self.quizzes[subpath] = {"title": title, "qs": qs}

    def start(
        self,
        *,
        host: str,
        port: int,
        **fastapi_kw,
    ):
        app = FastAPI(**fastapi_kw)
        app.mount(
            "/static",
            StaticFiles(directory=Path(__file__).parent / "static"),
            name="static",
        )

        templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

        @app.get("/", response_class=HTMLResponse)
        async def lobby_page(request: Request):
            """Lobby page showing all available quizzes."""
            quiz_list = [
                {"path": path, "title": data["title"]} 
                for path, data in self.quizzes.items()
            ]
            return templates.TemplateResponse(
                "lobby.html",
                context={
                    "request": request,
                    "quizzes": quiz_list,
                },
            )

        # Register routes for each quiz
        for subpath, quiz_data in self.quizzes.items():
            self._register_quiz_routes(app, subpath, quiz_data, templates)

        uvicorn.run(app, host=host, port=port)

    def _register_quiz_routes(self, app: FastAPI, subpath: str, quiz_data: dict, templates: Jinja2Templates):
        """Register all routes for a specific quiz."""
        title = quiz_data["title"]
        qs = quiz_data["qs"]
        prefix = f"/{subpath}"

        @app.get(prefix + "/", response_class=HTMLResponse)
        async def quiz_landing_page(request: Request):
            return templates.TemplateResponse(
                "index.html",
                context={
                    "request": request,
                    "title": title,
                    "categories": list(qs.keys()),
                },
            )

        @app.post(prefix + "/api/next", response_class=JSONResponse)
        async def quiz_next_question(request: Request):
            data = await request.json()
            print(data)
            categories = data.get("categories", [])
            cat = choice(categories)
            q = qs[cat]
            seed = q.get_seed()
            prompt = q.ask(seed)

            return JSONResponse(
                {
                    "complete": False,
                    "question": {
                        "category": cat,
                        "seed": seed,
                        "text": prompt["text"],
                        "type": prompt.get("type", "simple"),
                        "context": prompt.get("context", ""),
                        "hints": prompt.get("hints", []),
                    },
                }
            )

        @app.post(prefix + "/api/submit", response_class=JSONResponse)
        async def quiz_submit_answer(request: Request):
            data = await request.json()
            print(data)
            cat = data["category"]
            seed = data["seed"]
            submitted_ans = data["answer"]

            q = qs[cat]
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
