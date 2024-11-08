from flask import Blueprint, request, jsonify, current_app
import psycopg
import psycopg.rows

database_service = Blueprint("database", __name__)

def connect_postgres() -> psycopg.Connection[psycopg.rows.TupleRow]:
    database_client = psycopg.connect(
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        dbname=current_app.config["POSTGRES_DB"],
        row_factory=psycopg.rows.dict_row
    )
    return database_client

@database_service.route("/create_table", methods=["POST"])
def create_table():
    with connect_postgres() as client:
        cursor = client.cursor()
        cursor.execute(
            "CREATE TABLE classes (id UUID PRIMARY KEY, name TEXT)"
        )
    return jsonify({"message": "Table created successfully"}), 201

@database_service.route("/get_table", methods=["GET"])
def get_table():
    with connect_postgres() as client:
        cursor = client.cursor()
        cursor.execute("SELECT * FROM classes")
        return jsonify(cursor.fetchall())

@database_service.route("/add_class", methods=["POST"])
def add_class():
    with connect_postgres() as client:
        cursor = client.cursor()
        data = request.form
        cursor.execute(
            "INSERT INTO classes (id, name) VALUES (gen_random_uuid(), %s)",
            (data.get("class"),)
        )
    return jsonify({"message": "Class added successfully"}), 201
