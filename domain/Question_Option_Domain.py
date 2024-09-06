from .Base_Domain import Base_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Question_Option_Model


class Question_Option_Domain(Base_Domain):
    def __init__(self, question_object: Question_Option_Model) -> None:
        self.id: int = question_object.id
        self.question_id: int = question_object.question_id
        self.text: str = question_object.text
