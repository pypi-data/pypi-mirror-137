.. SMAP documentation master file, created by
   sphinx-quickstart on Wed Aug  5 13:28:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. raw:: html

    <style> .purple {color:purple} </style>

.. role:: purple


Haplotyping for different library preparation methods
=====================================================

| By design, different library preparations yield different output data and should therefore be processed in a slightly different way. 
| **SMAP haplotype-window** is currently usable for HiPlex and Shotgun Sequencing data and therefore the manual discusses these methods separately while accounting for dissimilarities.
| The principal differences between HiPlex and Shotgun Seq data are the input files. In HiPlex data, the read positions are known and stacked, whereas in Shotgun Seq data the read positions are randomly distributed across the genome reference sequence.
| It is **not necessary** to specify your library preparation method on the command line, but different GFF files delineating the Windows are constructed.


:purple:`Delineation of Windows for HiPlex data`

.. image:: ../../images/window/SMAP_window_step1_AS.png

For HiPlex, a simple GFF file defining Windows is created by listing two reference sequence positions (primer-based anchor points) for each border for each amplicon (an upstream border sequence within the forward primer, and a downstream border sequence within the reverse primer).
By design, all primer binding sites and expected amplicons are *a priori* known, and there is no need to search for alternative loci with mapped reads.

:purple:`Delineation of Windows for Shotgun Sequencing data`

.. image:: ../../images/window/SMAP_window_step1_SS.png

For Shotgun Sequencing, contrary to HiPlex read data, read positions are scattered across the genome and are not "stacked". Therefore, the delineation of Windows is a little different than in HiPlex data and the concept of sliding windows is introduced.
A GFF file containing sliding windows is created by iterating over the reference sequence with a fixed Stepsize and Windowsize. More information can be found on the :ref:`Shotgun Sequencing page <SMAPwindowShotgunHIW>`.

If only specific loci are of interest, it is also possible to follow the HiPlex Window delineation procedure.

:purple:`Haplotype-window considers different locus structures for HiPlex and Shotgun Seq`


.. image:: ../../images/window/haplotype_window_step_scheme_12.png

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   window_HiPlex_HIW
   window_Shotgun_HIW