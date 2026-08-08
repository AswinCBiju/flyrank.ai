import os
import psycopg2
from abc import ABC, abstractmethod
from typing import List, Optional


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[dict]: pass
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[dict]: pass
    @abstractmethod
    def create(self, title: str) -> dict: pass
    @abstractmethod
    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[dict]: pass
    @abstractmethod
    def delete(self, task_id: int) -> bool: pass

class PostgresTaskRepository(TaskRepository):
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")

    def _get_connection(self):
        return psycopg2.connect(self.db_url)

    def get_all(self) -> List[dict]:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title, done FROM tasks ORDER BY id;")
                rows = cursor.fetchall()
                return [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]

    def get_by_id(self, task_id: int) -> Optional[dict]:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
                row = cursor.fetchone()
                if row:
                    return {"id": row[0], "title": row[1], "done": row[2]}
                return None
    
    def create(self, title: str) -> dict:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
                    (title, False)
                )
                row = cursor.fetchone()
                conn.commit()
                return {"id": row[0], "title": row[1], "done": row[2]}
    
    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[dict]:
        task = self.get_by_id(task_id)
        if not task:
            return None
        
        new_title = title if title is not None else task["title"]
        new_done = done if done is not None else task["done"]
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                    (new_title, new_done, task_id)
                )
                row = cursor.fetchone()
                conn.commit()
                return {"id": row[0], "title": row[1], "done": row[2]}
    
    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
                conn.commit()
                return True