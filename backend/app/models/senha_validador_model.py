"""
Model SQLAlchemy da tabela senhas_validador.

Colunas:
  - id              : UUID, chave primária gerada automaticamente
  - created_at      : timestamp com fuso horário do momento do registro
  - senha_capturada : senha digitada pelo usuário (capturada após 3s de inatividade)
  - ip_origem       : endereço IP da máquina que fez a requisição
  - user_agent      : navegador/sistema operacional do usuário
  - score           : pontuação de força da senha (0–5)
  - strength_label  : rótulo textual da força (ex: "Forte")
  - entropy_bits    : entropia calculada em bits
  - is_common       : indica se a senha está na lista de senhas comuns
  - comprimento     : quantidade de caracteres da senha
  - tem_maiuscula   : booleano indicando presença de letra maiúscula
  - tem_minuscula   : booleano indicando presença de letra minúscula
  - tem_numero      : booleano indicando presença de número
  - tem_especial    : booleano indicando presença de caractere especial
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, DateTime, Float, Integer, String, Text
)
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class SenhaValidador(Base):
    __tablename__ = "senhas_validador"

    # ---- Identificação -------------------------------------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Identificador único do registro (UUID v4)",
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
        comment="Data e hora em que a senha foi capturada (UTC)",
    )

    # ---- Dados capturados do usuário -----------------------------------------
    senha_capturada = Column(
        Text,
        nullable=False,
        comment="Senha digitada pelo usuário, capturada após 3s de inatividade",
    )

    ip_origem = Column(
        String(45),   # suporta IPv4 (15) e IPv6 (45)
        nullable=True,
        index=True,
        comment="Endereço IP da máquina que enviou a requisição",
    )

    user_agent = Column(
        Text,
        nullable=True,
        comment="User-Agent HTTP — navegador e sistema operacional do usuário",
    )

    # ---- Resultado da análise ------------------------------------------------
    score = Column(
        Integer,
        nullable=False,
        comment="Pontuação de força da senha de 0 (muito fraca) a 5 (muito forte)",
    )

    strength_label = Column(
        String(30),
        nullable=False,
        comment="Rótulo da força: Muito Fraca | Fraca | Razoável | Forte | Muito Forte",
    )

    entropy_bits = Column(
        Float,
        nullable=False,
        comment="Entropia estimada da senha em bits (Shannon log2)",
    )

    is_common = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="True se a senha constar na lista de senhas mais comuns",
    )

    # ---- Características da senha -------------------------------------------
    comprimento = Column(
        Integer,
        nullable=False,
        comment="Número de caracteres da senha",
    )

    tem_maiuscula = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="True se a senha contém ao menos uma letra maiúscula",
    )

    tem_minuscula = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="True se a senha contém ao menos uma letra minúscula",
    )

    tem_numero = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="True se a senha contém ao menos um número",
    )

    tem_especial = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="True se a senha contém ao menos um caractere especial",
    )

    def __repr__(self) -> str:
        return (
            f"<SenhaValidador id={self.id} score={self.score} "
            f"ip={self.ip_origem} created_at={self.created_at}>"
        )

