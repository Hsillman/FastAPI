from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int= 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # This example is not secure, the password is not hashed. In a real 
    # life application you would need to hash the password and never save 
    # them in plaintext.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_email(db: Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def update_user(db: Session, email: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    for key, value in user.dict().items():
        # This won't update the password because it is stored as hashed_password in the db
        # TODO: fix this
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int= 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_user_item(db: Session, item:schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item