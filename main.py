from fastapi import FastAPI, HTTPException
from  pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # Разрешаем наш HTML сервер
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


books = [
    {"id":1,
     "title": "Колобок",
     "author": "Народ",
    },
    {"id":2,
     "title": "Золотая рыбка",
     "author": "Пушкин"
     }
]

class NewBook(BaseModel):
    title: str
    author: str


@app.get("/books", tags=["Книги"], summary=["Получить все книги"])
def root():
    return books

@app.get("/books/{book_id}", tags=["Книги"], summary=["Получить конкретную книгу"])
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="книга не найдена")


@app.post("/books", tags=["Книги"])
def create_book(new_book: NewBook):
    books.append({"id": len(books) + 1, "title": new_book.title,"author": new_book.author})
    return {"status": "succes"}

if __name__ == "__main__":
    uvicorn.run("main:app",reload= True)