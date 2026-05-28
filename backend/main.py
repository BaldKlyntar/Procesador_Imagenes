from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from redis_client import redis_client
from sse_starlette.sse import EventSourceResponse
import asyncio
import shutil
import json
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"


@app.get("/")
async def home():
    return {
        "message": "Image processor API running"
    }

@app.post("/process-image")
async def process_image(image:UploadFile = File(...), options: str = Form(...)):

    task_id = str(uuid.uuid4())
    file_extension = image.filename.split(".")[-1]

    saved_filename = f"{task_id}.{file_extension}"
    image_path = f"uploads/{saved_filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    task = {
        "task_id": task_id,
        "image_path": image_path,
        "options": json.loads(options),
        "status": "pending"
    }

    redis_client.set(f"task:{task_id}:status", "pending")

    redis_client.rpush(
        "image_queue",
        json.dumps(task)
    )

    return {
        "task_id": task_id,
        "status": "pending",
        "message": "Task added to queue"
    }

@app.get("/task-status/{task_id}")
async def get_task_status(task_id:str):
    status = redis_client.get(
        f"task:{task_id}:status"

    )

    if not status:
        return {
            "status": "not_found"
        }
    
    return{
        "task_id":task_id,
        "status": status
    }

@app.get("/tasks/{task_id}/events")
async def task_events(task_id: str):
    async def event_generator():
        last_status = None

        while True:
            status = redis_client.get(f"task:{task_id}:status")

            if not status:
                yield{
                    "event": "error",
                    "data": json.dumps({
                        "status": "not_found"
                    })
                }
                break

            if status != last_status:
                last_status = status

                yield {
                    "event": "status",
                    "data": json.dumps({
                        "task_id": task_id,
                        "status": status
                    })
                }

            if status in ["completed", "error"]:
                break
            
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())


