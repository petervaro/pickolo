## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.965 (20150104)                       ##
##                          File: pickolo/plugin.py                           ##
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

#------------------------------------------------------------------------------#
class PickoloPlugIn:
    """ Abstract Base Class """
    pass



#------------------------------------------------------------------------------#
class PlugIn(PickoloPlugIn):
    """ Base Class """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def execute(self, *args, **kwargs):
        print("{} has no 'execute' method".format(self.__class__))
