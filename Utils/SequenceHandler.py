import datetime
import uuid

import BDD.Database as Database


def getSequenceByUuid(database: Database.Database, sequence_id: str) -> list[dict[str, str]]:
    get_sequence = {
        "where": [
            ["sequences", "id", sequence_id, "and"]
        ],
        "from": {
            "tables": ["sequences"]
        }
    }

    return database.query(get_sequence)


def getSessionSequenceByUuid(database: Database.Database, session_sequence_id: str) -> list[dict[str, str]]:
    get_session_sequence = {
        "where": [
            ["session_sequence", "id", session_sequence_id]
        ],
        "from": {
            "tables": ["session_sequence"]
        }
    }

    return database.query(get_session_sequence)


def addSequence(database: Database.Database, question_list: list, commit: bool = True) -> str:
    sequence_uuid: str = str(uuid.uuid4())

    while len(getSequenceByUuid(database, sequence_uuid)) > 0:
        sequence_uuid = str(uuid.uuid4())

    create_sequence = {
        "table": "sequences",
        "action": "insert",
        "valeurs": [
            ["id", sequence_uuid],
            ["created_at", datetime.datetime.now()]
        ]
    }

    database.execute(create_sequence)

    for question in question_list:
        id_question = question['id']

        insert_question_sequence = {
            "table": "question_sequence",
            "action": "insert",
            "valeurs": [
                ["question_id", id_question],
                ["sequence_id", sequence_uuid]
            ]
        }

        database.execute(insert_question_sequence)

    if commit:
        database.commit()

    return sequence_uuid


def getQuestionsBySequenceId(database: Database.Database, sequence_id: str) -> list[dict[str, str]]:
    get_sequence_questions = {
        "select": [
            ["questions", "id"],
            ["questions", "label"],
            ["questions", "enonce"],
            ["questions", "type"],
            ["questions", "user_id"],
            ["questions", "created_at"],
            ["questions", "updated_at"]
        ],
        "where": [
            ["sequences", "id", sequence_id]
        ],
        "from": {
            "tables": ["sequences", "question_sequence", "questions"],
            "cond": [
                [
                    ["sequences", "id"],
                    ["question_sequence", "sequence_id"]
                ],
                [
                    ["question_sequence", "question_id"],
                    ["questions", "id"]
                ]
            ]
        }
    }

    return database.query(get_sequence_questions)


def creerSession(database: Database.Database, sequence_id: str, session_sequence_code: str, commit: bool = True) -> str:
    session_sequence_uuid: str = str(uuid.uuid4())

    while len(getSessionSequenceByUuid(database, session_sequence_uuid)) > 0:
        session_sequence_uuid = str(uuid.uuid4())

    insert_session_sequence = {
        "table": "session_sequence",
        "action": "insert",
        "valeurs": [
            ["id", session_sequence_uuid],
            ["sequence_id", sequence_id],
            ["code", session_sequence_code],
            ["created_at", datetime.datetime.now()]
        ]
    }

    database.execute(insert_session_sequence)

    if commit:
        database.commit()

    return session_sequence_uuid