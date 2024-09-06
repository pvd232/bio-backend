from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Question_Domain import Question_Domain
    from dto.Question_Option_DTO import Question_Option_DTO


class Question_Response_DTO(Base_DTO):
    def __init__(self, json: dict) -> None:
        self.user_id: int = json["user_id"]
        self.question_id: int = json["question_id"]
        self.type: str = json["question_type"]
        self.multi_option_ids: list[int] = []
        self.single_option_id: int = None
        self.short_answer: str = json["short_answer"]
