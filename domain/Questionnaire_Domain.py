from .Base_Domain import Base_Domain
from models import Questionnaire_Model


class Questionnaire_Domain(Base_Domain):
    def __init__(self, questionnaire_domain_object: Questionnaire_Model) -> None:
        self.id: int = questionnaire_domain_object.id
        self.name: str = questionnaire_domain_object.name
