# SMAP - Stack Mapping Anchor Points
![pipepeline status badge](https://gitlab.com/truttink/smap/badges/master/pipeline.svg)
[![coverage report](https://gitlab.com/truttink/smap/badges/master/coverage.svg)](https://gitlab.com/truttink/smap/-/commits/master)

SMAP is a software package that analyzes read mapping distributions and performs haplotype calling to create multi-allelic molecular markers. SMAP haplotyping works on all types of samples, including (di- and polyploid) individuals and Pool-Seq, and reads of various NGS methods, including Genotyping-by-Sequencing (GBS) and highly multiplex amplicon sequencing (HiPlex). 
* SMAP delineate analyses read mapping distributions for GBS read mapping QC, defines read mapping polymorphisms within loci and across samples, and selects high quality loci across the sample set for downstream analyses.
* SMAP compare identifies the number of common loci across two runs of SMAP delineate.
* SMAP haplotype-sites performs read-backed haplotyping using a priori known polymorphic SNP sites, and creates ShortHaps. SMAP haplotype-sites also captures GBS read mapping polymorphisms (here called SMAPs) as a novel genetic diversity marker type, and integrates those with SNPs for ShortHap haplotyping.

## Documentation

An extensive manual of the SMAP package can be found on [Read the Docs](https://ngs-smap.readthedocs.io/) including detailed explanations and illustrations.

## Citation

If you use SMAP, please cite "Ruttink, T. (2021) SMAP: a versatile approach to read-backed haplotyping in stacked NGS read data. [Online]. Available online at https://gitlab.com/truttink/smap/"

## Building and installing

SMAP is being developed and tested on Linux.
Additionally, some dependencies are only developed on Linux.

### Using pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install ngs-smap
```

### Via Git

1. `git clone https://gitlab.com/truttink/smap.git`
2. `cd smap`
3. `git checkout master`
4. `python3 -m venv .venv`
5. `source .venv/bin/activate`
6. `pip install --upgrade pip`
7. `pip install .`

or 

`git clone https://gitlab.com/truttink/smap.git ; cd smap ; git checkout master ; python3 -m venv .venv ; source .venv/bin/activate ; pip install --upgrade pip ; pip install .`

### Using Docker
A docker container is available on dockerhub. 
To pull the docker image and run SMAP using Docker, use:
`docker run dschaumont/smap --help`

## Contributions

* The Ghent University 2019 Computational Biology class under supervision of prof. Dr. Peter Dawyndt and Felix Van der Jeugt has made contributions to reduce memory usage and to speed up haplotype calculations.

## Links
* [Documentation](https://ngs-smap.readthedocs.io/)
* [Source Code](https://gitlab.com/truttink/smap)
* [Report an issue](https://gitlab.com/truttink/smap/-/issues)
* [GbprocesS: extraction of genomic inserts from NGS data for GBS experiments](https://gitlab.com/dschaumont/GBprocesS)
* [SMAP on pypi](https://pypi.org/project/ngs-smap/)
* [SMAP on dockerhub](https://hub.docker.com/repository/docker/dschaumont/smap)
* [ILVO (Flanders Research Institute for Agriculture, Fisheries and Food)](https://ilvo.vlaanderen.be/en/)