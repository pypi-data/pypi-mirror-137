# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 20:09:37 2021

@author: PURUSHOT

Post processing example scripts for results with LaueToolsNN
"""

import _pickle as cPickle
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable
import lauetoolsnn.lauetools.CrystalParameters as CP
import lauetoolsnn.lauetools.dict_LaueTools as dictLT
import scipy
from scipy.spatial.transform import Rotation as R

def rot_mat_to_euler(rot_mat): 
    r = R.from_matrix(rot_mat)
    return r.as_euler('zxz')* 180/np.pi

results_folder = r"path to results directory"
    
with open(results_folder+ "//results.pickle", "rb") as input_file:
    best_match, mat_global, rotation_matrix1, strain_matrix, strain_matrixs,\
        col, colx, coly, match_rate, files_treated,\
            lim_x, lim_y, spots_len, iR_pix, fR_pix, material_, \
                material1_, lattice_, lattice1_,\
                symmetry, symmetry1, crystal, crystal1 = cPickle.load(input_file)

## results directory
save_directory_ = os.getcwd() + "\\" + results_folder.split("\\")[-1]
if not os.path.exists(save_directory_):
    os.makedirs(save_directory_)
    
match_tol = 25
fR_tol = 2
matnumber = 1
bins = 100
rangeval = len(match_rate)
material_id = [material_, material1_]
matid = 0

#%%establish mu sigma range for all dataset
mu_sd = []
count = 0
for index in range(rangeval):
    ### index for nans
    nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
    nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
    mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
    nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
    nan_index = np.unique(nan_index)
    
    if count == 0:
        spots_len_plot = np.copy(spots_len[index][0])
        mr_plot = np.copy(match_rate[index][0])
        iR_pix_plot = np.copy(iR_pix[index][0])
        fR_pix_plot = np.copy(fR_pix[index][0])
        strain_matrix_plot = np.copy(strain_matrix[index][0])
        e11c = np.copy(strain_matrix_plot[:,0,0])#.reshape((lim_x, lim_y))
        e22c = np.copy(strain_matrix_plot[:,1,1])#.reshape((lim_x, lim_y))
        e33c = np.copy(strain_matrix_plot[:,2,2])#.reshape((lim_x, lim_y))
        e12c = np.copy(strain_matrix_plot[:,0,1])#.reshape((lim_x, lim_y))
        e13c = np.copy(strain_matrix_plot[:,0,2])#.reshape((lim_x, lim_y))
        e23c = np.copy(strain_matrix_plot[:,1,2])#.reshape((lim_x, lim_y))
        spots_len_plot[nan_index] = np.nan 
        mr_plot[nan_index] = np.nan 
        iR_pix_plot[nan_index] = np.nan 
        fR_pix_plot[nan_index] = np.nan 
        e11c[nan_index] = np.nan 
        e22c[nan_index] = np.nan 
        e33c[nan_index] = np.nan 
        e12c[nan_index] = np.nan 
        e13c[nan_index] = np.nan 
        e23c[nan_index] = np.nan 
        count = 1
        
    else:
        temp = np.copy(spots_len[index][0])
        temp[nan_index] = np.nan
        spots_len_plot = np.vstack((spots_len_plot,temp))
        
        temp = np.copy(match_rate[index][0])
        temp[nan_index] = np.nan
        mr_plot = np.vstack((mr_plot,temp))
        
        temp = np.copy(iR_pix[index][0])
        temp[nan_index] = np.nan
        iR_pix_plot = np.vstack((iR_pix_plot,temp))

        temp = np.copy(fR_pix[index][0])
        temp[nan_index] = np.nan
        fR_pix_plot = np.vstack((fR_pix_plot,temp))
        
        strain_matrix_plot = np.copy(strain_matrix[index][0])
        temp = np.copy(strain_matrix_plot[:,0,0])
        temp[nan_index] = np.nan
        e11c = np.vstack((e11c,temp))
        temp = np.copy(strain_matrix_plot[:,1,1])
        temp[nan_index] = np.nan
        e22c = np.vstack((e22c,temp))
        temp = np.copy(strain_matrix_plot[:,2,2])
        temp[nan_index] = np.nan
        e33c = np.vstack((e33c,temp))
        temp = np.copy(strain_matrix_plot[:,0,1])
        temp[nan_index] = np.nan
        e12c = np.vstack((e12c,temp))
        temp = np.copy(strain_matrix_plot[:,0,2])
        temp[nan_index] = np.nan
        e13c = np.vstack((e13c,temp))
        temp = np.copy(strain_matrix_plot[:,1,2])
        temp[nan_index] = np.nan
        e23c = np.vstack((e23c,temp))

spots_len_plot = spots_len_plot.flatten()
mr_plot = mr_plot.flatten()
iR_pix_plot = iR_pix_plot.flatten()
fR_pix_plot = fR_pix_plot.flatten() 
e11c = e11c.flatten()
e22c = e22c.flatten()
e33c = e33c.flatten()
e12c = e12c.flatten()
e13c = e13c.flatten()
e23c = e23c.flatten()

spots_len_plot = spots_len_plot[~np.isnan(spots_len_plot)]
mr_plot = mr_plot[~np.isnan(mr_plot)]
iR_pix_plot = iR_pix_plot[~np.isnan(iR_pix_plot)]
fR_pix_plot = fR_pix_plot[~np.isnan(fR_pix_plot)]
e11c = e11c[~np.isnan(e11c)]
e22c = e22c[~np.isnan(e22c)]
e33c = e33c[~np.isnan(e33c)]
e12c = e12c[~np.isnan(e12c)]
e13c = e13c[~np.isnan(e13c)]
e23c = e23c[~np.isnan(e23c)]

logdata = e11c
estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))

logdata = e22c
estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))

logdata = e33c
estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))

logdata = e12c
estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))

logdata = e13c
estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))

logdata = e23c
estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))


#%% Compute lattice params from strain
for index in range(rangeval):

    constantlength = "a"
    
    a,b,c,alp,bet,gam = [],[],[],[],[],[]
    #TODO all images and not only one
    for irot in range(len(rotation_matrix1[index][0])):
        if (match_rate[index][0][irot] < match_tol) or \
            fR_pix[index][0][irot] > fR_tol:
            continue
        
        lattice_parameter_direct_strain = CP.computeLatticeParameters_from_UB(rotation_matrix1[index][0][irot,:,:], 
                                                                              material_, 
                                                                              constantlength, 
                                                                              dictmaterials=dictLT.dict_Materials)
        a.append(lattice_parameter_direct_strain[0])
        b.append(lattice_parameter_direct_strain[1])
        c.append(lattice_parameter_direct_strain[2])
        alp.append(lattice_parameter_direct_strain[3])
        bet.append(lattice_parameter_direct_strain[4])
        gam.append(lattice_parameter_direct_strain[5])
    
    title = "Refined unit cell"+" "+material_id[0]+ " "+str(index)
    fig = plt.figure()
    axs = fig.subplots(2, 3)
    axs[0, 0].set_title(r"a", loc='center', fontsize=8)
    logdata = np.array(a)
    logdata = logdata[~np.isnan(logdata)]
    rangemin, rangemax = np.min(logdata)-0.01, np.max(logdata)+0.01
    axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    axs[0, 0].set_ylabel('Frequency', fontsize=8)
    axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
    axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)

    axs[0, 1].set_title(r"b", loc='center', fontsize=8)
    logdata = np.array(b)
    logdata = logdata[~np.isnan(logdata)]
    rangemin, rangemax = np.min(logdata)-0.01, np.max(logdata)+0.01
    axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    axs[0, 1].set_ylabel('Frequency', fontsize=8)
    axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
    axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
    
    axs[0, 2].set_title(r"c", loc='center', fontsize=8)
    logdata = np.array(c)
    logdata = logdata[~np.isnan(logdata)]
    rangemin, rangemax = np.min(logdata)-0.01, np.max(logdata)+0.01
    axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    axs[0, 2].set_ylabel('Frequency', fontsize=8)
    axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
    axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
    
    axs[1, 0].set_title(r"$\alpha$", loc='center', fontsize=8)
    logdata = np.array(alp)
    logdata = logdata[~np.isnan(logdata)]
    rangemin, rangemax = np.min(logdata)-0.01, np.max(logdata)+0.01
    axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    axs[1, 0].set_ylabel('Frequency', fontsize=8)
    axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
    axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
    
    axs[1, 1].set_title(r"$\beta$", loc='center', fontsize=8)
    logdata = np.array(bet)
    logdata = logdata[~np.isnan(logdata)]
    rangemin, rangemax = np.min(logdata)-0.01, np.max(logdata)+0.01
    axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    axs[1, 1].set_ylabel('Frequency', fontsize=8)
    axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
    axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
    
    axs[1, 2].set_title(r"$\gamma$", loc='center', fontsize=8)
    logdata = np.array(gam)
    logdata = logdata[~np.isnan(logdata)]
    rangemin, rangemax = np.min(logdata)-0.01, np.max(logdata)+0.01
    axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
    axs[1, 2].set_ylabel('Frequency', fontsize=8)
    axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
    axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
    

    plt.tight_layout()
    plt.savefig(save_directory_+"\\"+title+'.png', format='png', dpi=1000) 
    plt.close(fig)

    #%% Range min max for strain plots
    rangemin = -0.3
    rangemax = 0.3
    
    #%% Plot histograms
    mu_sd1 = []
    ### index for nans
    nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
    nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
    mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
    nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
    nan_index = np.unique(nan_index)
    
    spots_len_plot = np.copy(spots_len[index][0])
    mr_plot = np.copy(match_rate[index][0])
    iR_pix_plot = np.copy(iR_pix[index][0])
    fR_pix_plot = np.copy(fR_pix[index][0])
    strain_matrix_plot = np.copy(strain_matrix[index][0])
    e11c = np.copy(strain_matrix_plot[:,0,0])#.reshape((lim_x, lim_y))
    e22c = np.copy(strain_matrix_plot[:,1,1])#.reshape((lim_x, lim_y))
    e33c = np.copy(strain_matrix_plot[:,2,2])#.reshape((lim_x, lim_y))
    e12c = np.copy(strain_matrix_plot[:,0,1])#.reshape((lim_x, lim_y))
    e13c = np.copy(strain_matrix_plot[:,0,2])#.reshape((lim_x, lim_y))
    e23c = np.copy(strain_matrix_plot[:,1,2])#.reshape((lim_x, lim_y))
    strain_matrixs_plot = np.copy(strain_matrixs[index][0])
    e11s = np.copy(strain_matrixs_plot[:,0,0])#.reshape((lim_x, lim_y))
    e22s = np.copy(strain_matrixs_plot[:,1,1])#.reshape((lim_x, lim_y))
    e33s = np.copy(strain_matrixs_plot[:,2,2])#.reshape((lim_x, lim_y))
    e12s = np.copy(strain_matrixs_plot[:,0,1])#.reshape((lim_x, lim_y))
    e13s = np.copy(strain_matrixs_plot[:,0,2])#.reshape((lim_x, lim_y))
    e23s = np.copy(strain_matrixs_plot[:,1,2])#.reshape((lim_x, lim_y))
    spots_len_plot[nan_index] = np.nan 
    mr_plot[nan_index] = np.nan 
    iR_pix_plot[nan_index] = np.nan 
    fR_pix_plot[nan_index] = np.nan 
    e11c[nan_index] = np.nan 
    e22c[nan_index] = np.nan 
    e33c[nan_index] = np.nan 
    e12c[nan_index] = np.nan 
    e13c[nan_index] = np.nan 
    e23c[nan_index] = np.nan 
    e11s[nan_index] = np.nan 
    e22s[nan_index] = np.nan 
    e33s[nan_index] = np.nan 
    e12s[nan_index] = np.nan 
    e13s[nan_index] = np.nan 
    e23s[nan_index] = np.nan 
        
    spots_len_plot = spots_len_plot.flatten()
    mr_plot = mr_plot.flatten()
    iR_pix_plot = iR_pix_plot.flatten()
    fR_pix_plot = fR_pix_plot.flatten() 
    e11c = e11c.flatten()
    e22c = e22c.flatten()
    e33c = e33c.flatten()
    e12c = e12c.flatten()
    e13c = e13c.flatten()
    e23c = e23c.flatten()
    e11s = e11s.flatten()
    e22s = e22s.flatten()
    e33s = e33s.flatten()
    e12s = e12s.flatten()
    e13s = e13s.flatten()
    e23s = e23s.flatten()
    
    spots_len_plot = spots_len_plot[~np.isnan(spots_len_plot)]
    mr_plot = mr_plot[~np.isnan(mr_plot)]
    iR_pix_plot = iR_pix_plot[~np.isnan(iR_pix_plot)]
    fR_pix_plot = fR_pix_plot[~np.isnan(fR_pix_plot)]
    e11c = e11c[~np.isnan(e11c)]
    e22c = e22c[~np.isnan(e22c)]
    e33c = e33c[~np.isnan(e33c)]
    e12c = e12c[~np.isnan(e12c)]
    e13c = e13c[~np.isnan(e13c)]
    e23c = e23c[~np.isnan(e23c)]
    e11s = e11s[~np.isnan(e11s)]
    e22s = e22s[~np.isnan(e22s)]
    e33s = e33s[~np.isnan(e33s)]
    e12s = e12s[~np.isnan(e12s)]
    e13s = e13s[~np.isnan(e13s)]
    e23s = e23s[~np.isnan(e23s)]
    
    try:
        title = "Number of spots and matching rate"
        fig = plt.figure()
        axs = fig.subplots(1, 2)
        axs[0].set_title("Number of spots", loc='center', fontsize=8)
        axs[0].hist(spots_len_plot, bins=bins)
        axs[0].set_ylabel('Frequency', fontsize=8)
        axs[0].tick_params(axis='both', which='major', labelsize=8)
        axs[0].tick_params(axis='both', which='minor', labelsize=8)
        axs[1].set_title("Matching rate", loc='center', fontsize=8)
        axs[1].hist(mr_plot, bins=bins)
        axs[1].set_ylabel('Frequency', fontsize=8)
        axs[1].tick_params(axis='both', which='major', labelsize=8)
        axs[1].tick_params(axis='both', which='minor', labelsize=8)
        plt.tight_layout()
        plt.savefig(save_directory_+"\\"+title+"_"+material_id[matid]+"_"+str(index)+'.png', format='png', dpi=1000) 
        plt.close(fig)
    except:
        pass

    try:
        title = "strain Crystal reference"+" "+material_id[matid]
        fig = plt.figure()
        axs = fig.subplots(2, 3)
        axs[0, 0].set_title(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
        logdata = e11c #np.log(e11c)
        logdata = logdata[~np.isnan(logdata)]
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        mu_sd1.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        axs[0, 0].set_ylabel('Frequency', fontsize=8)
        axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
        
        axs[0, 1].set_title(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
        logdata = e22c #np.log(e22c)
        logdata = logdata[~np.isnan(logdata)]
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        mu_sd1.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        axs[0, 1].set_ylabel('Frequency', fontsize=8)
        axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
        
        axs[0, 2].set_title(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
        logdata = e33c #np.log(e33c)
        logdata = logdata[~np.isnan(logdata)]
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        mu_sd1.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        axs[0, 2].set_ylabel('Frequency', fontsize=8)
        axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
        axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
        
        axs[1, 0].set_title(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
        logdata = e12c#np.log(e12c)
        logdata = logdata[~np.isnan(logdata)]
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        mu_sd1.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        axs[1, 0].set_ylabel('Frequency', fontsize=8)
        axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
        
        axs[1, 1].set_title(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
        logdata = e13c#np.log(e13c)
        logdata = logdata[~np.isnan(logdata)]
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        mu_sd1.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        axs[1, 1].set_ylabel('Frequency', fontsize=8)
        axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
        
        axs[1, 2].set_title(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
        logdata = e23c#np.log(e23c)
        logdata = logdata[~np.isnan(logdata)]
        estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
        mu_sd1.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
        axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8, range=(rangemin, rangemax))
        axs[1, 2].set_ylabel('Frequency', fontsize=8)
        axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
        axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
        
        plt.tight_layout()
        plt.savefig(save_directory_+"\\"+title+"_"+str(index)+'.png', format='png', dpi=1000) 
        plt.close(fig)
    except:
        print("error")
        pass
    
    #%%    Plot strain data    

    nan_index11 = np.where(match_rate[index][0] < match_tol)[0]
    nan_index1 = np.where(fR_pix[index][0] > fR_tol)[0]
    mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
    nan_index = np.hstack((mat_id_index,nan_index1,nan_index11))
    nan_index = np.unique(nan_index)

    strain_matrix_plot = np.copy(strain_matrix[index][0])
    strain_matrix_plot[nan_index,:,:] = np.nan             

    fig = plt.figure(figsize=(11.69,8.27), dpi=100)
    bottom, top = 0.1, 0.9
    left, right = 0.1, 0.8
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
    
    try:
        vmin, vmax = mu_sd[matid*6]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs = fig.subplots(2, 3)
    axs[0, 0].set_title(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
    im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[0, 0].set_xticks([])
    axs[0, 0].set_yticks([])
    divider = make_axes_locatable(axs[0,0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd[matid*6+1]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[0, 1].set_title(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
    im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    divider = make_axes_locatable(axs[0,1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd[matid*6+2]
    except:
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[0, 2].set_title(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
    im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    divider = make_axes_locatable(axs[0,2])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd[matid*6+3]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[1, 0].set_title(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
    im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[1, 0].set_xticks([])
    axs[1, 0].set_yticks([])
    divider = make_axes_locatable(axs[1,0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd[matid*6+4]
    except:
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[1, 1].set_title(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
    im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[1, 1].set_xticks([])
    divider = make_axes_locatable(axs[1,1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd[matid*6+5]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[1, 2].set_title(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
    im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[1, 2].set_xticks([]) 
    divider = make_axes_locatable(axs[1,2])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 

    for ax in axs.flat:
        ax.label_outer()
    plt.savefig(save_directory_+"\\"+'figure_strainCRYSTAL_UB_'+str(matid)+"_"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
    plt.close(fig)
    
    #%%
    fig = plt.figure(figsize=(11.69,8.27), dpi=100)
    bottom, top = 0.1, 0.9
    left, right = 0.1, 0.8
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
    
    try:
        vmin, vmax = mu_sd1[matid*6]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs = fig.subplots(2, 3)
    axs[0, 0].set_title(r"$\epsilon_{11}$ (%)", loc='center', fontsize=8)
    im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[0, 0].set_xticks([])
    axs[0, 0].set_yticks([])
    divider = make_axes_locatable(axs[0,0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd1[matid*6+1]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[0, 1].set_title(r"$\epsilon_{22}$ (%)", loc='center', fontsize=8)
    im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    divider = make_axes_locatable(axs[0,1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd1[matid*6+2]
    except:
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[0, 2].set_title(r"$\epsilon_{33}$ (%)", loc='center', fontsize=8)
    im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    divider = make_axes_locatable(axs[0,2])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd1[matid*6+3]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[1, 0].set_title(r"$\epsilon_{12}$ (%)", loc='center', fontsize=8)
    im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[1, 0].set_xticks([])
    axs[1, 0].set_yticks([])
    divider = make_axes_locatable(axs[1,0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd1[matid*6+4]
    except:
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[1, 1].set_title(r"$\epsilon_{13}$ (%)", loc='center', fontsize=8)
    im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[1, 1].set_xticks([])
    divider = make_axes_locatable(axs[1,1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 
    
    try:
        vmin, vmax = mu_sd1[matid*6+5]
    except:
        print("error")
        vmin = rangemin
        vmax = rangemax
    # max_vm = np.max((np.abs(vmax),np.abs(vmin)))
    # vmin = -max_vm
    # vmax = max_vm
    axs[1, 2].set_title(r"$\epsilon_{23}$ (%)", loc='center', fontsize=8)
    im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    axs[1, 2].set_xticks([]) 
    divider = make_axes_locatable(axs[1,2])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=8) 

    for ax in axs.flat:
        ax.label_outer()
    plt.savefig(save_directory_+"\\"+'figure_strainCRYSTAL_UB_'+str(matid)+"_"+str(index)+'_localscale.png', bbox_inches='tight',format='png', dpi=1000) 
    plt.close(fig)
#%% write all rot mat in one ctf file for IPF plot
## write MTEX file
rotation_matrix = [[] for i in range(len(rotation_matrix1))]
for i in range(len(rotation_matrix1)):
    rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))

for i in range(len(rotation_matrix1)):
    temp_mat = rotation_matrix1[i][0]    
    for j in range(len(temp_mat)):
        orientation_matrix = temp_mat[j,:,:]
        ## rotate orientation by 40degrees to bring in Sample RF
        omega = np.deg2rad(-40.0)
        # # rotation de -omega autour de l'axe x (or Y?) pour repasser dans Rsample
        cw = np.cos(omega)
        sw = np.sin(omega)
        mat_from_lab_to_sample_frame = np.array([[cw, 0.0, sw], [0.0, 1.0, 0.0], [-sw, 0, cw]]) #Y
        orientation_matrix = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix)
        if np.linalg.det(orientation_matrix) < 0:
            orientation_matrix = -orientation_matrix
        rotation_matrix[i][0][j,:,:] = orientation_matrix    
# =================CALCULATION OF POSITION=====================================
for index in range(len(rotation_matrix1)):
    euler_angles = np.zeros((len(rotation_matrix[index][0]),3))
    phase_euler_angles = np.zeros(len(rotation_matrix[index][0]))
    for i in range(len(rotation_matrix[index][0])):
        if np.all(rotation_matrix[index][0][i,:,:] == 0):
            continue
        euler_angles[i,:] = rot_mat_to_euler(rotation_matrix[index][0][i,:,:])
        phase_euler_angles[i] = mat_global[index][0][i]    
        
    if index == 0:
        all_euler = euler_angles
        all_phase = phase_euler_angles
    else:
        all_euler = np.vstack((all_euler, euler_angles))
        all_phase = np.hstack((all_phase, phase_euler_angles))

lattice = lattice_
material0_LG = "3"
header = [
        "Channel Text File",
        "Prj     lauetoolsnn",
        "Author    [Ravi raj purohit]",
        "JobMode    Grid",
        "XCells    "+str(1),
        "YCells    "+str(len(all_euler)),
        "XStep    1.0",
        "YStep    1.0",
        "AcqE1    0",
        "AcqE2    0",
        "AcqE3    0",
        "Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0",
        "Phases    1",
        str(lattice._lengths[0]*10)+";"+str(lattice._lengths[1]*10)+";"+\
        str(lattice._lengths[2]*10)+"\t"+str(lattice._angles[0])+";"+\
            str(lattice._angles[1])+";"+str(lattice._angles[2])+"\t"+"Material1"+ "\t"+material0_LG+ "\t"+"????"+"\t"+"????",
        "Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS"]

filename125 = save_directory_+ "//"+material_+"_MTEX_ALL_UBmat.ctf"
    
f = open(filename125, "w")
for ij in range(len(header)):
    f.write(header[ij]+" \n")
    
y_step = 0
for j123 in range(all_euler.shape[0]):
    x_step = 1 * j123
    phase_id = int(all_phase[j123])
    eul =  str(phase_id)+'\t' + "%0.4f" % x_step +'\t'+"%0.4f" % y_step+'\t8\t0\t'+ \
                        "%0.4f" % all_euler[j123,0]+'\t'+"%0.4f" % all_euler[j123,1]+ \
                            '\t'+"%0.4f" % all_euler[j123,2]+'\t0.0001\t180\t0\n'
    string = eul
    f.write(string)
f.close()
