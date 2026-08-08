import time

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.routes.recipes import recipes_router
from backend.routes.ingredients import ingredients_router
from db.sql_init import get_session
from db.db_models import Recipe, Ingredient

RATE_LIMIT = 60   # max requests per window
RATE_WINDOW = 60  # window length in seconds

app = FastAPI(title="Recipe API", description="API for recipes")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory per-IP rate limiter."""

    def __init__(self, app):
        super().__init__(app)
        self.hits: dict[str, tuple[float, int]] = {}  # ip -> (window_start, count)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in {"/health", "/docs", "/openapi.json", "/redoc"}:
            return await call_next(request)

        client = request.client.host if request.client else "unknown"
        now = time.time()
        start, count = self.hits.get(client, (now, 0))
        if now - start >= RATE_WINDOW:
            start, count = now, 0
        count += 1
        self.hits[client] = (start, count)

        if count > RATE_LIMIT:
            return Response(status_code=429, content="Too Many Requests")

        return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)


@app.get("/health")
async def health_check() -> dict:
    """Check if the server is running and the DB is reachable."""
    try:
        with get_session() as session:
            recipes = session.scalar(select(func.count()).select_from(Recipe))
            ingredients = session.scalar(select(func.count()).select_from(Ingredient))
        return {
            "status": "ok",
            "num_recipes": recipes,
            "num_ingredients": ingredients,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking health: {str(e)}")


app.include_router(recipes_router)
app.include_router(ingredients_router)
