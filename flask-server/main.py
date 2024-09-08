from models import app, db, env
from flask import (
    Response,
    request,
    jsonify,
)
import os
import json
from werkzeug.exceptions import HTTPException
from uuid import uuid4


@app.errorhandler(404)
def not_found(e) -> Response:
    log_text = (
        "404 not found, requested url:"
        + str(request.path)
        + " method:"
        + str(request.method)
        + "error:"
        + str(e)
    )
    return Response(status=404, response=json.dumps(log_text))


@app.errorhandler(500)
def handle_exception(e) -> HTTPException | Response:
    res = {
        "code": 500,
        "errorType": "Internal Server Error",
        "errorMessage": "Something went really wrong!",
    }
    res["errorMessage"] = e.message if hasattr(e, "message") else f"{e}"
    return Response(status=500, response=json.dumps(res))


@app.route("/api/seed_db", methods=["GET"])
def seed_db() -> Response:
    from seed import seed_db

    seed_db()
    return jsonify({"message": "Database seeded successfully!"})


@app.route("/api/login", methods=["POST"])
def login() -> Response:
    from models import User_Model

    creds = request.json
    user = (
        db.session.query(User_Model)
        .filter(
            User_Model.id == creds["id"],
            User_Model.password == creds["password"],
            User_Model.role == creds["role"],
        )
        .first()
    )
    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "Login successful"})


@app.route("/api/questionnaire_junction", methods=["GET"])
def get_questionnaire_junction() -> Response:
    from models import Questionnaire_Model
    from dto.Questionnaire_DTO import Questionnaire_DTO

    questionnaires = db.session.query(Questionnaire_Model)

    # Convert to a list of dictionaries
    result_list = [Questionnaire_DTO(x).serialize() for x in questionnaires]

    return jsonify(result_list)


@app.route("/api/question_response", methods=["POST"])
def post_question_response() -> Response:
    from models import Question_Response_Model

    data = request.json  # Assuming data is a list of dictionaries

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of question responses"}), 400

    # List to hold the created Question_Response_Model objects
    responses = []
    for item in data:
        if item["type"] == "mcq_multi":
            for option_id in item["multiOptionIds"]:
                try:
                    # Validate and parse each item in the array
                    question_response = Question_Response_Model(
                        id=uuid4(),
                        user_id=item["userId"],
                        question_type=item["type"],
                        questionnaire_id=item["questionnaireId"],
                        question_id=item["questionId"],
                        option_id=option_id,
                        short_answer=item["shortAnswer"],
                    )
                    responses.append(question_response)
                except KeyError as e:
                    return jsonify({"error": f"Missing key: {e}"}), 400
        else:
            try:
                # Validate and parse each item in the array
                question_response = Question_Response_Model(
                    id=uuid4(),
                    user_id=item["userId"],
                    question_type=item["type"],
                    questionnaire_id=item["questionnaireId"],
                    question_id=item["questionId"],
                    option_id=item["singleOptionId"],
                    short_answer=item["shortAnswer"],
                )
                responses.append(question_response)
            except KeyError as e:
                return jsonify({"error": f"Missing key: {e}"}), 400
        # Frontend uses camelCase

    # Add all the responses to the session
    db.session.add_all(responses)

    try:
        # Commit the session to save to the database
        db.session.commit()
    except Exception as e:
        print("e", e)
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Question responses saved successfully"}), 201


@app.route("/api/question_response/<string:user_id>", methods=["GET"])
def get_question_response(user_id: str) -> Response:
    from service.Question_Response_Service import Question_Response_Service
    from dto.Question_Response_DTO import Question_Response_DTO

    response_dtos: list[Question_Response_DTO] = (
        Question_Response_Service().get_question_responses(user_id=user_id, db=db)
    )
    return jsonify([x.serialize() for x in response_dtos])


@app.route("/api/questionnaire_stats", methods=["GET"])
def questionnaire_stats() -> Response:
    from service.Questionnaire_Stats_Service import Questionnaire_Stats_Service

    response = [
        x.serialize()
        for x in Questionnaire_Stats_Service().get_questionnaire_stats(db=db)
    ]
    return jsonify(response)


if env == "debug":
    debug = True
else:
    debug = False

PORT = os.environ.get("PORT", 4000)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=debug)
