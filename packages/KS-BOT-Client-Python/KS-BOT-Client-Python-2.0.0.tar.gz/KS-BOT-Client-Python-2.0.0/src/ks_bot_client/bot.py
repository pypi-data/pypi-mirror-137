import socketio
import requests
import time

from ks_bot_client.ks_bot_exceptions import LoggingInError

class Bot:

  def __init__(self, name:str, password:str):
    """
    @param {string} name: Name can either email address, user name, or first name
    @param {string} password: Your password
    """

    self.sio =  socketio.Client()

    self.name = name

    self.password = password

    self.session_id = None


  def log_in(self):
    x = requests.post("https://ksbot.kidssmit.com/does_user_exist", json = {
      "name": self.name,
      "password": self.password
    })

    try: 
      if x.json()["returns"] == "User exist":
        self.session_id = x.json()['data']["id"]
        return True
    except Exception as e: pass
  
    return False

  def run(self):
    logged_in = self.log_in()
    
    if logged_in:
      self.sio.on("connect", handler=self.connect)
      self.sio.on("WelcomeMessage", handler=self.WelcomeMessage)
      self.sio.on("BotProcessReply", handler=self.BotProcessReply)
      self.sio.on("Timer Over", handler=self.TimerOver)
      self.sio.connect("https://ksbot.kidssmit.com")
      self.sio.wait()
    else:
      raise LoggingInError("There was a problem login you in")

  def connect(self):
    print("Client Connected")
    self.sio.emit("launch_bot", {"session_id": self.session_id})

  def WelcomeMessage(self, data):
    """
      This event gives you, your previous messages with bot.
    """
    print("KS-BOT said 'welcome'")

  def BotProcessReply(self, data):
    """
      Returns bot reply to the message you sent it
    """
    print("KS-BOT said: ", data)

  def TimerOver(self, data):
    """
      Handles Event Server sends when timer is over
    """

    print("KS-BOT said: Timer is over, Timer: ", data)

  def send_command(self, command, timeZone=None):
    """
      Sends command to server and wait for reply
    """

    self.sio.emit("process_new_message",  
      {
        "session_id": self.session_id, 
        "new_message": {
          "message":  command,
          "timeZone": timeZone or time.tzname
        }
      }
    )