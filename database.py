from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from pathlib import Path
import datetime

BASE_PATH = Path(__file__).parent
DB_PATH = BASE_PATH / "my_definitions.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

class Definition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    term: str = Field(index=True, unique=True)
    definition: str
    source: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[str] = Field(default_factory= lambda:datetime.datetime.now().isoformat())

SQLModel.metadata.create_all(engine)

def add_definition(term: str, definition: str, source: Optional[str], category: Optional[str]):
    with Session(engine) as session:
        existing = session.exec(select(Definition).where(Definition.term == term)).first()
        if existing:
            print(f"  '{term}' già presente nel DB. Aggiorno la definizione.")
            existing.definition = definition
            existing.source = source
            existing.category = category
            existing.created_at = datetime.datetime.now().isoformat()
        else:
            new_def = Definition(term=term, definition=definition, source=source, category=category)
            session.add(new_def)
            print(f"Aggiunto : {term}")
        session.commit()
    
def search_definitions(query: str = ""):
    with Session(engine) as session:
        statement = select(Definition)
        if query:
            statement = statement.where(
                Definition.term.ilike(f"%{query}%") |
                Definition.definition.ilike(f"%{query}%")
            )
        results = session.exec(statement).all()
        return results
    
def list_all():
    results = search_definitions()
    for r in results:
        print(f"\n→ {r.term}")
        print(f"   {r.definition[:100]}...")
        print(f"   Fonte: {r.source or 'N/A'} | Categoria: {r.category or 'N/A'}")