import re
import math
import os
from typing import Set

# ---------------------------------------------------------------------------
# Load common passwords list at module level (O(1) lookup)
# ---------------------------------------------------------------------------
_COMMON_PASSWORDS: Set[str] = set()

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_COMMON_PASSWORDS_FILE = os.path.join(_DATA_DIR, "common_passwords.txt")

try:
    with open(_COMMON_PASSWORDS_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                _COMMON_PASSWORDS.add(word)
except FileNotFoundError:
    pass  # file is optional; will still flag as not-common if missing

# ---------------------------------------------------------------------------
# Known sequential patterns (keyboard rows, numeric sequences, alpha runs)
# ---------------------------------------------------------------------------
_SEQUENTIAL_PATTERNS = [
    "0123456789",
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "qazwsxedcrfvtgbyhnujmikolp",
]

_KEYBOARD_PATTERNS = [
    "qwerty", "qwert", "werty", "asdfg", "sdfgh", "dfghj",
    "zxcvb", "xcvbn", "1234567890", "12345678", "123456",
    "!@#$%^&*()", "password", "passw0rd", "p@ssword",
]


def _charset_size(password: str) -> int:
    """Estimate charset size based on character classes used."""
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"\d", password):
        size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        size += 32  # approx. printable special chars
    return max(size, 1)


def _calc_entropy(password: str) -> float:
    """Shannon-style entropy: log2(charset^length)."""
    charset = _charset_size(password)
    return round(math.log2(charset) * len(password), 2)


def _has_repeated_chars(password: str) -> bool:
    """Returns True if there are 3+ consecutive repeated characters."""
    return bool(re.search(r"(.)\1{2,}", password))


def _has_sequential_chars(password: str) -> bool:
    """Returns True if the password contains a sequential run of 3+ chars."""
    lower = password.lower()
    for pattern in _SEQUENTIAL_PATTERNS:
        for i in range(len(pattern) - 2):
            chunk = pattern[i : i + 3]
            if chunk in lower or chunk[::-1] in lower:
                return True
    return False


def _has_keyboard_pattern(password: str) -> bool:
    """Returns True if the password contains known keyboard patterns."""
    lower = password.lower()
    for kp in _KEYBOARD_PATTERNS:
        if kp in lower:
            return True
    return False


def validate_password(password: str) -> dict:
    """
    Validate a password against NIST SP 800-63B and OWASP recommendations.
    Returns a dict matching PasswordResponse.
    """
    # ---- individual checks ------------------------------------------------
    length = len(password)
    length_ok = length >= 12
    length_great = length >= 16
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", password))
    is_common = password.lower() in _COMMON_PASSWORDS
    not_common = not is_common
    no_repeated = not _has_repeated_chars(password)
    no_sequential = not _has_sequential_chars(password)
    no_keyboard = not _has_keyboard_pattern(password)

    entropy = _calc_entropy(password)

    # ---- score (0–10, displayed as 0–5 stars / bar) -----------------------
    raw_score = 0

    if length >= 8:
        raw_score += 1
    if length >= 12:
        raw_score += 1
    if length >= 16:
        raw_score += 1
    if has_upper:
        raw_score += 1
    if has_lower:
        raw_score += 1
    if has_digit:
        raw_score += 1
    if has_special:
        raw_score += 1
    if not_common:
        raw_score += 1
    if no_repeated:
        raw_score += 0.5
    if no_sequential:
        raw_score += 0.5
    if no_keyboard:
        raw_score += 0.5
    if entropy >= 50:
        raw_score += 0.5

    # Normalise to 0–5
    score = min(5, round(raw_score / 2))

    # ---- labels & colors ---------------------------------------------------
    if score <= 1:
        label, color = "Muito Fraca", "#ef4444"   # red
    elif score == 2:
        label, color = "Fraca", "#f97316"          # orange
    elif score == 3:
        label, color = "Razoável", "#eab308"        # yellow
    elif score == 4:
        label, color = "Forte", "#22c55e"           # green
    else:
        label, color = "Muito Forte", "#06b6d4"     # cyan

    # ---- tips (what to improve) -------------------------------------------
    tips = []
    positive = []

    if not length_ok:
        tips.append("Use pelo menos 12 caracteres. Senhas longas são muito mais difíceis de quebrar.")
    elif not length_great:
        tips.append("Considere usar 16 ou mais caracteres para máxima segurança.")
    else:
        positive.append(f"Comprimento excelente ({length} caracteres)!")

    if not has_upper:
        tips.append("Adicione letras maiúsculas (A-Z) para aumentar a complexidade.")
    else:
        positive.append("Contém letras maiúsculas.")

    if not has_lower:
        tips.append("Adicione letras minúsculas (a-z).")
    else:
        positive.append("Contém letras minúsculas.")

    if not has_digit:
        tips.append("Inclua pelo menos um número (0-9).")
    else:
        positive.append("Contém números.")

    if not has_special:
        tips.append("Adicione caracteres especiais como !@#$%^&*() para dificultar ataques de força bruta.")
    else:
        positive.append("Contém caracteres especiais.")

    if is_common:
        tips.append("Essa senha está na lista das mais usadas e será a primeira tentativa em qualquer ataque de dicionário. Escolha outra senha completamente diferente.")
    else:
        positive.append("Não está na lista das senhas mais comuns.")

    if not no_repeated:
        tips.append("Evite caracteres repetidos em sequência (ex: 'aaa', '111'), pois reduzem drasticamente a entropia.")
    else:
        positive.append("Sem repetições excessivas de caracteres.")

    if not no_sequential:
        tips.append("Evite sequências óbvias como 'abc', '123', 'xyz'. Atacantes testam essas combinações primeiro.")
    else:
        positive.append("Sem sequências alfanuméricas óbvias.")

    if not no_keyboard:
        tips.append("Evite padrões de teclado como 'qwerty', 'asdf'. São muito fáceis de adivinhar.")
    else:
        positive.append("Sem padrões de teclado detectados.")

    if entropy < 50:
        tips.append(f"A entropia estimada é {entropy} bits. O ideal é ≥ 50 bits para resistir a ataques modernos.")
    else:
        positive.append(f"Entropia alta: {entropy} bits.")

    return {
        "score": score,
        "strength_label": label,
        "strength_color": color,
        "entropy_bits": entropy,
        "is_common": is_common,
        "checks": {
            "length_ok": length_ok,
            "length_great": length_great,
            "has_uppercase": has_upper,
            "has_lowercase": has_lower,
            "has_digit": has_digit,
            "has_special": has_special,
            "not_common": not_common,
            "no_repeated_chars": no_repeated,
            "no_sequential_chars": no_sequential,
            "no_keyboard_pattern": no_keyboard,
        },
        "tips": tips,
        "positive_feedbacks": positive,
    }

