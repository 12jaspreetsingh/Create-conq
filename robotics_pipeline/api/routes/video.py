from fastapi import APIRouter, UploadFile, File
from schemas.models import PipelineResponse
from services.pipeline import robotics_pipeline

router = APIRouter(prefix="/process-video", tags=["Video Processing"])

@router.post("/", response_model=PipelineResponse)
async def process_video_endpoint(file: UploadFile = File(None)):
    """
    Runs the full robotics pipeline on an uploaded video.
    If no file is provided, a dummy simulation is run.
    Extracts skills, predicts failures, generates intent, and stores knowledge in the Learning Memory System.
    """
    # In a real system, we'd save the UploadFile to a temporary location
    # e.g., video_path = save_upload_file_tmp(file)
    
    # For simulation, we'll just pass 'dummy' if no file is provided
    video_path = file.filename if file else "dummy"
    
    response = robotics_pipeline.run_pipeline(video_path)
    
    return response
