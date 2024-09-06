from .Base_Domain import Base_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Question_Model
    from domain.Question_Option_Domain import Question_Option_Domain


class Question_Domain(Base_Domain):
    def __init__(self, question_object: Question_Model) -> None:
        self.id: int = question_object.id
        self.text: str = question_object.text
        self.type: str = question_object.type
        self.options: list[Question_Option_Domain] = [
            Question_Option_Domain(question_object=x) for x in question_object.options
        ]
