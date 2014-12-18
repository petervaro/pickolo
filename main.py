## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.918 (20141218)                       ##
##                               File: main.py                                ##
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
from os.path import abspath

# Import pickolo modules
from pickolo.app import App
from pickolo.stripes import Stripes, HORIZONTAL, STRIPES

#------------------------------------------------------------------------------#
# Module level constants
SIZE = 32
IPATH = abspath('images/u3.jpg')
OPATH = abspath('output/u3.svg')



#------------------------------------------------------------------------------#
def manual():
    # Create Pickolo Application
    app = App()

    # Create plugin
    plugin = Stripes()
    plugin.divide = 2, 1, 1, 2, 3, 1
    plugin.divide = 4
    plugin.divide = 22.7, 78.12, 7
    plugin.divide = 7, None, False
    plugin.divide = ()
    plugin.divide = '1', '2'
    plugin.divide = '1', None
    plugin.divide = '1, 4'
    plugin.divide = '    12,,, 4, 5 6'
    plugin.divide = ''
    plugin.divide = '5'
    plugin.divide = 'hello'
    plugin.direction = HORIZONTAL
    app.load_plugin(plugin, reference=STRIPES)

    # Set images
    IMAGE = 'u3'
    app.load_image(IPATH, reference=IMAGE)

    # Execute plugin on image
    app.execute_plugin(STRIPES, IMAGE)

    # Save output
    app.save_image(OPATH)



#------------------------------------------------------------------------------#
def config():
    EXAMPLE = 'example'

    app = App()
    app.load_config('example.ini', reference=EXAMPLE)
    app.load_plugin(Stripes(), reference=STRIPES)
    app.execute_config(EXAMPLE)

    # global SIZE, PATH
    # SIZE = (SIZE,)*2
    # PATH = abspath(PATH)
    # try:
    #     image = Image.open(PATH)
    # except IOError:
    #     print('File: {!r} cannot be opened'.format(PATH))
    #     return

    # # TODO: if image.mode is 'RGB'

    # image.thumbnail(SIZE)
    # width, height = image.size
    # pixels = image.load()

    # #row, column = (width, height) if HORIZONTAL else (height, width)

    # colors = []
    # for i in range(height):
    #     row_r = []
    #     row_g = []
    #     row_b = []
    #     for j in range(width):
    #         r, g, b = pixels[j, i]
    #         row_r.append(r)
    #         row_g.append(g)
    #         row_b.append(b)

    #     colors.append((round(sum(row_r)/width),
    #                    round(sum(row_g)/width),
    #                    round(sum(row_b)/width)))

    # for i, color in zip(range(height), colors):
    #     for j in range(width):
    #         image.putpixel((j, i), color)

    # image.show()



#------------------------------------------------------------------------------#
if __name__ == '__main__':
    import build
    print('\n' + '-'*80 + '\n')
    manual()
    config()
