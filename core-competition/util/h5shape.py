#!/usr/bin/python3
# Copyright 2020 Institute of Advanced Research in Artificial Intelligence (IARAI) GmbH.
# IARAI licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This script takes as an input a zipped h5 file and spits out the shape of the tensor it contains.
"""
import getopt
import util
import sys

if __name__ == '__main__':

    # gather command line arguments.
    infile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["infile="])
    except getopt.GetoptError:
        print('usage: h5shape -i <path to h5 file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: h5shape -i <path to h5 file>')
            sys.exit()
        elif opt in ("-i","--infile"):
            infile = arg
    data = util.load_h5_file(infile)
    util.print_shape(data)

            
            
