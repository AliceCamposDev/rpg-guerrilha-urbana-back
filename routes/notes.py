from fastapi import APIRouter, HTTPException
import pandas as pd
from config import VAULT, init_vault
from utils import clean_dataframe_for_json

router = APIRouter(tags=["Notes"])


@router.get("/notes")
async def get_notes():
    """Lista todas as notas com metadados básicos"""
    try:
        vault = init_vault()
        notes_metadata = vault.get_note_metadata()
        return clean_dataframe_for_json(notes_metadata)
    except Exception as e:
        return {"error": f"Erro ao obter notas: {str(e)}"}


@router.get("/note/{note_name}")
async def get_note_content(note_name: str):
    """Retorna o conteúdo de uma nota específica"""
    try:
        vault = init_vault()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        if not note_name.endswith(".md"):
            note_name_with_ext = f"{note_name}.md"
        else:
            note_name_with_ext = note_name

        notes_metadata = vault.get_note_metadata()

        if note_name_with_ext not in notes_metadata.index:
            for note_id in notes_metadata.index:
                if isinstance(note_id, str) and note_id.replace(".md", "") == note_name:
                    note_name_with_ext = note_id
                    break
            else:
                raise HTTPException(
                    status_code=404, detail=f"Nota '{note_name}' não encontrada"
                )

        if hasattr(vault, "read_note"):
            content = vault.read_note(note_name_with_ext)
        elif hasattr(vault, "notes"):
            content = vault.notes.get(note_name_with_ext, "Conteúdo não disponível")
        else:
            note_path = notes_metadata.loc[note_name_with_ext, "abs_filepath"]
            if pd.isna(note_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Caminho da nota '{note_name}' não encontrado",
                )

            with open(str(note_path), "r", encoding="utf-8") as f:
                content = f.read()

        return {
            "name": note_name_with_ext,
            "content": content,
            "metadata": notes_metadata.loc[note_name_with_ext].to_dict()
            if note_name_with_ext in notes_metadata.index
            else {},
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar requisição: {str(e)}"
        )
