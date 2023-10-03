from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db
from security import utils as sec_utils

models.Base.metadata.create_all(bind=engine)

# TODO: Don't let users update other users information. Same with delete

app = FastAPI()
app.include_router(sec_utils.router)

@app.put("/users/{user_email}", response_model=schemas.User)
def update_user(
        current_user: Annotated[schemas.User, Depends(sec_utils.get_current_active_user)],
        user_email: str, 
        user: schemas.UserUpdate, 
        db: Session = Depends(get_db)
    ):
    db_user_path = crud.get_user_by_email(db, email=user_email)
    db_user_being_updated = crud.get_user_by_email(db, email=user.email)
    if db_user_being_updated and user.email != user_email:
        raise HTTPException(status_code=400, detail='This email is already registered')
    if db_user_path is None:
        raise HTTPException(status_code=404, detail='Cant update user, not found')
    return crud.update_user(db=db, email=user_email, user=user)

# Using the Accepted status code for delete response
@app.delete("/users/{user_email}", status_code=202, response_model=dict)
def delete_user_by_email(
        current_user: Annotated[schemas.User, Depends(sec_utils.get_current_active_user)],
        user_email: str, 
        db: Session = Depends(get_db)
    ):
    delete_success = crud.delete_user_by_email(db=db, email=user_email)
    if not delete_success:
        raise HTTPException(status_code=404, detail='User not found, unable to delete')
    return {"message": "User deleted successfully"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db),skip: int = 0, limit: int = 100):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int ,db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.delete("/items/{item_id}", status_code=202, response_model=dict)
def delete_item(
        current_user: Annotated[schemas.User, Depends(sec_utils.get_current_active_user)],
        item_id : int,
        db: Session = Depends(get_db)
    ):
    delete_success = crud.delete_item(db=db, item_id=item_id)
    if not delete_success:
        raise HTTPException(status_code=404, detail='Item not found, unable to delete')
    return  {"message": "Item deleted successfully"}

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db=db, skip=skip, limit=limit)
    return items

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(
        current_user: Annotated[schemas.User, Depends(sec_utils.get_current_active_user)],
        item_id: str, item: schemas.ItemUpdate, db: Session = Depends(get_db)
        ):
    db_item = crud.get_item_by_id(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail='Item not found, unable to update')
    return crud.update_item(db=db, item_id=item_id, item=item)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)