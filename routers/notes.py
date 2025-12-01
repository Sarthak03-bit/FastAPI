from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import get_async_db
# from sqlalchemy.orm import Session
from models import NotesDisplayModel, NotesModel, NotesUpdateModel
from routers.auth import get_current_active_user

from typing import List, Annotated
from database_models import Note
from database_models import User as UserModel



from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



api = APIRouter(prefix="/notes")

async def get_note_from_db(id: int, db: AsyncSession):
    result = await db.execute(
        select(Note).where(Note.id == id)
    )
    return result.scalar_one_or_none()


@api.get("/", response_model=List[NotesDisplayModel])
async def get_all_notes(db : Annotated[AsyncSession, Depends(get_async_db)],
                         current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    items = await db.execute(select(Note))
    return items.scalars().all()

    

@api.get("/{id}", response_model = NotesDisplayModel)
async def get_note(id : Annotated[ int , Path(..., ge=1, description="Note id")] ,db : Annotated[AsyncSession, Depends(get_async_db)],
                         current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    result = await db.execute(
        select(Note).where(Note.id == id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for id : {id}")
    return note



@api.post("/", response_model=NotesDisplayModel, status_code=status.HTTP_201_CREATED)
async def app_note(input_note :NotesModel ,  db : Annotated[AsyncSession, Depends(get_async_db)],
                         current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    id = input_note.id
    exists = await get_note_from_db(id, db)
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Data already present for id : {id}")
    else:
        new_note = Note(**input_note.model_dump())
        db.add(new_note)
        await db.commit()
        await db.refresh(new_note)
        return new_note 


@api.put("/{id}",response_model=NotesDisplayModel, status_code=status.HTTP_202_ACCEPTED)
async def update_note(id : Annotated[int , Path(..., ge=1)], input_note : Annotated[ NotesUpdateModel ,...], db : Annotated[AsyncSession, Depends(get_async_db)],
                         current_user: Annotated[UserModel, Depends(get_current_active_user)] ):
    exists = await get_note_from_db(id, db)
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No record found for given id, Failed to update")
    
    update_data = input_note.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exists, field, value)

    await db.commit()
    await db.refresh(exists)

    return exists 



@api.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: int, db : Annotated[AsyncSession, Depends(get_async_db)],
                         current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    existing_entry = await get_note_from_db(id, db)
    if not existing_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No record found for given id, Failed to delete",
        )

    await db.delete(existing_entry)
    await db.commit()

    return {"detail": f"Note with id {id} deleted successfully"}

