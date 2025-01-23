# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import List
from pydantic import BaseModel

# Jinja2 템플릿을 사용할 폴더 지정
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# 임시 데이터 저장(나중에 DB나 JSON 파일로 대체 가능)
todo_list = []

# Pydantic 모델 정의
class TodoItem(BaseModel):
    id: int
    title: str
    description: str = ""
    done: bool = False

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # 템플릿에 todo_list를 전달
    return templates.TemplateResponse("index.html", {"request": request, "todo_list": todo_list})

@app.post("/todo")
def create_todo(item: TodoItem):
    todo_list.append(item.dict())
    return {"message": "TODO created", "item": item}

@app.get("/todo", response_model=List[TodoItem])
def get_todos():
    return todo_list

@app.get("/todo/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    for item in todo_list:
        if item["id"] == todo_id:
            return item
    return {"error": "TODO not found"}

@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, updated_item: TodoItem):
    for idx, item in enumerate(todo_list):
        if item["id"] == todo_id:
            todo_list[idx] = updated_item.dict()
            return {"message": "TODO updated", "item": updated_item}
    return {"error": "TODO not found"}

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    for idx, item in enumerate(todo_list):
        if item["id"] == todo_id:
            removed_item = todo_list.pop(idx)
            return {"message": "TODO deleted", "item": removed_item}
    return {"error": "TODO not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)
"""