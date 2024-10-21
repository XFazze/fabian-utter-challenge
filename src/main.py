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
    summoner_id = {
        "fabian": "Sg9XI880vfFrXYfpBJaq2PxAeaoOaLO3sJh69NGPHv4JgjteqSRMNHeXGw",
        "utter": "CjlfRa9w4LMXs2HFaJmZN7z52-PSxlVd2eU13zTUt9jwpgVu",
        "noel": "z8OdNeGyWZ9ygC6OguFNsizZaSGhgxdg1giLqJeGkPWHPLvgDQhU20r5Dg",
        "olof": "8gv_pVLgDvmEGfLBnJUE554z3REvEkknBoTpqhe9wcVtmZhX",
        "ivorn": "0uoMgTHxBamOKxLCe8vWmwGxdyCmfGjYwZYJcRSyWmEwlbVkaxK6rB_N8A",
        "chris": "5tV5tzsUI9iako8U3OwGMbAXgfqwiBr9GvoaI3aCa0-zHEEX",
        "nix": "AgN3PBU6E98Fl6Gw2vEPQx5Z6uirglao2lcaX-HAlFPEMtHu",
        "octo": "CFMnuiVGdtzmdeWkJK-fJRshV3II2FUXWamrHR-Sl6eEYcHU",
        "abbe": "rGhM39SwatdCI8MMlwlFNQJ3GGPnCPNxqq9WMlaIzdw4OlI",
        "leo": "nmbjtla69-VM-0IVtbgJ6skxP6PDQZa_3imnDmNUfC9G-S0",
        "alex": "k7woLZsse5G2yMMecun2gtr00A5F0mhr8QCEdy-qO_WGTiE",
        "emser": "PSqliQsYNxzU5mEBVlgMKI4F5RGVgb1ls9Bs2kfw6K0L27s",
        "johanna": "lammjKiWJ_0BmUyLPlACs-ZXBH8VkjkB0FjuJE7y9kU1f5E",
    }
    return render_template(
        "index.html",
        top_players=[
            create_user(summoner_id["fabian"], "Fabian", "HAHAHA", "EUNEE"),
            create_user(summoner_id["noel"], "Utter", "utter THE butter", "EUW"),
        ],
        all_players=[
            create_user(summoner_id["noel"], "Noel", "im alright", "0000"),
            create_user(summoner_id["olof"], "Olof", "vG0Dv", "EUW"),
            create_user(summoner_id["ivorn"], "Ivorn", "ENJOYABLEGAME123", "SPIR"),
            create_user(summoner_id["chris"], "Chris", "twice is mommy", "ff15"),
            create_user(summoner_id["nix"], "Rasmus", "Ñix", "EUW"),
            create_user(summoner_id["octo"], "Simon", "mimass", "EUW"),
            create_user(
                summoner_id["abbe"], "Abbe", "Trockeltum", "0003", server="eun1"
            ),
            create_user(summoner_id["leo"], "Leo", "Leo", "12333", server="eun1"),
            create_user(
                summoner_id["alex"], "Alex", "godslayerenryu", "EUNE", server="eun1"
            ),
            create_user(
                summoner_id["emser"], "Emelie", "notemser10", "8567", server="eun1"
            ),
            create_user(
                summoner_id["johanna"], "Johanna", "jechir", "EUNE", server="eun1"
            ),
        ],
    )


# Run the site
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
