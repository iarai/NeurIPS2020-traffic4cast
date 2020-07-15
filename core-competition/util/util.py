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
import os, csv, sys
import h5py

# -----------------------------------------------------------------
# h5 file support
# -----------------------------------------------------------------

def load_h5_file(file_path):
    """
    Given a file path to an h5 file assumed to house a tensor, 
    load that tensor into memory and return a pointer.
    """
    # load
    fr = h5py.File(file_path, 'r')
    a_group_key = list(fr.keys())[0]
    data = list(fr[a_group_key])
    # transform to appropriate numpy array 
    data=data[0:]
    data = np.stack(data, axis=0)
    return data

def print_shape(data):
    """
    print data shape
    """
    print(data.shape)

def write_data_to_h5(data, filename):
    """
    write data in gzipped h5 format
    """
    f = h5py.File(filename, 'w', libver='latest')
    dset = f.create_dataset('array', shape=(data.shape), data=data, compression='gzip', compression_opts=9)
    f.close()


# -----------------------------------------------------------------
# os support
# -----------------------------------------------------------------

def create_directory_structure(root, structure_path_list):
    """
    This command will create in the file system location root a subdirectory path
    determined in structure_path_list. For example
    creat_directory_path(".",["this","is","working") will create the directory path
    /this/is/working
    in the current directory. A touch of touch.
    """
    path = os.path.join(root, *structure_path_list)
    try:
        os.makedirs(path)
    except OSError:
        print("failed to create directory structure")
        sys.exit(2)

def list_filenames(directory):
    return os.listdir(directory)
