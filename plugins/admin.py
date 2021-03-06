# Plugin made by iloveportalz0r, TheNoodle, Lukeroge and neersighted
from util import hook
import os
import re
import sys
import json
import time
import subprocess


@hook.command(autohelp=False)
def admins(inp, notice=None, bot=None):
    ".admins -- Lists bot's admins."
    if bot.config["admins"]:
        notice("Admins are: %s." % ", ".join(bot.config["admins"]))
    else:
        notice("No users are admins!")
    return


@hook.command(adminonly=True)
def addadmin(inp, notice=None, bot=None, config=None):
    ".addadmin <nick|host> -- Make <nick|host> an admin. " \
    "(you can add multiple admins at once)"
    targets = inp.split()
    for target in targets:
        if target in bot.config["admins"]:
            notice("%s is already an admin." % target)
        else:
            notice("%s is now an admin." % target)
            bot.config["admins"].append(target)
            bot.config["admins"].sort()
            json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return


@hook.command(adminonly=True)
def deladmin(inp, notice=None, bot=None, config=None):
    ".deladmin <nick|host> -- Make <nick|host> a non-admin." \
    "(you can delete multiple admins at once)"
    targets = inp.split()
    for target in targets:
        if target in bot.config["admins"]:
            notice("%s is no longer an admin." % target)
            bot.config["admins"].remove(target)
            bot.config["admins"].sort()
            json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
        else:
            notice("%s is not an admin." % target)
    return


@hook.command(autohelp=False)
def channels(inp, conn=None):
    ".channels -- Lists the channels that the bot is in."
    return "I am in these channels: %s" % ", ".join(conn.channels)


@hook.command("quit", autohelp=False, adminonly=True)
@hook.command(autohelp=False, adminonly=True)
def stop(inp, nick=None, conn=None):
    ".stop [reason] -- Kills the bot with [reason] as its quit message."
    if inp:
        conn.cmd("QUIT", ["Killed by %s (%s)" % (nick, inp)])
    else:
        conn.cmd("QUIT", ["Killed by %s." % nick])
    time.sleep(5)
    os.execl("./cloudbot", "cloudbot", "stop")


@hook.command(autohelp=False, adminonly=True)
def restart(inp, nick=None, conn=None):
    ".restart [reason] -- Restarts the bot with [reason] as its quit message."
    if inp:
        conn.cmd("QUIT", ["Restarted by %s (%s)" % (nick, inp)])
    else:
        conn.cmd("QUIT", ["Restarted by %s." % nick])
    time.sleep(5)
    os.execl("./cloudbot", "cloudbot", "restart")


@hook.command(autohelp=False, adminonly=True)
def clearlogs(inp, input=None):
    ".clearlogs -- Clears the bots log(s)."
    subprocess.call(["./cloudbot", "clear"])


@hook.command(adminonly=True)
def join(inp, conn=None, notice=None):
    ".join <channel> -- Joins <channel>."
    notice("Attempting to join %s..." % inp)
    conn.join(inp)


@hook.command(autohelp=False, adminonly=True)
def part(inp, conn=None, chan=None, notice=None):
    ".part <channel> -- Leaves <channel>." \
    "If [channel] is blank the bot will leave the " \
    "channel the command was used in."
    if inp:
        target = inp
    else:
        target = chan
    notice("Attempting to leave %s..." % target)
    conn.part(target)


@hook.command(autohelp=False, adminonly=True)
def cycle(inp, conn=None, chan=None, notice=None):
    ".cycle <channel> -- Cycles <channel>." \
    "If [channel] is blank the bot will cycle the " \
    "channel the command was used in."
    if inp:
        target = inp
    else:
        target = chan
    notice("Attempting to cycle %s..." % target)
    conn.part(target)
    conn.join(target)


@hook.command(adminonly=True)
def nick(inp, input=None, notice=None, conn=None):
    ".nick <nick> -- Changes the bots nickname to <nick>."
    if not re.match("^[A-Za-z0-9_|.-\]\[]*$", inp.lower()):
        notice("Invalid username!")
        return
    notice("Attempting to change nick to \"%s\"..." % inp)
    conn.set_nick(inp)


@hook.command(adminonly=True)
def raw(inp, conn=None, notice=None):
    ".raw <command> -- Sends a RAW IRC command."
    notice("Raw command sent.")
    conn.send(inp)


@hook.command(adminonly=True)
def say(inp, conn=None, chan=None, notice=None):
    ".say [channel] <message> -- Makes the bot say <message> in [channel]. " \
    "If [channel] is blank the bot will say the <message> in the channel " \
    "the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        message = ""
        for x in inp[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (inp[0], message)
    else:
        message = ""
        for x in inp[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (chan, message)
    conn.send(out)


@hook.command("act", adminonly=True)
@hook.command(adminonly=True)
def me(inp, conn=None, chan=None, notice=None):
    ".me [channel] <action> -- Makes the bot act out <action> in [channel]. " \
    "If [channel] is blank the bot will act the <action> in the channel the " \
    "command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        message = ""
        for x in inp[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION %s\x01" % (inp[0], message)
    else:
        message = ""
        for x in inp[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION %s\x01" % (chan, message)
    conn.send(out)
