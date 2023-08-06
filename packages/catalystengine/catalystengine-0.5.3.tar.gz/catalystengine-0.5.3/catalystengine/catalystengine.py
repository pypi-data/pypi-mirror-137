from time import sleep
from sys import stdout
from threading import Thread
from audioplayer import AudioPlayer


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


class marker:
  """
  Marker representing movable entity
  """
  gridx:int = 0
  gridy:int = 0
  _idcount:int = 0
  markers:list = []

  def __init__(self, x:int, y:int, rep:int=1):
    """
    - marker spawns at (x, y) coords\n
    - rep : How the marker is represented on mapgrid\n
    - mx, my : moves in steps forwards / backwards. Returns blocked steps if any\n
    Each instance of marker has a unique id equal to what number it was made at.\n
    """

    self.x = x
    self.y = y
    self.rep = rep

    self.id = marker._idcount
    marker._idcount += 1
    marker.markers.append(self)


  def _reinstate(self):
    marker.markers[self.id].x = self.x

  def mx(self, steps=0) -> int:
    """
    - dir : direction to move Ex: 'left'\n
    - steps : steps to move forward / backward
    - returns steps block by wall if over 0
    """
    bsteps = 0
    if steps != 0:
      self.x = self.x + steps


      if self.x < 0:
        self.x = 0
        bsteps = self.x + steps
      elif self.x > marker.gridx-1:
        self.x = marker.gridx-1
        bsteps = self.x + steps
    
    self._reinstate()
    return bsteps

  def my(self, steps=0) -> int:
    """
    - dir : direction to move Ex: 'left'\n
    - steps : steps to move. Returns steps past wall if it hits a wall.
    - returns steps block by wall if over 0
    """
    bsteps = 0
    if steps != 0:
      self.y = self.y + steps

      if self.y < 0:
        self.y = 0
        bsteps = self.y + steps
      elif self.y > marker.gridy-1:
        self.y = marker.gridy-1
        bsteps = self.y + steps

    self._reinstate()
    return bsteps


class catalyst:
  """
  Catalyst game engine class
  """
  currentsong:str
  menuopts:dict = {}
  markerlist:list = []


  def __init__(self, mapgrid:str = None, gridblank:int = 0):
    """
    - Optional grid initialize, EX : '3x3' = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]\n
    - Optional gridblank to represent empty spot. Defaults to 0
    """  
    if mapgrid:
      self.ilgrid = mapgrid.split('x')

    self.running = True 
    self.gridblank = gridblank
    marker.gridx, marker.gridy = int(self.ilgrid[0]), int(self.ilgrid[1])

    self.clock = self._timerInit()
    """
    Built in clock. Starts on loop start\n
    Reset() Resets clock to 0\n 
    time() returns time in S:M:H format
    """

  def _reinstatemap(self):
    self.mapgrid:list = [[self.gridblank 
                          for _2 in range(int(self.ilgrid[0]))] #map width
                          for _1 in range(int(self.ilgrid[1]))] #map height

  def addmarkers(self, markers:list):
    """
    - Argument must be list of marker objects
    Adds marker into the mapgrid\n
    Items in list must be of type (marker)
    """
    if markers:
      for mark in markers:
        self.markerlist.append(mark)

  def createoption(self, name, function, args:tuple):
    """
    Create option for mainloop to print each move\n
    Auto appends to main list of opts on creation\n
    - name : Name of menu option and how to call it\n
    - function : What function to call when name is called\n
    - args : Arguments to pass when function is called
    """ 
    if function:
      if args:   
        self.menuopts[name] = [function, args]
      else:
        self.menuopts[name] = [function]

  def _calloption(self, userinput):
    if userinput in self.menuopts.keys():
      if len(self.menuopts[userinput]) > 1:
        self.menuopts[userinput][0](self.menuopts[userinput][1])

  def audioloop(self, audio):
    """
    Initiate the bgm player with a given song\n
    supports: wav and mp3
    """
    def _adinit():

      while True:
        AudioPlayer(audio).play(block=True)

    if audio:
      self.currentsong = audio
      Thread(target=_adinit).start()

  def write(self, outstring, delay=0.02):
    """
    Writes out strings in a human format
    """
    for char in outstring:
      sleep(delay)
      stdout.write(char)
      stdout.flush()
  
  def gameloop(self):
    """
    Initialize game loop.
    """
    while True:
      self.markerlist = marker.markers
      self._reinstatemap()

      if self.markerlist: #place marker object
        for mark in self.markerlist:
          self.mapgrid[mark.y][mark.x] = mark.rep

      if self.mapgrid: #print mapgrid
        for row in self.mapgrid:
          print(row)

      print('\n\n')

      if self.menuopts != {}: print('\nOptions')
      for opt in self.menuopts.keys(): print(f' - {opt}')

      userinput = input('\nUse : ')

      self._calloption(userinput)

      print('\n'*20)
  
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