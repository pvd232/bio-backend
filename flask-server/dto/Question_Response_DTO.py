from .Base_DTO import Base_DTO
from models import Question_Response_Model
from typing import Optional


# Data transfer object for Question Response, used to un-flatten the data in a way the client can understand
class Question_Response_DTO(Base_DTO):
    def __init__(self, model: Question_Response_Model) -> None:
        self.question_id: int = model.question_id
        self.type: str = model.question_type
        self.questionnaire_id: int = model.questionnaire_id
        self.user_id: str = model.user_id
        self.single_option_id: Optional[int] = None
        self.short_answer: Optional[str] = None
        self.multi_option_ids: Optional[list[int]] = None

        if self.type == "mcq":
            self.single_option_id = model.option_id

        elif self.type == "input":
            self.short_answer = model.short_answer

        else:
            self.multi_option_ids = [model.option_id]

    def add_option_id(self, option_id: int):
        self.multi_option_ids.append(option_id)

    def serialize(self) -> dict:
        return super().serialize()
