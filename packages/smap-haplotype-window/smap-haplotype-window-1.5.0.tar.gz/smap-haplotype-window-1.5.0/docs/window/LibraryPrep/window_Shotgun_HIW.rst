.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

####################################
Shotgun Sequencing
####################################

.. _SMAPwindowShotgunHIW:

Setting the stage
-----------------

.. admonition:: Core

	**Windows are defined as any region enclosed by a pair of Borders**. **SMAP haplotype-window** considers the entire read sequence spanning the region between the Borders as a haplotype. Any pair of Borders can be chosen and searched for in a given set of reads. Because Shotgun Sequencing data covers the entire genome, it is advised to work with sliding windows.
	
Recognizing haplotypes
~~~~~~~~~~~~~~~~~~~~~~

| Shotgun Sequencing typically aims to completely cover the reference genome sequence by random sequencing and the read count for any given location is therefore often lower and not "stacked" as in HiPlex amplicon sequencing data. Shotgun Sequencing data may be scanned for short haplotypes by using sliding windows, which is explained further :ref:`below <SMAPwindowslidingwindow>`. Just like in HiPlex windows, windows are delineated by border sequences. 
| 
| The following images illustrate the delineation of haplotypes for a given window in 3 diploid individuals sequenced using Shotgun Sequencing. Although in reality the reads would be mapped differently between samples, here they are shown on the same position for comparison. For this window, only reads shown in bold are analyzed, as they contain both border sequences (shown in orange). Each unique read sequence in between the borders is considered as a haplotype.


.. tabs::

   .. tab:: Shotgun Seq Sample 1
	  
	   .. image:: ../../images/window/Sample1_window_bam_SS.png

   .. tab:: Shotgun Seq Sample 2
	  
	   .. image:: ../../images/window/Sample2_window_bam_SS.png
	  
   .. tab:: Shotgun Seq Sample 3
	  
	   .. image:: ../../images/window/Sample3_window_bam_SS.png

----

Step 1: Create sliding windows with customizable Windowsize, Stepsize, and Borderlength
---------------------------------------------------------------------------------------

procedure
~~~~~~~~~	  
To run SMAP haplotype-window on Shotgun Sequencing data, the user should create a custom GFF file with border positions that delineate sliding windows (see :ref:`instructions here <SMAPwindowquickstart>`).

.. image:: ../../images/window/SMAP_window_step1_SS.png

| For each locus (here called Window), **SMAP haplotype-window** will extract the Window regions from the GFF file with border positions. 
| For each BAM file, for every read that overlaps with the Window region with at least 1 nucleotide, the Read-ID is used to retrieve the corresponding read from the original FASTQ file. If the original read contains **both** border sequences, it is written to the corresponding locus-specific FASTQ file created per sample.
| Note that the sequence of a given read in the FASTQ file (before read mapping) may be different from the corresponding read in the BAM file (after mapping). 
| For instance, a Shotgun Sequence fragment may span across two border sequences, but also contain a large deletion (or highy polymorphic region with multiple flanking SNPs) in the middle of the fragment. Specifically, if read-reference alignments are truncated by soft clipping, BWA-MEM removes the unmapped region of the sequence read.  may result in soft clipping and removal of one end of the read sequence in the BAM file (namely the unmapped sequence flanking the large polymorphism). 
| This means that while the read is correctly mapped within the window region, the full-length haplotype information is lost from the BAM file. 
| Therefore, **SMAP haplotype-window** uses BAM files to sort out reads across the reference sequence, and bundle them in windows, but does not use the alignment information nor the read sequence listed in the BAM file to discover read-reference polymorphisms.
| Instead, **SMAP haplotype-window** retrieves the most complete sequence data from that locus by stepping back to the FASTQ file, and extracts haplotype information directly from those reads.

These border sequences have a recommended length between 5 and 10 bp and require an exact match between the reads and the reference genome sequence.


.. image:: ../../images/window/window_bam_2_fastq_SS.png

.. _SMAPwindowslidingwindow:

