from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, distinct
from dto.Question_Response_Stats_DTO import Question_Response_Stats_DTO
from models import Question_Response_Model


class Response_Stats_Service:
    def get_questionnaire_totals(self, db: SQLAlchemy):
        stmt = select(
            Question_Response_Model.user_id,
            func.count(distinct(Question_Response_Model.questionnaire_id)),
        ).group_by(Question_Response_Model.user_id)
        result_list = db.session.execute(stmt).all()
        result_dict = {row[0]: row[1] for row in result_list}
        return result_dict

    def get_questionnaire_stats(
        self, db: SQLAlchemy
    ) -> list[Question_Response_Stats_DTO]:
        from dto.Question_Response_Stats_DTO import Question_Response_Stats_DTO
        from dto.Questionnaire_Response_DTO import Questionnaire_Response_DTO
        from dto.Question_Response_DTO import Question_Response_DTO

        question_responses = (
            db.session.query(Question_Response_Model)
            .order_by(
                Question_Response_Model.user_id,
                Question_Response_Model.questionnaire_id,
                Question_Response_Model.question_id,
            )
            .all()
        )

        if len(question_responses) == 0:
            return

        # For each user, create question response stats dto with user_id, response count and list of questionnaire response dtos
        # Each questionnaire response dto has a list of associated question response dtos
        totals = self.get_questionnaire_totals(db=db)
        prev_response_stats = Question_Response_Stats_DTO(
            user_id=question_responses[0].user_id,
            response_cnt=totals[question_responses[0].user_id],
        )

        prev_qnaire_dto = Questionnaire_Response_DTO(
            questionnaire_id=question_responses[0].questionnaire_id
        )
        prev_q_response_dto = Question_Response_DTO(model=question_responses[0])

        result: list[Question_Response_Stats_DTO] = []
        for i in range(1, len(question_responses)):
            curr_q_res = question_responses[i]
            # If user_id updates create new stats dto
            if curr_q_res.user_id != prev_response_stats.user_id:
                prev_qnaire_dto.add_response(response=prev_q_response_dto)
                prev_response_stats.add_response(response=prev_qnaire_dto)
                result.append(prev_response_stats)
                prev_response_stats = Question_Response_Stats_DTO(
                    user_id=curr_q_res.user_id,
                    response_cnt=totals[curr_q_res.user_id],
                )
                prev_qnaire_dto = Questionnaire_Response_DTO(
                    questionnaire_id=curr_q_res.questionnaire_id
                )
                prev_q_response_dto = Question_Response_DTO(model=curr_q_res)

            # If qnnaire id updates create new qnnaire dto
            elif curr_q_res.questionnaire_id != prev_qnaire_dto.questionnaire_id:
                prev_qnaire_dto.add_response(prev_q_response_dto)
                prev_response_stats.add_response(prev_qnaire_dto)
                prev_qnaire_dto = Questionnaire_Response_DTO(
                    questionnaire_id=curr_q_res.questionnaire_id
                )
                prev_q_response_dto = Question_Response_DTO(model=curr_q_res)
            # If multi answer and same question then add response
            elif curr_q_res.question_type == "mcq_multi":
                if curr_q_res.question_id == prev_q_response_dto.question_id:
                    prev_q_response_dto.add_option_id(option_id=curr_q_res.option_id)

                # Otherwise add curr q response to dto and set new one
                else:
                    prev_qnaire_dto.add_response(response=prev_q_response_dto)
                    prev_q_response_dto = Question_Response_DTO(model=curr_q_res)
            else:
                prev_qnaire_dto.add_response(response=prev_q_response_dto)
                prev_q_response_dto = Question_Response_DTO(model=curr_q_res)

        prev_qnaire_dto.add_response(prev_q_response_dto)
        prev_response_stats.add_response(prev_qnaire_dto)
        result.append(prev_response_stats)
        return result
        # add curr question response dto to curr qnnaire dto
