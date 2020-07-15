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
import getopt, sys, os

if __name__ == '__main__':

    input_file = ''
    channel_list =[]
    output_file = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:c:o:",["help","input_file=", "channel=","output_file="])
    except getopt.GetoptError:
        print('usage: extract_time_range.py -i <input h5 file> - c <first time step> -c <second time step> ... -o <output_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in "-h":
            print('usage: extract_time_range.py -i <input h5 file> - c <first time step> -c <second time step> ... -o <output_file>')
            sys.exit(2)
        if opt in ("-c","--channel"):
            channel_list.append(int(arg))
        if opt in ("-o","--output_file"):
            output_file = arg
        if opt in ("-i","--input_file"):
            input_file = arg

    data = util.load_h5_file(input_file)
    data_shape = data.shape
    print("input file shape: {0}".format(data_shape))
    print("writing channel(s) {0}".format(str(channel_list)))
    out_array = np.take(data, channel_list, axis=0)
    util.write_data_to_h5(out_array, output_file)
    print("File writen.")


