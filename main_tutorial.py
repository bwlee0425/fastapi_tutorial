from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Item 모델 정의
class Item(BaseModel):
    name : str
    description : str = "입력 안됨"
    price : int
    tax : float = None
    is_offer: bool = None

@app.get("/") # urls.py path
def hello(): # view
    return {"Hello": "FastAPI"}

# fastapi 환경 구성
# main.py 파일 생성
# fastapi 코드 작성
# 서버 구동 uvicorn main:app --reload
# api 테스트 localhost:8000/docs

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/items/{pk}", description="이거 좋아요") #/books/<int:pk> -> view 함수 (pk)
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/item1/")
def create_item(name, description):
    # db에 저장
    return {"name":name, "description":description}

@app.post("/item/")
def create_item(item:Item):
        return {"name":item.name, "description":item.description, "price":item.price, "tax":item.tax}

@app.put("/item/{pk}")
def update_item(pk:int, item:Item):
        return {"pk":pk, "name":item.name, "description":item.description, "price":item.price, "tax":item.tax}

@app.delete("/item/{pk}")
def delete_item(pk:int):
        return {"message":"잘 지워졌어요!"}

students = {
    1: {"name": "김멋사", "email": "kimmutsa@example.com"},
    2: {"name": "이모양", "email": "leemoyang@example.com"},
    3: {"name": "박학사", "email": "parkhaksa@example.com"},
}

@app.get("/likelion/{student_id}")
def get_student(student_id: int):
    student = students.get(student_id)
    if student:
         return {"student_id": student_id, "name": student["name"], "email": student["email"] }
    else:
         return {"error": "학생 정보를 찾을 수 없습니다."}

@app.post("/project/", status_code=status.HTTP_201_CREATED)
def create_porject(item:Item):
        return {"name":item.name, "description":item.description}

# 프로젝트 저장소 (메모리 내 저장)
projects = {}

# POST: 프로젝트 등록
@app.post("/projects/")
async def create_project(item: Item):
    project_id = len(projects) + 1  # 프로젝트 ID 생성
    projects[project_id] = item
    return {"id": project_id, "name": item.name, "description": item.description}

# GET: 프로젝트 검색
@app.get("/projects/{project_id}")
async def get_project(project_id: int):
    project = projects.get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": project_id, "name": project.name, "description": project.description}

# DELETE: 프로젝트 삭제
@app.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    project = projects.pop(project_id, None)  # 프로젝트 삭제
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": f"Project with ID {project_id} has been deleted"}