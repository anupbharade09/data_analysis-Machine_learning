#netcdf4 package is used to read and modify cdf files
from netCDF4 import Dataset
import glob
from os.path import basename
from sys import argv

#function to add variables in cdf file

def add_variables_to_cdf(src_file):

    # below command opens the file into append mode
    rootgrp = Dataset(src_file, "r+", format="NETCDF4")

    # To create dimension createDimension function is used
    rootgrp.createDimension('instrument_number',size=1)

    # To create variables with the above dimenstion , creaeVariable function is used.
    rootgrp.createVariable('instrument_name','S1',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_id','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_mfr','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_model','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_serial_no','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_sw_version','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_fw_version','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_os_version','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_app_version','c',('instrument_number','_32_byte_string'))
    rootgrp.createVariable('instrument_comments','c',('instrument_number','_32_byte_string'))


# Files to be modified are picked up from a folder and list is created of their names

folder_name = argv[1]
print(folder_name)
filenames = (glob.glob(folder_name+"/*.cdf"))

# Recursive call to add_variables_to_cdf function

for file in filenames:
    print('Processing file "%s"' % basename(file))
    add_variables_to_cdf(file)