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

"""

import re, os
import textwrap
J_to_cal = 4.184

# from sys import platform

def findcodecs(filename):
    """Function to find the name of the encoding used to decode or encode any file    """
    data = open(filename, "rb").read()
    # data = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), 'rb').read()
    all_codecs = ['ascii', 'latin_1', 'utf_8']
    f = [0]*len(all_codecs)
    for j, i in enumerate(all_codecs):
        try:
            decoded = data.decode(i)
        except UnicodeDecodeError:
            f[j] = False
        else:
            for ch in decoded:
                if i == 'utf_8' and 0xD800 <= ord(ch) <= 0xDFFF:
                    f[j] = False
            f[j] = True
    if all(f) == True:
        return None
    else:
        return all_codecs[1]
        # if platform == "darwin": # OS X
        #     return all_codecs[1]
        # elif platform in ["linux", "linux2", "win32"]:   # linux and # Windows...
        #     return None


class db_reader:
    """Class to read direct-access and source thermodynamic database

    Parameters
    ----------
        dbaccess : string
            filename and location of the direct-access database, optional, default is speq21
        dbBerman_dir : string
            filename and location of the Berman mineral database, optional
        sourcedb : string
            filename of the source database, optional
        sourcedb : string
            filename of the source database, optional
        sourceformat : string
            specify the source database format, either 'GWB' or 'EQ36', optional
        sourcedb_codecs : string
            specify the name of the encoding used to decode or encode the sourcedb file, optional
        dbaccess_codecs : string
            specify the name of the encoding used to decode or encode the dbaccess file, optional

    Returns
    -------
        dbaccessdic : dict
            dictionary of minerals, gases, redox and aqueous species     \n
        dbaccess : string
            direct-access database file name     \n
        sourcedic : dict
            dictionary of reaction coefficients and species   \n
        specielist : list
            list of species segmented into the different categories [element, basis, redox, aqueous, minerals, gases, oxides]   \n
        speciecat : list
            list of species categories listed in 'specielist'   \n
        chargedic : dict
            dictionary of charges of species   \n
        MWdic : dict
            dictionary of MW of species   \n
        Mineraltype : dict
            mineral type for minerals   \n
        fugacity_info : dict
            fugacity information as stored in new tdat database for chi and critical ppts   \n
        Sptype : dict
            specie types and eq3/6 and revised date info   \n
        Elemlist : dict
            dictionary of elements and coefficients   \n

    Examples
    --------
    >>> ps = db_reader(sourcedb = './default_db/thermo.com.dat',
                       sourceformat = 'gwb',
                       dbaccess = './default_db/speq21.dat')
    >>> ps.sourcedic, ps.dbaccessdic, ps.specielist


    """
    kwargs = {"dbaccess": None,
              "dbBerman_dir": None,
              "sourcedb": None,
              "sourceformat": None,
              "sourcedb_codecs": None,
              "dbaccess_codecs": None}

    def __init__(self, **kwargs):
        self.kwargs = db_reader.kwargs.copy()
        self.__calc__(**kwargs)

    def __calc__(self, **kwargs):
        self.kwargs.update(kwargs)
        if self.kwargs['dbaccess'] is None:
            self.dbaccess_dir = './default_db/speq21.dat'
            self.dbaccess_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.dbaccess_dir)
        else:
            self.dbaccess_dir = self.kwargs["dbaccess"]
        self.dbBerman_dir = self.kwargs["dbBerman_dir"]
        self.sourcedb_dir = self.kwargs["sourcedb"]
        if self.kwargs['dbaccess_codecs'] is None:
            self.dbaccess_codecs = findcodecs(self.dbaccess_dir)
        else:
            self.dbaccess_codecs = self.kwargs['dbaccess_codecs']
        if self.kwargs["sourcedb"] is not None and self.kwargs['sourcedb_codecs'] is None:
            self.sourcedb_codecs = findcodecs(self.sourcedb_dir)
        else:
            self.sourcedb_codecs = self.kwargs['sourcedb_codecs']
        if self.dbaccess_dir is not None:
            self.dbaccess = self.dbaccess_dir.split('/')[-1]
        if self.sourcedb_dir is not None:
            if self.kwargs["sourceformat"].lower() == 'gwb':
                self.readSourceGWBdb()
            elif self.kwargs["sourceformat"].lower() == 'eq36':
                self.readSourceEQ36db()
        if self.dbaccess_dir is not None:
            self.readAqspecdb() #

    def readAqspecdb(self):
        """
        This function reads direct access thermodynamic database and can add other database sources
        at the bottom returns all constants of Maier-Kelley power function  for minerals and gases
        (dG [cal/mol], dH [cal/mol], S [cal/mol-K], V [cm3/mol] a [cal/mol-K], b [*10**3 cal/mol/K^2],
         c [*10^-5 cal/mol/K], Ttrans [K], Htr [cal/mol], Vtr [cm³/mol], dPdTtr [bar/K] ) and
        aqueous species (dG [cal/mol], dH [cal/mol], S [cal/mol-K], V [cm3/mol], a1 [*10 cal/mol/bar],
        a2 [*10**-2 cal/mol], a3 [cal-K/mol/bar], a4 [*10**-4 cal-K/mol], c1 [cal/mol/K], c2 [*10**-4 cal-K/mol],
        ω [*10**-5 cal/mol] ) packed into a dbacess dictionary. In addition, the function can read Berman's
        mineral properties such as (dG [J/mol], dH [J/mol], S [J/mol-K], V [cm³/mol], k0, k1, k2, k3,
        v1 [*10^5 K^-1], v2 [*10^5 K^-2], v3 [*10^5 bar^-1], v4 [*10^8 bar^-2], dTdP [K/bar], Tlambda [K],
        Tref [K], l1 [(J/mol)^0.5/K], l2 [(J/mol)^0.5/K^2], DtH, d0 [J/mol], d1 [J/mol], d2 [J/mol],
        d3 [J/mol], d4 [J/mol], d5 [J/mol], Tmin [K], Tmax [K]) \n
        Parameters
        ----------
            dbaccess        filename and location of the direct-access database     \n
            dbBerman_dir    filename and location of the Berman mineral database     \n
        Returns
        ----------
            dbaccessdic      dictionary of minerals, gases, redox and aqueous species     \n
            dbaccess        dat file name     \n
        Usage:
        ----------
        [dbaccessdic, dbname] = readAqspecdb(dbaccess)
        """
        # check if its a single liner data
        codecs = self.dbaccess_codecs
        with open(self.dbaccess_dir, encoding = codecs) as g:
            Rd = g.readlines()

        self.dbaccessdic = {}; counter = 0
        # if it is single line data like for dpeq20
        if len(Rd) <= 1:
            width = re.search('                     3 ', Rd[0]).start()
            Rd = textwrap.wrap(Rd[0], width=width)

            for i in range(len(Rd)): #
                s1 = Rd[i]
                if not s1.startswith(('*', ' '),0) | (s1.rstrip('\n').lstrip('0123456789.- ') == "") | (s1[0] == "-") :
                    if (s1.strip()[:3] != 'ref') and (s1.strip()[:3] != 'REF'):
                        name = s1.strip().split()[0]
                        if len(s1.strip().split()) > 1:
                            formula = s1.strip().split()[1]
                        else:
                            formula = ''
                        s2 = Rd[i + 1]
                        if (s2.strip()[:3] != 'ref') and (s2.strip()[:3] != 'REF') and (s2.split()[0].lstrip('0123456789.,- ') != ''):
                            s3 = Rd[i+2]; s4 = Rd[i+3]; s5 = Rd[i+4];
                            if s3.split()[0].lstrip('0123456789.,- ') != '':
                                if i >= len(Rd) - 5:
                                    s6 = 'Null'; s7 = 'Null'; s8 = 'Null';
                                    s9 = 'Null'; s10 = 'Null'; s11 = 'Null';
                                elif i >= len(Rd) - 6:
                                    s6  = Rd[i + 5]; s7 = 'Null'; s8 = 'Null';
                                    s9 = 'Null'; s10 = 'Null'; s11 = 'Null';
                                else:
                                    s6  = Rd[i + 5]; s7 = Rd[i + 6]; s8 = Rd[i + 7];
                                    s9 = Rd[i + 8]; s10 = Rd[i + 9]; s11 = Rd[i + 10];

                                if s3.strip()[:3] == 'ref':
                                    ref = s3#.split()[0][4:]
                                else:
                                    ref = s3#.split()[0]
                                if (s6.lower().islower() == True) | (s6.strip().split()[0] == name):
                                    params = s4.split() + s5.split()
                                elif (s7.lower().islower() == True) | (s7.strip().split()[0] == name):
                                    params = s4.split() + s5.split() + s6.split()
                                elif (s8.lower().islower() == True) | (s8.strip().split()[0] == name):
                                    params = s4.split() + s5.split() + s6.split() + s7.split()
                                elif (s9.lower().islower() == True) | (s9.strip().split()[0] == name):
                                    params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split()
                                elif (s10.lower().islower() == True) | (s10.strip().split()[0] == name):
                                    params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split() + \
                                        s9.split()
                                elif (s11.lower().islower() == True) | (s11.strip().split()[0] == name):
                                    params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split() + \
                                        s9.split() + s10.split()
                                else:
                                    params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split() + \
                                        s9.split() + s10.split() + s11.split()
                                params = [float(i) if float(i) != 999999 else 0 for i in params]
                                counter += 1
                                if name in self.dbaccessdic.keys():
                                    print('Duplicate found for species "%s" in %s' % (name, self.dbaccess_dir.split('/')[-1]))
                                    continue
                                else:
                                    self.dbaccessdic[name] = [formula, ref] + params
        else:
        # else for multi line data like for speq21
            for i in range(len(Rd)): #
                s1 = Rd[i].rstrip('\n').strip()
                if (not s1.lstrip().startswith(('*', '!'))) and (s1.lstrip('0123456789.- \t') != ""):
                    if (s1[:3] != 'ref') and (s1[:3] != 'REF') and (s1.split()[0] not in ['minerals', 'gases', 'gas', 'aqueous', 'abandoned']):
                        name = s1.strip().split()[0]
                        if len(s1.split()) > 1:
                            formula = s1.split()[1]
                        else:
                            formula = ''
                        s2 = Rd[i + 1].strip()
                        if (s2[:3] != 'ref') and (s2[:3] != 'REF') and (s2[0].lstrip('0123456789.,- ') != ''):
                            s3 = Rd[i+2]; s4 = Rd[i+3]; s5 = Rd[i+4];
                            if i >= len(Rd) - 5:
                                s6 = 'Null'; s7 = 'Null'; s8 = 'Null';
                                s9 = 'Null'; s10 = 'Null'; s11 = 'Null';
                            elif i >= len(Rd) - 6:
                                s6  = Rd[i + 5]; s7 = 'Null'; s8 = 'Null';
                                s9 = 'Null'; s10 = 'Null'; s11 = 'Null';
                            else:
                                s6  = Rd[i + 5]; s7 = Rd[i + 6]; s8 = Rd[i + 7];
                                s9 = Rd[i + 8]; s10 = Rd[i + 9]; s11 = Rd[i + 10];

                            if s3.strip()[:3] == 'ref':
                                ref = s3#.split()[0][4:]
                            else:
                                ref = s3#.split()[0]
                            if (s6.lower().islower() == True) | s6.startswith('*', 0):
                                params = s4.split() + s5.split()
                            elif (s7.lower().islower() == True) | s7.startswith('*', 0):
                                params = s4.split() + s5.split() + s6.split()
                            elif (s8.lower().islower() == True) | s8.startswith('*', 0):
                                params = s4.split() + s5.split() + s6.split() + s7.split()
                            elif (s9.lower().islower() == True) | s9.startswith('*', 0):
                                params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split()
                            elif (s10.lower().islower() == True) | s10.startswith('*', 0):
                                params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split() + \
                                    s9.split()
                            elif (s11.lower().islower() == True) | s11.startswith('*', 0):
                                params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split() + \
                                    s9.split() + s10.split()
                            else:
                                params = s4.split() + s5.split() + s6.split() + s7.split() + s8.split() + \
                                    s9.split() + s10.split() + s11.split()
                            params = [float(i) if float(i) != 999999 else 0 for i in params]
                            counter += 1
                            if name in self.dbaccessdic.keys():
                                print('Duplicate found for species "%s" in %s' % (name, self.dbaccess_dir.split('/')[-1]))
                                continue
                            else:
                                self.dbaccessdic[name] = [formula, ref] + params

                            if len(s5.split()) != 0 and len(s6.split()) and (s5.strip() == '' and s6.strip() == ''):
                                break
                            elif len(s7.split()) != 0 and len(s6.split()) and (s6.strip() == '' and s7.strip() == ''):
                                break
                            elif len(s7.split()) != 0 and len(s8.split()) and (s7.strip() == '' and s8.strip() == ''):
                                break
                            elif len(s8.split()) != 0 and len(s9.split()) and (s8.strip() == '' and s9.strip() == ''):
                                break
                            elif len(s9.split()) != 0 and len(s10.split()) and (s9.strip() == '' and s10.strip() == ''):
                                break
                            elif len(s6.split()) != 0 and (s6.split()[-1] in ['(nmin1)', '(nmin2)', '(nmin3)', '(nmin4)', '(ngas)', '(naqs)']):
                                break
                            elif len(s7.split()) != 0 and (s7.split()[-1] in ['(nmin1)', '(nmin2)', '(nmin3)', '(nmin4)', '(ngas)', '(naqs)']):
                                break
                            elif len(s8.split()) != 0 and (s8.split()[-1] in ['(nmin1)', '(nmin2)', '(nmin3)', '(nmin4)', '(ngas)', '(naqs)']) :
                                break
                            elif len(s9.split()) != 0 and (s9.split()[-1] in ['(nmin1)', '(nmin2)', '(nmin3)', '(nmin4)', '(ngas)', '(naqs)']) :
                                break
                            elif len(s10.split()) != 0 and (s10.split()[-1] in ['(nmin1)', '(nmin2)', '(nmin3)', '(nmin4)', '(ngas)', '(naqs)']):
                                break
                    if s1.split()[0] in ['gases', 'gas']:
                        last_mineral = list(self.dbaccessdic.keys())[-1]
        if self.dbBerman_dir is not None:
            codecs = findcodecs(self.dbBerman_dir)
            mineral_list = list(self.dbaccessdic.keys())[:list(self.dbaccessdic.keys()).index(last_mineral)+1]
            self.dbaccessdic = {k: v for k, v in self.dbaccessdic.items() if k not in mineral_list}
            specie_name = []
            with open(self.dbBerman_dir, encoding = codecs) as g:
                for i, line in enumerate(g, 1):
                    if line.strip('*').startswith('COMMENTS'):
                        break
                    if (not line.lstrip().startswith(('!', 'ST', 'C1', 'C2', 'C3', 'D1', 'D2',
                                                      'T1', 'T2', 'V1', '*'))) and (line.lstrip('0123456789.- \t\n') != ""):
                        specie_name.append(line.strip().split()[0])

            gid = open(self.dbBerman_dir, 'r', encoding = codecs)
            for i in range(5000):
                s1 = gid.readline()
                if s1.strip('*').startswith('MINERAL DATA'):
                    break

            s4 = '0'; s5 = '0'; s6 = '0'
            for i in range(5000):
                s1 = s4 if s4.strip().split()[0] in specie_name else s5 if s5.strip().split()[0] in specie_name else s6 if s6.strip().split()[0] in specie_name else gid.readline()
                if s1.strip('*').startswith('COMMENTS')|s6.strip('*').startswith('COMMENTS')|s5.strip('*').startswith('COMMENTS'):
                    break
                if (not s1.lstrip().startswith(('!', 'ST', 'C1', 'C2', 'C3', 'D1', 'D2', 'T1', 'T2', 'V1'))) and (s1.lstrip('0123456789.- \t\n') != ""):
                    name = s1.strip().split()[0]
                    if len(s1.split()) > 1:
                        formula = s1.split()[1]
                    else:
                        formula = ''
                    s2 = gid.readline(); s2 = gid.readline() if s2.lstrip().startswith('!') else s2;
                    s3 = gid.readline()
                    s4 = gid.readline() if (s3.strip().split()[0] not in specie_name) else '0'
                    s4 = s4 + '0' if s4.strip() == '' else s4
                    s5 = gid.readline() if s4.strip().split()[0] not in specie_name else '0'
                    s5 = s5 + '0' if s5.strip() == '' else s5
                    s6 = gid.readline() if s5.strip().split()[0] not in specie_name else '0'
                    s6 = s6 + '0' if s6.strip() == '' else s6
                    params = s2.split()[1:-1] if s2.lstrip().startswith('ST') else s3.split()[1:-1] if s3.lstrip().startswith('ST') else s4.split()[1:-1] if s4.lstrip().startswith('ST') else s5.split()[1:-1] if s5.lstrip().startswith('ST') else [0]*4
                    params += s3.split()[1:-1] if s3.lstrip().startswith('C1') else s4.split()[1:-1] if s4.lstrip().startswith('C1') else s5.split()[1:-1] if s5.lstrip().startswith('C1') else s6.split()[1:-1] if s6.lstrip().startswith('C1') else [0]*4
                    # params += s3.split()[1:-2] if s3.lstrip().startswith('C2') else s4.split()[1:-2] if s4.lstrip().startswith('C2') else s5.split()[1:-2] if s5.lstrip().startswith('C2') else s6.split()[1:-2] if s6.lstrip().startswith('C2') else [0]*3
                    params += s3.split()[1:-1] if s3.lstrip().startswith('V1') else s4.split()[1:-1] if s4.lstrip().startswith('V1') else s5.split()[1:-1] if s5.lstrip().startswith('V1') else s6.split()[1:-1] if s6.lstrip().startswith('V1') else [0]*4
                    params += s3.split()[1:2] if s3.lstrip().startswith('T2') else s4.split()[1:2] if s4.lstrip().startswith('T2') else s5.split()[1:2] if s5.lstrip().startswith('T2') else s6.split()[1:2] if s6.lstrip().startswith('T2') else [0]
                    params += s3.split()[1:] if s3.lstrip().startswith('T1') else s4.split()[1:] if s4.lstrip().startswith('T1') else s5.split()[1:] if s5.lstrip().startswith('T1') else s6.split()[1:] if s6.lstrip().startswith('T1') else [0]*5
                    params += s3.split()[1:-1] if s3.lstrip().startswith('D1') else s4.split()[1:-1] if s4.lstrip().startswith('D1') else s5.split()[1:-1] if s5.lstrip().startswith('D1') else s6.split()[1:-1] if s6.lstrip().startswith('D1') else []
                    params += s3.split()[1:-1] if s3.lstrip().startswith('D2') else s4.split()[1:-1] if s4.lstrip().startswith('D2') else s5.split()[1:-1] if s5.lstrip().startswith('D2') else s6.split()[1:-1] if s6.lstrip().startswith('D2') else []
                    ref = 'Berman_1988'
                    params = [float(i) if float(i) != 999999 else 0 for i in params]
                    # print(name, params)
                    if name in self.dbaccessdic.keys():
                        print('Duplicate found for species "%s" in %s' % (name, self.dbBerman_dir.split('/')[-1]))
                        continue
                    else:
                        self.dbaccessdic[name] = [formula, ref] + params
            gid.close()

        #%% other sources aside speq20 for solid solution calculation
        #dG dH S V a1 a2 a3 a4 a5
        # dG, dH, S from Arnorsson 1999, V and Cp from Robie and Hemingway #1995
        _Anorthite_ = ['Ca(Al2Si2)O8', 'R&H95, Stef2001',-4002095, -4227830, 199.30, 100.790*J_to_cal,
                       5.168e2, -9.249e-2, -1.408e6, -4.589e3, 4.188e-5]
        self.dbaccessdic['ss_Anorthite'] = [x/J_to_cal if type(x)!=str else x for x in _Anorthite_ ]

        self.dbaccessdic['ss_Albite_high'] = ['NaAlSi3O8', 'R&H95, Stef2001', -887368.32+8413/J_to_cal,
                                        -940769.52, 224.14/J_to_cal, 100.07, 139.56, -0.0221916826,
                                        401051.6, -1535.37, 5.430210e-06]

        _K_feldspar_ = ['KAlSi3O8', 'R&H95, A&S99', -3745958, -3965730, 232.90, 108.960*J_to_cal,
                        6.934e2, -1.717e-1, 3.462e6, -8.305e3, 4.919e-5]
        self.dbaccessdic['ss_K-feldspar'] = [x/J_to_cal if type(x)!=str else x for x in _K_feldspar_ ]

        _Ferrosilite_ = ['FeSiO3', 'R&H95, Stef2001', -1118000, -1195200, 94.6, 33.0*J_to_cal,
                       1.243e2, 1.454e-2, -3.378e6, 0, 0]
        self.dbaccessdic['ss_Ferrosilite'] = [x/J_to_cal if type(x)!=str else x for x in _Ferrosilite_]

        _Enstatite_=['MgSiO3', 'R&H95, Stef2001', -1458300, -1545600,  66.3, 31.31*J_to_cal,
                     3.507e2, -1.472e-1, 1.769e6, -4.296e3, 5.826e-5]
        self.dbaccessdic['ss_Enstatite'] = [x/J_to_cal if type(x)!=str else x for x in _Enstatite_]

        _Clinoenstatite_=['MgSiO3', 'R&H95, Stef2001', -1458100, -1545000,  67.9, 31.28*J_to_cal,
                     2.056e2, -1.280e-2, 1.193e6, -2.298e3, 0]
        self.dbaccessdic['ss_Clinoenstatite'] = [x/J_to_cal if type(x)!=str else x for x in _Clinoenstatite_]

        _Hedenbergite_=['CaFeSi2O6', 'R&H95, Stef2001', -2676300, -2839900,  174.2, 67.950*J_to_cal,
                     3.1046e2, 1.257e-2, -1.846e6, -2.040e3, 0]
        self.dbaccessdic['ss_Hedenbergite'] = [x/J_to_cal if type(x)!=str else x for x in _Hedenbergite_]

        _Diopside_=['CaMgSi2O6', 'R&H95, Stef2001', -3026800, -3201500,  142.7 , 66.090*J_to_cal,
                     4.7025e2, -9.864e-2, 0.2454e6, -4.823e3, 2.813e-5]
        self.dbaccessdic['ss_Diopside'] = [x/J_to_cal if type(x)!=str else x for x in _Diopside_]

        #dG dH S V a1 a2 a3 a4 a5
        _Forsterite_ = ['Mg2SiO4', 'R&H95, Stef2001', -2053600, -2171850, 94.1, 43.65*J_to_cal,
                      8.736e1, 8.717e-2, -3.699e6, 8.436e2, -2.237e-5]
        self.dbaccessdic['ss_Forsterite'] = [x/J_to_cal if type(x)!=str else x for x in _Forsterite_]

        _Fayalite_ = ['Fe2SiO4', 'R&H95, Stef2001', -1379100, -1478200, 151, 46.31*J_to_cal, 1.7602e2,
                    -8.808e-3, -3.889e6, 0, 2.471e-5]
        self.dbaccessdic['ss_Fayalite'] = [x/J_to_cal if type(x)!=str else x for x in _Fayalite_]

        _Fluorapatite_ = ['Ca5(PO4)3F', 'R&H95', -6489700, -6872000, 387.9, 157.56*J_to_cal,
                      7.543e2, -3.026e-2, -0.9084e6, -6.201e3, 0]
        self.dbaccessdic['Fluorapatite'] = [x/J_to_cal if type(x)!=str else x for x in _Fluorapatite_]

        _Hydroxyapatite_ = ['Ca5(OH)(PO4)3', 'R&H95', -6337100, -6738500, 390.4, 159.6*J_to_cal,
                            3.878e2, 11.186e-2, -12.70e6, 1.811e3, 0]
        self.dbaccessdic['Hydroxyapatite'] = [x/J_to_cal if type(x)!=str else x for x in _Hydroxyapatite_]

        self.dbaccessdic['Ankerite'] = ['CaFe(CO3)2', 'HP2011               31.DEC.11\n', -434945.7, -471178.3,
                                  45.043, 66.060,  81.500956, -0.277486, 0, -730.114720, 0]

        self.dbaccessdic['Acmite'] = ['NaFeSi2O6', 'HP2011               31.DEC.11\n', -577476.5, -617454.6,
                                40.774, 64.590,  1.994e2, 6.197e-2, -4.267e6, 0, 0]

        _Annite_ = ['KFe3AlSi3O10(OH)2', 'R&H95', -4798300, -5149300, 415.0, 154.3*J_to_cal,
                    6.366e2, 8.208e-2, -4.860e6, -3.731e3, 0]
        self.dbaccessdic['ss_Annite'] = [x/J_to_cal if type(x)!=str else x for x in _Annite_]

        _Phlogopite_ = ['KMg3AlSi3O10(OH)2', 'R&H95', -5860500, -6246000, 315.9, 149.65*J_to_cal,
                        8.639e2, -7.6076e-2, 3.5206e5, -8.470e3, 0]
        self.dbaccessdic['ss_Phlogopite'] = [x/J_to_cal if type(x)!=str else x for x in _Phlogopite_]
                                        #dG dH S V a1 a2 a3 a4 a5
        _Molybdenite_ = ['MoS2', 'R&H95', -262800, -271800, 62.6, 32.02*J_to_cal,
                        1.045e2, -4.812e-3, -6.291e3, -6.817e2, 0]
        self.dbaccessdic['Molybdenite'] = [x/J_to_cal if type(x)!=str else x for x in _Molybdenite_]

        _Molybdite_ = ['MoO3', 'R&H95', -668100, -745200, 77.7, 30.56*J_to_cal,
                        6.433e0, 6.278e-2, -2.46e6, 1.337e3, 0]
        self.dbaccessdic['Molybdite'] = [x/J_to_cal if type(x)!=str else x for x in _Molybdite_]

        return

    def readSourceGWBdb(self):
        """
        This function reads source GWB thermodynamic database and reaction coefficients of 'eh'
        and 'e-' has been added at the bottom returns all reaction coefficients and species,
        group species into redox, minerals, gases, oxides and aqueous species
        Parameters
        ----------
            sourcedb      :     filename of the source database
        Returns
        ----------
            sourcedic     :     dictionary of reaction coefficients and species
            specielist    :     list of species segmented into the different categories
                                [element, basis, redox, aqueous, minerals, gases, oxides]
            speciecat     :     list of species categories listed in 'specielist'
            chargedic     :     dictionary of charges of species
            MWdic         :     dictionary of MW of species
            Mineraltype   :     mineral type for minerals
            fugacity_info :     fugacity information as stored in new tdat database for chi and critical ppts
        Usage:
        ----------
        [sourcedic, specielist, chargedic, MWdic, Mineraltype, fugacity_info, activity_model] = readSourceGWBdb()
        """
        codecs = self.sourcedb_codecs
        with open(self.sourcedb_dir, encoding = codecs) as g:
            for line in g:
                if line.startswith('activity model'):
                    break

        with open(self.sourcedb_dir, encoding = codecs) as g:
            Rd = g.readlines()
        activity_model = line.strip('\n').split()[-1]
        data_fmt = [x for x in Rd if 'dataset format' in x][0].strip('\n').split(':')[-1].strip()

        unwanted = ['elements', 'basis species', 'redox couples', 'aqueous species',
                    'free electron', 'minerals', 'gases', 'oxides', 'stop.' ]
        #capture line numbers with line break
        d=[]; previousline = ''
        with open(self.sourcedb_dir, encoding = codecs) as fid:
            for idx, line in enumerate(fid, 1):
                if line.strip().rstrip('\n').lstrip('0123456789.- ') in unwanted:
                    x=idx
                    d.append(x-1)
                #elif line.strip(' \n*').startswith(('virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients', 'Pitzer parameters')):
                elif previousline.startswith('-end-') and line.startswith('*'):
                    x=idx; #print(x)
                    d.append(x+1)
                    break
                previousline = line

        if activity_model == 'h-m-w':
            d_act = [i for i, x in enumerate(Rd[d[-1]:]) if x.strip('\n') ==''][0]
        f = open(self.sourcedb_dir, 'r', encoding = codecs)
        #skip first 11 lines of database  .lstrip('0123456789.- ')
        for i in range(d[1]+2):
          s1 = f.readline()

        self.sourcedic = {} # initialize dictionary
        for i in range(d[-1]-d[1]):   #
            s1 = f.readline()
            if s1.strip(' \n*').startswith(("references", 'virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients', 'Pitzer parameters')) :
                break
            if not s1.startswith((' ', '*'), 0) | (s1.rstrip('\n') == "") | (len(s1) !=0 and s1[0] == "-") :
                if s1.rstrip('\n').lstrip('0123456789.- ') in unwanted:
                    continue
                elif s1.rstrip('\n').lstrip('0123456789.- ') == '':
                    continue
                else:
                    specie_name = s1.strip().split()[0]
                    s2 = f.readline(); s3 = f.readline()
                    s4 = f.readline(); s5 = f.readline();
                    if (s5.rstrip('\n') != ""):
                        s6 = f.readline()
                        if (s6.rstrip('\n') != ""):
                            s7 = f.readline()
                            if not s2.startswith('*',0):
                                if (len(s2.split()) > 1) and (s2.split()[0] != 'formula='):
                                    if len(s1.split('formula=')) <= 1:
                                        specie_formula = ""
                                    else:
                                        specie_formula = s1.rstrip('\n').split('formula=')[1]
                                    if not s3.lstrip().startswith(('chi', 'Pcrit'), 0):
                                        species_num = int(s3.split()[0])
                                        if species_num <= 3:
                                            reactant = s4.split()
                                        elif species_num <= 6:
                                            reactant = s4.split() + s5.split()
                                        else:
                                            reactant = s4.split() + s5.split() + s6.split()
                                    else:
                                        if not s4.lstrip().startswith(('chi','Pcrit'),0):
                                            species_num = int(s4.split()[0])
                                            if species_num <= 3:
                                                reactant = s5.split()
                                            elif species_num <= 6:
                                                reactant = s5.split() + s6.split()
                                            else:
                                                reactant = s5.split() + s6.split() + s7.split()
                                        else:
                                            species_num = int(s5.split()[0])
                                            if species_num <= 3:
                                                reactant = s6.split()
                                            else:
                                                reactant = s6.split() + s7.split()
                                else:
                                    if len(s2.split('formula=')) <= 1:
                                        specie_formula = ""
                                    else:
                                        specie_formula = s2.rstrip('\n').split('formula=')[1]
                                    species_num = int(s4.split()[0])
                                    if species_num <= 3:
                                        reactant = s5.split()
                                    elif species_num <= 6:
                                        reactant = s5.split() + s6.split()
                                    else:
                                        reactant = s5.split() + s6.split() + s7.split()
                            else:
                                specie_formula = s2.split()[2]
                                species_num = int(s4.split()[0])
                                if species_num <= 3:
                                    reactant = s5.split()
                                elif species_num <= 6:
                                    reactant = s5.split() + s6.split()
                                else:
                                    reactant = s5.split() + s6.split() + s7.split()
                        else:
                            specie_formula = ""
                            species_num = int(s3.split()[0])
                            if species_num <= 3:
                                reactant = s4.split()
                            elif species_num <= 6:
                                reactant = s4.split() + s5.split()
                            else:
                                reactant = s4.split() + s5.split() + s6.split()
                    else:
                        specie_formula = ""
                        species_num = int(s3.split()[0])
                        if species_num <= 3:
                            reactant = s4.split()
                        elif species_num <= 6:
                            reactant = s4.split() + s5.split()
                        else:
                            reactant = s4.split() + s5.split() + s6.split()

            self.sourcedic[specie_name] = [specie_formula, species_num] + reactant
        self.sourcedic['eh'] = ['eh', 3, '-2.0000', 'H2O', '1.0000', 'O2(g)', '4.0000', 'H+']
        self.sourcedic['e-'] = ['e-', 3, '0.50000', 'H2O', '-0.2500', 'O2(g)', '-1.0000', 'H+']

        element = []; basis = []; redox = []; aqueous = []; minerals = []; gases = []; oxides = [];
        charge = []; MW = []; electron = []; self.Mineraltype = {}; fugacity_chi = {}; fugacity_Pcrit = {}
        with open(self.sourcedb_dir, encoding = codecs) as fid:
            for i, line in enumerate(fid, 1):
                previousline = line
                if (line.strip(' \n*').startswith(("references", 'Pitzer parameters', 'virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients'))):
                    break
                # elif previousline.startswith('-end-') and line.startswith('*'):
                #     break
                if not line.startswith((' ','*'),0) | (line.rstrip('\n') == "") | (line[0] == "-") :
                    if not line.split()[0].replace('.','',1).isnumeric():
                        if not line.startswith(('charge', 'mole', 'formula'), 0):
                            if data_fmt == 'oct94':
                                if d[0] < i < d[1]:
                                    element.append(line.split()[0])
                                elif d[1] < i < d[2]:
                                    basis.append(line.split()[0])
                                elif d[2] < i < d[3]:
                                    redox.append(line.split()[0])
                                elif d[3] < i < d[4]:
                                    aqueous.append(line.split()[0])
                                elif d[4] < i < d[5]:
                                    minerals.append(line.split()[0])
                                elif d[5] < i < d[6]:
                                    gases.append(line.split()[0])
                                elif i > d[6]:
                                    oxides.append(line.split()[0])
                            elif data_fmt == 'apr20':
                                if d[0] < i < d[1]:
                                    element.append(line.split()[0])
                                elif d[1] < i < d[2]:
                                    basis.append(line.split()[0])
                                elif d[2] < i < d[3]:
                                    redox.append(line.split()[0])
                                elif d[3] < i < d[4]:
                                    aqueous.append(line.split()[0])
                                elif d[4] < i < d[5]:
                                    electron.append(line.split()[0])
                                elif d[5] < i < d[6]:
                                    minerals.append(line.split()[0])
                                elif d[6] < i < d[7]:
                                    gases.append(line.split()[0])
                                elif i > d[7]:
                                    oxides.append(line.split()[0])
                if (re.compile(r"charge").search(line) != None) and not line.startswith('*'):
                    charge.append(line)
                if (re.compile(r"mole wt.=").search(line) != None) and not line.startswith('*'):
                    MW.append(re.sub('[^0123456789\.]', '', line.strip('\n').split('wt.=')[1]))
                if (re.compile(r"type=").search(line) != None) and not line.startswith('*'):
                    if len(line.split()) <= 2:
                        self.Mineraltype[line.split()[0]] = ''
                    else:
                        self.Mineraltype[line.split()[0]] = line.split()[2]
                if (re.compile(r"chi=").search(line) != None) and not line.startswith('*'):
                    fugacity_chi[gases[-1]] = line
                if (re.compile(r"Pcrit=").search(line) != None) and not line.startswith('*'):
                    fugacity_Pcrit[gases[-1]] = line

        act_list = []; #previousline = ''
        if activity_model == 'h-m-w':
            with open(self.sourcedb_dir, encoding = codecs) as fid:
                for i, line in enumerate(fid, 1):
                    if i > d[-1] + d_act:
                        if not line.startswith(('  ', '\n', '-end-', '*')):
                            act_list.append(line)

        self.act_param = {'activity_model': activity_model, 'act_list': act_list, 'dataset_format' : data_fmt}
        self.fugacity_info = {'fugacity_chi': fugacity_chi,'fugacity_Pcrit': fugacity_Pcrit}
        res = basis + redox + aqueous + electron
        self.chargedic = {res[i]: charge[i].rstrip('\n') for i in range(len(charge))}
        res = element + basis + redox + aqueous + electron + minerals + gases + oxides
        self.MWdic = {res[i]: float(MW[i]) for i in range(len(MW))}
        self.specielist = [element, basis, redox, aqueous, electron, minerals, gases, oxides]
        self.speciecat = ['element', 'basis', 'redox', 'aqueous', 'electron', 'minerals', 'gases', 'oxides']
        fid.close()

        return

    def readSourceEQ36db(self):
        """
        This function reads source EQ3/6 thermodynamic database and reaction coefficients of 'eh'
        and 'e-' has been added at the bottom returns all reaction coefficients and species,
        group species into basis, auxiliary basis, minerals, gases, liquids and aqueous species
        Parameters
        ----------
            sourcedb      :     filename of the source database
        Returns
        ----------
            sourcedic     :     dictionary of reaction coefficients and species
            specielist    :     list of species segmented into the different categories
                                [element, basis, redox, aqueous, minerals, gases, oxides]
            speciecat     :     list of species categories listed in 'specielist'
            chargedic     :     dictionary of charges of species and DHazero info
            MWdic         :     dictionary of MW of species
            Sptype        :     specie types and eq3/6 and revised date info
            Elemlist      :     dictionary of elements and coefficients
        Usage:
        ----------
        [sourcedic, specielist, chargedic, MWdic, block_info, Elemlist, act_param] = readSourceEQ36db(sourcedb)
        """
        codecs = self.sourcedb_codecs
        with open(self.sourcedb_dir, encoding = codecs) as g:
            for line in g:
                if line.startswith(('bdot parameters', 'single-salt parameters', 'ca combinations')):
                    break

        if line.startswith('bdot parameters'):
            activity_model = 'debye-huckel'
        elif line.startswith(('single-salt parameters', 'ca combinations')):
            activity_model = 'h-m-w'

        subheading = ['elements', 'basis species', 'auxiliary basis species', 'aqueous species',
                    'solids', 'liquids', 'gases', 'solid solutions', 'references', 'stop.']
        d = []
        with open(self.sourcedb_dir, encoding = codecs) as f:
            for idx, line in enumerate(f, 1):
                if line.strip().rstrip('\n').lstrip('0123456789.- ') in subheading:
                    x=idx
                    d.append(x-1)
                if line.startswith(('bdot parameters', 'single-salt parameters', 'ca combinations')):
                    x=idx
                    d.append(x-1)

        element = []; basis = []; auxiliary = []; aqueous = []; minerals = []; MW = []; #DH = []
        gases = []; liquids = []; charge = []; solid_solutions = []; act_params = []

        with open(self.sourcedb_dir, encoding = codecs) as f:
            for i, line in enumerate(f, 1):
                if (line.rstrip('\n') == "references"):
                    break
                if not line.startswith('*',0) | line.startswith(' ',0) | (line.rstrip('\n') == "") | (line[0] == "-") :
                    if not line.split()[0].replace('.','',1).isnumeric() and not line.startswith('+',0):
                        if line.strip().rstrip('\n').lstrip('0123456789.- ') not in subheading:
                            line = line.strip().rstrip('\n')
                            if d[1] < i < d[2]:
                                element.append(line.split()[0])
                                MW.append(float(line.split()[1]))
                            elif d[2] < i < d[3]:
                                basis.append(line.split('  ')[0])
                            elif d[3] < i < d[4]:
                                if any(re.findall(r'|'.join(('acid', 'high', 'low')), line.split('  ')[0], re.IGNORECASE)):
                                    auxiliary.append(line.split('  ')[0].replace(' ', '_'))
                                else:
                                    auxiliary.append(line.split('  ')[0])
                            elif d[4] < i < d[5]:
                                if any(re.findall(r'|'.join(('acid', 'high', 'low')), line.split('  ')[0], re.IGNORECASE)):
                                    aqueous.append(line.split('  ')[0].replace(' ', '_'))
                                else:
                                    aqueous.append(line.split('  ')[0])
                            elif d[5] < i < d[6]:
                                if any(re.findall(r'|'.join(('acid', 'high', 'low', 'anhyd', 'hydr')), line.split('  ')[0], re.IGNORECASE)):
                                    minerals.append(line.split('  ')[0].replace(' ', '_'))
                                else:
                                    minerals.append(line.split('  ')[0])
                            elif d[6] < i < d[7]:
                                liquids.append(line.split('  ')[0])
                            elif d[7] < i < d[8]:
                                gases.append(line.split('  ')[0])
                            elif i > d[8]:
                                solid_solutions.append(line.split('  ')[0])
                if re.compile(r"charge").search(line) != None:
                    charge.append(line)
                if d[0] < i < d[1]:
                    act_params.append(line)

        self.MWdic = {element[i]: float(MW[i]) for i in range(len(MW))}
        res = basis + auxiliary + aqueous + minerals + liquids + gases + solid_solutions
        lstname = []; self.block_info = {}; self.Elemlist = {}; self.sourcedic = {}
        self.act_param = {'activity_model': activity_model, 'act_list': None, 'alpha_beta' : {},
                          'theta':{}, 'lambda':{}, 'psi':{},'zeta':{},'mu':{}, 'beta0' : {},
                          'beta1' : {}, 'beta2' : {}, 'alpha1' : {}, 'alpha2' : {}, 'cphi' : {}}
        keywords = [["+" + "-"*30,   "+" + "-"*30]  ]
        for num, k in enumerate(keywords):
            lst = []; counter = 0
            f = open(self.sourcedb_dir, 'r', encoding = codecs)

            for i in range(d[1] + len(element)):#
                s1 = f.readline()
                if (s1.rstrip('\n') == "elements") :
                    break
                act_list = [act_params[i +1] for i,x in enumerate(act_params) if x.rstrip('\n').startswith(k[0])]
                act_list = [x for x in act_list if not x.startswith(('*', 'nn', 'nc', 'cc', 'mixture'))]
                if (activity_model == 'h-m-w') and any(s1.lstrip().rstrip('\n').startswith(x) for x in act_list):
                    lst = []; lst.append(s1)
                    for j in range(50):
                        s = f.readline()
                        if s.lstrip().rstrip('\n').startswith(k[1]):
                            break
                        elif not s.lstrip().startswith(('****', '*',  'single-salt parameters', 'ca combinations')) | (s.rstrip('\n').strip('0123456789.- ') in ["", 'Miscellaneous parameters']+subheading):
                            lst.append(s)
                    if len(lst) > 2:
                        if any(['mu' in x for x in lst]):
                            checker = [x.strip(' \n').split()[-1] for i, x in enumerate(lst) if x.lstrip().startswith('mu')]
                            if re.sub('[^0123456789\.]', '', checker[0]) == '':
                                first_a = [i for i, x in enumerate(lst) if x.lstrip().startswith('a')][0]
                                mu = float(lst[first_a].split()[-1])
                            else:
                                mu = float(re.sub('[^0123456789\.]', '', checker[0]))
                            self.act_param['mu'][lst[0].rstrip('\n')] = mu
                        if any(['zeta' in x for x in lst]):
                            checker = [x.strip(' \n').split()[-1] for i, x in enumerate(lst) if x.lstrip().startswith('zeta')]
                            if re.sub('[^0123456789\.]', '', checker[0]) == '':
                                first_a = [i for i, x in enumerate(lst) if x.lstrip().startswith('a')][0]
                                zeta = float(lst[first_a].split()[-1])
                            else:
                                zeta = float(re.sub('[^0123456789\.]', '', checker[0]))
                            self.act_param['zeta'][lst[0].rstrip('\n')] = zeta
                        if any([('alpha' or 'beta') in x for x in lst]):
                            self.act_param['alpha_beta'][lst[0].rstrip('\n')] = lst
                            lster = ['beta0', 'beta1', 'beta2', 'alpha1', 'alpha2', 'cphi']
                            for pos in lster:
                                checker = [x.strip(' \n') for i, x in enumerate(lst) if pos in re.sub('[()]', '', x).lstrip().lower()]
                                if all([x in checker[0] for x in lster[:3]]):
                                    checker = checker[0].replace("=", "").split()
                                    par = float(checker[checker.index(pos) + 1])
                                elif all([x in checker[0] for x in lster[3:5]]):
                                    checker = checker[0].replace("=", "").split()
                                    par = float(checker[checker.index(pos) + 1])
                                else:
                                    # checker = checker.split()[-1]
                                    if re.sub('[^0123456789\.]', '', re.sub('[(012)]', '', checker[0])) == '':
                                        first_a = [i for i, x in enumerate(lst) if pos in re.sub('[()]', '', x).lstrip().lower() ][0] + 1
                                        par = float(lst[first_a].split()[-1])
                                    else:
                                        par = float(re.sub('[^0123456789\.]', '', re.sub('[()]', '', checker[0])))
                                self.act_param[pos][lst[0].rstrip('\n')] = par
                        if any(['psi' in x for x in lst]):
                            checker = [x.strip(' \n') for i, x in enumerate(lst) if 'psi' in x.lstrip() ]
                            if all([x in checker[0] for x in [' psi', 'theta']]):
                                checker = checker[0].replace("=", "").split()
                                psi = float(checker[checker.index('psi') + 1])
                            else:
                                if re.sub('[^0123456789\.]', '', checker[0]) == '':
                                    first_a = [i for i, x in enumerate(lst) if x.lstrip().startswith('a')][0]
                                    psi = float(lst[first_a].split()[-1])
                                else:
                                    psi = float(re.sub('[^0123456789\.]', '', checker[0]))
                            self.act_param['psi'][lst[0].rstrip('\n')] = psi
                        if any(['theta' in x for x in lst]):
                            checker = [x.strip(' \n') for i, x in enumerate(lst) if 'theta' in x.lstrip() ]
                            if all([x in checker[0] for x in ['theta', ' psi']]):
                                checker = checker[0].replace("=", "").split()
                                theta = float(checker[checker.index('theta') + 1])
                            else:
                                if re.sub('[^0123456789\.]', '', checker[0]) == '':
                                    first_a = [i for i, x in enumerate(lst) if x.lstrip().startswith('a')][0]
                                    theta = float(lst[first_a].split()[-1])
                                else:
                                    theta = float(re.sub('[^0123456789\.]', '', checker[0]))
                            self.act_param['theta'][lst[0].rstrip('\n')] = theta
                        if any(['lambda' in x for x in lst]):
                            checker = [x.strip(' \n').split()[-1] for i, x in enumerate(lst) if 'lambda' in x.lstrip()]
                            if re.sub('[^0123456789\.]', '', checker[0]) == '':
                                first_a = [i for i, x in enumerate(lst) if x.lstrip().startswith('a')][0]
                                lambdaa = float(lst[first_a].split()[-1])
                            else:
                                lambdaa = float(re.sub('[^0123456789\.]', '', checker[0]))
                            self.act_param['lambda'][lst[0].rstrip('\n')] = lambdaa

            for i in range(d[-1]) :  #
                s = f.readline()
                if (s.rstrip('\n') == "references") :
                    break
                s = s.replace(" acid", "_acid").replace(" high", "_high").replace(" low", "_low").replace(" anhyd", "_anhyd").replace(" hydr", "_hydr")

                if any(s.lstrip().rstrip('\n').startswith(x) for x in res):
                    lst = []; lst.append(s); counter += 1
                    for j in range(50):
                        s = f.readline()
                        if s.lstrip().rstrip('\n').startswith(k[1]):
                            break
                        elif not s.lstrip().startswith('****'):
                            lst.append(s)
                    lst[0] = lst[0].rstrip('\n')
                    if lst[0] not in subheading:
                        if lst[0].split('  ')[0] in res or lst[0].split()[0].replace(' ', '_') in res:
                            if any(re.findall(r'|'.join(('acid', 'high', 'low', 'anhyd', 'hydr')), lst[0].split('  ')[0], re.IGNORECASE)):
                                specie_name = lst[0].split('  ')[0].replace(' ', '_')
                            else:
                                specie_name = lst[0].split('  ')[0]
                            lstname.append(specie_name)
                            if specie_name not in solid_solutions:
                                indx, elem_numb =[(i,int(re.sub('[^0123456789\.]', '', x))) for i,x in enumerate(lst)
                                                  if x.strip('0123456789.,-: ').startswith('element(s)')][0]
                                elem_rows = list(range(indx + 1, indx + 2)) if elem_numb <= 3 else list(range(indx + 1, indx + 3)) if elem_numb <= 6 else list(range(indx + 1, indx + 4)) if elem_numb <= 9 else list(range(indx + 1, indx + 5))
                                reactant = [lst[x].rstrip('\n').split('  ') for x in elem_rows]
                                reactant = [item for sublist in reactant for item in sublist] # convert list of list to list
                                reactant = [y for x in reactant for y in x.split() if x != '' and x != '****']
                                self.Elemlist[specie_name] = reactant
                            else:
                                elem_rows = [20]
                            if specie_name not in basis[:-1] + solid_solutions and counter > len(basis):
                                indx, species_num =[(i,int(re.sub('[^0123456789\.]', '', x))) for i,x in enumerate(lst)
                                                    if x.strip('0123456789.,-: ').startswith('species in')][0]
                                spec_rows = list(range(indx + 1, indx + 2)) if species_num < 3 else list(range(indx + 1, indx + 3)) if species_num < 5 else list(range(indx + 1, indx + 4)) if species_num < 7 else list(range(indx + 1, indx + 5)) if species_num < 9 else  list(range(indx + 1, indx + 6))
                                reactants = [lst[x].rstrip('\n').split('  ') for x in spec_rows]
                                reactants = [item for sublist in reactants for item in sublist] # convert list of list to list
                                reactants = [y for x in reactants for y in x.split() if x != '' and x != '****']
                                reactants = [j.replace(' ', '_') if any(re.findall(r'|'.join(('acid', 'high', 'low', 'anhyd', 'hydr')),
                                                                                    j, re.IGNORECASE)) else j for j in reactants]
                            else:
                                spec_rows = [20]
                            if specie_name in solid_solutions:
                                indx, species_num =[(i,int(re.sub('[^0123456789\.]', '', x))) for i,x in enumerate(lst)
                                                    if x.strip('0123456789.,-: ').startswith('components')][0]
                                spec_rows = list(range(indx + 1, indx + 2)) if species_num < 3 else list(range(indx + 1, indx + 3)) if species_num < 5 else list(range(indx + 1, indx + 4)) if species_num < 7 else list(range(indx + 1, indx + 5)) if species_num < 9 else  list(range(indx + 1, indx + 6))
                                reactants = [lst[x].rstrip('\n').split('  ') for x in spec_rows]
                                reactants = [item for sublist in reactants for item in sublist] # convert list of list to list
                                reactants = [y for x in reactants for y in x.split() if x != '' and x != '****']
                            mw = [x for x in lst if x.strip('*    ').startswith('mol.wt.')]
                            mw = float(re.sub('[^0123456789\.]', '', mw[0].split()[-2])) if len(mw) != 0 else []
                            if len(lst[0].split()) <= 1:
                                specie_formula = ""
                            elif len(lst[0].split()) > 2:
                                specie_formula = lst[0].split()[2]
                            else:
                                specie_formula = lst[0].split()[1]
                            if (specie_name == 'O2(g)') and counter <= len(basis):
                                self.block_info['%s_b' % specie_name] = lst[1:min(elem_rows,spec_rows)[0] - 1]
                            elif specie_name in basis[:-1] + auxiliary + aqueous + minerals + liquids + gases:
                                self.block_info[specie_name] = lst[1:min(elem_rows,spec_rows)[0] - 1]
                            elif specie_name in solid_solutions:
                                self.block_info[specie_name] = [lst[1:min(spec_rows) - 1], lst[(max(spec_rows) + 1):]]
                            if specie_name in basis and counter <= len(basis):
                                self.sourcedic[specie_name] = [specie_formula, elem_numb] + reactant
                            elif specie_name == 'O2(g)':
                                self.sourcedic[specie_name] = [specie_formula, species_num] + reactants
                            else:
                                self.sourcedic[specie_name] = [specie_formula, species_num] + reactants
                            self.MWdic[specie_name] = mw

        self.sourcedic['eh'] = ['eh', 4, '-1.0000', 'eh', '-2.0000', 'H2O', '1.0000', 'O2(g)', '4.0000', 'H+']
        self.sourcedic['e-'] = ['e-', 4, '-1.0000', 'e-', '0.50000', 'H2O', '-0.2500', 'O2(g)', '-1.0000', 'H+']
        self.specielist = [element, basis, auxiliary, aqueous, minerals, liquids, gases, solid_solutions]
        self.speciecat = ['element', 'basis', 'redox', 'aqueous', 'minerals', 'liquids', 'gases', 'solid_solutions']
        res = basis + auxiliary + aqueous
        self.chargedic = {res[i]: charge[i].rstrip('\n') for i in range(len(charge))}
        self.act_param['act_list'] = act_list if activity_model == 'h-m-w' else ''
        self.act_param['activity_model'] = activity_model

        f.close()
        return

