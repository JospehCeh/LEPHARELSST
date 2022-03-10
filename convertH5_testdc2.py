import h5py
import numpy as np

def load_raw_hdf5_data(infile, groupname='None'):
    """
    read in h5py hdf5 data, return a dictionary of all of the keys
    """
    data = {}
    infp = h5py.File(infile, "r")
    if groupname != 'None':
        f = infp[groupname]
    else:
        f = infp
    for key in f.keys():
        data[key] = np.array(f[key])
    infp.close()
    return data

def group_entries(f):
    """
    group entries in single numpy array
    
    """
    galid = f['id'][()][:,np.newaxis]
    redshift = f['redshift'][()][:,np.newaxis]
    mag_err_g_lsst = f['mag_err_g_lsst'][()][:,np.newaxis]
    mag_err_i_lsst = f['mag_err_i_lsst'][()][:,np.newaxis]
    mag_err_r_lsst = f['mag_err_r_lsst'][()][:,np.newaxis]
    mag_err_u_lsst = f['mag_err_u_lsst'][()][:,np.newaxis]
    mag_err_y_lsst = f['mag_err_y_lsst'][()][:,np.newaxis]
    mag_err_z_lsst = f['mag_err_z_lsst'][()][:,np.newaxis]
    mag_g_lsst = f['mag_g_lsst'][()][:,np.newaxis]
    mag_i_lsst = f['mag_i_lsst'][()][:,np.newaxis]
    mag_r_lsst = f['mag_r_lsst'][()][:,np.newaxis]
    mag_u_lsst = f['mag_u_lsst'][()][:,np.newaxis]
    mag_y_lsst = f['mag_y_lsst'][()][:,np.newaxis]
    mag_z_lsst = f['mag_z_lsst'][()][:,np.newaxis]
    context = np.full(galid.shape, 255)
    
    full_arr=np.hstack( (galid, mag_u_lsst, mag_err_u_lsst,\
                                mag_g_lsst, mag_err_g_lsst,\
                                mag_r_lsst, mag_err_r_lsst,\
                                mag_i_lsst, mag_err_i_lsst,\
                                mag_z_lsst, mag_err_z_lsst,\
                                mag_y_lsst, mag_err_y_lsst,\
                                context, redshift) )
    return full_arr

def filter_mag_entries(d):
    """
    Filter accoding magnitudes
    
    Only remove creazy u values
    """
    
    u=d[:,1]
    
    idx_u= np.where(u>31.8)[0]  
    #d_del=np.delete(d,idx_u,axis=0)
    
    return np.array(idx_u)

def mag_to_flux(d):
    """  
    Convert magnitudes to fluxes

    :param d:
    :return:
    """

    nb=6
    fluxes=np.zeros_like(d)
   

    fluxes[:,0]=d[:,0]
    fluxes[:,13]=d[:,13]
    fluxes[:,14]=d[:,14]
    
    for idx in np.arange(nb):
        fluxes[:,1+2*idx]=np.power(10,-0.4*d[:,1+2*idx])
        fluxes[:,2+2*idx]=fluxes[:,1+2*idx]*d[:,2+2*idx]
    return fluxes

def filter_fluxes_entries(d,nsig=5):
    """
    """ 
    nb=6
    
    indexes=[]
    #indexes=np.array(indexes,dtype=np.int)
    indexes=np.array(indexes,dtype=int)
    
    for idx in np.arange(nb):
        ratio=d[:,1+2*idx]/d[:,2+2*idx]  # flux divided by sigma-flux
        bad_indexes=np.where(ratio<nsig)[0]
        indexes=np.concatenate((indexes,bad_indexes))
        
    indexes=np.unique(indexes)
    return np.sort(indexes)

def filter_sigtonoise_entries(d,nsig=5):
    """
    """ 
    nb=6
    
    indexes=[]
    #indexes=np.array(indexes,dtype=np.int)
    indexes=np.array(indexes,dtype=int)
    
    for idx in np.arange(nb):
        errMag=d[:,2+2*idx]  # error in M_AB
        bad_indexes=np.where(errMag > (1/nsig))[0]
        indexes=np.concatenate((indexes,bad_indexes))
        
    indexes=np.unique(indexes)
    return np.sort(indexes)

filename = 'test_dc2_validation_9816.hdf5'
h5_file = load_raw_hdf5_data(filename , groupname='photometry')

## produce a numpy array
dataArray=group_entries(h5_file)
#print(dataArray.shape)

# Filter mag entries
indexes=filter_mag_entries(dataArray)
#print(indexes.shape)
data_f0=dataArray
data_f=np.delete(dataArray,indexes,axis=0)
data_f_removed=dataArray[indexes,:]
print("U-Magnitude filter: {} original, {} removed, {} left ({} total for check).".format(data_f0.shape, data_f_removed.shape, data_f.shape, data_f_removed.shape[0]+data_f.shape[0]))

# Get data better than 6 SNR
indexes_bad=filter_sigtonoise_entries(data_f,nsig=5)
data_f=np.delete(data_f,indexes_bad,axis=0)
print("SNR filter: {} bad indexes, {} left ({} total for check).".format(indexes_bad.shape, data_f.shape, indexes_bad.shape[0]+data_f.shape[0]))

#h5_file=h5py.File(filename, "r")
#photometry=h5_file.get('photometry')
#photometry.keys()
#dataArray = np.empty(shape=(np.array(photometry['id']).shape[0], np.array(photometry).shape[0]+1))
#dataArray[:, 0] = np.array(photometry['id'], dtype=np.int64)

#keyList=['mag_u_lsst', 'mag_err_u_lsst',\
#            'mag_g_lsst', 'mag_err_g_lsst',\
#            'mag_r_lsst', 'mag_err_r_lsst',\
#            'mag_i_lsst', 'mag_err_i_lsst',\
#            'mag_z_lsst', 'mag_err_z_lsst',\
#            'mag_y_lsst', 'mag_err_y_lsst']

#ind=0
#for key in keyList:
#    ind+=1
#    dataArray[:, ind] = np.array(photometry[key])

#ind+=1
#dataArray[:, ind] = np.full(photometry['id'].shape, 255)
#ind+=1
#dataArray[:, ind] = np.array(photometry['redshift'])


np.savetxt('DC2_VALID_CAT_IN.in', data_f, fmt=['%1i', '%1.6g', '%1.6g',\
                                                         '%1.6g', '%1.6g',\
                                                         '%1.6g', '%1.6g',\
                                                         '%1.6g', '%1.6g',\
                                                         '%1.6g', '%1.6g',\
                                                         '%1.6g', '%1.6g',\
                                                         '%1i', '%1.3f'])
#h5_file.close()


