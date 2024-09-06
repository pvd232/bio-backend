from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Question_Domain import Question_Domain
    from dto.Question_Option_DTO import Question_Option_DTO


class Question_DTO(Base_DTO):
    def __init__(self, question_domain: "Question_Domain") -> None:
        self.id: int = question_domain.id
        self.text: str = question_domain.text
        self.type: str = question_domain.type
        self.options: list[Question_Option_DTO] = [
            Question_Option_DTO(question_option_domain=x)
            for x in question_domain.options
        ]
