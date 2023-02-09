import psycopg2
import psycopg2.extras

import Utils.Dotenv as Dotenv
import BDD.BDD_PSQL.PsqlParsers as PsqlParsers
from BDD.Database import Database


class PsqlDatabase(Database):
    """
    Classe SqlDatabase héritant de Database et implémentant ses fonctions abstraites
    Offre query et execute comme interfaces communes et disponibles
    """
    sql_connection = None
    sql_cursor = None

    def __init__(self) -> None:
        """
        Initialise la connection à une base de données MySQL en fonction des paramètres fournis
        """

        database = Dotenv.getenv("DB_DBNAME")
        url = Dotenv.getenv("DB_ADDRESS")
        user = Dotenv.getenv("DB_USERNAME")
        password = Dotenv.getenv("DB_PASSWORD")
        port = Dotenv.getenv("DB_PORT")

        if None in [database, url, user, password, port]:
            raise EnvironmentError("Paramètre manquants dans .env")

        self.sql_connection = psycopg2.connect(database=database, host=url, user=user, password=password, port=port)
        self.sql_cursor = self.sql_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def __del__(self) -> None:
        """
        Ferme la connection à la base de données lors de la destruction de la classe (Fin du programme)
        :return:
        """
        pass
        # del self.sql_cursor
        # self.sql_connection.close()
        # del self.sql_connection

    def query(self, request) -> list[dict[str, str]]:
        """
        Execute une requête (de lecture) sur la base de donnée et renvoie une liste de dictionnaires
        Associant pour chaque ligne le nom de la colonne à la valeur
        :param request:
        :return:
        """
        sql_request = PsqlParsers.jsonToPsqlQuery(request)
        self.sql_cursor.execute(sql_request)
        self.sql_connection.commit()
        query_result = self.sql_cursor.fetchall()

        parsed_query_response = [{column_name: row[column_name] for column_name in row} for row in query_result]

        return parsed_query_response

    def execute(self, request) -> list:
        """
        Execute une requête (d'écriture) sur la base de donnée et renvoie une confirmation
        :param request:
        :return:
        """
        # TODO: Ajout de vérification au préalable
        sql_request = PsqlParsers.jsonToPsqlExecute(request)
        return self.sql_cursor.execute(sql_request)

    def commit(self):
        return self.sql_connection.commit()

    def lastVal(self):
        self.sql_cursor.execute("select lastval();")
        return self.sql_cursor.fetchone()[0]
