.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

###########################
HiPlex amplicon sequencing
###########################

.. _SMAPwindowHiPlexHIW:

Setting the stage
-----------------

.. admonition:: Core

	**Windows are defined as any region enclosed by a pair of Borders**. **SMAP haplotype-window** considers the entire read sequence spanning the region between the Borders as haplotypes. Any pair of Borders can be chosen and searched for in a given set of reads. Because the primer sequence itself becomes incorporated into the amplicon molecule, (parts of) primers can naturally function as Border sequences delineating the enclosed amplified region.

HiPlex library preparation and preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

the schemes currently under the CRISPR chapter should be placed here (not the entire CRISPR chapter, the part on guides may be separate) to be checked. 

Recognizing haplotypes
~~~~~~~~~~~~~~~~~~~~~~

| In HiPlex data **primer sequences** are **preferably retained** during trimming in preprocessing in order to create more positive matches during mapping. Because these sequences are invariable and technical, they are not taken into consideration by **SMAP haplotype-window**, instead they are preferably used to recognize the start and stop positions of the enclosed amplified region, i.e. the Window to be haplotyped.
| Border sequences are recommended to have a length between **5** and **10** bp and require an **exact** match between the reads and the reference genome sequence.
| This sequence delineation by two border sequences in HiPlex data is identical to the delineation in Shotgun Seq data. However in Shotgun Seq data, border sequences are chosen at the hand of sliding windows, whereas in HiPlex data they can be defined. Therefore these border sequences are merely delineations and are invariable between reads on the same locus. 
| Primer positions/sequences are usually known, because primers are generally constructed from a reference genome. However HiPlex data often contain off-targets (*i.e.* combinations of primers from different pairs), which might contain interesting information depending on the research question. In this case, and when primer positions are unknown, they can be acquired through mapping with third party software (*e.g.* `BWA-MEM <https://janis.readthedocs.io/en/latest/tools/bioinformatics/bwa/bwamem.html>`_) 

The tabs below show the same locus/amplicon in 3 diploid individuals. A total of 4 SNPs and 2 deletions are found among the individuals; 4 haplotypes can clearly be defined (1 reference allele and 3 alternative alleles). 

.. tabs::

   .. tab:: HiPlex merged reads, Sample 1
	  
	  .. image:: ../../images/window/Sample1_window_bam_AS.png

   .. tab:: HiPlex merged reads, Sample 2
	  
	  .. image:: ../../images/window/Sample2_window_bam_AS.png
	  
   .. tab:: HiPlex merged reads, Sample 3
	  
	  .. image:: ../../images/window/Sample3_window_bam_AS.png

----
	  
Step 1: Extracting window-overlapping reads ID's from BAM files and reads from FASTQ files
-------------------------------------------------------------------------------------------

procedure
~~~~~~~~~	  

In order to run **SMAP haplotype-window** on HiPlex data, the user should create a custom GFF file with the desired Border positions enclosing Windows (see :ref:`instructions here <SMAPwindowquickstart>`). 

.. image:: ../../images/window/SMAP_window_step1_AS.png

| For each locus (here called Window), **SMAP haplotype-window** will extract the Window-sequence from the reference FASTA file and create an empty locus-specific FASTQ file. 
| For each BAM file, for every read that overlaps with the Window-sequence with at least 1 nucleotide, the Read-ID is saved and the corresponding read is retrieved from the original FASTQ file. If the original read contains **both** border sequences, it is written to the new locus-specific FASTQ file.
| This means that if for whatever reason, only one of the borders is present in any reads in a BAM file (in this case a large deletion that caused soft-clipping), it does not matter as the algorithm will only consult the corresponding FASTQ file to look to find the border sequences. This method therefore circumvents the incapacity of mapping algorithms to process large InDels.

.. image:: ../../images/window/window_bam_2_fastq_AS.png

----

Step 2: Trimming and counting haplotypes
-----------------------------------------

**Reads extracted from FASTQ files are evaluated to contain both border sequences and if so pattern trimmed and written to new sample specific FASTQ files**


.. image:: ../../images/window/SMAP_window_step2_AS.png

procedure
~~~~~~~~~

:purple:`The following procedure is performed per sample:`

| For each locus-specific FASTQ file, reads are first trimmed at border sequences using pattern trimming performed by `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_.
| Then, the remaining fragments of reads that correspond to the Window are sorted into haplotypes.
| These haplotypes are then counted per sample and passed through a read depth filter ``-c``, and the resulting haplotypes and counts are stored in tables.
| 
| **Thus the algorithm does not compare the sequences base by base but in their entirety. This procedure allows for the detection of InDels and SNPs without actually calling them.** 


filters
~~~~~~~

:purple:`loci with low read count are removed from the dataset with a read count threshold (option` ``-c``:purple:`)`

Accurate haplotype frequency estimation requires a minimum read count which is different between sample type (individuals and Pool-Seq) and ploidy levels.

The user is advised to use the read count threshold to ensure that the reported haplotype frequencies per locus are indeed based on sufficient read data. If a locus has a total haplotype count below the user-defined minimal read count threshold (option ``-c``; default 0, recommended 10 for diploid individuals, 20 for tetraploid individuals, and 30 for pools) then all haplotype observations are removed for that sample. For more information see page :ref:`Recommendations <SMAPwindowrec>`.

:purple:`Only loci with an number of haplotypes between a custom interval across all samples are returned`

``-j``, ``--min_distinct_haplotypes`` :white:`###` *(int)* :white:`###` Filter for the minimum number of distinct haplotypes per locus [0].
``-k``, ``--max_distinct_haplotypes`` :white:`###` *(int)* :white:`###` Filter for the maximum number of distinct haplotypes per locus [inf].

:purple:`Only haplotypes with a percentage higher than a custom number in at least one sample are retained` (see Step 3)

``-f``, ``--min_haplotype_frequency`` :white:`###` *(int)* :white:`###` Set minimal HF (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the FAST files are retained. Haplotypes that never reach this threshold in any of the FASTQ files are removed [0].
	
