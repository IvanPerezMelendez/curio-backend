from fastapi import APIRouter, HTTPException, status
from openai import AsyncOpenAI

from src.core.deps import CurrentUser
from src.modules.chat.schemas import ChatRequest, ChatResponse
from src.settings import settings

router = APIRouter(prefix="/chat", tags=["chat"])


def _build_system_prompt(exercise: dict) -> str:
    lines = [
        "Eres Curio, un tutor educativo amigable y conciso.",
        "El usuario está realizando un ejercicio de aprendizaje y tiene dudas.",
        "",
        f"Pregunta del ejercicio: {exercise.get('question', '')}",
    ]

    exp = exercise.get("explanation") or {}
    if exp.get("title") or exp.get("body"):
        lines.append(f"Explicación: {exp.get('title', '')} — {exp.get('body', '')}")

    ex_type = exercise.get("type", "")
    if ex_type in ("multiple-choice", "odd-one-out", "image"):
        options = exercise.get("options", [])
        if options:
            lines.append("Opciones: " + " / ".join(str(o) for o in options))
    elif ex_type == "true-false":
        lines.append("Tipo: verdadero o falso")

    lines += [
        "",
        "Responde en español de forma educativa y concisa (máximo 4 frases).",
        "No des directamente la respuesta correcta; ayuda a entender el concepto.",
    ]
    return "\n".join(lines)


@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    current_user: CurrentUser,
) -> ChatResponse:
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat no configurado: falta OPENAI_API_KEY en el servidor.",
        )

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    openai_messages = [{"role": "system", "content": _build_system_prompt(body.exercise)}]
    for msg in body.messages:
        openai_messages.append({"role": msg.role, "content": msg.content})

    completion = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=openai_messages,
        max_tokens=350,
        temperature=0.7,
    )

    return ChatResponse(reply=completion.choices[0].message.content or "")
