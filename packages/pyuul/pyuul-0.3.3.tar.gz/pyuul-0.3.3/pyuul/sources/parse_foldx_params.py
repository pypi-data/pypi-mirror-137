#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2021 Gabriele Orlando
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os,string
import numpy as np
letters={'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K', 'ASN': 'N', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ALA': 'A', 'HIS': 'H', 'GLY': 'G', 'ILE': 'I', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'} #gli aminoacidi, che male qui non fanno
hashing_hybrid = {"NO_HYBRID":0,"SP2_N_H1":1,"SP2_N_H2":2,"SP2_N_ORB1":3,"SP2_N_ORB2":4,"SP3_N_H3":5,"SP3_O_H1ORB2":6,"SP2_O_ORB2":7}
def read_h_positions(fil="parameters/hbond_coords_params.txt"): ### ADD BACKBONE PARTNERS MANUALLY!!! ###
	diz={}
	hlabel_addition=string.ascii_lowercase
	for i in open(fil).readlines():
		l=i.split("\t")
		
		if not l[0] in letters and l[0]!="ooo":
			continue
			
		aa=l[0]
		if l[6]=="_" or l[6][0]!="H":
			continue
			
		if not aa in diz:
			diz[aa]={}
			
		if not l[1] in diz[aa]:
			diz[aa][l[1]]={}
			
		if l[6] in diz[aa][l[1]]:
			#continue
			
			nameH = l[6]+hlabel_addition[0]
			cont=1
			while nameH in diz[aa][l[1]]:
				nameH = l[6]+hlabel_addition[cont]
				cont+=1
			l[6]=nameH
				
		diz[aa][l[1]][l[6]]=(float(l[7]),float(l[8]),float(l[9]))
	
	for aa in letters.keys():
	
		if aa!="PRO":
			diz[aa]["N"]={}
			diz[aa]["N"]["HN"] = diz["ooo"]["N"]["HN"]
	#print(diz["LYS"]["N"].keys())
	#ads
	del diz["ooo"]

			
		
	return diz


def read_hbond_params(fil="parameters/hbond_params.txt"):
	header=[]
	fin={}
	for l in open(fil,"r").readlines():
		if l[0]=="#":
			header+=[l.strip().replace("#","")]
		elif l.strip()=="":
			continue
		else:
			a=l.strip().replace('"',"").replace(' ',"").replace('\t',"").strip(",").split(",")
			#print(a,len(header))
			assert len(a)==len(header)
			diz={}
			for k in range(len(a)):
				if header[k]=="aa":
					aa_ind = k

				elif header[k]=="atom":
					at_ind = k

				elif header[k]!="hybridation":
					try:
						diz[header[k]]=float(a[k])
					except:
						diz[header[k]]=a[k]
				else:
					diz[header[k]]=hashing_hybrid[a[k]]
					
			
			if not a[0] in fin:
				fin[a[aa_ind]]={}
			
			fin[a[aa_ind]][a[at_ind]]=diz
		
	return fin
	
def read_hbond_partners(fil="parameters/hbond_coords_params.txt"): 
	diz={}
	for i in open(fil).readlines():
		l=i.split("\t")
		
		if not l[0] in letters:
			continue
			
		aa=l[0]
		if l[6]=="_":
			continue
			
		if not aa in diz:
			diz[aa]={}

		diz[aa][l[1]]=[[l[2],0],[l[4],0]]
		
		#### backbone manually ####

	for aa in letters.keys():

		if aa!="PRO":
			diz[aa]["N"] = [["C",-1],["O",-1]]
		diz[aa]["C"] = [["CA",0],["N",0]]
		diz[aa]["O"] = [["C",0],["CA",0]]

		#### virtual manually ####


	diz["ARG"]["ARG"] = [["NE",0],["NH1",0]]
	diz["PHE"]["R_C"] = [["CD1", 0], ["CG", 0]]
	diz["TYR"]["R_C"] = [["CD1", 0], ["CG", 0]]

	return diz
	
def read_FO_positions(fil="parameters/hbond_coords_params.txt"): 
	diz={}
	hlabel_addition=string.ascii_lowercase
	for i in open(fil).readlines():
		l=i.split("\t")
		
		if not (l[0] in letters or l[0]=="ooo"):
			continue
			
		aa=l[0]
		if len(l[6])<2 or l[6][:2]!="FO":
			continue
			
		if not aa in diz:
			diz[aa]={}
			
		if not l[1] in diz[aa]:
			diz[aa][l[1]]={}
		l[6]=l[6].replace("FO","X")	# names are too long for pdb
		if l[6] in diz[aa][l[1]]:
			#continue
			
			nameFO = l[6]+hlabel_addition[0]
			cont=1
			while nameFO in diz[aa][l[1]]:
				nameFO = l[6]+hlabel_addition[cont]
				cont+=1
			l[6]=nameFO
				
		diz[aa][l[1]][l[6]]=(float(l[7]),float(l[8]),float(l[9]))
	
	for aa in letters.keys():
		if not aa in diz:
			diz[aa]={}
		
		diz[aa]["O"]={}
		diz[aa]["O"]["X1"] = diz["ooo"]["O"]["X1"]
		diz[aa]["O"]["X2"] = diz["ooo"]["O"]["X2"]
	

	del diz["ooo"]

	return diz

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
