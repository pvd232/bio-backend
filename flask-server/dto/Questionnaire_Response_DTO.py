from .Base_DTO import Base_DTO
from dto.Admin_Question_Response_DTO import Admin_Question_Response_DTO


# Data transfer object for Question Response, used to un-flatten the data in a way the client can understand
class Questionnaire_Response_DTO(Base_DTO):
    def __init__(self, questionnaire_id: str) -> None:
        self.questionnaire_id: int = questionnaire_id
        self.question_responses: list[Admin_Question_Response_DTO] = []

    def add_response(self, response: Admin_Question_Response_DTO):
        self.question_responses.append(response)

    def serialize(self) -> dict:
        result = super().serialize()
        result["question_responses"] = [x.serialize() for x in self.question_responses]
        return result
