## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.995 (20150104)                       ##
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
from inspect import isclass
from itertools import count
from configparser import ConfigParser

# Import pillow modules
from PIL import Image

# Import pickolo modules
from .drawer import raster_to_vector

"""
The pickolo-app is a 'storage' and a 'controller' at the same time. One can load
plugins and images to the app, and save them by custom references, or can use
the generated ones. Once the images and plugins has been 'uploaded' they

PickoloApp can be used in two ways:

Via python calls:

    The usage is very simple, one has to create the app; create the plugins and
    upload them to the app; and create the images, and upload them too to the
    app and last but not least, execute the plugins on the images and save them.

    Example:

        main.py
        -------
        # Import python modules
        from itertools import product

        # Import pickolo modules
        from pickolo.app import App
        from pickolo.stripes import Stripes, HORIZONTAL, VERTICAL

        # Create Pickolo Application
        app = App()

        # Create two plugins and set their values
        plugin1 = Stripes()
        plugin1.divide    = 2, 1, 3, 1, 1, 1, 2
        plugin1.direction = HORIZONTAL

        plugin2 = Stripes()
        plugin2.divide    = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        plugin2.direction = VERTICAL

        # Load plugins
        ref_p1 = app.load_plugin(plugin1)
        ref_p2 = '2nd-plugin'
        app.load_plugin(plugin2, reference=ref_p2)

        # Load and store images
        ref_i1 = 'blue-sky'
        app.load_image('path/to/blue_sky_image.jpg', reference=ref_i1)
        ref_i2 = app.load_image('path/to/image.jpg')

        # Execute each plugin on each image and save their output
        for ref_p, ref_i in product((ref_p1, ref_p2), (ref_i1, ref_i2)):
            app.execute_plugin(ref_p, ref_i)

            # ??? what will reference the output of a plugin ???

            app.save_image('')

Via config files:

    This usage is built on pretty much the same logic as the previous one,
    although one has to call fewer functions, as most of the details are already
    stored in the config files, and pickolo-app will call those functions for
    us.

    Example:

        example.ini
        -----------
        [DEFAULT]
        input = input_images/my_image.jpg

        [0]
        output = output_images/my_image_0.jpg
        plugin = stripes
        plugin.divide    = 2, 1, 3, 1, 1, 1, 2
        plugin.direction = HORIZONTAL

        [1]
        output = output_images/my_image_1.jpg
        plugin = stripes
        plugin.divide    = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        plugin.direction = VERTICAL


        main.py
        -------
        # Import pickolo modules
        from pickolo.app import App
        from pickolo.stripes import Stripes, HORIZONTAL

        # Create Pickolo Application
        app = App(plugins_are_classes=True)

        # Load configuration
        app.load_config('example.ini', reference='example')
        app.load_plugin(Stripes, reference='stripes')

        # Execute configuration
        app.execute_config('example')
"""

#------------------------------------------------------------------------------#
# Module level private constants
_PLUGIN_PREFIX = 'plugin.'
_PLUGIN_PREFIX_LEN = len(_PLUGIN_PREFIX)

#------------------------------------------------------------------------------#
class App:

    ID_FACTORY = count(1)
    MISSING_OPTION = 'Missing option: {!r} from section: {!r}'
    INVALID_OPTION = 'Invalid value: {!r} for option: {!r} in section: {!r}'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, *, plugins_are_classes=False):
        self._isclass = plugins_are_classes
        self._images  = {}  # Store Image objects
        self._plugins = {}  # Store Plugin classes or instances
        self._configs = {}  # Store Config files
        self._outputs = {}  # Store output images


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def load_plugin(self, plugin_object, reference=None):
        # If application only accepts classes
        # TODO: Decide if throw error during the creation of an instance is a
        #       better idea or not. If it is better, that will allow the user to
        #       pass a function object too, which will return an instance...
        #       That's probably a way better approach... Although in that case
        #       the App has to check on each exception, wether self._isclass is
        #       True or not, which is not so ideal.
        if self._isclass and not isclass(plugin_object):
            raise TypeError('Plugin has to be a class-object')
        # Get ID and store plugin
        id = reference or next(self.ID_FACTORY)
        self._plugins[id] = plugin_object
        return id


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def load_image(self, image_path, reference=None):
        # If image_path is a valid path to an image
        try:
            image = Image.open(image_path)
            # TODO: Decide if we need to check if image.mode == 'RGB' or not
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
                print({key[_PLUGIN_PREFIX_LEN:] for key in config[section]
                        if key.startswith(_PLUGIN_PREFIX)})


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def save_image(self, output_id, image_path):
        try:
            raster_to_vector(self._outputs[output_id], image_path)
            self._outputs[output_id].save('output/u3.png', 'PNG')
        except KeyError:
            print('{!r} is not a valid output-id'.format(output_id))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def execute_plugin(self, plugin_id, image_id):
        # Get new output-id
        id = next(self.ID_FACTORY)

        # Get image
        try:
            temp = self._images[image_id].copy()
        # If image-id is not valid
        except KeyError:
            print('{!r} is not a valid image-id'.format(image_id))
            return

        # Get plugin
        try:
            self._plugins[plugin_id].execute(temp)
        # If plugin-id is not valid
        except KeyError as e:
            print('{!r} is not a vald plugin-id'.format(plugin_id))
            return

        # Save output and return reference
        self._outputs[id] = temp
        return id


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def execute_config(self):
        pass
