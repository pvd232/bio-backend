from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Question_Option_Domain import Question_Option_Domain


class Question_Option_DTO(Base_DTO):
    def __init__(self, question_option_domain: "Question_Option_Domain") -> None:
        self.id: int = question_option_domain.id
        self.question_id: int = question_option_domain.question_id
        self.text: str = question_option_domain.text
