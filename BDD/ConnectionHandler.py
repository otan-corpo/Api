from BDD.Database import Database
from BDD.BDD_PSQL.PsqlDatabase import PsqlDatabase
from BDD.BDD_Fichiers.FichierDatabase import RequetesFormatTxt
from Erreurs.BDD import BDDNonPriseEnCharge

handlers = {"fichier": RequetesFormatTxt, "psql": PsqlDatabase}


def initiate(systeme: str, params: dict[str, str]) -> Database:
    if systeme.lower() not in handlers.keys():
        raise BDDNonPriseEnCharge

    return handlers.get(systeme.lower())(params["database"], params["url"], params["user"], params["password"], params["port"])
