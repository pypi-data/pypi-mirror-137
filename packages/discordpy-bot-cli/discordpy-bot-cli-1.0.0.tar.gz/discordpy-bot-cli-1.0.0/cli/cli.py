#!/usr/env/bin python

import os
import click

@click.group(invoke_without_command = True)
@click.version_option("1.0.0")
def main():
    pass

@main.command("init")
@click.argument("name")
def dcinit(name):
    """
        Initializes a Discord bot project by creating bot.py, Procfile and requirements.txt files.
        Usage: dc init <project_name>
    """
    os.mkdir(name)
    os.chdir(name)

    os.system("echo from discord.ext import commands >> bot.py")
    os.system("echo. >> bot.py")
    os.system('echo client = commands.Bot(command_prefix = "") >> bot.py')
    os.system("echo. >> bot.py")
    os.system('echo client.run("") >> bot.py')
    print("INFO: bot.py created")

    os.system("echo worker: python bot.py >> Procfile")
    print("INFO: Procfile created")

    os.system("pipreqs --encoding=utf-8")
    print("Discord bot project created")
    print("Please use heroku whoami to make sure that you are logged into the correct credentials.")
    print("If you are not logged in, please log into your account in Heroku CLI.")

    pass

@main.command()
@click.argument("cog")
@click.option("-f", "--folder", help = "(Optional) Folder in which the cog file shall be made and the folder need not be made.")
def cog(cog, folder):
    """
        Creates a cog file and adds setup.
        Usage: dc cog <file_name> [-f or --folder <folder_name>]
    """

    if os.path.exists("bot.py") or os.path.exists("client.py"):
        if not os.path.isdir("cogs"):
            os.mkdir("cogs")
        os.chdir("cogs")

        if folder:
            if not os.path.exists(folder):
                os.mkdir(folder)
            os.chdir(folder)

        os.system(f"echo from discord.ext import commands >> {cog.lower()}.py")
        os.system(f"echo. >> {cog.lower()}.py")
        os.system(f"echo class {cog}(commands.Cog): >> {cog.lower()}.py")
        os.system(f"echo    def __init__(self, client): >> {cog.lower()}.py")
        os.system(f"echo         self.client = client >> {cog.lower()}.py")
        os.system(f"echo. >> {cog.lower()}.py")
        os.system(f"echo def setup(client): >> {cog.lower()}.py")
        os.system(f"echo    client.add_cog({cog}(client)) >> {cog.lower()}.py")
    else:
        print("ERROR: bot.py or client.py not found. Make sure you have made a Discord bot project.")

    pass

@main.command()
def deploy():
    """
        Deploys the Discord bot.
        Usage: dcpy deploy
    """

    if not os.path.isdir(".git"):
        os.system("git init")
        name = input("Heroku app name to connect to: ")
        os.system(f"heroku git:remote -a {name}")
        os.system(f"git branch -M main")
    
    os.system("git add .")
    os.system('git commit -m "Commit made with discord.py-bot-cli"')
    os.system("git push heroku main")
    print("Make sure that your bot is online by checking in the Resources tab of the project in Heroku.")

def start():
    main(obj = {})

if __name__ == '__main__':
    start()