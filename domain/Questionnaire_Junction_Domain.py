from .Base_Domain import Base_Domain
from models import Questionnaire_Junction_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Question_Domain import Question_Domain
    from domain.Questionnaire_Domain import Questionnaire_Domain


class Questionnaire_Junction_Domain(Base_Domain):
    def __init__(
        self, questionnaire_junction_object: Questionnaire_Junction_Model
    ) -> None:
        self.id: int = questionnaire_junction_object.id
        self.question_id: int = questionnaire_junction_object.question_id
        self.questionnaire_id: int = questionnaire_junction_object.questionnaire_id
        self.priority: int = questionnaire_junction_object.priority
        self.questions: list[Question_Domain] = [
            Question_Domain(question_object=x)
            for x in questionnaire_junction_object.questions
        ]
        self.questionnaires: list[Questionnaire_Domain] = [
            Questionnaire_Domain(questionnaire_object=x)
            for x in questionnaire_junction_object.questionnaires
        ]
