from time import sleep
from sys import stdout
from threading import Thread
from audioplayer import AudioPlayer

ostdef1 = './audio/defaultopen.wav'

class sfx:
  """
  Sound effect class
  """

  def __init__(self, sound):
    self.sound = sound

  def play(self):
    """
    Play sound effect
    """

    def _inplay():
      AudioPlayer(self.sound).play(loop=False, block=True)

    Thread(target=_inplay).start()


class Control:
  """
  Catalyst game engine class
  """
  mapList:list
  currentSong:str
  menuOpts:dict = {}


  def __init__(self):
    self.running = True

    self.clock = self._timerInit()
    """
    Built in clock. Starts on loop start\n
    Reset() Resets clock to 0\n 
    time() returns time in S:M:H format
    """


  def createOption(self, name, function, output=None):
    """
    Create option for mainloop to print each move\n
    Auto appends to main list of opts on creation\n
    - name : Name of menu option and how to call it\n
    - function : what function to call when name is called\n
    - output : What to print when option is called. Defaults to None
    """ 
    if output:
      print(output)
    self.menuOpts[name] = function

  def audioLoop(self, audio=ostdef1):
    """
    Initiate the bgm player with a given song\n
    supports: wav and mp3\n
    uses built-in ost if no argument passed
    """
    def _adinit():

      while True:
        AudioPlayer(audio).play(block=True)

    self.currentSong = audio
    Thread(target=_adinit).start()

  def write(self, outstring, delay=0.02):
    """
    Writes out strings in a human format
    """
    for char in outstring:
      sleep(delay)
      stdout.write(char)
      stdout.flush()
  
  def startLoop(self):
    """
    Initialize game loop.\n
    """
    while True:
      print('Options')
      for opt in self.menuOpts.keys():
        print(f' - {opt}')

      userInput = input('\nUse : ')

      if userInput in self.menuOpts.keys():
        self.menuOpts[userInput]()
  
  class _timerInit:
    """
    Initiates a clock timer in S|M|H format
    """
    def __init__(self):
      self.timerActive = True

      self.second = 0
      self.minute = 0
      self.hour = 0

      Thread(target=self._timestart).start()

    def _timestart(self):

      while self.timerActive:
        sleep(1)

        self.second += 1
        if self.second >= 60:
          self.minute += 1
          self.second = 0
        if self.minute >= 60:
          self.hour += 1
          self.minute = 0
        
    def reset(self):
      """Resets the loop clock"""
      self.second = 0
      self.minute = 0
      self.hour = 0

    def time(self):
      """Returns amounted time in S:M:H format"""
      return f'{self.second}:{self.minute}:{self.hour}'
  