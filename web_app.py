from fastapi import APIRouter, HTTPException, Depends
import model  # Модель, которая была написана ранее
import json
from typing import Dict, List
from datetime import datetime

NOTES_FILE = "notes.json"
TOKENS_FILE = "token.json"
NOTE_ID_FILE = "note_id"

api_router = APIRouter()


def get_notes() -> Dict[str, dict]:
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        FileNotFoundError()
    except json.decoder.JSONDecodeError:
        return {}


def get_tokens() -> List[str]:
    try:
        with open(TOKENS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        FileNotFoundError()
    except json.decoder.JSONDecodeError:
        return []


def save_notes(notes: Dict[str, dict]):
    with open(NOTES_FILE, 'w') as file:
        json.dump(notes, file)


def save_tokens(tokens: List[str]):
    with open(TOKENS_FILE, 'w') as file:
        json.dump(tokens, file)


def load_note_id():
    with open(NOTE_ID_FILE, 'r') as file:
        current_id = int(file.read())

    return current_id


def save_note_id(current_id: int):
    with open(NOTE_ID_FILE, 'w') as file:
        file.write(str(current_id))


def verify_token(token: str, tokens: List[str] = Depends(get_tokens)):
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")


@api_router.post("/notes/", response_model=model.CreateNoteResponse)
def create_note(note_text: str, token: str = Depends(verify_token)):
    current_id = load_note_id()
    new_node_id = str(current_id)
    notes = get_notes()
    now = datetime.now().isoformat()
    notes[new_node_id] = {
        "text": note_text,
        "created_at": now,
        "updated_at": now,
    }
    current_id += 1
    save_note_id(current_id)

    save_notes(notes)

    return {"id": new_node_id}


@api_router.get("/notes/{note_id}/note_info/", response_model=model.GetNoteInfoResponse)
def get_note_info(note_id: str, token: str = Depends(verify_token)):
    notes = get_notes()
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")

    note_data = notes[note_id]
    return {"created_at": note_data["created_at"], "updated_at": note_data["updated_at"]}


@api_router.get("/notes/{node_id}/note_text/", response_model=model.GetNoteTextResponse)
def get_note_text(note_id: str, token: str = Depends(verify_token)):
    notes = get_notes()
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")

    note_data = notes[note_id]
    return {"id": int(note_id), "text": note_data["text"]}


@api_router.get("/all_notes/", response_model=model.GetNoteListResponse)
def get_list_notes(token: str = Depends(verify_token)):
    notes = get_notes()
    keys_list = list(notes.keys())
    dict_ids = {}
    for i in range(len(keys_list)):
        dict_ids[i] = keys_list[i]

    return {"notes": dict_ids}


@api_router.put("/notes/{note_id}", response_model=model.GetNoteTextResponse)
def edit_note_text(note_id: str, text: str, token: str = Depends(verify_token)):
    notes = get_notes()
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")

    note = notes[note_id]
    now = datetime.now().isoformat()
    notes[note_id] = {
        "text": text,
        "created_at": note["created_at"],
        "updated_at": now
    }
    save_notes(notes)

    return {"id": int(note_id), "text": text}


@api_router.delete("/notes/{note_id}/", response_model=model.GetNoteTextResponse)
def delete_note(note_id: str, token: str = Depends(verify_token)):
    notes = get_notes()
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")

    note = notes[note_id]
    notes.pop(note_id)

    save_notes(notes)

    return {"id": int(note_id), "text": note["text"]}