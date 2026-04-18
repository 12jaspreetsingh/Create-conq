from fastapi import APIRouter
from typing import List
from schemas.models import TaskMemory, MemoryQueryRequest, MemoryQueryResponse
from services.memory_manager import memory_manager

router = APIRouter(prefix="/memory", tags=["Learning Memory System"])

@router.get("/", response_model=List[TaskMemory])
async def get_all_memories():
    """
    Returns all stored skills and tasks from the Learning Memory System.
    """
    return memory_manager.get_all_memories()

@router.post("/query", response_model=MemoryQueryResponse)
async def query_memory(query: MemoryQueryRequest):
    """
    Retrieves similar past tasks based on input actions.
    Enables reuse of previously learned skills.
    """
    similar_tasks = memory_manager.query_similar_tasks(query.actions)
    return MemoryQueryResponse(similar_tasks=similar_tasks)
