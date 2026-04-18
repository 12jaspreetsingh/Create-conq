import uuid
from typing import Dict, Any
from schemas.models import TaskMemory, PipelineResponse, Action, SkillStep, FailurePrediction
from services.video_processor import video_processor
from services.ml_models import ml_pipeline
from services.memory_manager import memory_manager

class RoboticsPipeline:
    def __init__(self):
        self.video_processor = video_processor
        self.ml_pipeline = ml_pipeline
        self.memory_manager = memory_manager

    def run_pipeline(self, video_path: str) -> PipelineResponse:
        """
        Executes the full end-to-end robotics processing pipeline.
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"

        # 1. Video Processing & Frame Sampling
        frames = self.video_processor.process_video(video_path)

        # 2. ML Inference (Placeholders)
        objects = self.ml_pipeline.detect_objects(frames)
        raw_actions = self.ml_pipeline.extract_actions(frames, objects)
        raw_steps = self.ml_pipeline.segment_skills(raw_actions)
        raw_failures = self.ml_pipeline.predict_failures(raw_steps)
        intent = self.ml_pipeline.generate_intent(raw_steps)

        # 3. Convert raw dictionaries to Pydantic models
        actions = [Action(**act) for act in raw_actions]
        steps = [SkillStep(**step) for step in raw_steps]
        failures = [FailurePrediction(**fail) for fail in raw_failures]

        # 4. Construct Task Memory Object
        task_memory = TaskMemory(
            task_id=task_id,
            actions=actions,
            steps=steps,
            failures=failures,
            intent=intent
        )

        # 5. Query Memory for Similar Past Tasks (BEFORE storing the new one to avoid self-match, or store after)
        action_names = [act.action_name for act in actions]
        similar_past_tasks = self.memory_manager.query_similar_tasks(action_names)

        # 6. Store Output in Memory (Continuous Learning)
        self.memory_manager.store_task(task_memory)

        # 7. Construct and Return Pipeline Response
        return PipelineResponse(
            task_id=task_id,
            actions=actions,
            structured_skills=steps,
            predicted_failures=failures,
            generated_intent=intent,
            similar_past_tasks=similar_past_tasks
        )

# Global pipeline instance
robotics_pipeline = RoboticsPipeline()
