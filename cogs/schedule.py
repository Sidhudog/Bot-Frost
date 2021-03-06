import traceback
from datetime import datetime

import dateutil.parser
import discord
import pytz
import requests
from discord.ext import commands

from utils.consts import CD_GLOBAL_RATE, CD_GLOBAL_PER, CD_GLOBAL_TYPE
from utils.embed import build_schedule_embed

leagueDict = {
    'top25': 0,
    'acc': 1,
    'american': 151,
    'big12': 4,
    'b12': 4,
    'big10': 5,
    'b10': 5,
    'sec': 8,
    'pac12': 9,
    'p12': 9,
    'mac': 15,
    'independent': 18
}
cfbWeeks = [
    datetime(2019, 1, 1),
    datetime(2019, 9, 2),
    datetime(2019, 9, 9),
    datetime(2019, 9, 16),
    datetime(2019, 9, 23),
    datetime(2019, 9, 30),
    datetime(2019, 10, 7),
    datetime(2019, 10, 14),
    datetime(2019, 10, 21),
    datetime(2019, 10, 28),
    datetime(2019, 11, 4),
    datetime(2019, 11, 11),
    datetime(2019, 11, 18),
    datetime(2019, 11, 25),
    datetime(2019, 12, 2)
]
nflWeeks = [
    datetime(2019, 1, 1),
    datetime(2019, 9, 11),
    datetime(2019, 9, 18),
    datetime(2019, 9, 25),
    datetime(2019, 10, 2),
    datetime(2019, 10, 9),
    datetime(2019, 10, 16),
    datetime(2019, 10, 23),
    datetime(2019, 10, 30),
    datetime(2019, 10, 6),
    datetime(2019, 11, 13),
    datetime(2019, 11, 20),
    datetime(2019, 11, 27),
    datetime(2019, 12, 4),
    datetime(2019, 12, 11),
    datetime(2019, 12, 18),
    datetime(2019, 12, 25)
]


