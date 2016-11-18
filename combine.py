# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 07:12:50 2016

@author: Eric Schmidt
"""

"""
See README.md for information.

"""

import numpy as np
import csv
import os
import glob

output_dir = "../Output/"

# Output for each particle
particle_matrix_header = np.array(["Particle #","Steps","Kill Event",
                             "Charge",
                             "Starting Global x-Position (mm)",
                             "Starting Global y-Position (mm)",
                             "Starting Global z-Position (mm)",
                             "Ending Calorimeter x-Position (mm)",
                             "Ending Calorimeter y-Position (mm)",
                             "Starting Momentum (GeV/c)",
                             "Ending Momentum (GeV/c)",
                             "Delta Momentum (GeV/c)",
                             "Steps Inside Short Quad",
                             "Distance Inside Short Quad (cm)",
                             "Total # of Photons Released",
                             "# of Detectable Photons Released",
                             "Steps Inside Long Quad",
                             "Distance Inside Long Quad (cm)",
                             "Total # of Photons Released",
                             "# of Detectable Photons Released",
                             "Steps Inside Standoff Plate",
                             "Distance Inside Standoff Plate (cm)",
                             "Total # of Photons Released",
                             "# of Detectable Photons Released",
                             "Steps Inside HV Standoff",
                             "Distance Inside HV Standoff (cm)",
                             "Total # of Photons Released",
                             "# of Detectable Photons Released",
                             "Steps Inside HV Standoff Screws",
                             "Distance Inside HV Standoff Screws (cm)",
                             "Total # of Photons Released",
                             "# of Detectable Photons Released",
                             "dt","Pair Produced",
                             "Kill Timestamp",
                             "x Calorimeter Angle",
                             "y Calorimeter Angle",
                             "Total Calorimeter Angle",
                             "Starting Local x (m)",
                             "Starting Local y (m)",
                             "Starting Local x-prime (rad)",
                             "Starting Local y-prime (rad)"])
                             
                             
      
# Output for each photon
photon_matrix_header = np.array(["Photon #","Steps","Kill Event",
                           "Starting Global x-Position",
                           "Starting Global y-Position",
                           "Starting Global z-Position",
                           "Ending Calorimeter x-Position (mm)",
                           "Ending Calorimeter y-Position (mm)",
                           "Energy (GeV)","Steps Inside Matter",
                           "Distance Inside Matter (cm)",
                           "dt",
                           "Kill Timestamp",
                           "x Calorimeter Angle",
                           "y Calorimeter Angle",
                           "Total Calorimeter Angle"])
                           
N_part_mat = len(particle_matrix_header)                               
N_phot_mat = len(photon_matrix_header)
#==============================================================================
# Particle Files
#==============================================================================
                                                               
particle_files = \
    glob.glob("%s/../Output/13/particle_*.csv"%(os.getcwd()))
path = output_dir + "combined_particle_matrix.csv"
i = 1

particle_matrix_full = np.zeros((50000,N_part_mat),dtype=object)
                     
# Output for each particle
particle_matrix_full[0] = particle_matrix_header

for file in particle_files:

    with open(file, "rt") as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader, None)  # skip the headers
        stuff = list(reader)
        for row in stuff:
            particle_matrix_full[i] = row
            i = i + 1
            
particle_matrix_full = particle_matrix_full[0:i:1]
        
#particle_matrix_full = particle_matrix_full[np.any(
#                        particle_matrix_full != 0,axis=1)]

with open(path, "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for row in particle_matrix_full:
        writer.writerow(row)

#==============================================================================
# Photon Files
#==============================================================================

photon_files = \
    glob.glob("%s/../Output/13/photon_*.csv"%(os.getcwd()))
path = output_dir + "combined_photon_matrix.csv"
i = 1

photon_matrix_full = np.zeros((50000,N_phot_mat),dtype=object)
          
# Output for each photon
photon_matrix_full[0] = photon_matrix_header

for file in photon_files:

    with open(file, "rt") as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader, None)  # skip the headers
        stuff = list(reader)
        for row in stuff:
            photon_matrix_full[i] = row
            i = i + 1
            
photon_matrix_full = photon_matrix_full[0:i:1]
        
#photon_matrix_full = photon_matrix_full[np.any(
#                        photon_matrix_full != 0,axis=1)]

with open(path, "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for row in photon_matrix_full:
        writer.writerow(row)