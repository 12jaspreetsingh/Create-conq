import json
import os
from typing import List, Dict, Any
from schemas.models import TaskMemory

# Base directory for the data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(BASE_DIR, "data", "memory.json")

class MemoryManager:
    """
    Core Learning Memory System.
    Stores and retrieves structured skills to enable continuous learning.
    """

    def __init__(self, file_path: str = MEMORY_FILE):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the memory JSON file exists."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def _load_memory(self) -> List[Dict[str, Any]]:
        """Loads all memories from the JSON file."""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_memory(self, data: List[Dict[str, Any]]):
        """Saves data to the JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def store_task(self, task: TaskMemory):
        """
        Stores a processed task into the memory system.
        """
        memories = self._load_memory()
        memories.append(task.dict())
        self._save_memory(memories)

    def get_all_memories(self) -> List[TaskMemory]:
        """
        Retrieves all stored tasks from memory.
        """
        memories = self._load_memory()
        return [TaskMemory(**mem) for mem in memories]

    def query_similar_tasks(self, query_actions: List[str], top_k: int = 3) -> List[TaskMemory]:
        """
        Retrieves similar past tasks based on the input actions.
        Uses a basic Jaccard similarity to simulate matching.
        """
        if not query_actions:
            return []

        memories = self.get_all_memories()
        query_set = set(action.lower() for action in query_actions)

        scored_tasks = []
        for task in memories:
            # Extract action names from the stored task
            task_actions = set(action.action_name.lower() for action in task.actions)
            
            # Calculate Jaccard Similarity: |Intersection| / |Union|
            intersection = query_set.intersection(task_actions)
            union = query_set.union(task_actions)
            
            similarity = len(intersection) / len(union) if len(union) > 0 else 0
            
            if similarity > 0: # Only keep if there is some overlap
                scored_tasks.append((similarity, task))

        # Sort by highest similarity
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        
        # Return top K similar tasks
        return [task for _, task in scored_tasks[:top_k]]

# Global instance for dependency injection
memory_manager = MemoryManager()
