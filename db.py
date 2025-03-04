import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime

from models import Zone, Place, Task, State


DB_NAME = "database.db"


def get_all_work_zones(color: str = "gray") -> List[Zone]:
    """Возвращает список всех рабочих зон."""

    zones = []
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Work_Zone")
        for id_, x, y, width, height, zone_name in cursor.fetchall():
            zone = Zone(
                id=id_,
                poss=(x, y),
                height=height,
                width=width,
                name=zone_name,
                color=color,
                places=get_storage_areas_by_work_zone(work_zone_id=id_)
            )
            zones.append(zone)
    return zones


def get_storage_areas_by_work_zone(work_zone_id: int, color: str = "yellow") -> List[Place]:
    """Возвращает список мест для складирования в указанной рабочей зоне."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        places = []
        cursor.execute("SELECT * FROM Storage_Area WHERE work_zone_id = ?", (work_zone_id,))

        for id_, x, y, width, height, name, *_ in cursor.fetchall():
            place = Place(
                id=id_,
                name=name,
                poss=(x, y),
                width=width,
                height=height,
                color=color
            )
            places.append(place)

        return places


def get_tasks_by_state(state_id: int) -> List[Task]:
    """Возвращает список всех заданий по состоянию."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        tasks = []
        cursor.execute(
            "SELECT id, from_id, to_id, state_id, comment, sheet_count, creation_date, start_date, end_date, operator_id  FROM Task WHERE state_id = ?",
            (state_id,)
        )
        for id_, from_id, to_id, state_id, comment, sheet_count, creation_date, start_date, end_date, operator_id in cursor.fetchall():
            task = Task(
                id=id_,
                from_id=from_id,
                to_id=to_id,
                count=sheet_count,
                comment=comment,
                state=State(state_id),
                creation_date=creation_date,
                start_date=start_date,
                end_date=end_date,
                operator_id=operator_id
            )
            tasks.append(task)

        return tasks


####
def change_state_task(task_id: int, to_change: State, flag_time_end: bool = False, flag_time_start: bool = False) -> int:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if flag_time_start or flag_time_end:
            time = str(datetime.now())

            cursor.execute(f'''
                UPDATE 
                    Task 
                SET 
                    state_id = ?,
                    {"end_date" if flag_time_end else "start_date"} = ?
                WHERE 
                    id = ?
            ''', (to_change.value, time, task_id ))
        else:
            cursor.execute('''
                            UPDATE 
                                Task 
                            SET 
                                state_id = ?
                            WHERE 
                                id = ?
                        ''', (to_change.value, task_id))
        conn.commit()
        return task_id


def create_task(operator_id: int, sheet_count: int, from_id: int, to_id: int, comment: str) -> int:
    state_id: int = 0
    """Создает новое задание и возвращает его ID."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Task (operator_id, creation_date, sheet_count, from_id, to_id, state_id, comment) 
            VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
        ''', (operator_id, sheet_count, from_id, to_id, state_id, comment))
        conn.commit()
        return cursor.lastrowid


def get_task_by_id(task_id: int) -> Task:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, from_id, to_id, state_id, comment, sheet_count, creation_date, start_date, end_date, operator_id  FROM Task WHERE id = ?",
            (task_id,)
        )
        id_, from_id, to_id, state_id, comment, sheet_count, creation_date, start_date, end_date, operator_id = cursor.fetchone()

        task = Task(
            id=id_,
            from_id=from_id,
            to_id=to_id,
            count=sheet_count,
            comment=comment,
            state=State(state_id),
            creation_date=creation_date,
            start_date=start_date,
            end_date=end_date,
            operator_id=operator_id
        )

        return task


####
def get_place_by_id(place_id: int, color: str = "yellow") -> Place:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Storage_Area WHERE id = ?", (place_id,))
        id_, x, y, width, height, name, *_ = cursor.fetchone()
    return Place(
            id=id_,
            name=name,
            poss=(x, y),
            width=width,
            height=height,
            color=color
        )