.. SMAP documentation master file, created by
   sphinx-quickstart on Wed Aug  5 13:28:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Haplotyping for different sample types (individual or pool)
===========================================================

Individual and pooled samples are different in two major ways; 
	
	*	In individuals, low frequency haplotypes (<5%) are generally noise and need to be removed from the data. In pools on the other hand it is hard to discriminate between noise and low frequency alleles. 
	*	In individuals and pools haplotype frequencies are calculated. In addition, in individuals these haplotypes can be converted into discrete haplotype calls, which can be either dominant (0/1) or dosed (0/1/2(/3/4)).
	
| Therefore these two sample types are separately discussed.
| It is **not necessary** to define your sample type in the program/command line.

.. image:: ../../images/window/haplotype_step_scheme_34.png

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   window_individuals_HIW
   window_pools_HIW