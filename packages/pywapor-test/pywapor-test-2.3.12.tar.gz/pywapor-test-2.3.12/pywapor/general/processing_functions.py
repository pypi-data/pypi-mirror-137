# -*- coding: utf-8 -*-
"""
"""
import os
from osgeo import osr
from osgeo import gdal
import gzip
import zipfile
import numpy as np
from scipy.interpolate import NearestNDInterpolator, LinearNDInterpolator
from pywapor.general.logger import log
import xarray as xr
import pandas as pd

def ds_remove_except(ds, keep_vars):
    keep_vars_coords = list()
    for var in keep_vars:
        if var in list(ds.variables):
            keep_vars_coords += [k for k, v in ds[var].coords.items() if v.size > 0]
    keep_vars_coords = keep_vars + np.unique(keep_vars_coords).tolist()
    drop_vars = [x for x in list(ds.variables) if x not in keep_vars_coords]
    ds = ds.drop_vars(drop_vars)
    return ds

def export_ds_to_tif(ds, vars, base_folder):

    all_files = dict()

    if isinstance(base_folder, type(None)):
        base_folder = os.path.split(ds.encoding["source"])[0]
    
    for var in vars:

        if var not in list(ds.variables):
            continue

        if "lat" not in list(ds[var].coords) or "lon" not in list(ds[var].coords):
            continue

        all_files[var] = list()

        folder = os.path.join(base_folder, f"{var}_output")
        
        if not os.path.exists(folder):
            os.makedirs(folder)

        if "source" in ds[var].attrs.keys():
            source = ds[var].source
        else:
            source = "-"

        if "unit" in ds[var].attrs.keys():
            unit = ds[var].unit
        else:
            unit = "-"

        if "time" in list(ds[var].coords):
            iterator = ds.time
            instantaneous = True
        elif "epoch" in list(ds[var].coords):
            iterator = ds.epoch
            instantaneous = False
        else:
            log.warning(f"! --> not exporting {var}")

        for t in iterator:

            if instantaneous:
                tlength = "inst"
                date_str = pd.Timestamp(t.values).strftime("%Y.%m.%d.%H.%M")
                array = ds[var].sel(time = t).values
            else:
                tdelta = ds.epoch_ends.sel(epoch = t) - ds.epoch_starts.sel(epoch = t)
                tlength = tdelta.values.astype('timedelta64[D]').astype(int)
                date_str = pd.Timestamp(ds.epoch_starts.sel(epoch = t).values).strftime("%Y.%m.%d")
                array = ds[var].sel(epoch = t).values

            fn = f"{var.replace('_','-')}_{source}_{unit}_{tlength}_{date_str}.tif"
            fh = os.path.join(folder, fn)

            Save_as_tiff(fh, array, ds.geotransform, ds.projection)

            all_files[var].append(fh)

    return all_files

def select_template(fhs):
    # Flatten a list-of-lists into a  single list.
    fhs = [val for sublist in fhs for val in sublist]

    # Determine amount of pixels in each file.
    sizes = [gdal.Open(fh).RasterXSize * gdal.Open(fh).RasterYSize for fh in fhs]

    # Find index of file with most pixels.
    idx = np.argmax(sizes)

    # Create resample info.
    example_fh = fhs[idx]
    example_ds = xr.open_dataset(example_fh).isel(band = 0).drop_vars(["band", "spatial_ref"]).rename({"x": "lon", "y": "lat"})
    example_geoinfo = get_geoinfo(example_fh)

    # Calculate pixel size in meters.
    resolution = get_resolution(example_fh)
    log.info(f"--> Resampling resolution is ~{resolution:.0f} meter.")

    return example_fh, example_ds, example_geoinfo, resolution

def get_resolution(example_filepath):
    ds = gdal.Open(example_filepath)
    geo_ex = ds.GetGeoTransform()
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    dlat, dlon = calc_dlat_dlon(geo_ex, xsize, ysize)
    dem_resolution = (np.nanmean(dlon) + np.nanmean(dlat))/2
    return dem_resolution

