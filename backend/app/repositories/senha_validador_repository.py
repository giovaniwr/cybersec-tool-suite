"""
Repositório da tabela senhas_validador.
Responsável por todas as operações de leitura e escrita no banco.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.models.senha_validador_model import SenhaValidador


class SenhaValidadorRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    # ------------------------------------------------------------------
    # Escrita
    # ------------------------------------------------------------------

    async def salvar(self, dados: dict) -> SenhaValidador:
        """Persiste um novo registro de análise de senha no banco."""
        registro = SenhaValidador(**dados)
        self.session.add(registro)
        await self.session.flush()   # obtém o id sem fazer commit (commit feito pelo get_db)
        await self.session.refresh(registro)
        return registro

    # ------------------------------------------------------------------
    # Leitura
    # ------------------------------------------------------------------

    async def listar(self, limite: int = 50, offset: int = 0) -> list[SenhaValidador]:
        """Retorna os registros mais recentes (para dashboard/admin)."""
        resultado = await self.session.execute(
            select(SenhaValidador)
            .order_by(desc(SenhaValidador.created_at))
            .limit(limite)
            .offset(offset)
        )
        return resultado.scalars().all()

    async def total(self) -> int:
        """Retorna o total de senhas analisadas."""
        resultado = await self.session.execute(
            select(func.count(SenhaValidador.id))
        )
        return resultado.scalar_one()

    async def distribuicao_scores(self) -> list[dict]:
        """Retorna a contagem de senhas por score (útil para gráficos)."""
        resultado = await self.session.execute(
            select(SenhaValidador.score, func.count(SenhaValidador.id).label("total"))
            .group_by(SenhaValidador.score)
            .order_by(SenhaValidador.score)
        )
        return [{"score": row.score, "total": row.total} for row in resultado]

