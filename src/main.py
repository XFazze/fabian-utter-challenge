from flask import Flask, render_template
from dotenv import load_dotenv
from os import getenv
from requests import get

load_dotenv()

# Initializing flask
app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = getenv("secret-key")


def create_user(summonerId: str, name: str, riot_name: str, riot_tag: str):
    api_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}?api_key={getenv('riot-token')}"

    rank_api = get(api_url)
    # app.logger.debug(api_url)
    res = {
        "name": name,
        "riot_name": f"{riot_name}#{riot_tag}",
        "opgg": f"https://www.op.gg/summoners/euw/{riot_name}-{riot_tag}",
    }
    # app.logger.debug(rank_api.status_code)
    if rank_api.status_code == 200:
        for rank in rank_api.json():

            if rank["queueType"] == "RANKED_SOLO_5x5":
                res["tier"] = rank["tier"]
                res["rank"] = rank["rank"]
                res["leaguePoints"] = rank["leaguePoints"]
                res["hotStreak"] = rank["hotStreak"]
                res["games"] = rank["wins"] + rank["losses"]
                res["wr"] = round(
                    100
                    * (
                        rank["wins"] / (rank["wins"] + rank["losses"])
                        if (rank["wins"] + rank["losses"]) != 0
                        else 0
                    )
                )
    # app.logger.debug(res)
    return res


@app.route("/")
def index():
    fabian_summonerId = "Sg9XI880vfFrXYfpBJaq2PxAeaoOaLO3sJh69NGPHv4JgjteqSRMNHeXGw"
    # utter_summonerId = "CjlfRa9w4LMXs2HFaJmZN7z52-PSxlVd2eU13zTUt9jwpgVu"
    utter_summonerId = "_tj833H4mvDeiajG95DpYoINt1jg0IXZBqQYmN6YAfBjFlYnTNujiRPtLA"

    return render_template(
        "index.html",
        players=[
            create_user(fabian_summonerId, "Fabian", "HAHAHA", "EUNEE"),
            create_user(utter_summonerId, "Utter", "utter THE butter", "EUW"),
        ],
    )


# Run the site
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
