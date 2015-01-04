## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.991 (20150104)                       ##
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
def manual():
    # Function level constants
    IPATH = abspath('images/u3.jpg')
    OPATH = abspath('output/u3.svg')

    # Create Pickolo Application
    app = App()

    # Create plugin
    plugin = Stripes()
    plugin.divide = 2, 1, 1, 2, 3, 1
    plugin.direction = HORIZONTAL
    app.load_plugin(plugin, reference=STRIPES)

    # Set images
    IMAGE = 'u3'
    app.load_image(IPATH, reference=IMAGE)

    # Execute plugin on image and save output
    app.save_image(app.execute_plugin(STRIPES, IMAGE), OPATH)



#------------------------------------------------------------------------------#
def config():
    EXAMPLE = 'example'

    app = App(plugins_are_classes=True)
    app.load_config('example.ini', reference=EXAMPLE)
    app.load_plugin(Stripes, reference=STRIPES)
    app.execute_config(EXAMPLE)

#------------------------------------------------------------------------------#
if __name__ == '__main__':
    import build
    print('\n' + '-'*80 + '\n')
    manual()
    # config()
