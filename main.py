from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from DatabaseCore import Base, engine
from Product.ProductController import router as product_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/")
async def root():
    return {"message": "the root endpoint is working!"}

""" Only uncomment below to create new tables, 
otherwise the tests will fail if not connected
"""

Base.metadata.create_all(bind=engine)

app.include_router(product_router)
