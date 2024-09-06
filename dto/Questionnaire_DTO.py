from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Questionnaire_Domain import Questionnaire_Domain


class Questionnaire_DTO(Base_DTO):
    def __init__(self, questionnaire_domain: "Questionnaire_Domain") -> None:
        self.id: int = questionnaire_domain.id
        self.name: str = questionnaire_domain.name
