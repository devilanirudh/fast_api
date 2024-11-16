from multiprocessing.managers import public_methods
from typing import Optional

from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel , Field
from starlette import status


app = FastAPI()

class Book:
    id: int
    title : str
    author : str
    description : str
    rating : int
    published_date:int

    def __init__(self , id, title, author, description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id:Optional[int] = Field(description="id not needed on create" , default = None )
    title:str = Field(min_length=3)
    author:str = Field(min_length= 1)
    description:str = Field(min_length=1, max_length=100)
    rating : int = Field(gt=-1,lt=6)
    published_date:int

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title": "a new book",
                "author": "anirudh",
                "description": "a new descripton of a book",
                "rating": 5,
                "published_date": 2012
            }
        }
    }

BOOKS = [
    Book(1,'computer science' , 'code with anirudh', 'a very nice book' , 5 , 2012),
    Book(2,'be fast' , 'code with anirudh', 'a very nice book' , 5, 2013),
    Book(3,'anirudh' , 'code with anirudh', 'a very nice book' , 5, 2013),
    Book(4,'cp1' , 'code with anirudh', 'bd' , 2, 2012),
    Book(5,'cs1' , 'code with anirudh', 'bd' , 2, 2015),
    Book(6 ,'cd4' , 'code with anirudh', 'bd' , 1, 2015)
]

@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='item not found')


@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/{published_date}")
async def by_published_date(published_date:int):
    book_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            book_to_return.append(BOOKS[i])
    return book_to_return


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#@app.post("/crete_book")
#async def create_book(book_request = Body()):
 #   BOOKS.append(book_request)

@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='item not found')

@app.get("/books/" , status_code=status.HTTP_200_OK)
async def read_by_rating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/books")
async def create_book(book_request:BookRequest):
 #   print(type(book_request))
    new_book = Book(**book_request.model_dump())
    #print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id +1
    else:
        book.id =1
    return book

@app.put("/books/update_book" , status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
        if not book_changed:
            raise HTTPException(status_code=404,detail='item not found')

@app.delete("/books/{delete_book}")
async def delete_book(delete_book:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == delete_book:
            BOOKS.pop(i)
            break

@app.get("/books/{published_date}")
async def by_published_date(published_date:int):
    book_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            book_to_return.append(BOOKS[i])
    return book_to_return
