import asyncio
import json
import queue


from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi import FastAPI, WebSocket, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models import Task, State, Zone, Place, BaseTask
from db import get_all_work_zones, get_tasks_by_state, change_state_task, create_task


active_task: queue.Queue[Task] = queue.Queue()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешаем все заголовки
)

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


@app.post("/task/сreate",)
async def task_create(task: BaseTask):
    print(task)
    # Создать таск, сохранить в бд, сохранить в кеш
    data = create_task(
            operator_id=task.operator_id,
            sheet_count=task.count,
            from_id=task.from_id,
            to_id=task.to_id,
            comment=task.comment
        )
    print(
        data
    )
    # task = Task(
    #     *create_task(
    #         operator_id=task.operator_id,
    #         sheet_count=task.count,
    #         from_id=task.from_id,
    #         to_id=task.to_id
    #     )
    # )


@app.post("/task/accept")
async def task_accepted(task_id: int = Query(..., description="ID задачи")):
    # изменяем статус задачи в бд и отправляем оператору этот статус и даем добро на смену стейта у крановщика
    task_id = change_state_task(task_id=task_id, to_change=State.IN_PROGRESS)
    return {
        "id": task_id,
        "state": "in_progress"
    }


@app.post("/task/complete")
async def task_completed(task_id: int = Query(..., description="ID задачи")):
    task_id = change_state_task(task_id=task_id, to_change=State.COMPLETED)
    return {
        "task_id": task_id,
        "state": "completed"
    }


@app.get(
    "/crane22/work_zone",
    response_class=JSONResponse)
@cache(expire=3600)
async def get_work_zone():

    return {
        "zones": get_all_work_zones()
    }


@app.websocket("/crane22/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while not active_task.empty():  # Очищаем очередь
        active_task.get()


    # таски как уже выполняемые, так и не начатые
    tasks = get_tasks_by_state(State.IN_PROGRESS.value) + get_tasks_by_state(State.WAIT_START.value)
    for task in tasks:
        await websocket.send_text(task.json())

    while True:
        if not active_task.empty():
            task = active_task.get()
            await websocket.send_text(task.json())
        await asyncio.sleep(0.5)


