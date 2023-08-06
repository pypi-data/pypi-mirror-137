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

import os,torch
import numpy as np
from pyuul.sources.globalVariables import *
from pyuul.sources import  hashings
def parseSDF(SDFFile):
	"""
	function to parse pdb files. It can be used to parse a single file or all the pdb files in a folder. In case a folder is given, the coordinates are gonna be padded

	Parameters
	----------
	SDFFile : str
		path of the PDB file or of the folder containing multiple PDB files

	Returns
	-------
	coords : torch.Tensor
		coordinates of the atoms in the pdb file(s). Shape ( batch, numberOfAtoms, 3)

	atomNames : list
		a list of the atom identifier. It encodes atom type, residue type, residue position and chain

	"""
	if not os.path.isdir(SDFFile):
		fil = SDFFile
		totcoords=[]
		totaname=[]
		coords = []
		atomNames = []
		for line in open(fil).readlines():
			a=line.strip().split()
			if len(a)==16: ## atom
				element = a[3]
				x = float(a[0])
				y = float(a[1])
				z = float(a[2])
				coords += [[x,y,z]]
				#aname = line[17:20].strip()+"_"+str(resnum)+"_"+line[12:16].strip()+"_"+line[21]
				aname = "MOL"+"_"+"0"+"_"+element+"_"+"A"

				atomNames += [aname]
			elif "$$$$" in line:
				totcoords+=[torch.tensor(coords)]
				totaname += [atomNames]
				coords=[]
				atomNames=[]
		return torch.torch.nn.utils.rnn.pad_sequence(totcoords, batch_first=True, padding_value=PADDING_INDEX),totaname
	else:
		totcoords = []
		totaname = []
		for fil in sorted(os.listdir(SDFFile)):
			coords = []
			atomNames = []
			for line in open(SDFFile+fil).readlines():
				a = line.strip().split()
				if len(a) == 16:  ## atom
					element = a[3]
					x = float(a[0])
					y = float(a[1])
					z = float(a[2])
					coords += [[x, y, z]]
					aname = "MOL"+"_"+"0"+"_"+element+"_"+"A"

					atomNames += [aname]
				elif "$$$$" in line:
					totcoords += [torch.tensor(coords)]
					totaname += [atomNames]
					coords = []
					atomNames = []
		return torch.torch.nn.utils.rnn.pad_sequence(totcoords, batch_first=True, padding_value=PADDING_INDEX),totaname


def parsePDB(PDBFile,keep_only_chains=None,keep_hetatm=True,bb_only=False):

	"""
	function to parse pdb files. It can be used to parse a single file or all the pdb files in a folder. In case a folder is given, the coordinates are gonna be padded

	Parameters
	----------
	PDBFile : str
		path of the PDB file or of the folder containing multiple PDB files
	bb_only : bool
		if True ignores all the atoms but backbone N, C and CA
	keep_only_chains : str or None
		ignores all the chain but the one given. If None it keeps all chains
	keep_hetatm : bool
		if False it ignores heteroatoms
	Returns
	-------
	coords : torch.Tensor
		coordinates of the atoms in the pdb file(s). Shape ( batch, numberOfAtoms, 3)

	atomNames : list
		a list of the atom identifier. It encodes atom type, residue type, residue position and chain

	"""

	bbatoms = ["N", "CA", "C"]
	if not os.path.isdir(PDBFile):
		fil = PDBFile
		coords = []
		atomNames = []
		cont = -1
		oldres=-999
		for line in open(fil).readlines():


			if line[:4] == "ATOM":
				if keep_only_chains is not None and (not line[21] in keep_only_chains):
					continue
				if bb_only and not line[12:16].strip() in bbatoms:
						continue
				if oldres != int(line[22:26]):
					cont+=1
					oldres=int(line[22:26])
				resnum = int(line[22:26])
				atomNames += [line[17:20].strip()+"_"+str(resnum)+"_"+line[12:16].strip()+"_"+line[21]]

				x = float(line[30:38])
				y = float(line[38:46])
				z = float(line[47:54])
				coords+=[[x,y,z]]

			elif line[:6] == "HETATM" and keep_hetatm:

				resname_het = line[17:20].strip()
				resnum = int(line[22:26])
				x = float(line[30:38])
				y = float(line[38:46])
				z = float(line[47:54])
				coords += [[x, y, z]]
				atnameHet = line[12:16].strip()
				atomNames += [resname_het+"_"+str(resnum)+"_"+atnameHet+"_"+line[21]]
		return torch.tensor(coords).unsqueeze(0), [atomNames]
	else:
		coords = []
		atomNames = []

		for fil in sorted(os.listdir(PDBFile)):

			atomNamesTMP = []
			coordsTMP = []
			cont = -1
			oldres=-999
			for line in open(PDBFile+"/"+fil).readlines():

				if line[:4] == "ATOM":
					if keep_only_chains is not None and (not line[21] in keep_only_chains):
						continue
					if bb_only and not line[12:16].strip() in bbatoms:
						continue
					if oldres != int(line[22:26]):
						cont += 1
						oldres = int(line[22:26])

					resnum = int(line[22:26])
					atomNamesTMP += [line[17:20].strip()+"_"+str(resnum)+"_"+line[12:16].strip()+"_"+line[21]]

					x = float(line[30:38])
					y = float(line[38:46])
					z = float(line[47:54])
					coordsTMP+=[[x,y,z]]

				elif line[:6] == "HETATM" and keep_hetatm:
					if line[17:20].strip()!="GTP":
						continue
					x = float(line[30:38])
					y = float(line[38:46])
					z = float(line[47:54])
					resnum = int(line[22:26])
					coordsTMP += [[x, y, z]]
					atnameHet = line[12:16].strip()
					atomNamesTMP += ["HET_"+str(resnum)+"_"+atnameHet+"_"+line[21]]
			coords+=[torch.tensor(coordsTMP)]
			atomNames += [atomNamesTMP]

		return torch.torch.nn.utils.rnn.pad_sequence(coords, batch_first=True, padding_value=PADDING_INDEX),atomNames


