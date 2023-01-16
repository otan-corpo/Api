import flask
import os


def main(route: str, app: flask.Flask) -> None:
    def me() -> dict[str, str]:
        return {"a": "b"}

    filename = os.path.basename(__file__)[:-3]
    url = f"{route}{filename.lower()}"

    print(f"{filename} !\tRoute : {url}/")
    app.route(url)(me)