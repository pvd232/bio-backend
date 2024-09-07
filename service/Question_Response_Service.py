from flask_sqlalchemy import SQLAlchemy
from dto.Question_Response_DTO import Question_Response_DTO


class Question_Response_Service:
    def get_question_responses(
        self, user_id: str, db: SQLAlchemy
    ) -> list[Question_Response_DTO]:
        from models import Question_Response_Model

        result: list[Question_Response_DTO] = []

        question_responses = (
            db.session.query(Question_Response_Model)
            .where(Question_Response_Model.user_id == user_id)
            .order_by(
                Question_Response_Model.user_id,
                Question_Response_Model.questionnaire_id,
                Question_Response_Model.question_id,
            )
            .all()
        )

        if len(question_responses) == 0:
            return result

        # For each user, create question response stats dto with user_id, response count and list of questionnaire response dtos
        # Each questionnaire response dto has a list of associated question response dtos
        prev_q_response_dto = Question_Response_DTO(model=question_responses[0])

        for i in range(1, len(question_responses)):
            curr_q_res = question_responses[i]
            # If multi answer and same question then add response
            if (
                curr_q_res.question_type == "mcq_multi"
                and curr_q_res.question_id == prev_q_response_dto.question_id
            ):
                prev_q_response_dto.add_option_id(option_id=curr_q_res.option_id)

            # Otherwise add curr q response to dto and set new one
            else:
                result.append(prev_q_response_dto)
                prev_q_response_dto = Question_Response_DTO(model=curr_q_res)

        result.append(prev_q_response_dto)
        return result
