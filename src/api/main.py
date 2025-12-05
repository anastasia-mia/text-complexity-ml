from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.predict import router as predict_router
from src.api.routes.stats import router as stats_router
from src.api.dependencies.ml_model import load_resources

app = FastAPI(title="Text Complexity API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api")
app.include_router(stats_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    load_resources()