This repository contains a set of python scripts to filter VCF files that were produced using the GATK v3.4.0 pipeline.

# countHeterozygousGenotypes.py
- takes a gzipped VCF file and counts the numbers of heterozygous and missing genotypes per site.
- the output is printed to a table.

# findCpGpolymorphism.py
- takes a gzipped VCF file containing variant and monomorphic/invariant sites, and finds the positions of CpG, CpA and TpG sites, incl CpG/CpA and TpG/CpG polymorphisms within the resequencing data.
- not only REF and ALT, but also allele frequency (AF) and genotype information (individual GT) are considered. 
- site pairs with positions not directly adjacent to each other will be ignored. 
- the output is printed to a bed file.

# setGenotypesMissing.py
- takes a gzipped VCF file to set a random number of genotypes to missing (./.) for each site until a certain number of called genotypes remains per site. 
- the aim is to obtain a VCF file in which each site contains the same number of actually called genotypes, e.g. 30 out of 115. In this case, 85 randomly picked genotypes need to be set to missing per site. 
- a tool like vcftools (https://vcftools.github.io/index.html) should be run before, deleting sites with more than a certain number of genotypes missing, e.g. 85 as in the example above.
