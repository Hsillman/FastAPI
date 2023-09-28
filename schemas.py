# This file contains the Pydantic models
# These Pydantic models define more or less a 
# "schema" (a valid data shape).
from typing import Union
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

# This is a Pydantic model (schema) that will be used
# when reading data, when returning it from the API.
# Before creating an item, we don't know what will be 
# the ID assigned to it, but when reading it (when 
# returning it from the API) we will already know its ID.
class Item(ItemBase):
    id: int
    owner_id: int 

    class Config:
        orm_mode = True




class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    # For security, the password won't be in other 
    # Pydantic models, for example, it won't be sent 
    # from the API when reading a user.
    password: str 

class UserUpdate(UserBase):
    is_active: bool
    password: str
    # TODO: Bring the list of items when user update is called.
    items: list[Item] = []

# This is a Pydantic model (schema) that will be used
# when reading data, when returning it from the API.
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True