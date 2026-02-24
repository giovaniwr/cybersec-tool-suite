from pydantic import BaseModel
from typing import Dict, List


class PasswordRequest(BaseModel):
    password: str


class PasswordChecks(BaseModel):
    length_ok: bool
    length_great: bool
    has_uppercase: bool
    has_lowercase: bool
    has_digit: bool
    has_special: bool
    not_common: bool
    no_repeated_chars: bool
    no_sequential_chars: bool
    no_keyboard_pattern: bool


class PasswordResponse(BaseModel):
    score: int
    strength_label: str
    strength_color: str
    entropy_bits: float
    is_common: bool
    checks: PasswordChecks
    tips: List[str]
    positive_feedbacks: List[str]

