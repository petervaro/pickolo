## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.966 (20150104)                       ##
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
def _store_int(container, values):
    # If values is iterable
    try:
        for value in values:
            # Prevent infinite recursion
            if value == values:
                raise TypeError
            _store_int(container, value)
    # If values is a single value
    except TypeError:
        try:
            container.append(int(values) or 1)
        except (TypeError, ValueError):
            container.append(1)
    # Return container
    return container



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
        # If numbers is a string
        elif isinstance(numbers, str):
            numbers = tuple(number.strip() for number in numbers.split(',') if number)

        # Convert all values to ints and store them
        numbers = _store_int([], numbers)

        # Store meaningful values
        self._dimension = sum(numbers)
        self._divide = numbers


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

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def execute(self, image):
        # Resize image, and get new dimension
        image.thumbnail((self._dimension,)*2)
        width, height = image.size
        pixels = image.load()

        #row, column = (width, height) if HORIZONTAL else (height, width)

        colors = []
        for i in range(height):
            row_r = []
            row_g = []
            row_b = []
            for j in range(width):
                r, g, b = pixels[j, i]
                row_r.append(r)
                row_g.append(g)
                row_b.append(b)

            colors.append((round(sum(row_r)/width),
                           round(sum(row_g)/width),
                           round(sum(row_b)/width)))

        for i, color in zip(range(height), colors):
            for j in range(width):
                image.putpixel((j, i), color)

        # image.show()