def reproject_clip(source_fp, dest_fp = None, bb = None,
                    compress = True, dstSRS = "epsg:4326"):
    """Function that calls gdal.Warp().

    Parameters
    ----------
    source_fp : [type]
        [description]
    dest_fp : [type], optional
        [description], by default None
    bb : tuple, optional
        First item is latlim, second item is lonlim, by default None
    compress : bool, optional
        [description], by default True
    dstSRS : str, optional
        [description], by default "epsg:4326"
    """
    options_dict = {"dstSRS": dstSRS}
    
    if not isinstance(bb, type(None)):
        options_dict["outputBounds"] = (bb[1][0], bb[0][0], 
                                        bb[1][1], bb[0][1])

    if compress:
        options_dict["creationOptions"] = ["COMPRESS=DEFLATE", "ZLEVEL=8"]

    if isinstance(dest_fp, type(None)):
        log.debug(f"Overwriting input file ({source_fp}).")
        dest_fp = source_fp

    options = gdal.WarpOptions(**options_dict)

    out = gdal.Warp(dest_fp, source_fp, options = options)
    out.FlushCache()
    out = None

    return dest_fp

def apply_mask(a, indices, axis):
    """
    https://stackoverflow.com/questions/15469302/numpy-3d-to-2d-transformation-based-on-2d-mask-array
    # replace with np.take(....)?
    """
    magic_index = [np.arange(i) for i in indices.shape]
    magic_index = np.ix_(*magic_index)
    magic_index = magic_index[:axis] + (indices,) + magic_index[axis:]
    return a[magic_index]

def reproj_file(file, template, method):
    ds = reproject_dataset_example(file, template, method = method)
    array = open_as_array(ds)
    return array

def combine_dicts(dicts):
    new_dict = dict()
    for d in dicts:
        for key, value in d.items():
            if key in new_dict.keys():
                new_dict[key].append(value)
            else:
                new_dict[key] = [value]
    return new_dict

def get_geoinfo(template_file):
    if isinstance(template_file, str):
        ds = gdal.Open(template_file)
    elif isinstance(template_file, gdal.Dataset):
        ds = template_file
    geo_ex = ds.GetGeoTransform()
    proj_ex = ds.GetProjection()
    size_x_ex = ds.RasterXSize
    size_y_ex = ds.RasterYSize
    return (geo_ex, proj_ex, size_x_ex, size_y_ex)

def Extract_Data_gz(zip_filename, outfilename):
    """
    This function extract the zip files

    Keyword Arguments:
    zip_filename -- name, name of the file that must be unzipped
    outfilename -- Dir, directory where the unzipped data must be
                           stored
    """

    with gzip.GzipFile(zip_filename, 'rb') as zf:
        file_content = zf.read()
        save_file_content = open(outfilename, 'wb')
        save_file_content.write(file_content)
    save_file_content.close()
    zf.close()
    os.remove(zip_filename)
    
def Save_as_MEM(data='', geo='', projection=''):
    """
    This function save the array as a memory file

    Keyword arguments:
    data -- [array], dataset of the geotiff
    geo -- [minimum lon, pixelsize, rotation, maximum lat, rotation,
            pixelsize], (geospatial dataset)
    projection -- interger, the EPSG code
    """
    # save as a geotiff
    driver = gdal.GetDriverByName("MEM")
    dst_ds = driver.Create('', int(data.shape[1]), int(data.shape[0]), 1,
                           gdal.GDT_Float32)
    srse = osr.SpatialReference()
    if projection == '':
        srse.SetWellKnownGeogCS("WGS84")

    else:
        try:
            if not srse.SetWellKnownGeogCS(projection) == 6:
                srse.SetWellKnownGeogCS(projection)
            else:
                try:
                    srse.ImportFromEPSG(int(projection))
                except:
                    srse.ImportFromWkt(projection)
        except:
            try:
                srse.ImportFromEPSG(int(projection))
            except:
                srse.ImportFromWkt(projection)
    dst_ds.SetProjection(srse.ExportToWkt())
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    dst_ds.SetGeoTransform(geo)
    dst_ds.GetRasterBand(1).WriteArray(data)
    return(dst_ds)   
    