def atomlistToChannels(atomNames, hashing="Element_Hashing", device="cpu"):
	"""
	function to get channels from atom names (obtained parsing the pdb files with the parsePDB function)

	Parameters
	----------
	atomNames : list
		atom names obtained parsing the pdb files with the parsePDB function

	hashing : "TPL_Hashing" or "Element_Hashing" or dict
		define which atoms are grouped together. You can use two default hashings or build your own hashing:

		TPL_Hashing: uses the hashing of torch protein library (https://github.com/lupoglaz/TorchProteinLibrary)
		Element_Hashing: groups atoms in accordnce with the element only: C -> 0, N -> 1, O ->2, P ->3, S- >4, H ->5, everything else ->6

		Alternatively, if you are not happy with the default hashings, you can build a dictionary of dictionaries that defines the channel of every atom type in the pdb.
		the first dictionary has the residue tag (three letters amino acid code) as key (3 letters compound name for hetero atoms, as written in the PDB file)
		every residue key is associated to a dictionary, which the atom tags (as written in the PDB files) as keys and the channel (int) as value

		for example, you can define the channels just based on the atom element as following:
		{
		'CYS': {'N': 1, 'O': 2, 'C': 0, 'SG': 3, 'CB': 0, 'CA': 0}, # channels for cysteine atoms
		'GLY': {'N': 1, 'O': 2, 'C': 0, 'CA': 0}, # channels for glycine atom
		...
		'GOL': {'O1':2,'O2':2,'O3':2,'C1':0,'C2':0,'C3':0}, # channels for glycerol atom
		...
		}

		The default encoding is the one that assigns a different channel to each element

		other encodings can be found in sources/hashings.py

	device : torch.device
			The device on which the model should run. E.g. torch.device("cuda") or torch.device("cpu:0")
	Returns
	-------
	coords : torch.Tensor
		coordinates of the atoms in the pdb file(s). Shape ( batch, numberOfAtoms, 3)

	channels : torch.tensor
		the channel of every atom. Shape (batch,numberOfAtoms)

	"""
	if hashing == "TPL_Hashing":
		hashing = hashings.TPLatom_hash

	elif hashing == "Element_Hashing":
		hashing = hashings.elements_hash
	else:
		assert type(hashing) is dict

	if type(hashing[list(hashing.keys())[0]]) == dict:
		useResName = True
	else:
		useResName = False
		assert type(hashing[list(hashing.keys())[0]]) == int
	channels = []
	for singleAtomList in atomNames:
		haTMP = []
		for i in singleAtomList:
			resname = i.split("_")[0]
			atName = i.split("_")[2]
			# if resname=="HET":
			#	atName="HET"
			if useResName:
				if resname in hashing and atName in hashing[resname]:
					haTMP += [hashing[resname][atName]]
				else:
					haTMP += [PADDING_INDEX]
					print("missing ", resname, atName)
			else:
				if atName in hashing:
					haTMP += [hashing[atName]]
				elif atName[0] in hashing:
					haTMP += [hashing[atName[0]]]
				elif hashing == "Element_Hashing":
					haTMP += [6]
				else:
					haTMP += [PADDING_INDEX]
					print("missing ", resname, atName)

		channels += [torch.tensor(haTMP, dtype=torch.float, device=device)]
	channels = torch.torch.nn.utils.rnn.pad_sequence(channels, batch_first=True, padding_value=PADDING_INDEX)
	return channels


