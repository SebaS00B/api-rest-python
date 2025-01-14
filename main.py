from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Curso(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simularemos una base de datos
db: List[Curso] = []

# CRUD

# Obtener todos los cursos
@app.get("/curso/", response_model=List[Curso])
def obtener_cursos():
    return db

# Agregar un nuevo curso
@app.post("/curso/", response_model=Curso)
def agregar_curso(curso: Curso):
    curso.id = str(uuid.uuid4())
    db.append(curso)
    return curso

# Leer un curso por ID
@app.get("/curso/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next((curso for curso in db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# Actualizar un curso
@app.put("/curso/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso: Curso):
    curso_actual = next((c for c in db if c.id == curso_id), None)
    if curso_actual is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso.id = curso_id  # Mantener el mismo ID
    index = db.index(curso_actual)
    db[index] = curso
    return curso

# Eliminar un curso
@app.delete("/curso/{curso_id}")
def eliminar_curso(curso_id: str):
    curso = next((c for c in db if c.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.remove(curso)
    return {"mensaje": "Curso eliminado correctamente"}



 
    