def Save_as_tiff(name='', data='', geo='', projection=''):
    """
    This function save the array as a geotiff

    Keyword arguments:
    name -- string, directory name
    data -- [array], dataset of the geotiff
    geo --  [minimum lon, pixelsize, rotation, maximum lat, rotation,
            pixelsize], (geospatial dataset)
    projection -- integer, the EPSG code
    """
    # Change no data values
    data[np.isnan(data)] = -9999

    if not os.path.exists(os.path.split(name)[0]):
        os.makedirs(os.path.split(name)[0])
    
    # save as a geotiff
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(name, int(data.shape[1]), int(data.shape[0]), 1,
                           gdal.GDT_Float32, ['COMPRESS=LZW', 'PREDICTOR=3'])
    srse = osr.SpatialReference()
    if projection == '':
        srse.SetWellKnownGeogCS("WGS84")

    # Set the projection, which can be an EPSG code or a well known GeogCS
    else:
        try:
            if not srse.SetWellKnownGeogCS(projection) == 6:
                srse.SetWellKnownGeogCS(projection)
            else:
                try:
                    srse.ImportFromEPSG(int(projection))
                except:
                    srse.ImportFromWkt(projection)
        except:
            try:
                srse.ImportFromEPSG(int(projection))
            except:
                srse.ImportFromWkt(projection)
                
    # Save the tiff file
    dst_ds.SetProjection(srse.ExportToWkt())
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    dst_ds.SetGeoTransform(geo)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds = None
    
    return()
    
def reproject_MODIS(input_name, epsg_to):
    '''
    Reproject the merged data file by using gdalwarp. The input projection must be the MODIS projection.
    The output projection can be defined by the user.

    Keywords arguments:
    input_name -- 'C:/file/to/path/file.tif'
        string that defines the input tiff file
    epsg_to -- integer
        The EPSG code of the output dataset
    '''
    
    # Define the output name
    name_out = ''.join(input_name.split(".")[:-1]) + '_reprojected.tif'
   
    src_ds = gdal.Open(input_name)
    
    # Define target SRS
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(int(epsg_to))
    dst_wkt = dst_srs.ExportToWkt()
    
    error_threshold = 0.125  # error threshold --> use same value as in gdalwarp
    resampling = gdal.GRA_NearestNeighbour
    
    # Call AutoCreateWarpedVRT() to fetch default values for target raster dimensions and geotransform
    tmp_ds = gdal.AutoCreateWarpedVRT( src_ds,
                                   None, # src_wkt : left to default value --> will use the one from source
                                   dst_wkt,
                                   resampling,
                                   error_threshold )
    dst_ds = gdal.GetDriverByName('GTiff').CreateCopy(name_out, tmp_ds)
    dst_ds = None 

    return(name_out)
    
