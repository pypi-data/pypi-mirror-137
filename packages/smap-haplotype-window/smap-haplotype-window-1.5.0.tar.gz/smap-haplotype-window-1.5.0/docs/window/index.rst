.. SMAP documentation master file, created by
   sphinx-quickstart on Wed Aug  5 13:28:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _SMAPwindowindex:

SMAP haplotype-window
===================================

| This is the manual for the haplotype-window component of the SMAP package.
| **SMAP haplotype-window** can extract haplotypes from HiPlex or Shotgun Sequencing reads mapped onto a reference sequence.
| The scheme below shows the workflow combining either of two library preparation methods and/or sample types (individual genotyping or Pool-Seq).

.. image:: ../images/window/haplotype_window_step_scheme.png

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   window_scope_quickstart
   LibraryPrep/index
   SampleType/index
   window_rec_HIW
   window_code
   window_crispr
   window_gff_sliding_window