## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.997 (20150104)                       ##
##                          File: pickolo/drawer.py                           ##
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

# Import python modules
from os import makedirs
from os.path import dirname

# Import svgwrite modules
from svgwrite import Drawing

# Module level private constants
_RGB = '#{:02X}{:02X}{:02X}'

#------------------------------------------------------------------------------#
def _add_rectangles(drawing, width, color, start_x, start_y, close_x, close_y):
    # If multi-line
    if start_y != close_y:
        middle_start_y = start_y
        middle_close_y = close_y
        # If not starting from 0
        if start_x:
            middle_start_y += 1
            drawing.add(drawing.rect((start_x, start_y),
                                     (width - start_x, 1),
                                     fill=color))
        # If not reaching the end
        if close_x and width - close_x:
            drawing.add(drawing.rect((0, close_y),
                                     (close_x, 1),
                                     fill=color))

        # If there is a "middle" rectangle
        if middle_start_y != middle_close_y:
            drawing.add(drawing.rect((0, middle_start_y),
                                     (width, middle_close_y),
                                     fill=color))
    # If single-line
    else:
        drawing.add(drawing.rect((start_x, start_y),
                                 (close_x - start_x, 1),
                                 fill=color))


#------------------------------------------------------------------------------#
def raster_to_vector(image, path):
    drawing = Drawing(path, profile='tiny')
    width, height = image.size
    pixels = image.load()

    start_x = start_y = 0
    last_pixel = pixels[0, 0]
    for close_y in range(height):
        for close_x in range(width):
            pixel = pixels[close_x, close_y]
            # If pixel has different color
            if pixel != last_pixel:
                color = _RGB.format(*last_pixel)
                _add_rectangles(drawing, width, color,
                                start_x, start_y,
                                close_x, close_y)
                # Reset values
                last_pixel = pixel
                start_x = close_x
                start_y = close_y

    _add_rectangles(drawing, width, color,
                    start_x, start_y,
                    close_x, close_y)
    # Save constructed SVG
    try:
        drawing.save()
    except FileNotFoundError:
        makedirs(dirname(path))
        drawing.save()
