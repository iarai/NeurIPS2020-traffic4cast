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
import util
import numpy as np
import getopt, sys

if __name__=='__main__':
    lhs =''
    rhs =''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:r:",["help","lhs","rhs"])
    except getopt.GetoptError:
        print('usage: compare_h5.py -l <left hand side file> -r <right hand side file> ')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-l","--lhs"):
            lhs = arg
        elif opt in ("-r","--rhs"):
            rhs = arg
        elif opt == "-h":
            print('usage: compare_h5.py -l <left hand side file> -r <right hand side file> ')
            sys.exit(2)

    lhs_data = util.load_h5_file(lhs)
    rhs_data = util.load_h5_file(rhs)

    if lhs_data.shape == rhs_data.shape:
        print((lhs_data == rhs_data).all())
    else:
        print("False")

