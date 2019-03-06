import netCDF4 as nc
import glob
from os.path import basename
from sys import argv

def create_file_from_source(src_file,trg_file,scan_start,scan_end):
    scan_start = int(scan_start)
    scan_end = int(scan_end)
    no_scans = int(scan_end) - int(scan_start)
    print('scan_start: ',scan_start)
    print('scan_end: ',scan_end)
    print('co_scans: ',no_scans)
    src = nc.Dataset(src_file)
    #src_data = nc.Dataset(src_data_file)
    trg = nc.Dataset(trg_file, mode='w',format="NETCDF3_CLASSIC")
    names = []


    # Create the dimensions of the file
    for name, dim in src.dimensions.items():
        #print(name)
        #print(len(dim))
        if name == 'scan_number':
            #trg.createDimension(name, 655 if not dim.isunlimited() else None)
            trg.createDimension(name, no_scans if not dim.isunlimited() else None)
        else:
            trg.createDimension(name, len(dim) if not dim.isunlimited() else None)

    # Copy the global attributes
    trg.setncatts({a:src.getncattr(a) for a in src.ncattrs()})

    for na,var in src.variables.items():
        #since dimensions of mass_Vales, intensity and error_log is different

        if na == 'mass_values' or na == 'intensity_values' or na == 'error_log':
            names.append(na)

    # Create the variables in the file
    for name, var in src.variables.items():
        trg.createVariable(name, var.dtype, var.dimensions)

        # Copy the variable attributes
        trg.variables[name].setncatts({a:var.getncattr(a) for a in var.ncattrs()})

        # Copy the variables values (as 'f4' eventually)
        if name not in names:
            # For  acid's RT values

            trg.variables[name][:] = src.variables[name][scan_start:scan_end]
        elif name == 'mass_values':

            trg.variables[name][:] = src.variables[name][src.variables['scan_index'][scan_start]:src.variables['scan_index'][scan_end]]

        elif name == 'intensity_values':

            trg.variables[name][:] = src.variables[name][src.variables['scan_index'][scan_start]:src.variables['scan_index'][scan_end]]
        else:

            trg.variables[name][:] = src.variables[name][:]

    # update scan index starting from 0 since we are shifting it

    trg.variables['scan_index'][:] = [x - trg.variables['scan_index'][0] for x in trg.variables['scan_index']]

    # Save the file
    trg.close()


src_folder = argv[1]
trg_folder = argv[2]
src_files = (glob.glob(src_folder+"/*.cdf"))

for i in src_files:
    open(trg_folder+''+basename(i),'a').close()

trg_files = (glob.glob(trg_folder+"/*.cdf"))

scan_start = argv[3]
scan_end= argv[4]


for src_file,trg_file in zip(src_files,trg_files):
    create_file_from_source(src_file,trg_file,scan_start,scan_end)
