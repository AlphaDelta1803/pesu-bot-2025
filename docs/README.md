# PES25 Bot

<p align="center">
    <a href="https://github.com/acmpesuecc/pesu-bot-2025/issues" alt="issues">
    <img alt="GitHub forks" src="https://img.shields.io/github/issues/alfadelta10010/pesu-bot-2025"></a>
    <a href="https://github.com/acmpesuecc/pesu-bot-2025/stargazers" alt="Stars">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/acmpesuecc/pesu-bot-2025"></a>
    <img alt="Github license" src="https://img.shields.io/github/license/acmpesuecc/pesu-bot-2025"></a>
    <a href="https://github.com/acmpesuecc/pesu-bot-2025/contributors" alt="Contributors">
    <img src="https://img.shields.io/github/contributors/acmpesuecc/pesu-bot-2025"/></a>
</p>

The source code for authentication and moderation bot used in "PES'25" discord server

## Tech stack

Uses [discord.py](https://github.com/Rapptz/discord.py), [discord-py-slash-command](https://pypi.org/project/discord-py-slash-command/), and [Selenium](https://pypi.org/project/selenium/)

## Testing

Add an alias to the bash shell to allow the bot to start:

` alias botstart = source bin/activate; nohup python3 start.py `

Enable the Virtual Environment with the following command:

`source botEnv/bin/activate`

Create a `.env` file with the following contents:

`DISCORD_TOKEN=token_here`

Then, run the bot by using the following command:

`python3 bot.py`

## Owner and Maintainer

[alfadelta10010](https://github.com/alfadelta10010)