def hex_to_rgb(_hex):
    new_hex = _hex.lstrip("#")
    hlen = len(new_hex)
    rgb = tuple(int(new_hex[i:i + hlen // 3], 16) for i in range(0, hlen, int(hlen // 3)))
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    c = discord.Colour.from_rgb(r=r, g=g, b=b)
    return c


class ScheduleCommands(commands.Cog, name="Scheduling Commands"):
    @commands.group(aliases=["sched"])
    @commands.cooldown(rate=CD_GLOBAL_RATE, per=CD_GLOBAL_PER, type=CD_GLOBAL_TYPE)
    async def schedule(self, ctx):
        """ [year|week] Nebraska's football schedule """
        if not ctx.invoked_subcommand:
            from utils.client import client
            raise AttributeError(f"Missing a subcommand. Review '{client.command_prefix}help {ctx.command.qualified_name}' to view subcommands.")

    @schedule.command()
    @commands.cooldown(rate=CD_GLOBAL_RATE, per=CD_GLOBAL_PER, type=CD_GLOBAL_TYPE)
    async def year(self, ctx, year=datetime.now().year):
        """ Specific year of Nebraska's football schedule """
        edit_msg = await ctx.send("Loading...")
        await edit_msg.edit(content="", embed=build_schedule_embed(year))

    @schedule.command()
    @commands.cooldown(rate=CD_GLOBAL_RATE, per=CD_GLOBAL_PER, type=CD_GLOBAL_TYPE)
    async def week(self, ctx, which_week, which_year=datetime.now().year):
        """ Specific week in a specific year of Nebraska's schedule"""
        edit_msg = await ctx.send("Loading...")

        await edit_msg.edit(content="", embed=build_schedule_embed(which_year, week=which_week))

    @commands.command()  ## Jeyrad's code ###
    @commands.cooldown(rate=CD_GLOBAL_RATE, per=CD_GLOBAL_PER, type=CD_GLOBAL_TYPE)
    async def cfb(self, ctx, league='top25', week=-1, year=datetime.now().year):
        """Returns a schedule w/ scores (if in past or in progress) from ESPN for a given league, week and year.
        Usage is: `cfbsched <league> <week> <year>"""

        leagueInt = leagueDict.get(league.lower(), 0)

        if week == -1:
            week = self.getCurrentWeek(cfbWeeks)

        url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard" \
              f"?lang=en&region=us&calendartype=blacklist&limit=300&dates={year}&seasontype=2&week={week}"

        if leagueInt > 0:
            url += f"&groups={leagueInt}"

        try:
            r = requests.get(url)
            sched_json = r.json()
            response = self.build_scoreboard_response(sched_json["events"])
            await ctx.send(response)

        except:
            await ctx.send("An error occurred retrieving schedule data from ESPN.")
            traceback.print_exc()
            return

    @commands.command()
    @commands.cooldown(rate=CD_GLOBAL_RATE, per=CD_GLOBAL_PER, type=CD_GLOBAL_TYPE)
    async def nfl(self, ctx, week=-1, year=datetime.now().year):
        """ Returns a schedule w/ scores (if in past or in progress) from ESPN for a given week and year.
        Usage is: `nflsched <week> <year>"""

        if week == -1:
            week = self.getCurrentWeek(nflWeeks)

        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard" \
              f"?lang=en&region=us&calendartype=blacklist&limit=100&dates={year}&seasontype=2&week={week}"

        try:
            r = requests.get(url)
            sched_json = r.json()
            response = self.build_scoreboard_response(sched_json["events"])
            await ctx.send(response)

        except:
            await ctx.send("An error occurred retrieving schedule data from ESPN.")
            traceback.print_exc()
            return

    def build_scoreboard_response(self, events):
        if len(events) == 0:
            return "No events appear to be scheduled."

        response = '```prolog'
        current_date = ''
        for event in events:
            date_str = event["date"]
            period = event["status"]["period"]
            date = dateutil.parser.parse(date_str)

            # Move timezone to Eastern for ESPN.
            date = date.astimezone(pytz.timezone("America/New_York"))
            # Grab central for display purposes.
            date_central = date.astimezone(pytz.timezone("America/Chicago"))

            # Add day of week header w/ date
            event_day = date.strftime("%A")
            if current_date != event_day:
                if current_date != "":
                    response += "\n"
                current_date = event_day
                response += "\n{event_day} - {date.strftime('%#m/%#d')}"
                response += "\n-------------------------------------------------"

            game = event["competitions"][0]
            if len(game["broadcasts"]) != 0:
                network = game["broadcasts"][0]["names"][0]
            else:
                network = "TBD"

            home = self.parseTeam(game["competitors"][0], True)
            away = self.parseTeam(game["competitors"][1], False)

            status = " Time TBD"
            if period > 0:
                # Game has started progress. Display scores.
                status_txt = event["status"]["type"]["shortDetail"]
                status = f"{away['score']:>3}-{home['score']:<3}{status_txt:<12}"
            elif date.hour != 0:
                # ESPN sets their TBD games to midnight Eastern.
                status = "{date_central.strftime('%#I:%M %p %Z'):>12}"

            response += f"\n{network:<8}{away['name']:>10} @ {home['name']:<10} {status:<7}"

        response += '\n```'

        return response

    def parseTeam(self, teamJson, isHomeTeam):
        name = teamJson["team"]["abbreviation"]
        is_winner = teamJson.get("winner", False)
        rank = teamJson.get("curatedRank", {'current': 99}).get("current", 99)
        score = teamJson.get("score", 0)
        if is_winner:
            name = name + "*" if isHomeTeam else "*" + name
        if rank <= 25:
            name = f"{name if isHomeTeam else rank} {rank if isHomeTeam else name}"

        return {
            'name': name,
            'is_winner': is_winner,
            'rank': rank,
            'score': score
        }

    def getCurrentWeek(self, weeks):
        cur_time = datetime.now()

        cur_week = len(weeks)
        # Reverse it, we'll compare from oldest to newest to find the current week.
        for week in reversed(weeks):
            if cur_time > week:
                return cur_week
            cur_week = cur_week - 1

        return len(weeks)
    ### Jeyrad's code ###


def setup(bot):
    bot.add_cog(ScheduleCommands(bot))

# print("### Schedule Commands loaded! ###")
