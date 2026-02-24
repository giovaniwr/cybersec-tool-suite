from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.password_models import PasswordRequest, PasswordResponse
from app.services.password_validator import validate_password
from app.database import get_db
from app.repositories.senha_validador_repository import SenhaValidadorRepository

router = APIRouter(prefix="/api/password", tags=["password"])


def _extrair_ip(request: Request) -> str:
    """
    Extrai o IP real do cliente respeitando proxies reversos.
    Verifica X-Forwarded-For antes de usar o IP direto da conexão.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "desconhecido"


@router.post("/analyze", response_model=PasswordResponse)
async def analyze(body: PasswordRequest):
    """
    Análise em tempo real — apenas valida a senha, SEM persistir no banco.
    Chamado a cada 400 ms enquanto o usuário digita.
    """
    return validate_password(body.password)


@router.post("/validate", response_model=PasswordResponse)
async def validate(
    request: Request,
    body: PasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Captura definitiva — valida E persiste no banco de dados.
    Chamado pelo frontend após 3 segundos de inatividade no input.
    """
    result = validate_password(body.password)

    repo = SenhaValidadorRepository(db)
    await repo.salvar({
        "senha_capturada":  body.password,
        "ip_origem":        _extrair_ip(request),
        "user_agent":       request.headers.get("User-Agent"),
        "score":            result["score"],
        "strength_label":   result["strength_label"],
        "entropy_bits":     result["entropy_bits"],
        "is_common":        result["is_common"],
        "comprimento":      len(body.password),
        "tem_maiuscula":    result["checks"]["has_uppercase"],
        "tem_minuscula":    result["checks"]["has_lowercase"],
        "tem_numero":       result["checks"]["has_digit"],
        "tem_especial":     result["checks"]["has_special"],
    })

    return result


@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    """Retorna estatísticas agregadas das senhas analisadas."""
    repo = SenhaValidadorRepository(db)
    return {
        "total_analisadas": await repo.total(),
        "distribuicao_scores": await repo.distribuicao_scores(),
    }




