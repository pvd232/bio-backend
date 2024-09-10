from .Base_DTO import Base_DTO
from dto.Questionnaire_Response_DTO import Questionnaire_Response_DTO


# Data transfer object for Question Response, used to un-flatten the data in a way the client can understand
class Question_Response_Stats_DTO(Base_DTO):
    def __init__(self, user_id: str, response_cnt: int) -> None:
        self.user_id: str = user_id
        self.count: int = response_cnt
        self.questionnaire_responses: list[Questionnaire_Response_DTO] = []

    def add_response(self, response: Questionnaire_Response_DTO):
        self.questionnaire_responses.append(response)

    def serialize(self):
        result = super().serialize()
        result["questionnaire_responses"] = [
            x.serialize() for x in self.questionnaire_responses
        ]
        return result
