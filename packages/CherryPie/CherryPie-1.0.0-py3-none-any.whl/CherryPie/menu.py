""" 
 _____ _                   _____ _
|     | |_ ___ ___ ___ _ _|  _  |_|___
|   --|   | -_|  _|  _| | |   __| | -_|
|_____|_|_|___|_| |_| |_  |__|  |_|___|
                      |___| 
Github : https://github.com/NotReeceHarris/CherryPie
Developer: Reece Harris (https://github.com/NotReeceHarris)
"""

from .lib.color import Color
from .lib.color import ColorList
from .lib.__exceptions__ import *

import os

"""  
  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
  │        │ │        │ │        │ │        │ │        │
┌─┘        └─┴────────┴─┴────────┴─┴────────┴─┴────────┴┐
│                                                       │
└───────────────────────────────────────────────────────┘
"""


class Menu:

    """ 
    @Menu.__init__(self, tabs, content, color=['BLACK','LIGHT_WHITE','RED'])

    Params
      tabs:     array()
      content:  array()
      color:    array([OUTLINE COLOR, TEXT COLOR, ACTIVE COLOR])
    """

    def __init__(self, tabs, content, color=['BLACK', 'LIGHT_WHITE', 'RED']):
        # Define class variables
        self.tabs = []
        self.content = []
        self.color = []

        (c, r) = os.get_terminal_size()
        self.screenWidth = c
        self.screenHeight = r

        self.layoutWidth = c - 21
        self.tabSize = 21

        for x in tabs : self.tabSize += len(x)

        # Validation of data

        # Validate param tabs, content
        if len(tabs) != len(content):
            raise Exception(invalidTagAndContent_AMOUNT)

        for x in tabs:
            if len(x) > 20 or 0 >= len(x):
                raise Exception(invalidTag_LENGTH)
            else:
                self.tabs.append((x.encode('utf-8')).decode('utf-8'))

        for x in content:
            self.content.append((x.encode('utf-8')).decode('utf-8'))

        # Validate param color
        colorListJustColor = ColorList
        del colorListJustColor[15:23]

        if len(color) != 3:
            raise Exception(invalidCustomColors_AMOUNT)
        elif color[0] not in colorListJustColor:
            raise Exception(invalidCustomColors_OUTLINE +
                            Color.RED + str(colorListJustColor) + Color.END)
        elif color[1] not in ColorList and color[2] not in ColorList:
            raise Exception(invalidCustomColors_TEXT +
                            Color.RED + str(ColorList) + Color.END)
        else:
            self.color = color

    """ 
    @Menu.display(self, active=0)

    Params
      active:   int
    """

    def display(self, active=0):

        if len(self.tabs) < active or active < 0:
            raise Exception(invalidDisplay_VALUE)

        # Create layout level 1

        self.layoutLevel1 = getattr(Color, self.color[0]) + ' '
        for x in self.tabs:
            self.layoutLevel1 += f' ┌{"─"*(len(x)+2)}┐'

        # Create layout level 2

        self.layoutLevel2 = ' '
        for i, x in enumerate(self.tabs):
            if i == active:
                self.layoutLevel2 += f' {getattr(Color, self.color[0])}│{Color.END} {getattr(Color, self.color[2])}{Color.BOLD}{x}{Color.END} {getattr(Color, self.color[0])}│{Color.END}'
            else:
                self.layoutLevel2 += f' {getattr(Color, self.color[0])}│{Color.END} {getattr(Color, self.color[1])}{x}{Color.END} {getattr(Color, self.color[0])}│{Color.END}'

        # Create layout level 3

        self.layoutLevel3 = ''
        for i, x in enumerate(self.tabs):
            if i == 0 and i != active:
                self.layoutLevel3 += f'{getattr(Color, self.color[0])}┌─┴{"─"*(len(x)+2)}┴{Color.END}'
            elif i == 0 and i == active:
                self.layoutLevel3 += f'{getattr(Color, self.color[0])}┌─┘{" "*(len(x)+2)}└{Color.END}'
            elif i == len(self.tabs) - 1 and i != active:
                self.layoutLevel3 += f'{getattr(Color, self.color[0])}─┴{"─"*(len(x)+2)}┴{"─"*(self.screenWidth - self.tabSize - 3)}┐{Color.END}'
            elif i == len(self.tabs) - 1 and i == active:
                self.layoutLevel3 += f'{getattr(Color, self.color[0])}─┘{" "*(len(x)+2)}└{"─"*(self.screenWidth - self.tabSize - 3)}┐{Color.END}'

            elif i != len(self.tabs) - 1 and i != 0 and i == active:
                self.layoutLevel3 += f'{getattr(Color, self.color[0])}─┘{" "*(len(x)+2)}└{Color.END}'
            else:
                self.layoutLevel3 += f'{getattr(Color, self.color[0])}─┴{"─"*(len(x)+2)}┴{Color.END}'

        # Create layout level 4
        self.layoutLevel4 = ''
        
        content = list(self.content[active])
        count = 0
        charCount = 0
        lineCount = 0
        while True:

            if count == 0:
                self.layoutLevel4 += f'{getattr(Color, self.color[0])}│{Color.END}{getattr(Color, self.color[1])} '
                count += 1

            elif count == self.screenWidth - 5:
                self.layoutLevel4 += f' {getattr(Color, self.color[0])}│{Color.END}\n'
                lineCount = 0
                count = 0

            else:
                self.layoutLevel4 += f'{content[charCount]}'
                charCount += 1
                lineCount += 1
                if charCount == len(content):
                    if charCount > self.screenWidth:
                        self.layoutLevel4 += f'{" "*( int( self.screenWidth - lineCount -5 ) ) }{getattr(Color, self.color[0])}│{Color.END}'
                    else:
                        self.layoutLevel4 += f'{" "*( int( ( self.screenWidth - charCount ) -5 ) ) }{getattr(Color, self.color[0])}│{Color.END}'
                    break
                count += 1

        # Create layout level 5
        self.layoutLevel5 = f'{getattr(Color, self.color[0])}└{"─"*(self.screenWidth-4)}┘{Color.END}'
        
            
        # Display the menu
        print(f'{self.layoutLevel1}\n{self.layoutLevel2}\n{self.layoutLevel3}\n{self.layoutLevel4}\n{self.layoutLevel5}')

