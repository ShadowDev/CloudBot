from util import hook, http


def find_location(ip, api):
    response = http.get("http://api.ipinfodb.com/v3/ip-city/", key=api, ip=ip)
    response = response.split(";")
    results = {}
    results["country"] = response[4].title()
    results["country_short"] = response[3].upper()
    results["state"] = response[5].title()
    results["city"] = response[6].title()
    results["timezone"] = response[10].title()
    return results


def timezone(ip):
    time = find_location(ip)["timezone"]
    time = time.replace(":", ".")
    time = time.replace(".00", "")
    return int(time)


@hook.command
@hook.command("location")
def geoip(inp, say=None, bot=None):
    ".geoip <ip> - Performs a location check on <ip>."
    api_key = bot.config.get("api_keys", {}).get("geoip", None)
    if api_key is None:
        return "error: no api key set"

    give = find_location(inp, api_key)
    if give["country"] not in ["", " ", "-", " - ", None]:
        if give["state"] == give["city"]:
            localstring = give["city"]
        else:
            localstring = give["city"] + ", " + give["state"]
        say("That IP comes from " + give["country"] +
        " (" + give["country_short"] + ")")
        say("I think it's in " + localstring +
        " with a timezone of " + give["timezone"] + "GMT")
    else:
        say("Either that wasn't an IP or I cannot locate it in my database.")
    return
