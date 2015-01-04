#!/usr/bin/env python3
## INFO ########################################################################
##                                                                            ##
##                                  pickolo                                   ##
##                                  =======                                   ##
##                                                                            ##
##                    Effect Images Based On Color Picking                    ##
##                       Version: 0.1.70.955 (20150104)                       ##
##                               File: test.py                                ##
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

from pickolo.app import App
from pickolo.stripes import Stripes

#------------------------------------------------------------------------------#
def stupid_inputs():
    a = App()
    p = Stripes()

    inputs = ((2, 1, 1, 2, 3, 1),
              4,
              (22.7, 78.12, 7),
              (7, None, False),
              (),
              ('1', '2'),
              ('1', None),
              '1, 4',
              '    12,,, 4, 5 6',
              '',
              '5',
              '7,',
              'hello',
              ('1', (23, 1), (9, (8, (7, ('hello')))), '0'),)

    print('DIM  :: DIV')
    for input in inputs:
        p.divide = input
        print('{:4d} => {}'.format(p._dimension, p._divide))



#------------------------------------------------------------------------------#
if __name__ == '__main__':
    stupid_inputs()
