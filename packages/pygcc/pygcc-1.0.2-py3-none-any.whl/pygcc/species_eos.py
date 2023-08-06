#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 16:02:22 2021

@author: adedapo.awolayo and Ben Tutolo, University of Calgary

Copyright (c) 2020 - 2021, Adedapo Awolayo and Ben Tutolo, University of Calgary

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Functions implemented here include gas, mineral and aqueous species equation of state

"""

import numpy as np #, os, json, pandas as pd
from .water_eos import iapws95, ZhangDuan, water_dielec, convert_temperature
J_to_cal = 4.184

def heatcap(TC, P, species, **kwargs):
    """
    This function evaluates Gibbs energy and heat capacity as a function of temperature
    and pressure for any mineral or gas specie using Helgeson et al (1978) equations and Maier-Kelley
    power function for heat capacity

    Parameters
    ----------
       TC : float, vector
           Temperature [°C]
       P : float, vector
           Pressure [bar]
       species : array
           Properties such as ( dG [cal/ml], dH [cal/mol], S [cal/mol-K], V [cm³/mol], a [cal/mol-K],b [*10^3 cal/mol/K^2], c [*10^-5 cal/mol/K], Ttrans [K], Htr [cal/mol], Vtr [cm³/mol], dPdTtr [bar/K] ), etc \n
       spec_name : string
           species name, optional for all cases except Coesite and Quartz

    Returns
    ----------
       delGfPT : float, vector
           Gibbs Energy [cal/mol]
       delCp : float, vector
           Heat capacity [cal/mol/K]

    Examples
    --------
    >>> from pygcc.pygcc_utils import db_reader
    >>> ps = db_reader() # utilizes the default direct-access database, speq21
    >>> [delGfPT, delCp] = heatcap( 100, 50, ps.dbaccessdic['H2S(g)'])
        -11782.47165818, 8.58416135
    >>> [delGfPT, delCp] = heatcap( 100, 50, ps.dbaccessdic['Quartz'],
                               spec_name = 'Quartz')
        -205292.75498942, 12.34074489

    References
    ----------
        (1) Helgeson, H. C., Delany, J. M., Nesbitt, H. W. and Bird, D. K.(1978). Summary and critique of the
            thermodynamic properties of rock-forming minerals.
        (2) Kelley K. K (1960) Contributions to the data on theoretical metallurgy. XIII. High
            temperature heat content, heat capacity and entropy data for elements and inorganic compounds US Bur Mines Bull 548: 232 p
    """
    kwargs = dict({"spec_name": None }, **kwargs)
    spec_name = kwargs['spec_name'];
    if (np.ndim(TC) == 0):
        T = np.array(convert_temperature( TC, Out_Unit = 'K' )).ravel()
    else:
        T = convert_temperature( TC, Out_Unit = 'K' ).ravel()
    if np.size(P) <= 2:
        P = np.ravel(P)
        P = P[0]*np.ones(np.size(TC))
    delGref = species[2]
    Sr = species[4]
    Vr = species[5]/41.84   # conversion: cal/bar/cm3  See Johnson et al., 1992
    a = np.array([]); b = np.array([]); c = np.array([]); Ttrans = np.array([]);
    Htr = np.array([]); Vtr = np.array([]); dPdTtr = np.array([])
    eosparam_cycle = round(len(species[6:])/7)
    eosparam_cycle = eosparam_cycle if eosparam_cycle != 0 else 1
    for i in range(eosparam_cycle):
        i = i*7 + 6
        a = np.append(a, species[i])
        b = np.append(b, species[i + 1])
        c = np.append(c, species[i + 2])
        Ttrans = np.append(Ttrans, species[i + 3]) if (i + 3) < len(species) else np.append(Ttrans, 0)   # K
        Htr = np.append(Htr, species[i + 4]) if (i + 4) < len(species) else np.append(Htr, 0)
        Vtr = np.append(Vtr, species[i + 5]) if (i + 5) < len(species) else np.append(Vtr, 0)
        dPdTtr = np.append(dPdTtr, species[i + 6]) if (i + 6) < len(species) else np.append(dPdTtr, 0)

    b = b*10**-3; c = c*10**5;  Vtr = Vtr/41.84
    phasetrans_no = round(len(species[6:])/8)
    Tr = 298.15
    Pr = 1.0
    Cp = lambda T, x, y, z: x + y*T + z*T**-2
    CpdT = lambda T1, T2, x, y, z: x*(T2 - T1) + y*(T2**2 - T1**2)/2 - z*(1/T2 - 1/T1)
    CplndT = lambda T1, T2, x, y, z: x*np.log(T2/T1) + y*(T2 - T1) - z*(1/T2**2 - 1/T1**2)/2

    PtransT = np.zeros(phasetrans_no)
    delCpdT = np.zeros(len(T)); delCp = np.zeros(len(T)); delCplndT = np.zeros(len(T));
    VtrdP = np.zeros(len(T)); VdP = np.zeros(len(T))
    for i in range(len(T)):
        if (phasetrans_no  == 0) | (T[i] <= Ttrans[0]):
            # no phase transition
            delCp[i] = Cp(T[i], a[0], b[0], c[0])
            delCpdT[i] = CpdT(Tr, T[i], a[0], b[0], c[0])
            delCplndT[i] = CplndT(Tr, T[i], a[0], b[0], c[0])
            VdP[i] = Vr*(P[i] - Pr)
            VtrdP[i] = 0

        elif phasetrans_no == 1:
            delCp[i] = Cp(T[i], a[1], b[1], c[1])
            delCpdT[i] = CpdT(Tr, Ttrans[0], a[0], b[0], c[0]) + CpdT(Ttrans[0], T[i], a[1], b[1], c[1])
            delCplndT[i] = CplndT(Tr, Ttrans[0], a[0], b[0], c[0]) + CplndT(Ttrans[0], T[i], a[1], b[1], c[1])
            if (T[i] <= Ttrans[0]) | (dPdTtr[0] == 0):
                # if Pressure integration and Temperature does not cross phase transition boundaries
                VdP[i] = Vr*(P[i] - Pr)
            elif (T[i] < Ttrans[1]):
                PtransT[0] = Pr + (T[i] - Ttrans[0])*dPdTtr[0]
                VdP[i] = Vr*(P[i] - Pr) + Vtr[0]*(PtransT[0] - Pr)
            VtrdP[i] = Htr[0]*(1 - T[i]/Ttrans[0])

        elif phasetrans_no == 2:
            if Ttrans[0] < T[i] < Ttrans[1]:
                delCp[i] = Cp(T[i], a[1], b[1], c[1])
                delCpdT[i] = CpdT(Tr, Ttrans[0], a[0], b[0], c[0]) + CpdT(Ttrans[0], T[i], a[1], b[1], c[1])
                delCplndT[i] = CplndT(Tr, Ttrans[0], a[0], b[0], c[0]) + CplndT(Ttrans[0], T[i], a[1], b[1], c[1])
            else:
                delCp[i] = Cp(T[i], a[2], b[2], c[2])
                delCpdT[i] = CpdT(Tr, Ttrans[0], a[0], b[0], c[0]) + CpdT(Ttrans[0], Ttrans[1], a[1], b[1], c[1]) + \
                    CpdT(Ttrans[1], T[i], a[2], b[2], c[2])
                delCplndT[i] = CplndT(Tr, Ttrans[0], a[0], b[0], c[0]) + CplndT(Ttrans[0], Ttrans[1], a[1], b[1], c[1]) + \
                    CplndT(Ttrans[1], T[i], a[2], b[2], c[2])

            if (T[i] < Ttrans[1]):
                PtransT[0] = Pr + (T[i] - Ttrans[0])*dPdTtr[0]
                VdP[i] = (Vr  + Vtr[0])*(P[i] - Pr)
                VtrdP[i] = Htr[0]*(1 - T[i]/Ttrans[0]) #+ Htr[1]*(1 - T[i]/Ttrans[1])
            else:
                PtransT[0] = Pr + (T[i] - Ttrans[0])*dPdTtr[0]
                PtransT[1] = Pr + (T[i] - Ttrans[1])*dPdTtr[1]
                if dPdTtr[1] != 0:
                    VdP[i] = (Vr  + Vtr[0] + Vtr[1])*(P[i] - Pr)
                else:
                    VdP[i] = Vr*(P[i] - Pr) + Vtr[0]*(PtransT[0] - Pr) + Vtr[1]*(PtransT[1] - Pr)
                VtrdP[i] = Htr[0]*(1 - T[i]/Ttrans[0]) + Htr[1]*(1 - T[i]/Ttrans[1])

        elif phasetrans_no == 3:
            if Ttrans[0] < T[i] < Ttrans[1]:
                delCp[i] = Cp(T[i], a[1], b[1], c[1])
                delCpdT[i] = CpdT(Tr, Ttrans[0], a[0], b[0], c[0]) + CpdT(Ttrans[0], T[i], a[1], b[1], c[1])
                delCplndT[i] = CplndT(Tr, Ttrans[0], a[0], b[0], c[0]) + CplndT(Ttrans[0], T[i], a[1], b[1], c[1])
            elif T[i] < Ttrans[2]:
                delCp[i] = Cp(T[i], a[2], b[2], c[2])
                delCpdT[i] = CpdT(Tr, Ttrans[0], a[0], b[0], c[0]) + CpdT(Ttrans[0], Ttrans[1], a[1], b[1], c[1]) + \
                    CpdT(Ttrans[1], T[i], a[2], b[2], c[2])
                delCplndT[i] = CplndT(Tr, Ttrans[0], a[0], b[0], c[0]) + CplndT(Ttrans[0], Ttrans[1], a[1], b[1], c[1]) + \
                    CplndT(Ttrans[1], T[i], a[2], b[2], c[2])
            else:
                delCp[i] = Cp(T[i], a[3], b[3], c[3])
                delCpdT[i] = CpdT(Tr, Ttrans[0], a[0], b[0], c[0]) + CpdT(Ttrans[0], Ttrans[1], a[1], b[1], c[1]) + \
                    CpdT(Ttrans[1], Ttrans[2], a[2], b[2], c[2]) + CpdT(Ttrans[2], T[i], a[3], b[3], c[3])
                delCplndT[i] = CplndT(Tr, Ttrans[0], a[0], b[0], c[0]) + CplndT(Ttrans[0], Ttrans[1], a[1], b[1], c[1]) + \
                    CplndT(Ttrans[1], Ttrans[2], a[2], b[2], c[2]) + CplndT(Ttrans[2], T[i], a[3], b[3], c[3])

            if (T[i] < Ttrans[1]):
                PtransT[0] = Pr + (T[i] - Ttrans[0])*dPdTtr[0]
                VdP[i] = (Vr  + Vtr[0])*(P[i] - Pr)
                VtrdP[i] = Htr[0]*(1 - T[i]/Ttrans[0]) #+ Htr[1]*(1 - T[i]/Ttrans[1])
            else:
                PtransT[0] = Pr + (T[i] - Ttrans[0])*dPdTtr[0]
                PtransT[1] = Pr + (T[i] - Ttrans[1])*dPdTtr[1]
                if dPdTtr[1] != 0:
                    VdP[i] = (Vr  + Vtr[0] + Vtr[1])*(P[i] - Pr)
                else:
                    VdP[i] = Vr*(P[i] - Pr) + Vtr[0]*(PtransT[0] - Pr) + Vtr[1]*(PtransT[1] - Pr)
                VtrdP[i] = Htr[0]*(1 - T[i]/Ttrans[0]) + Htr[1]*(1 - T[i]/Ttrans[1])

    if (spec_name == 'Quartz') | (spec_name == 'Coesite') & (dPdTtr[0] != 0):
        Vr_alpha, Vdiff, k = Vr*41.84, 2.047, dPdTtr[0]
        VPtTt_alpha, VPrTt_beta, calpha = 23.348, 23.72, -4.973e-5
        # aalpha, balpha = 0.549824e3,  0.65995
        aalpha =  Ttrans[0] - Pr/k - Tr
        balpha = VPtTt_alpha - Vr_alpha + calpha*Pr
        qphase = np.zeros(len(T)); Pstar = np.zeros(len(T)); V = np.zeros(len(T))
        for i in range(len(T)):
            qphase[i] = 1 if (T[i] <= Ttrans[0]) | (P[i] >= (Pr + k*(T[i] - Ttrans[0]))) else 2
            Pstar[i] = Pr if (T[i] <= Ttrans[0]) else P[i] if qphase[i] == 2 else Pr + k*(T[i] - Ttrans[0])
            V[i] = VPrTt_beta if qphase[i] == 2 else Vr_alpha + calpha*(P[i] - Pr) + \
                (VPtTt_alpha - Vr_alpha - calpha*(P[i] - Pr))*(T[i] - Tr) /(Ttrans[0] + (P[i] - Pr)/k - Tr)
        if (spec_name == 'Coesite'):
            V = V - Vdiff
            GVterm = ((Vr_alpha - Vdiff)*(P-Pstar) + (VPrTt_beta - Vdiff)*(Pstar-Pr) -
                      0.5*calpha*(2.0*Pr*(P-Pstar) - (P**2-Pstar**2)) - calpha*k*(T-Tr)*(P-Pstar) +
                      k*(balpha + aalpha*calpha*k)*(T-Tr)*np.log((aalpha + P/k)/(aalpha + Pstar/k)))/41.84
        else:
            GVterm = (Vr_alpha*(P-Pstar) + VPrTt_beta*(Pstar-Pr) -
                      0.5*calpha*(2.0*Pr*(P-Pstar) - (P**2-Pstar**2)) - calpha*k*(T-Tr)*(P-Pstar) +
                      k*(balpha + aalpha*calpha*k)*(T-Tr)*np.log((aalpha + P/k)/(aalpha + Pstar/k)))/41.84
        delGfPT = delGref - Sr*(T-Tr) + delCpdT - T*delCplndT +  VtrdP + GVterm
    else:
        delGfPT = delGref - Sr*(T-Tr) + delCpdT - T*delCplndT + VdP +  VtrdP

    return delGfPT, delCp


def heatcapusgscal(TC, P, species):
    """
    This function evaluates Gibbs energy and heat capacity as a function of temperature and pressure
    for any mineral or gas specie using Haas and Fisher (1976)'s heat capacity parameter fit (utilized for solid-solutions)

    Parameters
    ----------
       TC : float, vector
           Temperature [°C]
       P : float, vector
           Pressure [bar]
       species : array
           Properties such as [dG [cal/ml], dH [cal/mol], S [cal/mol-K], V [cm³/mol], a [cal/mol-K], b [cal/mol/K^2], c [cal/mol/K], g [cal/mol/K^0.5], f [cal/mol/K^3] )

    Returns
    ----------
       delGfPT : float, vector
           Gibbs Energy [cal/mol]
       delCp : float, vector
           Heat capacity [cal/mol/K]

    Examples
    --------
    >>> from pygcc.pygcc_utils import db_reader
    >>> ps = db_reader() # utilizes the default direct-access database, speq21
    >>> [delGfPT, delCp] = heatcapusgscal( 100, 50, ps.dbaccessdic['ss_Anorthite'])
        -960440.79915641, 57.46776903

    References
    ----------
        (1) Haas JL Jr, Fisher JR (1976) Simultaneous evaluation and correlation of thermodynamic data.
            American Journal of Science 276:525-545
    """
    if (np.ndim(TC) == 0) | (np.ndim(P) == 0):
        T = np.array(convert_temperature( TC, Out_Unit = 'K' )).ravel()
        P = np.array(P).ravel()
    else:
        T = convert_temperature( TC, Out_Unit = 'K' ).ravel()
        P = P.ravel()
    Tr = 298.15 # K
    Pr = 1.0    # bar
    delGref = species[2] #cal/mol
    Sr = species[4] # cal/mol/K
    Vr = species[5]/41.84 # conversion: cal/bar/cm3  See Johnson et al., 1992
    a = species[6] #
    b = species[7] # T
    c = species[8] # T^-2
    g = species[9] # T^-.5
    f = species[10] # T^2

    delCp = a + b*T + c*(T**-2.0) + g*(T**-.5) + f*(T**2.0)
    delGfPT = np.nan*np.ones(len(T))
    if len(species[2:]) == 9:

        delGfPT = delGref - Sr*(T-Tr) + Vr*(P-Pr) + a*(T-Tr-T*np.log(T/Tr)) + (b/2)*(-T**2-Tr**2+2*T*Tr) \
            + c*((-T**2-Tr**2+2*T*Tr)/(2*T*Tr**2)) + (f/6)*(-T**3-2*Tr**3+3*T*Tr**2) \
                + 2*g*(2*T**0.5-Tr**0.5-(T/(Tr**0.5)))

    elif len(species[2:]) == 15:  #There is one phase transition to be accounted for

        delGfPT = delGref - Sr*(T-Tr) + Vr*(P-Pr) + a*(T-Tr-T*np.log(T/Tr)) + (b/2)*(-T**2-Tr**2+2*T*Tr) \
            + c*((-T**2-Tr**2+2*T*Tr)/(2*T*Tr**2)) + (f/6)*(-T**3-2*Tr**3+3*T*Tr**2)  \
                + 2*g*(2*T**.5-Tr**.5-(T/(Tr**.5)))

        Ttrans = species[11] #K
        # For T greater than the phase transition:
        # Get the heat capacity coefficients for T>Ttrans
        a = species[12] #
        b = species[13] # T
        c = species[14] # T^-2
        f = species[16] # T^2
        g = species[15] # T^-.5

        delGfPT[T>Ttrans] = delGfPT[T>Ttrans] + a*(T[T>Ttrans]-Ttrans-T[T>Ttrans]*np.log(T[T>Ttrans]/Ttrans)) \
            + (b/2)*(-T[T>Ttrans]**2 - Ttrans**2 + 2*T[T>Ttrans]*Ttrans)   \
                + c*((-T[T>Ttrans]**2 - Ttrans**2 + 2*T[T>Ttrans]*Ttrans)/(2*T[T>Ttrans]*Ttrans**2))  \
                    + (f/6)*(-T[T>Ttrans]**3 - 2*Ttrans**3 + 3*T[T>Ttrans]*Ttrans**2)   \
                        + 2*g*(2*T[T>Ttrans]**.5 - Ttrans**.5 - (T[T>Ttrans]/(Ttrans**.5)))

    return delGfPT, delCp


def supcrtaq(TC, P, specieppt, Dielec_method = None, **rhoE):
    """
    This function evaluates the Gibbs free energy of aqueous species at T and P
    using the revised HKF equation of state

    Parameters
    ----------
       TC : float, vector
           Temperature [°C] \n
       P : float, vector
           Pressure [bar] \n
       specieppt : array
           Properties such as (dG [cal/mol], dH [cal/mol], S [cal/mol-K], V [cm3/mol], a1 [*10 cal/mol/bar], a2 [*10**-2 cal/mol], a3 [cal-K/mol/bar], a4 [*10**-4 cal-K/mol], c1 [cal/mol/K], c2 [*10**-4 cal-K/mol], ω [*10**-5 cal/mol] )
       Dielec_method : string
           specify either 'FGL97' or 'JN91' or 'DEW' as the method to calculate dielectric constant (optional), if not specified default - 'JN91'
       rhoE : dict
           dictionary of water properties like density (rho) and dielectric factor (E) (optional)

    Returns
    -------
       delG : float, vector
           Gibbs energy [cal/mol]

    Usage
    -------
        The general usage of supcrtaq without the optional arguments is as follows: \n
        (1) Not on steam saturation curve: \n
            delG = supcrtaq(TC, P, specieppt) \n
            where T is temperature in celsius and P is pressure in bar
        (2) On steam saturation curve: \n
            delG = supcrtaq(TC, 'T', specieppt),  \n
            where T is temperature in celsius, followed with a quoted char 'T' \n
            delG = supcrtaq(P, 'P', specieppt),  \n
            where P is pressure in bar, followed with a quoted char 'P'.
        (3) Meanwhile, usage with any specific dielectric constant method ('FGL97') for
            condition not on steam saturation curve is as follows. Default method is 'JN91' \n
            delG = supcrtaq(TC, P, specieppt, Dielec_method = 'FGL97')

    Examples
    --------
    >>> from pygcc.pygcc_utils import db_reader
    >>> ps = db_reader() # utilizes the default direct-access database, speq21
    >>> delG = supcrtaq( 100, 50, ps.dbaccessdic['H2S(aq)'], Dielec_method = 'JN91')
        -9221.81721068
    >>> delG = supcrtaq( 100, 50, ps.dbaccessdic['H2S(aq)'], Dielec_method = 'FGL97')
        -9221.6542038

    References
    ----------
        (1) Johnson JW, Oelkers EH, Helgeson HC. 1992. SUPCRT92: A software package for calculating
            the standard molal thermodynamic properties of minerals, gases, aqueous species, and
            reactions from 1 to 5000 bar and 0 to 1000°C. Computers & Geosciences 18(7): 899-947.
            doi: 10.1016/0098-3004(92)90029-Q \n
    """
    delGref = specieppt[2]
    # Href = specieppt[3]
    Sref = specieppt[4]
    a1 = specieppt[5]*1e-1
    a2 = specieppt[6]*1e2
    a3 = specieppt[7]
    a4 = specieppt[8]*1e4
    c1 = specieppt[9]
    c2 = specieppt[10]*1e4
    omegaref = specieppt[11]*1e5
    Z = specieppt[12] #Z is formal charge

    Dielec_method = 'JN91' if Dielec_method is None else Dielec_method
    if type(P) == str:
        if P == 'T':
            P = iapws95(T = TC).P
            P[np.isnan(P) | (P < 1)] = 1.0133
        elif P == 'P':
            P = TC   # Assign first input T to pressure in bar
            TC = iapws95(P = P).TC

    if np.ndim(TC) == 0:
        TC = np.array(TC).ravel()
    else:
        TC = TC.ravel()
    if np.ndim(P) == 0:
        P = np.array(P).ravel()
    else:
        P = P.ravel()
    length = len(TC)

    if rhoE.__len__() != 0:
        rho = rhoE['rho'].ravel()
        rhohat = rho/1000  #g/cm^3
        E = rhoE['E'].ravel()
    else:
        if Dielec_method.upper() == 'DEW':
            rho = ZhangDuan(T = TC, P = P).rho
        else:
            rho = iapws95(T = TC, P = P).rho
        waterdielec = water_dielec(T = TC, P = P, Dielec_method = Dielec_method)
        E, rhohat = waterdielec.E, waterdielec.rhohat

    TK = convert_temperature( TC, Out_Unit = 'K' )
    Tr = 298.15 #K

    g = np.zeros([length, 1]).ravel()
    theta = 228 #K
    psi = 2600 #bars
    Pr = 1 #bars
    # Conversionfactor = 41.8393  # bar cm3 cal^-1
    # Yref = -5.802E-5 #K^-1
    # Eref = 78.2396
    if Dielec_method.upper() == 'FGL97':
        Eref, Yref = 78.40836752, -5.836655257780387e-05
        #(calculated at 298.15K and 1 bar)
        # waterdielec_TrPr = water_dielec(T = convert_temperature( Tr, Out_Unit = 'C' ), P = Pr, Dielec_method = Dielec_method)

    elif Dielec_method.upper() ==  'JN91':
        Eref, Yref = 78.24385513, -5.795647242492297e-05
        #(calculated at 298.15K and 1 bar)
        # waterdielec_TrPr = water_dielec(T = convert_temperature( Tr, Out_Unit = 'C' ), P = Pr, Dielec_method = Dielec_method)
    elif Dielec_method.upper() ==  'DEW':
        # Eref, Yref = 77.94949459, -5.446705267498e-05
        Eref, Yref = 78.47, -5.79865E-05
        #(calculated at 298.15K and 1 bar)
        # waterdielec_TrPr = water_dielec(T = convert_temperature( Tr, Out_Unit = 'C' ), P = Pr, Dielec_method = Dielec_method)
    # Eref, dEdT_P = waterdielec_TrPr.E, waterdielec_TrPr.dEdT_P
    # Yref = dEdT_P/Eref**2

    n = 1.66027e5
    f1_T = TK*np.log(TK/Tr) - TK + Tr
    f2_T = (((1/(TK - theta)) - (1/(Tr - theta)))*((theta - TK)/(theta)) - \
            (TK/(theta**2))*np.log(Tr*(TK - theta)/(TK*(Tr - theta))))
    f1_P = (P - Pr)
    f2_P = np.log((psi + P)/(psi + Pr))
    f1_PT = ((P - Pr)/(TK - theta))
    f2_PT = (1/(TK - theta))*np.log((psi + P)/(psi + Pr))
    f3_PT = ((1/E) - (1/Eref) + Yref*(TK - Tr))

    if Z == 0:
        r = 0
        f4_PT = 0
    else:
        agi = [-2.037662,  5.747e-3, -6.557892e-6]
        bgi = [6.107361, -1.074377e-2, 1.268348e-5]

        for k in range(length):
            if rhohat[k]<1:
                ag = agi[0] + agi[1]*TC[k] + agi[2]*TC[k]**2
                bg = bgi[0] + bgi[1]*TC[k] + bgi[2]*TC[k]**2
                g[k] = ag*(1 - rhohat[k])**bg

                if ((TC[k]<155) | (P[k] > 1000) | (TC[k] >355)):
                    g[k] = g[k]
                else:
                    afi = [0.3666666e2, -1.504956e-10, 5.01799e-14]
                    Tg = (TC[k] - 155)/300
                    Pg = 1000 - P[k]
                    f_T = Tg**4.8 + afi[0]*Tg**16
                    f_P = afi[1]*Pg**3 + afi[2]*Pg**4

                    f_PT = f_T*f_P
                    g[k] = g[k] - f_PT
        r = Z**2*(omegaref/n + Z/3.082)**-1 + abs(Z)*g   # eqn 48
        omega = n*((Z**2/r) - (Z/(3.082 + g)))           # eqn 55
        f4_PT = (omega - omegaref)*((1/E) - 1)


    delG = delGref - Sref*(TK-Tr) - c1*f1_T - c2*f2_T + a1*f1_P + a2*f2_P + a3*f1_PT + \
        a4*f2_PT + omegaref*f3_PT + f4_PT               # eqn 59

    rhominCA = 0.35
    rhominNA = 0.05
    Pmax1 = 500
    # Pmax2 = 1000
    Tmin = 350
    Tmax = 400

    if Z != 0:
        xall = ((np.around(rhohat,3) < rhominCA) | (P < Pmax1) & (TC > Tmin) & (TC < Tmax))
    else:
        xall = (np.around(rhohat,3) < rhominNA)

    delG[xall] = np.nan

    return delG


def Element_counts(formula):
    """
    This function calculates the elemental composition of a substance given by its chemical formula
    It was a modified version of https://github.com/cgohlke/molmass/blob/master/molmass/molmass.py

    Parameters
    ----------
        formula : string
            Chemical formula

    Returns
    ----------
        elements : dict
            dictionary of elemental composition and their respective number of atoms

    Usage:
    ----------
        [elements] = Element_counts(formula)
            Examples of valid formulas are "H2O", "[2H]2O", "CH3COOH", "EtOH", "CuSO4:5H2O", "(COOH)2", "AgCuRu4(H)2[CO]12{PPh3}2", "CGCGAATTCGCG", and, "MDRGEQGLLK" .
    """

    validchars = set('([{<123456789ABCDEFGHIKLMNOPRSTUVWXYZ')
    validchars |= set(']})>0abcdefghiklmnoprstuy')

    elements = {}
    ele = ''  # parsed element
    num = 0  # number
    level = 0  # parenthesis level
    counts = [1]  # parenthesis level multiplication
    formula = formula.strip("(aq)").strip("(am)")
    i = len(formula)
    while i:
        i -= 1
        char = formula[i]

        if char in '([{<':
            level -= 1
        elif char in ')]}>':
            if num == 0:
                num = 1
            level += 1
            if level > len(counts) - 1:
                counts.append(0)
            counts[level] = num * counts[level - 1]
            num = 0
        elif char.isdigit():
            j = i
            while i and (formula[i - 1].isdigit() or formula[i - 1] == '.'):
                i -= 1
            num = float(formula[i : j + 1])
        elif char.islower():
            ele = char
        elif char.isupper():
            ele = char + ele
            if num == 0:
                num = 1
            j = i
            number = num * counts[level]
            if ele in elements.keys():
                elements[ele] = number + elements[ele]
            else:
                elements[ele] = number
            ele = ''
            num = 0
        elif char == ':':
            if num == 0:
                num = 1
            for k in elements.keys():
                elements[k] = elements[k]*num

    return elements


def heatcap_Berman(TC, P, species):
    """
    This function evaluates Gibbs energy and heat capacity as a function of temperature
    and pressure for any mineral or gas specie using Berman (1988) equations and datasets with
    Berman and Brown (1985)'s heat capacity parameter fit

    Parameters
    ----------
       TC : float, vector
           Temperature [°C]
       P : float, vector
           Pressure [bar]
       species : array
           Properties such as [dG [J/mol], dH [J/mol], S [J/mol-K], V [cm³/mol], k0, k1, k2, k3, v1 [*10^5 K^-1], v2 [*10^5 K^-2], v3 [*10^5 bar^-1], v4 [*10^8 bar^-2], dTdP [K/bar], Tlambda [K], Tref [K], l1 [(J/mol)^0.5/K], l2 [(J/mol)^0.5/K^2], DtH, d0 [J/mol], d1 [J/mol], d2 [J/mol], d3 [J/mol], d4 [J/mol], d5 [J/mol], Tmin [K], Tmax [K]] \n
    Returns
    ----------
       delGfPT : float, vector
           Gibbs Energy [cal/mol]
       delCp : float, vector
           Heat capacity [cal/mol/K]

    Examples
    ----------
    >>> from pygcc.pygcc_utils import db_reader
    >>> # utilizes the default speq21 and specified Berman dataset database
    >>> ps = db_reader(dbBerman_dir = './default_db/Berman.dat')
    >>> [delGfPT, delCp] = heatcap_Berman( 100, 50, ps.dbaccessdic['Quartz'])
        -205472.3365716, 12.32381279

    References
    ----------
        (1) Berman, R. G. (1988). Internally-consistent thermodynamic data for minerals in the system
            Na2O-K2O-CaO-MgO-FeO-Fe2O3-Al2O3-SiO2-TiO2-H2O-CO2. Journal of petrology, 29(2), 445-522.
        (2) Berman RG, Brown TH (1985) Heat Capacities of minerals in the system Na2O-K2O-CaO-MgO-FeO-Fe2O3-Al2O3-SiO2-TiO2-H2O-CO2:
            Representation, estimation, and high temperature extrapolation. Contrib Mineral Petrol 89:168-183
    """
    if (np.ndim(TC) == 0):
        T = np.array(convert_temperature( TC, Out_Unit = 'K' )).ravel()
    else:
        T = convert_temperature( TC, Out_Unit = 'K' ).ravel()
    if np.size(P) <= 2:
        P = np.ravel(P)
        P = P[0]*np.ones(np.size(TC))
     # delGref = species[2]
    Hr = species[3]
    Sr = species[4]
    Vr = species[5] #*0.0239005736   # conversion: cal/bar/cm3  See Johnson et al., 1992
    k0 = species[6]
    k1 = species[7]
    k2 = species[8]
    k3 = species[9]
    v1 = species[10]*10**-5
    v2 = species[11]*10**-5
    v3 = species[12]*10**-5
    v4 = species[13]*10**-8
    dTdP = species[14] if len(species) > 14 else 0
    Tlambda = species[15] if len(species) > 15 else 0
    Tref = species[16] if len(species) > 16 else 0
    l1  = species[17] if len(species) > 17 else 0
    l2 = species[18] if len(species) > 18 else 0
    # DtH	 = species[19] if len(species) > 19 else 0
    d0	 = species[20] if len(species) > 20 else 0
    d1	 = species[21] if len(species) > 21 else 0
    d2	 = species[22] if len(species) > 22 else 0
    d3	 = species[23] if len(species) > 23 else 0
    d4	 = species[24] if len(species) > 24 else 0
    d5 = species[25] if len(species) > 25 else 0
    Tmin = species[26] if len(species) > 26 else 0
    Tmax = species[27] if len(species) > 27 else 0
    Tr = 298.15
    Pr = 1.0
    # Entropy of the elements (CODATA) in J/K/mol
    S_elem = {'Si' : 18.81, 'Al' : 28.3, 'Mg' : 32.67, 'B' : 5.9, 'Be' : 9.5, 'K' : 64.68,
              'Na' : 51.3, 'Ca' : 41.59, 'Fe' : 27.32, 'Li' : 29.12, 'Mn' : 32.01, 'Ni' : 29.87,
              'Co' : 30.04, 'Cs' : 85.23, 'Rb' : 76.78, 'Ba' : 62.48, 'Sr' : 55.69, 'Cu' : 33.15,
              'Cd' : 51.8, 'Zn' : 41.72, 'N2' : 191.6, 'V' : 28.94, 'Cr' : 23.62, 'Ti' : 30.72,
              'O' : 205.152, 'H' : 130.68, 'F' : 202.791, 'Cl' : 223.081, 'S' : 228.167, 'C' : 158.100}
    Cp = k0 + k1 * T**-0.5 + k2 * T**-2 + k3 * T**-3  # + k4*T**-1 + k5*T + k6*T**2
    # V =  Vr * (1 + v1 * (T - Tr) + v2 * (T - Tr)**2 + v3 * (P - Pr) + v4 * (P - Pr)**2)

    CpdT = k0*(T - Tr) + 2*k1*(T**0.5 - Tr**0.5) - k2*(1/T - 1/Tr) - k3/2*(1/T**2 - 1/Tr**2)
    V_TdVdT = - Vr + P*(Vr + Vr*v4 - Vr*v3 - Tr*Vr*v1 + Vr*v2*Tr**2 - Vr*v2*T**2) +\
        P**2*(Vr*v3/2 - Vr*v4) + Vr*v3/2 - Vr*v4/3 + Tr*Vr*v1 + Vr*v2*T**2 - Vr*v2*Tr**2 + Vr*v4*P**3/3
    H = Hr + CpdT + V_TdVdT

    CpTdT = k0*(np.log(T) - np.log(Tr)) - 2*k1*(T**-0.5 - Tr**-0.5) - k2/2*(1/T**2 - 1/Tr**2) - k3/3*(1/T**3 - 1/Tr**3)
    dVdT = Vr*(P - Pr)*(v1 + 2*v2*(T - Tr))
    S = Sr + CpTdT - dVdT
    # According to Berman-Brown convention (DG = DH - T*S, no S(element))
    # G = H - T * S
    G = Hr - T * Sr + k0*((T - Tr) - T*(np.log(T) - np.log(Tr))) + \
        2*k1*( (T**0.5 - Tr**0.5) + T*(T**-0.5 - Tr**-0.5) ) - \
            k2*( (T**-1 - Tr**-1) - T*(T**-2 - Tr**-2)/2 ) - \
                k3*( (T**-2 - Tr**-2)/2 - T*(T**-3 - Tr**-3)/3 ) + \
                    Vr*( (v3/2 - v4)*(P**2 - Pr**2) + v4*(P**3 - Pr**3)/3 +\
                              (1 - v3 + v4 + v1*(T - Tr) + v2*(T - Tr)**2)*(P - Pr) )
    # use S(element) to convert G back to Benson-Helgeson convention
    Sr_elements = np.sum([S_elem[k]*j if k not in ['O', 'H', 'F', 'Cl', 'S']
                          else S_elem[k]*j/2 for k,j in Element_counts(species[0]).items()])
    G = G + Tr * Sr_elements
    H = G + T * S

    ### polymorphic transition contributions
    Gtrans = np.zeros(len(T)); Htrans = np.zeros(len(T)); Strans = np.zeros(len(T)); Cptrans = np.zeros(len(T));
    for i in range(len(T)):
        if (Tlambda != 0) & (Tref  != 0) & (T[i] > Tref) & (dTdP  != 0):
            Tlambda_P = Tlambda + dTdP * (P[i] - 1)                 # Eq. 9
            Td = Tlambda - Tlambda_P
            Tprime = T[i] + Td
            # with the condition that Tref < Tprime < Tlambda(1bar)
            if (Tref < Tprime < Tlambda):
                Cptrans[i] = Tprime * (l1 + l2 * Tprime)**2         # Eq. 8a
            else:
                Cptrans[i] = 0
            Ttrans = Tlambda_P if T[i] >= Tlambda_P else T[i]       # the upper integration limit is Tlambda_P
            tref = Tref - Td                                        # the lower integration limit is Tref
            x1 = l1**2 * Td + 2 * l1 * l2 * Td**2 + l2**2 * Td**3
            x2 = l1**2 + 4 * l1 * l2 * Td + 3 * l2**2 * Td**2
            x3 = 2 * l1 * l2 + 3 * l2**2 * Td
            x4 = l2 ** 2
            # Eqs. 10, 11, 12
            Htrans[i] = x1 * (Ttrans - tref) + x2 / 2 * (Ttrans**2 - tref**2) + x3 / 3 * (Ttrans**3 - tref**3) + \
                x4 / 4 * (Ttrans**4 - tref**4)
            Strans[i] = x1 * (np.log(Ttrans) - np.log(tref)) + x2 * (Ttrans - tref) + x3 / 2 * (Ttrans**2 - tref**2) + \
                x4 / 3 * (Ttrans**3 - tref**3)
            Gtrans[i] = Htrans[i] - T[i] * Strans[i]
            Gtrans[i] = Gtrans[i] - (T[i] - Tlambda_P)*Strans[i] if (dTdP == 0)&(T[i] >= Tlambda_P) else Gtrans[i] # Eq. 13

    ### order-disorder contributions
    Gds = np.zeros(len(T)); Hds = np.zeros(len(T)); Sds = np.zeros(len(T)); Cpds = np.zeros(len(T)); Vds = np.zeros(len(T))
    for i in range(len(T)):
        if ((Tmin != 0) & (Tmax != 0) & (T[i] > Tmin) ):
            Tds = Tmax if T[i] > Tmax else T[i]  # the lower integration limit is Tmin and the upper integration limit is Tmax
            # Eqs. 15, 16, 17, 18
            Cpds[i] = d0 + d1*Tds**-0.5 + d2*Tds**-2 + d3*Tds + d4*Tds**2
            Hds[i] = d0*(Tds - Tmin) + 2*d1*(Tds**0.5 - Tmin**0.5) - d2*(Tds**-1 - Tmin**-1) + \
                d3*(Tds**2 - Tmin**2)/2 + d4*(Tds**3 - Tmin**3)/3
            Sds[i] = d0*(np.log(Tds) - np.log(Tmin)) - 2*d1*(Tds**-0.5 - Tmin**-0.5) - \
                d2*(Tds**-2 - Tmin**-2)/2 + d3*(Tds - Tmin) + d4*(Tds**2 - Tmin**2)/2
            Vds[i] = Hds[i] / d5 if (d5 != 0) else 0
            Gds[i] = Hds[i] - T[i] * Sds[i] + Vds[i] * (P[i] - Pr)         #  Eq. 19
            # disordering above Tmax (Eq. 20)
            Gds[i] = Gds[i] - (T[i] - Tmax) * Sds[i] if T[i] > Tmax else Gds[i]

    # apply the transition and disorder contributions
    G = (G + Gtrans + Gds)/J_to_cal
    S = (S + Strans + Sds)/J_to_cal
    H = (H + Htrans + Sds)/J_to_cal
    # V = (V + Vds)/J_to_cal
    Cp = (Cp + Cptrans + Cpds)/J_to_cal

    return G, Cp

