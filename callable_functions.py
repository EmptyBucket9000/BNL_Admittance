# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 08:29:11 2016

@author: Eric Schmidt
"""

"""
See README.md for information.

"""

import numpy as np

#==============================================================================
# Global Constants
#==============================================================================

c = 2.99792458*10**8 # (m/s) Speed of light

#==============================================================================
# Particle movement and position
#==============================================================================
    
## Get the electric field based on position

def getElectricField(x,B,R,n,inEField):
    
    if inEField == 1:
        
        theta = getParticleTheta(x)
        r = getParticleRadialPosition(x)
        
        E_r = ((n*mag(B))/R)*(r - R)
        E_x = E_r*np.cos(theta)
        E_y = E_r*np.sin(theta)
        E_z = -((n*mag(B))/R)*x[2]
        E = np.array([E_x,E_y,E_z])/0.41 # /41 added as 'n' is average over all
    
    else:
        E = ([0,0,0])
        
    return E
    
## Get the angle of the particle position
    
def getParticleTheta(x):
    
    # Angle of particle position
    theta = np.arctan2(x[1],x[0])
    
    # Translate to 0-2pi
    if theta < 0:
        theta = 2*np.pi + theta
    
    return theta
    
## Get the particle's distance from origin
    
def getParticleRadialPosition(x):
    
    # Radial distance of particle from origin
    r = np.sqrt(x[0]**2 + x[1]**2)
    
    return r
    
## Check if pair-production occurs
    
def ifPairProduction(E,photon_dt,mat):
    
    '''
    These probability functions come from fitting experimental data provided
    by NIST. The data was attenuation length in cm**2/g as a function of 
    the photon energy.
    '''
    
    # Divide energy by 10**9 as probability was calculated as a function of GeV
    E = E/10**9
    
    if mat == "Al":
        # Probability of nucleus pair production as a function of photon energy
        P_n = (0.023248 - 9.56748*10**-9 / E**5 + 5.52086*10**-7 / E**4 - 
             0.0000122004 / E**3 + 0.000139708 / E**2 - 0.00125509 / E)
             
        # Probability of electron pair production
        P_e = (0.00211641 - 1.89942*10**-9 / E**5 + 1.12441*10**-7 / E**4 -
            2.55265*10**-6 / E**3 + 0.0000290766 / E**2 - 0.000213793 / E)
            
        P = P_n + P_e
             
    elif mat == "SiBr":
    
        # Probability of pair production as a function of photon energy
        P_n = (0.044872 - 1.13514*10**-8 / E**5 + 6.75616*10**-7 / E**4 - 
            0.000015688 / E**3 + 0.000195951 / E**2 - 0.00205794 / E)
             
        # Probability of electron pair production
        P_e = (0.0018329 - 1.21326*10**-9 / E**5 + 7.13317*10**-8 / E**4 - 
            1.61749*10**-6 / E**3 + 0.0000188146 / E**2 - 0.000152661 / E)
            
        P = P_n + P_e
             
    elif mat == "Ma":
    
        # Probability of pair production as a function of photon energy
        P_n = (0.0209591 - 6.58903*10**-9 / E**5 + 3.95365*10**-7 / E**4 - 
            9.25002*10**-6 / E**3 + 0.00011525 / E**2 - 0.0011283 / E)
             
        # Probability of electron pair production
            
        P_e = (0.00219828 - 1.92149*10**-9 / E**5 + 1.13176*10**-7 / E**4 - 
            2.56364*10**-6 / E**3 + 0.0000293949 / E**2 - 0.000220787 / E)
            
        P = P_n + P_e
         
    # Adjust the probability based on actual photon_dt as the above equations
    # assume photon_dt = 10**-11
    P = P * (photon_dt/10**-11)
    
    rn = np.random.random()
    
    if rn < P:
        return True
    
## Create electron and positron and note their existance for future tracking

def doPairProduction(E,particle_count,particle_proc,m,p_norm,x,step_counter):
    
    E_part = E/2                           # (eV) Energy of each particle
    p = np.sqrt(E_part**2 - m**2)*p_norm   # (eV/c) Momentum of each particle
    
    i = 0
    while i < 2:
        particle_count = particle_count + 1
        particle_proc[particle_count] = np.array([x[0],x[1],x[2],
                                                  p[0],p[1],p[2],(-1)**i,0,
                                                  step_counter,1])
        i = i + 1
    return particle_proc,particle_count

## Check if photon is released between energies k_min and k_max while particle
## is traveling through material

def isPhotonReleased(k_min,energy,X0,p,dt,m):
    
    d = mag(p)/(energy)*c*dt
    
    # Determine the average number of photons released in distance d
    N = (d/X0) * ((4/3)*np.log(energy/k_min) - (4*(energy-k_min))/(3*energy) +
        (energy**2-k_min**2)/(2*energy**2))
        
    # Determine the probability that 1,2,3,... photon(s) is(are) released using
    # Poisson statistics
    P1 = poissonProb(N,1)
    P2 = poissonProb(N,2)
    P3 = poissonProb(N,3)
    P4 = poissonProb(N,4)
    P5 = poissonProb(N,5)
    P6 = poissonProb(N,6)
    rn = np.random.rand()
    if rn < P1:
        return 1
    elif rn > P1 and rn < P1 + P2:
        return 2
    elif rn > P1 + P2 and rn < P1 + P2 + P3:
        return 3
    elif rn > P1 + P2 + P3 and rn < P1 + P2 + P3 + P4:
        return 4
    elif rn > P1 + P2 + P3 + P4 and rn < P1 + P2 + P3 + P4 + P5:
        return 5
    elif rn > P1 + P2 + P3 + P4 + P5 and rn < P1 + P2 + P3 + P4 + P5 + P6:
        return 6
    else:
        return 0
        
## Adjust momentum of particle when photon is released
        
def adjustParticleMomentumFromBremsstrahlung(p,k_min,energy,m):
    
    # Normalize the velocity vector
    p_vec_norm = p/mag(p)
    
    ## Randomly get the energy of the released photon between k_min and the
    ## current energy based on the Bremsstrahlung intensity plot
    
    # Get the smallest wavelength available equal to the particle momentum
    lambda_min = energy2Wavelength(energy)
    
    # Get the largest wavelength to be used
    lambda_max = energy2Wavelength(k_min)
    
    # Range of possible energies
    dist_range = np.linspace(lambda_min,lambda_max,10000) # (m)
    
    # Weights for the random mean position based on the distribution    
    dist_weights = (dist_range/lambda_min - 1)*(1/dist_range**2)
    
    # Normalize the weights to give a total probability of 1
    dist_weights = dist_weights/sum(dist_weights)
    
    # Randomly choose a mean within allowed range
    l = np.random.choice(dist_range, 1, p=dist_weights)[0]

    # Get photon energy from wavelength
    photon_energy = wavelength2Energy(l)
    
    # Get the energy of the particle before photon release
    E_old = np.copy(energy)
    
    # Get the new particle energy
    E_new = E_old - photon_energy
    
    # Get the new particle momentum scalar
    p_mag_new = energy2Momentum(E_new,m)
    
    # Get the new momentum vector
    p_new = p_mag_new * p_vec_norm
    
    return p_new,photon_energy
    
## If bremsstrahlung procs, release a photon and update appropriate variables
    
def bremsstrahlung(p,m,k_min,energy,i,photon_count,
                   min_detectable_energy,total_photon_count):
    
    # Readjust the particle momentum from the photon's release
    p,photon_energy = \
        adjustParticleMomentumFromBremsstrahlung(p,k_min,energy,m)
    
    # Note if a new high energy photon was released
    if photon_energy > min_detectable_energy:
        photon_count[1] = photon_count[1] + 1
    
    # Note that a new photon was released
    photon_count[0] = photon_count[0] + 1
    
    total_photon_count = total_photon_count + 1
    
    return p,photon_count,photon_energy,total_photon_count

#==============================================================================
# Contact Functions
#==============================================================================

## Checks if is inside quad for E-field generation

def isInSQuad(x,el_theta,R):

    # Get particle's r and theta positions
    
    theta = getParticleTheta(x)
    r = getParticleRadialPosition(x)

    # Check if particle is inside an electrode

    for row in el_theta:
        if row[0] > theta and \
            row[1] < theta and \
            r < R + 0.05 and \
            r > R - 0.05:
            
            return True

## Checks if is inside quad for E-field generation

def isInDQuad(x,el_theta,R):

    # Get particle's r and theta positions
    
    theta = getParticleTheta(x)
    r = getParticleRadialPosition(x)

    # Check if particle is inside an electrode

    for row in el_theta:
        if row[0] > theta and \
            row[1] < theta and \
            r < R + 0.05 and \
            r > R - 0.05:
                
            return True

## Checks if inside an element it can pass through
    
def passthroughElementContact(x,el_rad,el_theta):

    # Get particle's r and theta positions
    
    theta = getParticleTheta(x)
    r = getParticleRadialPosition(x)

    # Check if particle is inside an electrode

    for row in el_theta:
        if row[0] > theta and \
            row[1] < theta and \
            el_rad[0] < r and \
            el_rad[1] > r:
                
            return True
            
## Checks if inside HV standoff
            
def passthroughHVStandoff(x,so_rad,so_theta):

    so_inner_diameter = 0.138/39.3701   # (m)
    so_outer_diameter = 0.3/39.3701     # (m)

    # Get particle's r and theta positions
    
    theta = getParticleTheta(x)
    r = getParticleRadialPosition(x)
    
    for row in so_theta:
    
        slocal_x = r*np.abs(row[0] - np.abs(row[0] - row[1])/2 - theta)
        slocal_y = x[2]
        slocal_r = np.sqrt(slocal_x**2 + slocal_y**2)
        
        if slocal_r > so_inner_diameter/2 and \
            slocal_r < so_outer_diameter/2 and \
            so_rad[0] < r and so_rad[1] > r:
                
            return True
            
## Checks if inside HV standoff screws
            
def passthroughHVStandoffScrews(x,so_rad,so_theta):

    sos_diameter = 0.138/39.3701 # (m)

    # Get particle's r and theta positions
    
    theta = getParticleTheta(x)
    r = getParticleRadialPosition(x)
    
    for row in so_theta:
    
        slocal_x = r*np.abs(row[0] - np.abs(row[0] - row[1])/2 - theta)
        slocal_y = x[2]
        slocal_r = np.sqrt(slocal_x**2 + slocal_y**2)
        
        if slocal_r < sos_diameter/2 and \
            ((so_rad[0] < r and (so_rad[0] + 0.00635) > r) or \
            ((so_rad[1] - 0.00635) < r and so_rad[1] > r)):
                
            return True

## Checks if contacts the front panel of the calorimeter

def noPassthroughElementContact(x,cal_rad,cal_theta):
    
    # Get particle's r and theta positions
    
    theta = getParticleTheta(x)
    r = getParticleRadialPosition(x)
    
    # Check if particle is inside a calorimeter box
    
    for row in cal_theta:
        if row[0] > theta and \
            row[1] < theta and \
            cal_rad[0] < r and \
            cal_rad[1] > r:
    
            return True

## Checks if reaches inner radial limit

def innerLimit(x,R_i):
    
    r = getParticleRadialPosition(x)
    
    if r < R_i:
        return True
    
## Checks if reaches outer radial limit

def outerLimit(x,R):
    
    r = getParticleRadialPosition(x)
    
    if r > R + 0.2:
        return True
        
## Checks if contact with trolly rail
        
def railContact(x,R,rail_height,rail_rad):
    
    r = getParticleRadialPosition(x)
    
    if r > rail_rad[0] and r < rail_rad[1] and np.abs(x[2]) > rail_height:
        return True
        
## Returns the position of the particle in the calorimeter local coordinates
        
def getPositionOnCalorimeter(x,cal_width,R_i):
    
    r = getParticleRadialPosition(x)
    cal_con_x = np.array([R_i + cal_width/2 - r,x[2],0])
    
    return cal_con_x
    
## Returns the angles of the particle/photon vector relative to the calorimeter
    
def getAnglesFromCalorimeter(cal_con_pre_x,cal_con_x,cal_theta_glob):
    
    # Get the updated calorimeter basis x unit-vector due angle off radial
    new_cal_x_unit_array = getUpdatedCalorimeterBasis(cal_theta_glob)
                                
    # Determine the momentum vector of the particle
    inc_vec = cal_con_pre_x - cal_con_x
    
    # Get the angle of the momentum vector from the calorimeter x-axis
    ang_x = np.arccos(np.dot(inc_vec,new_cal_x_unit_array) / mag(inc_vec))
    
    # Get the angle of the momentum vector from the calorimeter y-axis
    ang_y = np.arccos(np.dot(inc_vec,np.array([0,1,0])) / mag(inc_vec))
    
    # Get the projection of the momentum vector onto the calorimeter,
    # incorporating the angle of the calorimeter off radial
    inc_vec_proj = np.array([-np.abs(cal_con_pre_x[2]*np.cos(ang_x)),
                             cal_con_pre_x[2]*np.cos(ang_y),
                             0])
                             
    # Get the angle between the momentum vector and its projection            
    ang_tot = np.arccos(np.dot(inc_vec_proj,inc_vec) / 
                        (mag(inc_vec_proj) * mag(inc_vec)))
                        
    
                        
    return ang_x,ang_y,ang_tot
    
## Returns updated calorimeter basis x unit-vector due angle to radial
    
def getUpdatedCalorimeterBasis(cal_theta_glob):
        
    # The calorimeter plane is originally assumed to have to angle wrt the
    # radial from the center of the ring. A3 is the z-component of the
    # new x-basis unit vector that takes into account the angle off radial.
    # new_cal_x_unit_array is the new x-basis unit vector for the plane.
    
    A3 = np.sqrt(1-np.cos(cal_theta_glob))
    new_cal_x_unit_array = np.array([np.cos(cal_theta_glob),0,A3])
    
    return new_cal_x_unit_array

#==============================================================================
# Misc. functions
#==============================================================================

# Updates some tracked variables when particle is inside matter

def updateInsideMatter(p,energy,dt,steps_inside,d_matter):
    
    steps_inside = steps_inside + 1
    d_matter = d_matter + mag(p)/energy * c * dt
    
    return steps_inside,d_matter

## Poisson probability

def poissonProb(l,n):
    
    P = (l**n * np.exp(-l))/(np.math.factorial(n))
    
    return P

## Get energy of photon from its wavelength

def wavelength2Energy(l):
    
    E = 1240/l
    
    return E

## Get wavelength of photon from its energy

def energy2Wavelength(E):
    
    l = 1240/E
    
    return l

## Get momentum from total energy and mass

def energy2Momentum(E,m):
    
    if E >= m:
        p = np.sqrt(E**2 - m**2)
    else:
        p = 0
    
    return p

## Get total energy from momentum and mass

def momentum2Energy(p,m):

    energy = np.sqrt(np.dot(p,p) + m**2)
 
    return energy

## Convert total energy to relativistic gamma

def energy2Gamma(E,m):
    
    gamma = E/m
    
    return gamma
    
## Get the magnitude of some vector
    
def mag(v):
    
    return np.sqrt(np.dot(v,v))
    
#==============================================================================
# Setting initial conditions
#==============================================================================
    
## Return the particle momentum at decay in the local coordinate system
    
def getParticleMomentumAtDecay(m_p,m_theta,m_m,alpha_sign,m,):
    
    c = 2.99792458*10**8
    
    while True:
    
        E_p_s_max = 52.83*10**6
        g_m = np.sqrt((momentum2Energy(m_p,m_m)/m_m)**2 + 1)
        beta_m = np.array((0, 0, np.sqrt(1 - 1/g_m**2)))
        
        theta_min = 0
        theta_max = np.pi
        
        alpha = alpha_sign*np.arccos(1/np.sqrt(3))
        phi_s = 2*np.pi*np.random.random()
        
        y = 0.5*(np.random.random() + 1)

        # Range of possible energies
        dist_range = np.linspace(theta_min,theta_max,10000) # (m)
        
        # Weights for the random mean position based on the distribution    
        dist_weights = 1 + ((2*y-1)/(3-2*y))*np.cos(dist_range)
        
        # Normalize the weights to give a total probability of 1
        dist_weights = dist_weights/sum(dist_weights)
        
        # Randomly choose a mean within allowed range
        th_s = np.random.choice(dist_range, 1, p=dist_weights)[0]
        
        E_p_s = y*E_p_s_max
        p_p_s_mag = np.sqrt(E_p_s**2 - m**2)
        g_p_s = np.sqrt((E_p_s/m)**2 + 1)
        
        p_x = p_p_s_mag*(np.sin(th_s)*np.cos(phi_s)*np.cos(alpha) + 
                   np.cos(th_s)*np.sin(alpha))
        p_y = p_p_s_mag*(np.sin(th_s)*np.sin(phi_s))
        p_z = p_p_s_mag*(-np.sin(th_s)*np.cos(phi_s)*np.sin(alpha) + 
                   np.cos(th_s)*np.cos(alpha))
        
        p_p_s = np.array((p_x,p_y,p_z))
        b_p_s = p_p_s/(g_p_s*m)
#            print(mag(b_p_s))
        
        ## Boost to lab frame
        
        v_p = ((b_p_s + beta_m*g_m*((g_m/(g_m + 1))*
                                    np.dot(beta_m,b_p_s) + 1))*c /
            (g_m*(1 + np.dot(beta_m,b_p_s))))
        
#            print(v_p)
        beta_p = mag(v_p)/c
        g_p = 1/np.sqrt(1-(beta_p)**2)
        p_p = g_p*m*v_p/c
        E_p_mag = np.sqrt(mag(p_p)**2 + m**2)
        E_p_mag = mag(g_p)*m
        
        if E_p_mag > 1.8*10**9:
#                print("good************************************")
            return p_p
#            else:
#                print("too low")
        
#    else:
#    
#        # Magnitude of the particle momentum
#        rn = np.random.random()
#        p_tot = (1.79453 + 5.92129*10**-7 * np.exp(12.8423*rn**3) + 0.756197*rn - 
#        0.276462*rn**2 + 0.580407*rn**3) * 10**9
#        #    p_tot = 2.3*10**9
#        
#        # Convert to momentum vector based on position
#    #    p = np.array([p_tot*np.sin(m_theta),-p_tot*np.cos(m_theta),0])
#        p = p_tot * m_p / mag(m_p)
#        
#        # Add in the randomness of the angle away from the muon momentum vector.
#        # 's' in the variable names refer to 'star', the center of mass frame
#        
#        p_s_mag = mag(p)
#        gamma = mag(m_p) / m_m
#        
#        # Make sure the momentum isn't greater than 1/2 of the rest mass of the
#        # muon as in the muon frame, the positron cannot take more than half its
#        # energy without failing to conserve momentum. The approximation is used
#        # that energy = momentum due to the highly relativistic nature of the
#        # particles.
#        
#        while True:
#        
#            ths = np.pi * np.random.random()
#            p_ss = p_s_mag / (gamma * (np.cos(ths) + 1))
#            
#            if p_ss < 52.8*10**6: # 52.8 MeV/c: 1/2 the rest mass of the muon
#                break
#
#    if decay_dir_set == 0:        
#    
#        phs = 2*np.pi * np.random.random()
#        p_x = p_ss * np.sin(ths) * np.cos(phs)
#        p_y = p_ss * np.sin(ths) * np.sin(phs)
#    
#    elif decay_dir_set == 1:
#    
#        p_x = np.copy(p_ss)
#        p_y = 0
#    
#    p[0] = p[0] + p_x
#    p[1] = p[1] + p_y
#    
#    return p
    
'''  
#==============================================================================
# #============================================================================
# # The following code is no longer used but left in for reference in case it
# # gets used in the future. It was used to create the muon beam data 
# # statistically from extrapolated beam shapes, phase-space data, etc... With
# # the introduction of the muon data .csv file, this code became obsolete.
# # It should be noted that it was not fully complete, only the code for the 
# # x-direction was fully working.
# #============================================================================
#==============================================================================
'''
#
### Return the muon beam distribution width
#    
#def getParticleSigma(m_sigma_amp,m_sigma_ideal,m_sigma_0,num):
#    
#    sigma = np.zeros(len(m_sigma_amp))    
#    
#    i = 0
#    while i < 2:
#    
#        if m_sigma_ideal[i] == 1:
#            
#            sigma[i] = 0
#            
#        elif m_sigma_ideal[i] == 0:
#    
#        # Range of possible particle positions. The subraction is due to the 
#        # fact that the probability function of a cosine goes to infinity at
#        # the cosine amplitudes.
#            dist_range = np.linspace(-(m_sigma_amp[i] - m_sigma_amp[i]/30),
#                                     m_sigma_amp[i] - m_sigma_amp[i]/30,
#                                     num[i]) # (m)
#            
#            # Weights for the random mean position based on the distribution
#            
#            dist_weights = (np.pi*np.sqrt(1-(dist_range/m_sigma_amp[i])**2)) \
#                               **(-1)
#            
#            # Normalize the weights to give a total probability of 1
#            dist_weights = dist_weights/sum(dist_weights)
#            
#            # Randomly choose a mean within allowed range
#            sigma_temp = np.random.choice(dist_range, 1, p=dist_weights)
#            
#            # Add xbar to the value around which it oscillates
#            sigma[i] = sigma_temp[0] + m_sigma_0[i]
#    
#        i = i + 1
#        
#    return sigma
#    
### Return the mean particle position related to current particle being tracked
#    
#def getParticleXBar(m_xbar_amp,m_xbar_ideal,num,m_xbar_0,ax):
#    
#    if m_xbar_ideal == 1:
#        
#        xbar = 0
#        
#    elif m_xbar_ideal == 0:
#    
#        # Range of possible particle positions. The subraction is due to the 
#        # fact that the probability function of a cosine goes to infinity at
#        # the cosine amplitudes.
#        dist_range = np.linspace(-(m_xbar_amp - m_xbar_amp/30),
#                                 m_xbar_amp - m_xbar_amp/30,
#                                 num) # (m)
#        
#        # Weights for the random mean position based on the distribution
#        
#        if ax == 'x':
#            dist_weights = (np.pi*np.sqrt(1-(dist_range/m_xbar_amp)**2))**(-1)
#            
#        if ax == 'y':
#            dist_weights = (np.pi*np.sqrt(1-(dist_range/m_xbar_amp)**2))**(-1)
#        
#        # Normalize the weights to give a total probability of 1
#        dist_weights = dist_weights/sum(dist_weights)
#        
#        # Randomly choose a mean within allowed range
#        xbar = np.random.choice(dist_range, 1, p=dist_weights)
#        
#        # Add xbar to the value around which it oscillates
#        xbar = xbar[0] + m_xbar_0
#    
#    return xbar
#    
### Return the local muon x-position based on distribution function
#
#def getXParticlePositions(xbar,sigma,xmin_init,xmax_init,num,fit):
#    
#    # Range of possible particle positions
#    init_dist_range = np.linspace(xmin_init, xmax_init, num) # (m)
#    dist_range = xbar + init_dist_range # (m)
#    
#    # Weights for the random position based on the distribution 
#    
#    if sigma != 0:
#    
#        if fit == "Gaussian":
#            dist_weights = (np.sqrt(2*np.pi*sigma**2)**(-1)) * \
#                np.exp(-((init_dist_range-xbar)**2)/(2*sigma**2))
#    
#        # Normalize the weights to give a total probability of 1
#        dist_weights = dist_weights/sum(dist_weights)
#        
#        # Randomly choose a position within allowed range
#        particle_position = np.random.choice(dist_range, 1, p=dist_weights)
#        
#        # Convert from single-element array to float
#        particle_position = particle_position[0]
#        
#    elif sigma == 0:
#        
#        particle_position = xbar
#    
#    return particle_position
#    
### Return the local muon x' based on distribution function
#    
#def getParticleXPrime(xbar,x,x_max,xprime_max):
#    
#    sigma = (1/3)*x_max
#    
#    xprime_lim = np.sqrt(xprime_max**2*(1-((x - xbar)**2 / x_max**2)))
#    
#    init_dist_range = np.linspace(-xprime_lim,xprime_lim,1000) # mrad
#    dist_range = xbar + init_dist_range
#    
#    dist_weights = (np.sqrt(2*np.pi*sigma**2)**(-1)) * \
#        np.exp(-((init_dist_range-xbar)**2)/(2*sigma**2))
#    
#    # Normalize the weights to give a total probability of 1
#    dist_weights = dist_weights/sum(dist_weights)
#    
#    # Randomly choose a position within allowed range
#    xprime = np.random.choice(dist_range, 1, p=dist_weights)
#    
#    # Convert from single-element array to float and choose randomly whether
#    # xprime is positive or negative
#    xprime = xprime[0] * (-1)**(round(np.random.random()))
#    
#    return xprime
#    
### Return the local muon y-position based on distribution function
#    
#def getYParticlePositions(ybar,sigma,ymin_init,ymax_init,num,fit):
#    
#    # See 'getXParticlePositions' for comments
#    
#    init_dist_range = np.linspace(ymin_init, ymax_init, num)
#    dist_range = ybar + init_dist_range
#    
#    dist_weights = 1 * init_dist_range
#    dist_weights = dist_weights/sum(dist_weights)
#    particle_position = np.random.choice(dist_range, 1, p=dist_weights)
#    
#    particle_position = particle_position[0]
#    
#    particle_position = 0
#    
#    return particle_position