from flask_sqlalchemy import SQLAlchemy
from dto.Question_Response_DTO import Question_Response_DTO
from models import Question_Response_Model


class Question_Response_Service:
    def group_multi_responses(
        self,
        responses: list[Question_Response_Model],
    ) -> list[Question_Response_DTO]:
        filtered_responses: list[Question_Response_Model] = []
        multi_question = {}
        for response in responses:
            # If the question is a multi-option question, we need to group the option_ids by question_id
            if response.question_id not in multi_question:
                multi_question[response.question_id] = (
                    []
                )  # Initialize list of unique multi-option questions
                filtered_responses.append(response)  # Add the response to the list
            # Append the option_id to the list regardless of whether the question_id is already in the dictionary
            multi_question[response.question_id].append(response.option_id)
        # Convert to a list of dictionaries
        result_list = [Question_Response_DTO(model=x) for x in filtered_responses]

        # Add the multi_option_ids to the Question_Response_DTO objects and remove the single_option_id
        for item in result_list:
            item.multi_option_ids = multi_question[item.question_id]

        return result_list

    def get_question_responses(
        self, user_id: str, db: SQLAlchemy
    ) -> list[Question_Response_DTO]:
        from models import Question_Response_Model

        mcq_select_all_question_responses = (
            db.session.query(Question_Response_Model)
            .filter(
                Question_Response_Model.user_id == user_id,
                Question_Response_Model.question_type == "mcq_multi",
            )
            .all()
        )
        multi_response_dtos = self.group_multi_responses(
            responses=mcq_select_all_question_responses
        )
        other_responses = (
            db.session.query(Question_Response_Model)
            .filter(
                Question_Response_Model.user_id == user_id,
                Question_Response_Model.question_type != "mcq_multi",
            )
            .all()
        )

        other_response_dtos = [Question_Response_DTO(model=x) for x in other_responses]
        all_dtos = multi_response_dtos + other_response_dtos
        return all_dtos
