from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from models import Questionnaire_Model


# Aggregates questions by questionnaire
class Questionnaire_DTO(Base_DTO):
    def __init__(self, questionnaire_model: "Questionnaire_Model") -> None:
        self.id: int = questionnaire_model.id
        self.name: str = questionnaire_model.name
        self.questions: list[dict] = [
            x.question.to_dict() for x in questionnaire_model.questionnaire_junction
        ]

    def serialize(self) -> dict:
        return super().serialize()