def clip_data(input_file, latlim, lonlim):
    """
    Clip the data to the defined extend of the user (latlim, lonlim)

    Keyword Arguments:
    input_file -- output data, output of the clipped dataset
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    """
    try:
        if input_file.split('.')[-1] == 'tif':
            dest_in = gdal.Open(input_file)
        else:
            dest_in = input_file
    except:
        dest_in = input_file

    # Open Array
    data_in = dest_in.GetRasterBand(1).ReadAsArray()

    # Define the array that must remain
    Geo_in = dest_in.GetGeoTransform()
    Geo_in = list(Geo_in)
    Start_x = np.max([int(np.floor(((lonlim[0]) - Geo_in[0])/ Geo_in[1])),0])
    End_x = np.min([int(np.ceil(((lonlim[1]) - Geo_in[0])/ Geo_in[1])),int(dest_in.RasterXSize)])

    Start_y = np.max([int(np.floor((Geo_in[3] - latlim[1])/ -Geo_in[5])),0])
    End_y = np.min([int(np.ceil(((latlim[0]) - Geo_in[3])/Geo_in[5])), int(dest_in.RasterYSize)])

    #Create new GeoTransform
    Geo_in[0] = Geo_in[0] + Start_x * Geo_in[1]
    Geo_in[3] = Geo_in[3] + Start_y * Geo_in[5]
    Geo_out = tuple(Geo_in)

    data = np.zeros([End_y - Start_y, End_x - Start_x])

    data = data_in[Start_y:End_y,Start_x:End_x]
    dest_in = None

    return(data, Geo_out)    
    
    
def Extract_Data(input_file, output_folder):
    """
    This function extract the zip files

    Keyword Arguments:
    output_file -- name, name of the file that must be unzipped
    output_folder -- Dir, directory where the unzipped data must be
                           stored
    """
    # extract the data
    z = zipfile.ZipFile(input_file, 'r')
    z.extractall(output_folder)
    z.close()    

def reproj_ds(source_file, example_file, ndv = -9999, override_dtype = True):
    
    source_ds = gdal.Open(source_file)

    example_ds = gdal.Open(example_file)
    example_xsize = example_ds.RasterXSize
    example_ysize = example_ds.RasterYSize

    if override_dtype:
        example_dtype = example_ds.GetRasterBand(1).DataType
    else:
        example_dtype = source_ds.GetRasterBand(1).DataType

    mem_drv = gdal.GetDriverByName('MEM')
    dest_ds = mem_drv.Create('', example_xsize, example_ysize, 1, example_dtype)
    dest_ds.SetGeoTransform(example_ds.GetGeoTransform())
    dest_ds.SetProjection(example_ds.GetProjection())
    dest_ds.GetRasterBand(1).Fill(ndv)
    dest_ds.GetRasterBand(1).SetNoDataValue(ndv)

    gdal.ReprojectImage(source_ds,
                        dest_ds,
                        source_ds.GetProjection(),
                        dest_ds.GetProjection(),
                        gdal.GRA_NearestNeighbour)

    return dest_ds

def reproject_dataset_example(dataset, dataset_example, method=1):
    """
    A sample function to reproject and resample a GDAL dataset from within
    Python. The user can define the wanted projection and shape by defining an example dataset.

    Keywords arguments:
    dataset -- 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(filename))
        string that defines the input tiff file or gdal file
    dataset_example -- 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(filename))
        string that defines the input tiff file or gdal file
    method -- 1,2,3,4 default = 1
        1 = Nearest Neighbour, 2 = Bilinear, 3 = lanzcos, 4 = average
    """
    # open dataset that must be transformed
    if isinstance(dataset, str):
        g = gdal.Open(dataset)
    elif isinstance(dataset, gdal.Dataset):
        g = dataset
    else:
        raise ValueError
    epsg_from = Get_epsg(g)

    #exceptions
    if epsg_from == 9001:
        epsg_from = 5070

    # open dataset that is used for transforming the dataset
    if isinstance(dataset_example, str):
        gland = gdal.Open(dataset_example)
    elif isinstance(dataset_example, gdal.Dataset):
        gland = dataset_example
    else:
        raise ValueError
    epsg_to = Get_epsg(gland)

    # Set the EPSG codes
    osng = osr.SpatialReference()
    osng.ImportFromEPSG(epsg_to)
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromEPSG(epsg_from)

    # Get shape and geo transform from example
    geo_land = gland.GetGeoTransform()
    col=gland.RasterXSize
    rows=gland.RasterYSize

    # Create new raster
    mem_drv = gdal.GetDriverByName('MEM')
    dest = mem_drv.Create('', col, rows, 1, gdal.GDT_Float32)
    dest.SetGeoTransform(geo_land)
    dest.SetProjection(osng.ExportToWkt())

    # https://gis.stackexchange.com/questions/158503/9999-no-data-value-becomes-0-when-writing-array-to-gdal-memory-file
    ndv = g.GetRasterBand(1).GetNoDataValue()
    band = dest.GetRasterBand(1)
    band.SetNoDataValue(ndv)
    band.Fill(ndv, 0.0)

    # Perform the projection/resampling
    if method == 1:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_NearestNeighbour)
    if method == 2:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Bilinear)
    if method == 3:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Lanczos)
    if method == 4:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Average)
    if method == 5:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Cubic)
    if method == 6:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_CubicSpline)
    if method == 7:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Mode)
    if method == 8:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Max)
    if method == 9:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Min)
    if method == 10:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Med)
    if method == 11:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Q1)
    if method == 12:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Q3)
    if method == 13:
        gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Sum)
        
    return(dest)

