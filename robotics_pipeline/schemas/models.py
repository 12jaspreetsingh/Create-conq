from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Action(BaseModel):
    action_name: str
    confidence: float

class SkillStep(BaseModel):
    step_description: str
    start_time: float
    end_time: float

class FailurePrediction(BaseModel):
    probability: float
    reason: Optional[str] = None

class TaskMemory(BaseModel):
    task_id: str
    actions: List[Action]
    steps: List[SkillStep]
    failures: List[FailurePrediction]
    intent: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class MemoryQueryRequest(BaseModel):
    actions: List[str]

class MemoryQueryResponse(BaseModel):
    similar_tasks: List[TaskMemory]

class PipelineResponse(BaseModel):
    task_id: str
    actions: List[Action]
    structured_skills: List[SkillStep]
    predicted_failures: List[FailurePrediction]
    generated_intent: str
    similar_past_tasks: List[TaskMemory]
