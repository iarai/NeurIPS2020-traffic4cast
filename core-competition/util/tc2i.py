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
import numpy as np
import util
from PIL import Image
import sys, getopt

if __name__ =='__main__':
    input_file =''
    output_name_stub=''
    channel=int(0)
    factor=int(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:c:s:f:",["help","input_file=","output_name_stub=","factor="])
    except getopt.GetoptError:
        print("usage: tc2i.py -i <input file with h5 array> -c <channel(s)> -s <output file name stub> -f <factor>")
        sys.exit(2)

    for opt, arg in opts:
        if opt =='-h':
            print("usage: tc2i.py -i <input file with h5 array> -c <channel(s)> -s <output file name stub> ")
            sys.exit()
        elif opt in ("-i","--input_file"):
            input_file = arg
        elif opt in ("-s","--output_name_stub"):
            output_name_stub = arg
        elif opt in ("-c","--channel"):
            channel = int(arg)
        elif opt in ("-f","--factor"):
            factor = int(arg)

    data = util.load_h5_file(input_file)
    for i in range(data.shape[0]):
        d = np.clip( data[i,:,:,channel]*factor, 0, 255).astype('uint8')
        img = Image.fromarray(d)
        name = output_name_stub+"_"+"{:03d}".format(i)+".png"
        img.save(name)
        print("image {0} written".format(name))