def Get_epsg(g):
    """
    This function reads the projection of a GEOGCS file or tiff file

    Keyword arguments:
    g -- string
        Filename to the file that must be read
    extension -- tiff or GEOGCS
        Define the extension of the dataset (default is tiff)
    """
    try:
        # Get info of the dataset that is used for transforming
        g_proj = g.GetProjection()
        Projection=g_proj.split('EPSG","')
        epsg_to=int((str(Projection[-1]).split(']')[0])[0:-1])            
    except:
        epsg_to=4326

    return(epsg_to)

def Show_tif(image_file, Limits = None, Color = None):
    """
    This function plot a tiff array in the console

    Keyword arguments:
    image_file -- string
        Filename to the file that must be shown
    Limits -- [min, max] (Default = min and max image)
        User can define the limits of the colorbar
    Color -- string (Default = "viridis")
        User can define the wanted colormap, all options are listed here:
        https://matplotlib.org/examples/color/colormaps_reference.html
    """    
    dest = gdal.Open(image_file)
    Array = dest.GetRasterBand(1).ReadAsArray()
    Array[Array==-9999] = np.nan
    if Limits == None:
        Limits = [np.nanmin(Array), np.nanmax(Array)]
    
    if Color == None:
        Color = "viridis"
    
    import matplotlib.pyplot as plt
    
    plt.imshow(Array, cmap = Color, vmin=Limits[0], vmax=Limits[1])
    plt.colorbar()
    plt.show()
    
    return()

def open_as_array(input):
    if isinstance(input, str):
        ds = gdal.Open(input)
    elif isinstance(input, gdal.Dataset):
        ds = input
    array = ds.GetRasterBand(1).ReadAsArray().astype(float)
    ndv = ds.GetRasterBand(1).GetNoDataValue()
    array[array == ndv] = np.nan
    return array  

def Open_tiff_array(filename='', band=''):
    """
    Opening a tiff array.

    Keyword Arguments:
    filename -- 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(filename))
        string that defines the input tiff file or gdal file
    band -- integer
        Defines the band of the tiff that must be opened.
    """
    f = gdal.Open(filename)
    if f is None:
        print('%s does not exists' %filename)
    else:
        if band == '':
            band = 1
        Data = f.GetRasterBand(band).ReadAsArray()
    return(Data)

def Open_array_info(filename=''):
    """
    Opening a tiff info, for example size of array, projection and transform matrix.

    Keyword Arguments:
    filename -- 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(filename))
        string that defines the input tiff file or gdal file

    """
    try:
        if filename.split('.')[-1] == 'tif':
            f = gdal.Open(r"%s" %filename)
        else:
            f = filename
    except:
            f = filename       
    try:
        geo_out = f.GetGeoTransform()
        proj = f.GetProjection()
        size_X = f.RasterXSize
        size_Y = f.RasterYSize
        f = None
    except:
        print('%s does not exists' %filename)
        
    return(geo_out, proj, size_X, size_Y)