def atomlistToRadius(atomList, hashing="FoldX_radius", device="cpu"):
	"""
	function to get radius from atom names (obtained parsing the pdb files with the parsePDB function)



	Parameters
	----------
	atomNames : list
		atom names obtained parsing the pdb files with the parsePDB function
	hashing : FoldX_radius or dict
		"FoldX_radius" provides the radius used by the FoldX force field

		Alternatively, if you are not happy with the foldX radius, you can build a dictionary of dictionaries that defines the radius of every atom type in the pdb.
		The first dictionary has the residue tag (three letters amino acid code) as key (3 letters compound name for hetero atoms, as written in the PDB file)
		every residue key is associated to a dictionary, which the atom tags (as written in the PDB files) as keys and the radius (float) as value

		for example, you can define the radius as following:
		{
		'CYS': {'N': 1.45, 'O': 1.37, 'C': 1.7, 'SG': 1.7, 'CB': 1.7, 'CA': 1.7}, # radius for cysteine atoms
		'GLY': {'N': 1.45, 'O': 1.37, 'C': 1.7, 'CA': 1.7}, # radius for glycine atoms
		...
		'GOL': {'O1':1.37,'O2':1.37,'O3':1.37,'C1':1.7,'C2':1.7,'C3':1.7}, # radius for glycerol atoms
		...
		}

		The default radius are the ones defined in FoldX

		Radius default dictionary can be found in sources/hashings.py

	device : torch.device
			The device on which the model should run. E.g. torch.device("cuda") or torch.device("cpu:0")
	Returns
	-------
	coords : torch.Tensor
		coordinates of the atoms in the pdb file(s). Shape ( batch, numberOfAtoms, 3)

	radius : torch.tensor
		The radius of every atom. Shape (batch,numberOfAtoms)

	"""
	if hashing == "FoldX_radius":
		hashing = hashings.radius
		hahsingSomgleAtom = hashings.radiusSingleAtom
	else:
		assert type(hashing) is dict

	radius = []
	for singleAtomList in atomList:
		haTMP = []
		for i in singleAtomList:
			resname = i.split("_")[0]
			atName = i.split("_")[2]
			if resname in hashing and atName in hashing[resname]:
				haTMP += [hashing[resname][atName]]
			elif atName[0] in hahsingSomgleAtom:
				haTMP += [hahsingSomgleAtom[atName[0]]]
			else:
				haTMP += [1.0]
				print("missing ", resname, atName)
		radius += [torch.tensor(haTMP, dtype=torch.float, device=device)]
	radius = torch.torch.nn.utils.rnn.pad_sequence(radius, batch_first=True, padding_value=PADDING_INDEX)
	return radius


'''
def write_pdb(batchedCoords, atomNames , name=None, output_folder="outpdb/"): #I need to add the chain id

	if name is None:
		name = range(len(batchedCoords))

	for struct in range(len(name)):
		f = open(output_folder + str(name[struct]) + ".pdb", "w")

		coords=batchedCoords[struct].data.numpy()
		atname=atomNames[struct]
		for i in range(len(coords)):

			rnName = atname[i].split("_")[0]#hashings.resi_hash_inverse[resi_list[i]]
			atName = atname[i].split("_")[2]#hashings.atom_hash_inverse[resi_list[i]][atom_list[i]]
			pos = atname[i].split("_")[1]
			chain = "A"

			num = " " * (5 - len(str(i))) + str(i)
			a_name = atName + " " * (4 - len(atName))
			numres = " " * (4 - len(str(pos))) + str(pos)

			x = round(float(coords[i][0]), 3)
			sx = str(x)
			while len(sx.split(".")[1]) < 3:
				sx += "0"
			x = " " * (8 - len(sx)) + sx

			y = round(float(coords[i][1]), 3)
			sy = str(y)
			while len(sy.split(".")[1]) < 3:
				sy += "0"
			y = " " * (8 - len(sy)) + sy

			z = round(float(coords[i][2]), 3)
			sz = str(z)
			while len(sz.split(".")[1]) < 3:
				sz += "0"
			z = " " * (8 - len(sz)) + sz
			chain = " " * (2 - len(chain)) + chain

			if rnName !="HET":
				f.write("ATOM  " + num + "  " + a_name + "" + rnName + chain + numres + "    " + x + y + z + "  1.00 64.10           " + atName[0] + "\n")
			else:
				f.write("HETATM" + num + "  " + a_name + "" + rnName + chain + numres + "    " + x + y + z + "  1.00 64.10           " + atName[0] + "\n")
'''
