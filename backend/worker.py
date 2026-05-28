from redis_client import redis_client
from image_processor import process_image
import json
import time
import time

print("Worker iniciado...", flush=True)

while True:
    task_data = redis_client.lpop("image_queue")

    if not task_data:
        print("Esperando tarea...", flush=True)
        time.sleep(2)
        continue

    task = json.loads(task_data)
    task_id = task["task_id"]

    try:

        print(f"Procesando tarea: {task_id}", flush=True)

        redis_client.set(
            f"task:{task_id}:status",
            "pending"
        )

        redis_client.set(
            f"task:{task_id}:status",
            "processing"
        )

        output_path = process_image(task)

        redis_client.set(
            f"task:{task_id}:status",
            output_path
        )

        redis_client.set(
            f"task:{task_id}:status",
            "completed"
        )

        print(f"Tarea completada: {task_id}", flush=True)

    except Exception as error:
        redis_client.set(
            f"task:{task_id}:status",
            "error"
        )

        print(f"Error al completar la tarea {task_id}")
        print(error)
