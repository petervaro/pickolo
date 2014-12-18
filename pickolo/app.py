## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.913 (20141218)                       ##
##                            File: pickolo/app.py                            ##
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
from configparser import ConfigParser
from itertools import count

# Import pillow modules
from PIL import Image

#------------------------------------------------------------------------------#
# MOdule level private constants
_PLUGIN_PREFIX = 'plugin.'
_PLUGIN_PREFIX_LEN = len(_PLUGIN_PREFIX)

#------------------------------------------------------------------------------#
class App:

    ID_FACTORY = count(1)
    MISSING_OPTION = 'Missing option: {!r} from section: {!r}'
    INVALID_OPTION = 'Invalid value: {!r} for option: {!r} in section: {!r}'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        self._images  = {}
        self._plugins = {}
        self._configs = {}


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def load_plugin(self, plugin_object, reference=None):
        id = reference or next(self.ID_FACTORY)
        self._plugins[id] = plugin_object
        return id


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def load_image(self, image_path, reference=None):
        # If image_path is a valid path to an image
        try:
            image = Image.open(image_path)
            id = reference or next(self.ID_FACTORY)
            self._images[id] = image
            return id
        # If there was any complication during opening the path
        except IOError as error:
            print('Image {!r} cannot be opened'.format(image_path))
            raise error


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def load_config(self, config_path):
        with open(config_path) as file:
            config = ConfigParser()
            config.read_file(file)

            # Get local references
            load_image = self.load_image
            configs = self._configs
            plugins = self._plugins

            for section in config.sections():
                configuration = {}

                # Get and set option: input
                option = 'input'
                try:
                    # If image is not a valid image
                    value = config.get(section, option)
                    load_image(value)
                # If option cannot be found
                except configparser.NoOptionError:
                    print(self.MISSING_OPTION.format(option, section))
                    continue
                # If
                except IOError:
                    print(self.INVALID_OPTION.format(value, option, section))
                    continue

                # Get and set option: output
                option = 'output'
                try:
                    configuration[option] = config.get(section, option)
                # If option cannot be found
                except configparser.NoOptionError:
                    print(self.MISSING_OPTION.format(option, section))
                    continue

                # Get and set option: plugin
                option = 'plugin'
                try:
                # TODO: Consider if checking if plugin has already been loaded
                #       is a good idea or not. If checking will be 'lazy' and
                #       will happen only during execution, it gives the freedom
                #       of mixing the order of the load function callings to the
                #       user => which is probably a better API design?
                    value = config.get(section, option)
                    configuration[option] = plugins[value]
                # If option cannot be found
                except configparser.NoOptionError:
                    print(self.MISSING_OPTION.format(option, section))
                    continue
                # If option is not valid
                except KeyError:
                    print(self.INVALID_OPTION.format(value, option, section))
                    print('Plugin has not been loaded')
                    continue






                    configuration[option] = config.get(section, option)
                # Save configuration
                configs[section] = configuration


                for option, value in config.items(section):

                    print(option, value)
                print({key[_PLUGIN_PREFIX_LEN:] for key in config[section] if key.startswith(_PLUGIN_PREFIX)})


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def save_image(self, image_path):
        pass


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def execute_plugin(self, plugin_id, image_id):
        pass


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def execute_config(self):
        pass
