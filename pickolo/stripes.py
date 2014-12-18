## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.913 (20141218)                       ##
##                          File: pickolo/stripes.py                          ##
##                                                                            ##
##               For more information about the project, visit                ##
##                  <https://github.com/petervaro/pickolo>.                   ##
##                       Copyright (C) 2014 Peter Varo                        ##
##                                                                            ##
##  This program is free software: you can redistribute it and/or modify it   ##
##   under the terms of the GNU General Public License as published by the    ##
##       Free Software Foundation, either version 3 of the License, or        ##
##                    (at your option) any later version.                     ##
##                                                                            ##
##    This program is distributed in the hope that it will be useful, but     ##
##         WITHOUT ANY WARRANTY; without even the implied warranty of         ##
##            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.            ##
##            See the GNU General Public License for more details.            ##
##                                                                            ##
##     You should have received a copy of the GNU General Public License      ##
##     along with this program, most likely a file in the root directory,     ##
##        called 'LICENSE'. If not, see <http://www.gnu.org/licenses>.        ##
##                                                                            ##
######################################################################## INFO ##

# Import pickolo modules
from .plugin import PlugIn

#------------------------------------------------------------------------------#
# Module level public constants
HORIZONTAL = 0x00
VERTICAL   = 0x01
STRIPES = 'stripes'

# Module level private constants
_DEFAULT_DIVIDE = (1,)


#------------------------------------------------------------------------------#
class Stripes(PlugIn):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        self._dimension = 0


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def divide(self):
        return self._divide

    @divide.setter
    def divide(self, numbers):
        # If numbers is empty or None
        if not numbers:
            numbers = _DEFAULT_DIVIDE
        # If numbers is not empty
        else:
            # If a single token is passed
            try:
                numbers = (int(numbers),)
            # If multiple numbers have been passed
            except ValueError:
                print('ValueError: {!r}'.format(numbers))
                # If numbers is a string
                if isinstance(numbers, str):
                    numbers = (n.strip() for n in numbers.split(',') if n)
            except TypeError:
                print('TypeError {!r}'.format(numbers))

        # If all values are tokens which can be converted to int
        try:
            numbers = tuple(map(int, numbers))
        # If there are values which cannot be converted to int
        except (TypeError, ValueError):
            numbers = _DEFAULT_DIVIDE

        # If numbers is an iterable of integers
        try:
            self._dimension = sum(numbers)
        # If numbers is a single integer
        except TypeError:
            self._dimension = numbers = int(numbers)
        # Store numbers
        self._divide = numbers
        print('{:4d} => {}'.format(self._dimension, self._divide))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

        # If vertical stripes
        if value == VERTICAL:
            pass
        # If horizontal stripes, or invalid
        else:
            pass