Sliding window concept
~~~~~~~~~~~~~~~~~~~~~~

Contrary to HiPlex amplicon sequencing, the genomic location of reads in Shotgun Sequencing is random and unstacked. Therefore border sequences can not be defined based on primer positions and another method must be applied.
For this purpose the concept of sliding windows was employed. Sliding windows have a customizable window size and step size and are flanked by border sequences. 
Consider the image below which depicts a sliding window with Windowsize 50 and Stepsize 20, always flanked by border sequences of length 10. The sliding window iterates over the reference sequence and not the sequencing reads; therefore due to InDels, the read length within windows is sometimes different than the window size.

.. image:: ../../images/window/window_sliding_window_concept.png

Why window size and step size matter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Window size is a trade-off between haplotype size and read count; the larger a window, the larger the haplotypes and the more variation captured by these haplotypes. On the other hand, the larger a window, the fewer reads that will contain both border sequences.
| Step size is a trade-off between redundancy and coverage; a step size larger than the window size makes that the windows do not cover the entire genome. A step size shorter than the window size creates possible redundant windows. 
| The tabs below illustrate the differences between window sizes.

.. tabs::

   .. tab:: Window size 100
	
	  .. image:: ../../images/window/haplotype_window_shotgun_window_size_100.png
   
	  For this specific locus, a window size of 100 bp results in an effective read count of 4 (marked in bold).
	  
   .. tab:: Window size 80

	  .. image:: ../../images/window/haplotype_window_shotgun_window_size_80.png
	  
	  Reducing the window size from 100 to 80 bp results in the increase of the read count by 2. So, shortening the window length increases the total read count, and may increase the total number of loci with read count above the custom minimum read count threshold.

----

Step 2: Calling and counting haplotypes
---------------------------------------

**Reads extracted from FASTQ files are evaluated to contain both border sequences and if so pattern trimmed and written to new sample and locus-specific FASTQ files**


.. image:: ../../images/window/SMAP_window_step2_SS.png

procedure
~~~~~~~~~

:purple:`The following procedure is performed per sample:`

| For each locus-specific FASTQ file, reads are first trimmed at border sequences using pattern trimming performed by `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_.
| Then, the remaining fragments of reads that correspond to the Window are sorted into haplotypes.
| These haplotypes are then counted per sample and passed through a read count filter ``-c``, and the resulting haplotypes and counts are stored in tables.
|
| **Thus the algorithm does not compare the sequences base by base but in their entirety. This procedure allows for the detection of InDels and SNPs without actually calling them *a priori*. 


filters
~~~~~~~  

:purple:`loci with low read count are removed from the dataset with a read count threshold (option` ``-c``:purple:`)`

Accurate haplotype frequency estimation requires a minimum read count which is different between sample type (individuals and Pool-Seq) and ploidy levels.

The user is advised to use the read count threshold to ensure that the reported haplotype frequencies per locus are indeed based on sufficient read data. If a locus has a total haplotype count below the user-defined minimal read count threshold (option ``-c``; default 0, recommended 10 for diploid individuals, 20 for tetraploid individuals, and 30 for pools) then all haplotype observations are removed for that sample. For more information see page :ref:`Recommendations <SMAPwindowrec>`.

:purple:`Only loci with an number of haplotypes within a custom interval across all samples are returned`

``-j``, ``--min_distinct_haplotypes`` :white:`###` *(int)* :white:`###` Filter for the minimum number of distinct haplotypes per locus [0].
``-k``, ``--max_distinct_haplotypes`` :white:`###` *(int)* :white:`###` Filter for the maximum number of distinct haplotypes per locus [inf].

:purple:`Only haplotypes with a percentage higher than a custom threshold in at least one sample are retained` (see Step 3)

``-f``, ``--min_haplotype_frequency`` :white:`###` *(int)* :white:`###` Set minimal haplotype frequency (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the FASTQ files are retained. Haplotypes that never reach this threshold in any of the FASTQ files are removed [0].
	
