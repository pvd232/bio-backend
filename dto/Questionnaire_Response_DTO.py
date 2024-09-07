from .Base_DTO import Base_DTO
from dto.Question_Response_DTO import Question_Response_DTO


# Data transfer object for Question Response, used to un-flatten the data in a way the client can understand
class Questionnaire_Response_DTO(Base_DTO):
    def __init__(self, questionnaire_id: str) -> None:
        self.questionnaire_id = questionnaire_id
        self.question_response_dtos: list[Question_Response_DTO] = []

    def add_response(self, response: Question_Response_DTO):
        self.question_response_dtos.append(response)

    def serialize(self) -> dict:
        result = super().serialize()
        result["question_response_dtos"] = [
            x.serialize() for x in self.question_response_dtos
        ]
        return result
