def seed_db():
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import (
        Questionnaire_Model,
        Question_Model,
        Question_Option_Model,
        Questionnaire_Junction_Model,
        User_Model,
        connection_string,
        db,
    )

    db.drop_all()
    db.create_all()
    from pathlib import Path
    import json

    # Load the CSV file into a Pandas DataFrame
    file_path = Path("biov.xlsx")

    sheets = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

    # Setup SQLAlchemy session
    engine = create_engine(connection_string)  # Update with your database URL
    Session = sessionmaker(bind=engine)
    session = Session()

    # Process the Questionnaire Junction Sheet
    junction_df = sheets.get("questionnaire_junction")
    for _, row in junction_df.iterrows():
        junction = Questionnaire_Junction_Model(
            id=int(row["id"]),  # Convert numpy.int64 to native int
            question_id=int(row["question_id"]),
            questionnaire_id=int(row["questionnaire_id"]),
            priority=int(row["priority"]),
        )
        session.add(junction)

    # Process the Questionnaires Sheet
    questionnaire_df = sheets.get("questionnaire_questionnaires")
    for _, row in questionnaire_df.iterrows():
        questionnaire = Questionnaire_Model(
            id=int(row["id"]), name=row["name"]  # Convert numpy.int64 to native int
        )
        session.add(questionnaire)

    # Process the Questions Sheet
    questions_df = sheets.get("questionnaire_questions")
    for _, row in questions_df.iterrows():
        question_data = json.loads(row["question"])
        if question_data.get("type") == "mcq" and "apply" in question_data.get(
            "question"
        ):
            question_type = "mcq_multi"
        else:
            question_type = question_data.get("type", "")
        question = Question_Model(
            id=int(row["id"]),  # Convert numpy.int64 to native int
            text=question_data.get("question", ""),
            type=question_type,
        )
        session.add(question)

        if question_data.get("type") == "mcq" and "options" in question_data:
            for option_text in question_data["options"]:
                option = Question_Option_Model(
                    question_id=int(row["id"]),  # Convert numpy.int64 to native int
                    text=option_text,
                )
                session.add(option)

    user_ids = ["a", "b", "c"]
    user_passwords = ["a", "b", "c"]
    for i in range(len(user_ids)):
        user = User_Model(id=user_ids[i], password=user_passwords[i], role="non-admin")
        session.add(user)

    admin_ids = ["d", "e", "f"]
    admin_passwords = ["d", "e", "f"]
    for i in range(len(admin_ids)):
        admin = User_Model(id=admin_ids[i], password=admin_passwords[i], role="admin")
        session.add(admin)
    # Commit the session to save everything in the database
    session.commit()

    # Close the session
    session.close()
