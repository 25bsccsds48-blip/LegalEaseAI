from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator,
)
from backend.config import get_settings
from backend.schemas import (
    DocumentRequest,
    DocumentResponse,
)


router = APIRouter(
    tags=["Documents"]
)


@router.get("/health")
def health():

    settings = get_settings()

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "model": settings.gemini_model,
        "mock_mode": settings.mock_mode,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
    }


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
def generate_document(
    request: DocumentRequest,
):

    settings = get_settings()

    generator = GeminiDocumentGenerator(
        settings
    )

    try:

        content = generator.generate_document(
            request
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)[:500],
        ) from exc

    return DocumentResponse(
        document_type=request.document_type,
        content=content,
        model=settings.gemini_model,
        mock=settings.mock_mode,
    )