def gap_filling(dataset, NoDataValue, method = 1):
    """
    This function fills the no data gaps in a numpy array

    Keyword arguments:
    dataset -- 'C:/'  path to the source data (dataset that must be filled)
    NoDataValue -- Value that must be filled
    """
    try:
        if dataset.split('.')[-1] == 'tif':
            # Open the numpy array
            data = Open_tiff_array(dataset)
            Save_as_tiff_bool = 1
        else:
            data = dataset
            Save_as_tiff_bool = 0
    except:
        data = dataset
        Save_as_tiff_bool = 0

    # fill the no data values
    if NoDataValue == np.nan:
        mask = ~(np.isnan(data))
    else:
        mask = ~(data==NoDataValue)
    xx, yy = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
    xym = np.vstack( (np.ravel(xx[mask]), np.ravel(yy[mask])) ).T
    data0 = np.ravel( data[:,:][mask] )

    if method == 1:
        interp0 = NearestNDInterpolator( xym, data0 )
        data_end = interp0(np.ravel(xx), np.ravel(yy)).reshape( xx.shape )

    if method == 2:
        interp0 = LinearNDInterpolator( xym, data0 )
        data_end = interp0(np.ravel(xx), np.ravel(yy)).reshape( xx.shape )

    if Save_as_tiff_bool == 1:
        EndProduct=dataset[:-4] + '_GF.tif'

        # collect the geoinformation
        geo_out, proj, size_X, size_Y = Open_array_info(dataset)

        # Save the filled array as geotiff
        Save_as_tiff(name=EndProduct, data=data_end, geo=geo_out, projection=proj)

    else:
        EndProduct = data_end

    return (EndProduct)  
    
def calc_dlat_dlon(geo_out, size_X, size_Y, lat_lon = None):
    """
    This functions calculated the distance between each pixel in meter.

    Parameters
    ----------
    geo_out: array
        geo transform function of the array
    size_X: int
        size of the X axis
    size_Y: int
        size of the Y axis

    Returns
    -------
    dlat: array
        Array containing the vertical distance between each pixel in meters
    dlon: array
        Array containing the horizontal distance between each pixel in meters
    """
    if isinstance(lat_lon, type(None)):
        # Create the lat/lon rasters
        lon = np.arange(size_X + 1)*geo_out[1]+geo_out[0] - 0.5 * geo_out[1]
        lat = np.arange(size_Y + 1)*geo_out[5]+geo_out[3] - 0.5 * geo_out[5]
    else:
        lat, lon = lat_lon

    dlat_2d = np.array([lat,]*int(np.size(lon,0))).transpose()
    dlon_2d =  np.array([lon,]*int(np.size(lat,0)))

    # Radius of the earth in meters
    R_earth = 6371000

    # Calculate the lat and lon in radians
    lonRad = dlon_2d * np.pi/180
    latRad = dlat_2d * np.pi/180

    # Calculate the difference in lat and lon
    lonRad_dif = abs(lonRad[:,1:] - lonRad[:,:-1])
    latRad_dif = abs(latRad[:-1] - latRad[1:])

    # Calculate the distance between the upper and lower pixel edge
    a = np.sin(latRad_dif[:,:-1]/2) * np.sin(latRad_dif[:,:-1]/2)
    clat = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    dlat = R_earth * clat

    # Calculate the distance between the eastern and western pixel edge
    b = np.cos(latRad[1:,:-1]) * np.cos(latRad[:-1,:-1]) * np.sin(lonRad_dif[:-1,:]/2) * np.sin(lonRad_dif[:-1,:]/2)
    clon = 2 * np.arctan2(np.sqrt(b), np.sqrt(1-b))
    dlon = R_earth * clon

    return(dlat, dlon)  
    
