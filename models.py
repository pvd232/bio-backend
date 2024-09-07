from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from helpers.get_db_connection_string import get_db_connection_string
import os
from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
from sqlalchemy.inspection import inspect
from sqlalchemy import asc
from sqlalchemy.dialects.postgresql import UUID

load_dotenv()

app = Flask(__name__)

# Env var from cloud run
env = os.getenv("DEPLOYMENT_ENV") or "debug"

db_username = os.getenv("DB_USER") or GCP_Secret_Manager_Service().get_secret("DB_USER")
db_password = os.getenv("DB_PASSWORD") or GCP_Secret_Manager_Service().get_secret(
    "DB_PASSWORD"
)
host = os.getenv("DB_HOST") or GCP_Secret_Manager_Service().get_secret("DB_HOST")
port = os.getenv("DB_PORT") or GCP_Secret_Manager_Service().get_secret("DB_PORT")
db_name = os.getenv("DB_NAME") or GCP_Secret_Manager_Service().get_secret("DB_NAME")

connection_string = get_db_connection_string(
    username=db_username,
    password=db_password,
    env=env,
    host=host,
    port=port,
    name=db_name,
)

app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


if env == "debug":
    from flask_cors import CORS

    CORS(app)

db = SQLAlchemy(app)


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class User_Model(BaseModel):
    __tablename__ = "user"
    id = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Admin_Model(BaseModel):
    __tablename__ = "admin"
    id = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Question_Option_Model(BaseModel):
    __tablename__ = "question_option"
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    question_id = db.Column(db.Integer(), db.ForeignKey("question.id"), nullable=False)
    text = db.Column(db.String(400), nullable=False)


class Question_Model(BaseModel):
    __tablename__ = "question"
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    text = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)

    options: Mapped[list[Question_Option_Model]] = relationship(
        "Question_Option_Model", lazy="joined"
    )

    def to_dict(self):
        result = super().to_dict()
        result["options"] = [option.to_dict() for option in self.options]
        return result


class Question_Response_Model(BaseModel):
    __tablename__ = "question_response"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)
    questionnaire_id = db.Column(
        db.Integer(), db.ForeignKey("questionnaire.id"), nullable=False
    )
    question_id = db.Column(db.Integer(), db.ForeignKey("question.id"), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    option_id = db.Column(
        db.Integer(), db.ForeignKey("question_option.id"), nullable=True
    )
    short_answer = db.Column(db.String(400), nullable=True)

    def to_dict(self):
        result = super().to_dict()
        return result


# Composite model for many-to-many relationship between Questionnaire and Question
class Questionnaire_Junction_Model(BaseModel):
    __tablename__ = "questionnaire_junction"
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    question_id = db.Column(db.Integer(), db.ForeignKey("question.id"), nullable=False)
    questionnaire_id = db.Column(
        db.Integer(),
        db.ForeignKey("questionnaire.id"),
        nullable=False,
    )
    priority = db.Column(db.Integer(), nullable=False)
    question: Mapped[Question_Model] = relationship("Question_Model", lazy="joined")

    def to_dict(self):
        result = super().to_dict()
        result["question"] = self.question.to_dict()
        return result


# One to many relationship between questionnaire and questionnaire junction
class Questionnaire_Model(BaseModel):
    __tablename__ = "questionnaire"
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    questionnaire_junction: Mapped[list[Questionnaire_Junction_Model]] = relationship(
        "Questionnaire_Junction_Model",
        lazy="joined",
        order_by=asc(
            Questionnaire_Junction_Model.priority
        ),  # Order questions by priority
    )

    def to_dict(self):
        result = super().to_dict()
        result["questionnaire_junction"] = [
            junction.to_dict() for junction in self.questionnaire_junction
        ]
        return result


# Allows for db.drop_all() to work by setting universal cascade
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"
