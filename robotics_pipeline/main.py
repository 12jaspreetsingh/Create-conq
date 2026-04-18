from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import video, memory

app = FastAPI(
    title="AI Robotics Learning Pipeline",
    description="A backend system that converts human activity videos into robot-understandable skills and learns over time.",
    version="1.0.0"
)

# CORS middleware for potential frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(video.router)
app.include_router(memory.router)

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "AI Robotics Learning Pipeline Backend is running!"}
