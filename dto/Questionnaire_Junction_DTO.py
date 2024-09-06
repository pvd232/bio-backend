from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Questionnaire_Junction_Domain import Questionnaire_Junction_Domain
    from .Question_DTO import Question_DTO
    from .Questionnaire_DTO import Questionnaire_DTO


class Questionnaire_Junction_DTO(Base_DTO):
    def __init__(
        self, questionnaire_junction_domain: "Questionnaire_Junction_Domain"
    ) -> None:
        self.id: int = questionnaire_junction_domain.id
        self.question_id: int = questionnaire_junction_domain.question_id
        self.questionnaire_id: int = questionnaire_junction_domain.questionnaire_id
        self.priority: int = questionnaire_junction_domain.priority
        self.questions: list[Question_DTO] = questionnaire_junction_domain.questions
        self.questionnaires: list[Questionnaire_DTO] = [
            Questionnaire_DTO(questionnaire_domain=x)
            for x in questionnaire_junction_domain.questionnaires
        ]
