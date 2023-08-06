# Version of the KS_Bot_Client package
__version__ = "1.0.0"

from ks_bot_client.bot import Bot

if __name__ == "__main__":
  bot =  Bot("codingwithcn", "Cn031705!s")
  bot.run()