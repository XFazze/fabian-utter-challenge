import datetime
from flask import Flask, render_template
from dotenv import load_dotenv
from os import getenv
from requests import get

load_dotenv()

# Initializing flask
app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = getenv("secret-key")


def create_user(
    summonerId: str, name: str, riot_name: str, riot_tag: str, server: str = "euw1"
):

    api_url = f"https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}?api_key={getenv('riot-token')}"

    rank_api = get(api_url)
    app.logger.debug(api_url)
    res = {
        "name": name,
        "riot_name": f"{riot_name}#{riot_tag}",
        "opgg": f"https://www.op.gg/summoners/euw/{riot_name}-{riot_tag}",
    }
    app.logger.debug(rank_api.status_code)
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
    fabian= create_user("46dvXDw9AnOvX2DMT_KPBX6bLbzQSleAaz9N8HzOfq77QSwvQv0wuMZlfg", "Fabian", "smile", "abv")
    utter = create_user("8gyVZAgG6WX-vlWDzDC9OL7225X4v1ojVp_3WBvllzDtlGRN", "Utter", "utter THE butter", "EUW")
    tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM" "EMERALD", "DIAMOND"]
    ranks = ["IIII", "III", "II", "I"]
    if tiers.index(fabian["tier"]) > tiers.index(utter["tier"]):
        leader="Fabian"
    elif tiers.index(fabian["tier"]) < tiers.index(utter["tier"]):
        leader="Utter"
    else:
        if ranks.index(fabian["rank"]) > ranks.index(utter["rank"]):
            leader="Fabian"
        elif ranks.index(fabian["rank"]) < ranks.index(utter["rank"]):
            leader="Utter"
        else:
            leader="Abbe"
    return render_template(
        "index.html",
        top_players=[fabian, utter],
        leader=leader,
        all_players=[
            create_user("GVDwScE54s3NBg12lnP_L6DQkfMLtvy3pWeS-dmrXvhEmhE0", "Simon", "mimass", "EUW"),
            create_user("rGakeiLsBxijLA-6trktG_xgxDM1R9cQkNz2blNsw0YxEAKg", "Chris", "twice is mommy", "ff15"),
            create_user("94r6TxbdgBHMQue8jUOyDhkp-h2TBIIZ9JSCFKEBm0-fgdED", "Rasmus", "Ñix", "EUW"),
            create_user("96KBRzJFbDhz9ohTf-9oyFxPPbu7eQzC6MR8_3FXsD_EgFbnneIBaHiWRw", "Noel", "im alright", "0000"),
            create_user(
                "3k_jQlYfSjBhW4a7Aly9nxmgYdo5VicbUBe8rjM0oKXpCc0", "Alex", "godslayerenryu", "EUNE", server="eun1"
            ),
            create_user("1CYBGll9W0iE6AeAUX4LslgLHV2cxLj1VpmRP7LTiX5e2cpyJ1LkdQ9dRQ", "Ivorn", "ENJOYABLEGAME123", "SPIR"),
            create_user("ZMqekpd_Vz2FqEjJv_k8HDYQ0kJw8Ge1y8FSgD-42ck1C7_s", "Olof", "vG0Dv", "EUW"),
            create_user("ZGJASbYaYTPb0bai9k1KDD-4co8APgUJtZJv3sVCWXdIyqHrGtuK84rDzg", "Leo", "krokodil mobil", "EUW"),
            create_user(
                "bBsykldkThylOk5bIoz9KpRDpMXIvzQYPZV-MQxabouRz4s", "Abbe", "Trockeltum", "0003", server="eun1"
            ),
            create_user("fykH-mYEG7zCH5hW3Qvqs7TVDqBvnPYY8iey9ugWMULVBMHg", "Robin", "Búck", "EUW"),
            create_user(
                "UVpPLaF5f7-g-Q52XaO8PG8g84bOInSt3EGag4-w7G0Ib4s", "Emelie", "notemser10", "8567", server="eun1"
            ),
            create_user(
                "LP-3QxijR2qsRVCknITKRb3QhwRrn8ufSD9s3c6ApM42yIw", "Johanna", "jechir", "EUNE", server="eun1"
            ),
            create_user("PaoeorEzZpEgeY1DyADI3eIbADRdsgvnUC3AVSyXdmRxXEjAgLng8GkSnQ", "Maddie", "TwoGirlsOneTeemo", "0000"),
        ],
    )


# Run the site
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
