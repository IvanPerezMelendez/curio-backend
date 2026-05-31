  ---
  Estructura del backend — repaso para otra IA

  Stack

  FastAPI + SQLAlchemy + Pydantic. Base de datos SQL con Alembic para migraciones.

  ---
  Capas: Router → Service → Repository
  
  1. Router (api/routers/)

  - Define los endpoints HTTP.
  - No contiene lógica de negocio.
  - Recibe dependencias inyectadas (servicio, usuario, etc.) vía Annotated[..., Depends(...)].
  - Solo llama al servicio y devuelve la respuesta.

  @router.put("/{section_id}/user-notes")
  def upsert_user_section_note(
      service: Annotated[SectionService, Depends(get_sections_service)],
      section: Annotated[SectionModel, Depends(get_section_by_location_id_from_path_or_raise)],
      request_data: UserSectionNoteRequest,
  ) -> UserSectionNoteResponse:
      return service.upsert_user_note(...)

  ---
  2. Service (services/<nombre>.py)
  
  - Extiende BaseService[Model, Repository, CreateSch, UpdateSch].
  - Contiene toda la lógica de negocio.
  - Regla clave: si necesita datos de otro módulo, importa el servicio de ese módulo, NUNCA su repositorio directamente.
  - Puede tener múltiples repositorios en __init__, pero solo del mismo módulo.
  - Nunca hace self.db.query(...) — eso va en el repositorio.

  class SectionService(BaseService[SectionModel, SectionRepository, SectionCreateSch, SectionUpdateSch]):
      def __init__(self, repository: SectionRepository, user_section_notes_service: UserSectionNotesService):
          super().__init__(repository)
          self.user_section_notes_service = user_section_notes_service  # servicio, no repo

  ---
  3. Repository (repositories/<nombre>.py)

  - Extiende BaseRepository[Model].
  - Solo recibe db: Session en __init__.
  - Solo accede a su propia tabla. JOINs se ponen en el repo de la tabla "primaria/driving".
  - La mayoría solo necesita el __init__ + super().__init__(Model, db). Métodos custom solo cuando BaseRepository no cubre el caso.

  class SectionRepository(BaseRepository[SectionModel]):
      def __init__(self, db: Session):
          super().__init__(SectionModel, db)

  ---
  Dependency Injection — dos niveles
  
  services/dependencies/<nombre>.py — construye el servicio desde una Session raw (para uso interno entre servicios):
  def get_sections_service_from_session(session: Session) -> SectionService:
      repository = SectionRepository(db=session)
      user_section_notes_service = get_user_section_notes_service_from_session(session)
      return SectionService(repository=repository, user_section_notes_service=user_section_notes_service)
      
  api/dependencies/<nombre>.py — wrapper de FastAPI que llama al anterior via Depends(get_db):
  def get_sections_service(session: Annotated[Session, Depends(get_db)]) -> SectionService:
      return get_sections_service_from_session(session)

  ---
  Schemas — dos niveles
  
  - services/schemas/ — Pydantic schemas internos del servicio (CreateSch, UpdateSch, respuestas internas).
  - api/schemas/ — Pydantic schemas del contrato HTTP (Request/Response hacia el cliente).

  ---
  Estructura de un módulo

  src/modules/<modulo>/
  ├── api/
  │   ├── dependencies/   # Depends() para FastAPI
  │   ├── routers/        # Endpoints HTTP
  │   └── schemas/        # Request/Response HTTP
  ├── models/             # SQLAlchemy models
  ├── repositories/       # Acceso a BBDD (1 repo = 1 tabla)
  └── services/
      ├── dependencies/   # Factory functions (Session → Service)
      ├── schemas/        # Pydantic schemas internos
      └── <nombre>.py     # Lógica de negocio

  ---
  BaseService — métodos que ya existen (no reimplementar)

  ┌──────────────────────────────────┬──────────────────────────────────────────────┐
  │              Método              │                     Uso                      │
  ├──────────────────────────────────┼──────────────────────────────────────────────┤
  │ get_by_id(id)                    │ Busca por PK, devuelve None si no existe     │
  ├──────────────────────────────────┼──────────────────────────────────────────────┤
  │ get_by_id_or_raise(id)             │ Busca por PK, lanza ValueError si no existe  │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ get_by_attributes(**filters)       │ Busca por campos, devuelve el primero o None │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ get_all_by_attributes(**filters)   │ Devuelve lista filtrando por campos          │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ create(schema)                     │ Crea entidad desde Pydantic schema           │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ create_bulk(schemas)               │ Crea múltiples entidades                     │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ update(id, schema)                 │ Actualiza entidad                            │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ delete(id)                         │ Elimina por PK                               │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ delete_bulk(ids)                   │ Elimina múltiples                            │
  ├────────────────────────────────────┼──────────────────────────────────────────────┤
  │ upsert(lookup_fields, create_data) │ Crea o actualiza según campos de búsqueda    │O

