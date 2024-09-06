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
        .filter(User_Model.id == creds["id"], User_Model.password == creds["password"])
        .first()
    )
    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "Login successful"})


@app.route("/api/questionnaire_junction", methods=["GET"])
def get_questionnaire_junction() -> Response:
    from models import Questionnaire_Model
    from dto.Questionnaire_Compressed_DTO import Questionnaire_Compressed_DTO

    questionnaire_junctions = db.session.query(Questionnaire_Model).all()

    # Convert to a list of dictionaries
    result_list = [
        Questionnaire_Compressed_DTO(x).serialize() for x in questionnaire_junctions
    ]

    return jsonify(result_list)


@app.route("/api/question_response", methods=["POST"])
def post_question_response() -> Response:
    from models import Question_Response_Model

    data = request.json  # Assuming data is a list of dictionaries

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of question responses"}), 400

    # List to hold the created Question_Response_Model objects
    responses = []
    print("data", data)
    for item in data:
        if item["multiOptionIds"] != None:
            for option_id in item["multiOptionIds"]:
                try:
                    # Validate and parse each item in the array
                    question_response = Question_Response_Model(
                        id=uuid4(),
                        user_id=item["userId"],
                        question_type=item["type"],
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


@app.route("/api/question_response/<string:id>", methods=["GET"])
def get_question_response(id) -> Response:
    from models import Question_Response_Model
    from dto.Question_Response_DTO import Question_Response_DTO

    question_responses = (
        db.session.query(Question_Response_Model)
        .filter(Question_Response_Model.user_id == id)
        .all()
    )

    filtered_responses: list[Question_Response_Model] = []
    question_dict = {}
    for response in question_responses:
        if response.question_type == "mcq_multi":
            # If the question is a multi-option question, we need to group the option_ids by question_id
            if response.question_id not in question_dict:
                question_dict[response.question_id] = []  # Initialize the list
                filtered_responses.append(response)  # Add the response to the list
            # Append the option_id to the list regardless of whether the question_id is already in the dictionary
            question_dict[response.question_id].append(response.option_id)
        else:
            filtered_responses.append(response)

    # Convert to a list of dictionaries
    result_list = [Question_Response_DTO(json=x.to_dict()) for x in filtered_responses]

    # Add the multi_option_ids to the Question_Response_DTO objects
    for item in result_list:
        if item.question_id in question_dict:
            item.multi_option_ids = question_dict[item.question_id]

    return jsonify([x.serialize() for x in result_list])


if env == "debug":
    debug = True
else:
    debug = False

PORT = os.environ.get("PORT", 4000)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=debug)
