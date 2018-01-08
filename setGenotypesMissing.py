#!/usr/bin/env python
'''This script takes a VCF file to set a random number of genotypes to missing (./.) for each site until a certain number of called genotypes remains per site. 
The aim is to obtain a VCF file in which each site contains the same number of actually called genotypes, e.g. 30 out of 115. 
In this case, 85 randomly picked genotypes need to be set to missing per site. 

VcfTools should be run before, deleting sites with more than a certain number of genotypes missing, e.g. 85 as in the example above.
 
The script loops through each line (site) and counts the number of missing genotypes (./.). If less than a specified number of genotypes is missing (e.g. <85), 
the number of actually missing genotypes is subtracted from the desired number of missing genotypes. This number of genotypes is next picked randomly from the calles genotypes, 
setting them to missing.  Written by Verena Kutschera, September 2015.

Usage:
Adjust the desired number of genotypes that should be set to missing in the script (line 16, variable m). Adjust opening and writing to file section for compressed or decompressed files (lines 18-22).

python setGenotypesMissing.py myData.vcf.gz myData_setToMissing.vcf'''

import sys
import gzip
import re
import random

m = 88 #total number of genotypes that should be set to missing. Adjust accordingly!

vcfRead = gzip.open(sys.argv[1], 'r') #open the gzipped VCF file.

vcfWrite = open(sys.argv[2], 'w') #write to outputfile (unzipped).

lines = vcfRead.readlines()


def calcSetMissing(site, numbGT): #function to get the number of genotypes that are supposed to be set to missing
    col = site.strip().split()
    missing = []
    for j in col:
        geno = j.split(':')[0]
        if geno == './.':
            missing.append(1)
    setMissing = numbGT - sum(missing) #if less than a certain number, subtract the number of actually missing genotypes from the desired number of missing genotypes. 
    return setMissing   


def replace_random(site, num):
    parts = re.split(r"([:\s])", site) #split the line and store the parts in a list
    indexCalled = [] #collect indices of called genotypes in the list "parts"
    for k, l in enumerate(parts):
        if re.match("[0-9]/[0-9]", l): #maybe adjust so that also sites with >9 alleles can be included. 
            indexCalled.append(k)
        else:
            continue
    randomIndex = random.sample(indexCalled, num) #randomly sample indices of called genotypes
    for n in randomIndex: #loop through list of sampled indices of called genotypes
        parts[n] = './.' #replace the respective called genotype in the list "parts" by "missing"
    newSite = "".join(parts)
    return newSite    


for i in lines: #loop through sites in vcf file. For each site replace a certain number of genotypes by "missing"" ('./.')
    if i.startswith('#'):
        print >> vcfWrite, i.rstrip('\n')
    else:
        numSetMissing = calcSetMissing(i, m)
        newLine = replace_random(i, numSetMissing)
        print >> vcfWrite, newLine.rstrip('\n')
            
vcfRead.close()
vcfWrite.close()
