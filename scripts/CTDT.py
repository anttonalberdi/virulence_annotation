#!/usr/bin/env python
#_*_coding:utf-8_*_
import argparse
import re
from collections import Counter
import numpy
import itertools

def readFasta(file):
	with open(file) as f:
		records = f.read()
	if re.search('>', records) == None:
		print('The input file seems not in fasta format.')
		sys.exit(1)
	records = records.split('>')[1:]
	myFasta = []
	for fasta in records:
		array = fasta.split('\n')
		name, sequence = array[0].split()[0], re.sub('[^ARNDCQEGHILKMFPSTWYV-]', '-', ''.join(array[1:]).upper())
		myFasta.append([name, sequence])
	return myFasta

def CTDT(fastas):
	group1 = {
                'hydrophobicity_PRAM900101': 'RKEDQN',
                'hydrophobicity_ARGP820101': 'QSTNGDE',
                'hydrophobicity_ZIMJ680101': 'QNGSWTDERA',
                'hydrophobicity_PONP930101': 'KPDESNQT',
                'hydrophobicity_CASG920101': 'KDEQPSRNTG',
                'hydrophobicity_ENGD860101': 'RDKENQHYP',
                'hydrophobicity_FASG890101': 'KERSQD',
                'normwaalsvolume': 'GASTPDC',
                'polarity':        'LIFWCMVY',
                'polarizability':  'GASDT',
                'charge':          'KR',
                'secondarystruct': 'EALMQKRH',
                'solventaccess':   'ALFCGIVW'
        }
	group2 = {
                'hydrophobicity_PRAM900101': 'GASTPHY',
                'hydrophobicity_ARGP820101': 'RAHCKMV',
                'hydrophobicity_ZIMJ680101': 'HMCKV',
                'hydrophobicity_PONP930101': 'GRHA',
                'hydrophobicity_CASG920101': 'AHYMLV',
                'hydrophobicity_ENGD860101': 'SGTAW',
                'hydrophobicity_FASG890101': 'NTPG',
                'normwaalsvolume': 'NVEQIL',
                'polarity':        'PATGS',
                'polarizability':  'CPNVEQIL',
                'charge':          'ANCQGHILMFPSTWYV',
                'secondarystruct': 'VIYCWFT',
                'solventaccess':   'RKQEND'
	}
	group3 = {
                'hydrophobicity_PRAM900101': 'CLVIMFW',
                'hydrophobicity_ARGP820101': 'LYPFIW',
                'hydrophobicity_ZIMJ680101': 'LPFYI',
                'hydrophobicity_PONP930101': 'YMFWLCVI',
                'hydrophobicity_CASG920101': 'FIWC',
                'hydrophobicity_ENGD860101': 'CVLIMF',
                'hydrophobicity_FASG890101': 'AYHWVMFLIC',
                'normwaalsvolume': 'MHKFRYW',
                'polarity':        'HQRKNED',
                'polarizability':  'KMHFRYW',
                'charge':          'DE',
                'secondarystruct': 'GNPSD',
                'solventaccess':   'MSPTHY'
        }

	groups = [group1, group2, group3]
	property = (
        'hydrophobicity_PRAM900101', 'hydrophobicity_ARGP820101', 'hydrophobicity_ZIMJ680101', 'hydrophobicity_PONP930101',
        'hydrophobicity_CASG920101', 'hydrophobicity_ENGD860101', 'hydrophobicity_FASG890101', 'normwaalsvolume',
        'polarity', 'polarizability', 'charge', 'secondarystruct', 'solventaccess')

	encodings = []
	header = ['#']
	for p in property:
		for tr in ('Tr1221', 'Tr1331', 'Tr2332'):
                        header.append(p + '.' + tr)
	encodings.append(header)

	for i in fastas:
		name, sequence = i[0], re.sub('-', '', i[1])
		code = [name]
		aaPair = [sequence[j:j + 2] for j in range(len(sequence) - 1)]
		for p in property:
                        c1221, c1331, c2332 = 0, 0, 0
                        for pair in aaPair:
                                if (pair[0] in group1[p] and pair[1] in group2[p]) or (pair[0] in group2[p] and pair[1] in group1[p]):
                                        c1221 = c1221 + 1
                                        continue
                                if (pair[0] in group1[p] and pair[1] in group3[p]) or (pair[0] in group3[p] and pair[1] in group1[p]):
                                        c1331 = c1331 + 1
                                        continue
                                if (pair[0] in group2[p] and pair[1] in group3[p]) or (pair[0] in group3[p] and pair[1] in group2[p]):
                                        c2332 = c2332 + 1
                        code = code + [c1221/len(aaPair), c1331/len(aaPair), c2332/len(aaPair)]
		encodings.append(code)
	return encodings

def savetsv(encodings, file = 'encoding.tsv'):
	with open(file, 'w') as f:
		if encodings == 0:
			f.write('Descriptor calculation failed.')
		else:
			for i in range(len(encodings[0]) -1):
				f.write(encodings[0][i] + '\t')
			f.write(encodings[0][-1] + '\n')
			for i in encodings[1:]:
				f.write(i[0] + '\t')
				for j in range(1, len(i) - 1):
					f.write(str(float(i[j])) + '\t')
				f.write(str(float(i[len(i)-1])) + '\n')
	return None



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process fasta input with random forest virulence prediction model')
	parser.add_argument("--file", required=True, help="input fasta file")
	parser.add_argument("--out", dest='outFile',
						help="the generated descriptor file")
	args = parser.parse_args()

	fastas = readFasta(args.file)
	encodings = CTDT(fastas)
	outFile = args.outFile if args.outFile != None else 'encoding.tsv'
	savetsv(encodings, outFile)
