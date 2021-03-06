from util import hook, http, timesince
from datetime import datetime

@hook.command('l', autohelp=False)
@hook.command(autohelp=False)
def lastfm(inp, nick='', say=None, db=None, bot=None):
    ".lastfm [user] [dontsave] -- Displays the now playing (or last played)" \
    " track of LastFM user [user]."
    api_key = bot.config.get("api_keys", {}).get("lastfm")
    if not api_key:
        return "error: no api key set"

    user = inp		
	
    api_url = "http://ws.audioscrobbler.com/2.0/?format=json"

    dontsave = user.endswith(" dontsave")
    if dontsave:
        user = user[:-9].strip().lower()

    db.execute("create table if not exists lastfm(nick primary key, acc)")

    if not user:
        user = db.execute("select acc from lastfm where nick=lower(?)",
                          (nick,)).fetchone()
        if not user:
            notice(lastfm.__doc__)
            return
        user = user[0]

    response = http.get_json(api_url, method="user.getrecenttracks",
                             api_key=api_key, user=user, limit=1)

    if 'error' in response:
        return "Error: %s." % response["message"]

    if not "track" in response["recenttracks"] or len(response["recenttracks"]["track"]) == 0:
        return 'No recent tracks for user "%s" found.' % user
		
    tracks = response["recenttracks"]["track"]

    if type(tracks) == list:
        # if the user is listening to something, the tracks entry is a list
        # the first item is the current track
        track = tracks[0]
        status = 'is listening to'
        ending = '.'
    elif type(tracks) == dict:
        # otherwise, they aren't listening to anything right now, and
        # the tracks entry is a dict representing the most recent track
        track = tracks
        status = 'last listened to'
        # lets see how long ago they listened to it
        time_listened = datetime.fromtimestamp(int(track["date"]["uts"]))
        time_since = timesince.timesince(time_listened)
        ending = ' (%s ago)' % time_since
        
    else:
        return "error: could not parse track listing"

    title = track["name"]
    album = track["album"]["#text"]
    artist = track["artist"]["#text"]

    out = '%s %s "%s"' % (user, status, title)
    if artist:
        out += " by \x02%s\x0f" % artist
    if album:
        out += " from the album \x02%s\x0f" % album
        
    # append ending based on what type it was
    out += ending
		
    if inp and not dontsave:
        db.execute("insert or replace into lastfm(nick, acc) values (?,?)",
                     (nick.lower(), user))
        db.commit()

    return out
