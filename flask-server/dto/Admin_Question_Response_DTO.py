from .Question_Response_DTO import Question_Response_DTO
from models import Question_Response_Model
from typing import Optional


# Data transfer object for Question Response, used to un-flatten the data in a way the client can understand
class Admin_Question_Response_DTO(Question_Response_DTO):
    def __init__(self, model: Question_Response_Model) -> None:
        super().__init__(model=model)
        self.question_text = model.question.text
        self.option_text = None
        self.multi_options: Optional[list[str]] = None

        if self.type == "mcq":
            self.option_text = model.option.text
        elif self.type == "input":
            self.option_text = model.short_answer
        else:
            self.multi_options = [model.option.text]

    def add_option_text(self, option_text: str):
        self.multi_options.append(option_text)

    def serialize(self) -> dict:
        return super().serialize()
