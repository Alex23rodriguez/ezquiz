"""APIGame - FastAPI-based quiz server with web interface.

This module provides a FastAPI application for serving interactive quizzes
with category selection, question rendering, and answer validation.

The server supports multiple quizzes through a lobby system where users can
select from available quizzes.

Example:
    >>> from ezquiz import APIGame, Q
    >>>
    >>> # Create a quiz game
    >>> game = APIGame()
    >>>
    >>> # Add a math quiz
    >>> math_qs = Q.from_dict({
    ...     "What is 2 + 2?": "4",
    ...     "What is 5 + 3?": "8",
    ... })
    >>> game.add_quiz("math", "Basic Math", {"addition": math_qs})
    >>>
    >>> # Add a geography quiz
    >>> geo_qs = Q.from_dict(
    ...     {"The capital of France is [...].": "Paris"},
    ...     question_type="fill"
    ... )
    >>> game.add_quiz("geo", "Geography", {"capitals": geo_qs})
    >>>
    >>> # Start the server
    >>> game.start(host="localhost", port=8000)
    >>> # Visit http://localhost:8000/ for the lobby
"""

from pathlib import Path
from random import choice

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ezquiz.ezquiz import Q


class APIGame:
    """FastAPI-based quiz server supporting multiple quizzes.

    This class manages a collection of quizzes and serves them through
    a web interface with a lobby for quiz selection.

    Each quiz is accessible at its own URL path (e.g., /math/, /geo/)
    and has its own set of question categories.

    Attributes:
        quizzes: Dictionary mapping subpaths to quiz configurations.
                Each entry contains "title" and "qs" (questions dict).

    Example:
        >>> game = APIGame()
        >>>
        >>> # Add multiple quizzes
        >>> game.add_quiz("math", "Mathematics", {"algebra": algebra_q, "geometry": geometry_q})
        >>> game.add_quiz("spanish", "Spanish 101", {"vocab": vocab_q, "grammar": grammar_q})
        >>>
        >>> # Access:
        >>> # - Lobby: http://localhost:8000/
        >>> # - Math:  http://localhost:8000/math/
        >>> # - Spanish: http://localhost:8000/spanish/
        >>> game.start(host="localhost", port=8000)
    """

    def __init__(self) -> None:
        """Initialize an empty quiz server."""
        self.quizzes = {}  # subpath -> {"title": str, "qs": dict[str, Q]}

    def add_quiz(self, subpath: str, title: str, qs: dict[str, Q]) -> None:
        """Add a quiz at the given subpath.

        The quiz will be accessible at `/{subpath}/` and will appear in the lobby.

        Args:
            subpath: URL path for this quiz (e.g., "math", "spanish").
                    Leading/trailing slashes are automatically stripped.
            title: Display title for the quiz shown in the lobby and quiz page.
            qs: Dictionary mapping category names to Q question objects.

        Raises:
            ValueError: If subpath is empty after stripping slashes.

        Example:
            >>> game = APIGame()
            >>>
            >>> # Simple quiz with one category
            >>> game.add_quiz("math", "Basic Math", {"addition": add_q})
            >>>
            >>> # Quiz with multiple categories
            >>> game.add_quiz(
            ...     "spanish",
            ...     "Spanish Basics",
            ...     {
            ...         "vocabulary": vocab_q,
            ...         "grammar": grammar_q,
            ...         "phrases": phrases_q,
            ...     }
            ... )
        """
        # Normalize subpath (remove leading/trailing slashes)
        subpath = subpath.strip("/")
        if not subpath:
            raise ValueError("subpath cannot be empty")
        self.quizzes[subpath] = {"title": title, "qs": qs}

    def start(
        self,
        *,
        host: str,
        port: int,
        **fastapi_kw,
    ) -> None:
        """Start the FastAPI server and serve all registered quizzes.

        This method blocks until the server is stopped. The server provides:
        - A lobby page at the root URL listing all quizzes
        - Individual quiz pages at /{subpath}/
        - Static assets (JS, CSS) for the web interface
        - REST API endpoints for fetching questions and submitting answers

        Args:
            host: Hostname to bind the server to (e.g., "localhost", "0.0.0.0").
            port: Port number to listen on.
            **fastapi_kw: Additional keyword arguments passed to FastAPI.

        Example:
            >>> game = APIGame()
            >>> game.add_quiz("test", "Test Quiz", {"cat1": q1})
            >>>
            >>> # Start on localhost
            >>> game.start(host="localhost", port=8000)
            >>>
            >>> # Start on all interfaces
            >>> game.start(host="0.0.0.0", port=8080)
        """
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

    def _register_quiz_routes(
        self, app: FastAPI, subpath: str, quiz_data: dict, templates: Jinja2Templates
    ):
        """Register all routes for a specific quiz.

        This internal method sets up the URL routes for a single quiz,
        including the landing page, question API, and submission API.

        Args:
            app: The FastAPI application instance.
            subpath: The URL path prefix for this quiz.
            quiz_data: Dictionary containing "title" and "qs" for the quiz.
            templates: Jinja2 templates instance for rendering pages.
        """
        title = quiz_data["title"]
        qs = quiz_data["qs"]
        prefix = f"/{subpath}"

        @app.get(prefix + "/", response_class=HTMLResponse)
        async def quiz_landing_page(request: Request):
            """Landing page for a specific quiz with category selection."""
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
            """API endpoint to fetch the next question.

            Request body: {"categories": ["cat1", "cat2", ...]}
            Response: {"complete": false, "question": {...}}
            """
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
            """API endpoint to submit an answer.

            Request body: {"category": "...", "seed": ..., "answer": "..."}
            Response: {"correct": true/false, "explanation": {...}, ...}
            """
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
