.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

######################
Scope & Quick Start
######################

Scope
-----

| **SMAP haplotype-window** extracts haplotypes from reads aligned to a predefined set of Windows in a reference sequence, wherein each Window is enclosed by a pair of Border regions.
| **SMAP haplotype-window** can be used for Highly Multiplex (HiPlex) amplicon sequencing or Shotgun Sequencing data.
| **SMAP haplotype-window** extracts an entire DNA sequence between two Borders as a haplotype allele, without prior knowledge of polymorphisms within that sequence, and considers any unique DNA sequence as a haplotype. This is different from :ref:`SMAP haplotype-sites <SMAPwindowcrispr>`, which performs read-backed haplotyping using prior positional information of read alignments and creates multi-allelic haplotypes from a concatenated short string of polymorphic sites (ShortHaps).

| image:: ../images/window/haplotype_window_scheme_short_TR_all.png

:purple:`SMAP haplotype-window requires this input:`
	
	1. a FASTA file with the reference sequence.
	2. a GFF file with the coordinates of pairs of Borders that enclose a Window. Any number of Windows may be given and will be processed in parallel.
	3. a set of FASTQ files with reads that need to be haplotyped. Any number of samples may be given and will be processed in parallel.
	4. a set of BAM files made with `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ using the respective reference sequence and FASTQ files.
	5. optional: a FASTA file containing the sgRNA sequences in case CRISPR was performed by stable transformation with a CRISPR/sgRNA delivery vector, see also :ref:`CRISPR <SMAPwindowcrispr>`.


| In the haplotype-window workflow, the user first selects Windows (loci to be haplotyped) enclosed by pairs of Border regions. Then, for each BAM file and each Window, **SMAP haplotype-window** extracts the ID's of reads that overlap with the respective Windows with at least one nucleotide. Using the list of Read-IDs, a new FASTQ file is created for each sample-Window combination. Then, for each sample-Window FASTQ file, the corresponding Border sequences are used for pattern-match read trimming with `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_. The remaining read sequences per Window are considered haplotypes, which are counted and listed in an integrated haplotype table per sample and per Window. Filtering options are available to filter out low frequency noise.
|
| **SMAP haplotype-window** considers the entire read sequence spanning the region between the Borders as haplotype.
| **SMAP haplotype-window** filters out genotype calls of Windows with low read depth and low frequency haplotypes to control for noise in the data.
| **SMAP haplotype-window** creates a multi-allelic haplotype matrix listing haplotype counts and frequencies per Window, per sample, across the sample set.
| **SMAP haplotype-window** plots the haplotype frequency distribution across all Windows per sample, and the distribution of haplotype diversity (number of distinct haplotypes per locus) across the sample set.

----
 
.. _SMAPwindowquickstart:
 
Quick Start
-----------

.. tabs::

   .. tab:: rationale behind the procedure
	  
      Issue I: Read-locus assignment is correct, but read-reference alignment is incomplete (soft clipping)      
	  | Polymorphisms are usually identified by first aligning sequence reads to a reference sequence and then detecting differences in DNA sequence with respect to the reference (position by position).
      | Consider a sequenced fragment derived from a given genomic locus with a large deletion (or highly polymorphic region with multiple flanking SNPs) in the middle of the fragment. The two flanking regions in the same read contain (near-)exact sequence similarity to the genomic locus.
      | Mapping reads with BWA-MEM defines which genomic locus is the origin of the sequenced fragment (the maximal exact match that seeds the alignment), and extends the alignment outwards untill a maximum number of mismatches is reached.
      | If read-reference alignments are truncated before the end of the read, BWA-MEM removes the unmapped region of the sequence read in the resulting BAM file (called soft clipping).
      | Consequently, the sequence of a given read in the FASTQ file (before read mapping) may be different from the corresponding read in the BAM file (after mapping). 
      | Also, the polymorphisms that caused the truncation of the read alignment are no longer present as actual sequence data in the BAM file, and can not be used to detect polymorphisms by direct read-reference alignment comparison.

      | **SMAP haplotype-window** resolves this issue via the following steps.
      | While a read may be correctly assigned to a given genomic locus (by positional overlap in a partial alignment), the full-length haplotype information is lost from the BAM file.
      | Therefore, the **SMAP haplotype-window** workflow still uses BAM files to sort out reads across the reference sequence, but does not use the alignment information nor the read sequence listed in the BAM file to discover read-reference polymorphisms.        
      | Instead, **SMAP haplotype-window** retrieves the Read-IDs per genomic locus (here called window) and extracts the most complete sequence data from that locus by stepping back to the FASTQ file.
      
      Issue II: haplotyping needs a start and an end
      
      | A haplotype is defined as a given 

      A BAM file bundles all reads derived from the same genomic locus.
      
      may result in soft clipping and removal of one end of the read sequence in the BAM file (namely the unmapped sequence flanking the large polymorphism). 

      a Shotgun Sequence fragment may span across two border sequences, but also contain a large deletion (or highy polymorphic region with multiple flanking SNPs) in the middle of the fragment.
      
      For each locus (here called Window), **SMAP haplotype-window** will extract the Window regions from the GFF file with border positions. 
	  | For each BAM file, for every read that overlaps with the Window region with at least 1 nucleotide, the Read-ID is used to retrieve the corresponding read from the original FASTQ file. If the original read contains **both** border sequences, it is written to the corresponding locus-specific FASTQ file created per sample.
	  | Note that t 
	  |  	  
	  | 
   .. tab:: overview
	  
	  | The scheme below shows an overview of the **SMAP haplotype-window** workflow.
	  
	  .. image:: ../images/window/haplotype_window_scheme_short_TR_all.png
	  
   .. tab:: required input

	  .. tabs::

		 .. tab:: reference sequence
		 
			The FASTA file containing the reference sequence.

		 .. tab:: GFF
         
			| The `GFF <https://en.wikipedia.org/wiki/General_feature_format#:~:text=In%20bioinformatics%2C%20the%20general%20feature,DNA%2C%20RNA%20and%20protein%20sequences.>`_ file describes the position of the Border regions on the reference sequence in 9 columns. **SMAP haplotype-window** expects two Borders that together enclose a Window, which are paired based on the \'NAME=\' field in the 9th column. The file does not need to contain a header. These fields need to be specified:

				| 1. Name of the sequence in the reference that contains the Window.
				| 2. Source of the feature. [SMAP haplotype-window]. 
				| 3. Feature type. Because in SMAP haplotype-window pairs of Borders define Windows, two feature types are used: Border_upstream and Border_downstream. Each line in the GFF is one of those borders.
				| 4. The start coordinate of the Border region. [in the 1-based GFF coordinate system].
				| 5. The end coordinate of the Border region [in the 1-based GFF coordinate system, value must always be higher than column 4].
				| 8. Score. Irrelevant for SMAP haplotype-window [.].
				| 7. Orientation of the Border [always +].
				| 8. Phase. Irrelevant for SMAP haplotype-window [.].
				| 9. Attributes of the Border, the field \'NAME=\' is required. This field is used to pair Borders (by exact \'NAME=\' matching), and define the corresponding Window regions. The field Name must be unique for each Window and will be used to name loci in the haplotype frequency tables.

			| Depending on the type of data (HiPlex or Shotgun Seq), a specific GFF file must be created to define pairs of Borders enclosing Windows.

				.. tabs::

					.. tab:: HiPlex / primer binding sites
					
						| For HiPlex data it is advised to use the 10 nucleotides on the 3' of the primer binding site, where they flank the Window (sequence read region inbetween the primers). 

						# .. csv-table:: 	  
						#    :file: ../tables/window/example_HiPlex_gff.csv
						#    :header-rows: 0

					.. tab:: Shotgun Sequencing / Sliding Windows
					
						| Shotgun Seq data may be analysed with a set of sliding Windows, with a customisable Window size (here 50), step size (here 20), and Border length (here 10). See also :ref:`Scripts <SMAPwindowgffscripts>` for template scripts for creating sliding windows.

						# .. csv-table:: 	  
						#    :file: ../tables/window/example_walking_window_gff.csv
						#    :header-rows: 0

		 .. tab:: FASTQ
		 
			A set of FASTQ files with reads that need to be haplotyped.

		 .. tab:: BAM
			
			 A set of BAM files made with `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ using the respective reference sequence and FASTQ files.
		 
   .. tab:: procedure

	  | **SMAP haplotype-window** extracts haplotypes from reads aligned to a predefined set of Windows in a reference sequence, each Window is enclosed by a pair of Border regions.
	  | 
	  | **Step 1**
	  | For each locus (here called Window), **SMAP haplotype-window** will define the Window region by pairing Border regions defined in a GFF file. 
	  | For each BAM file and for each Window, **SMAP haplotype-window** will identify the IDs of reads that overlap with at least one nucleotide, retrieve their original complete read sequence from the corresponding sample's FASTQ file and create a separate FASTQ file for each sample-Window combination. 
	  | These steps make sure that reads that are soft-clipped during read alignment by `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_, but that initially do contain the border sequences at their respective ends, can still be evaluated in their entirety. Soft-clipping results in partial read alignment and removal of the unmapped part of the sequence read from the BAM file.
	  | **SMAP haplotype-window** then retrieves the respective sequences for the Border_upstream and Border_downstream regions using the GFF coordinates and the reference genome FASTA sequence for each Window. 
	  |
	  | **Step 2**
	  | All separate FASTQ files (one for each sample-Window combination) are then passed to `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_ using the Window-specific pair of Border sequences for pattern trimming. 
	  | Because the Window is defined as the region *inbetween* the Borders (*i.e.* read regions retained after removal of the Borders), the entire read sequence spanning the Window is considered as a unique haplotype. 
	  | These haplotypes are then counted per Window per sample, filtered for total read count per Window per sample (option ``-c``)
	  |
	  | **Step 3**
	  | All individual BAM file specific haplotype count tables are integrated into a large haplotype count matrix.
	  | **SMAP haplotype-window** then retrieves the Window-sequence from the reference genome FASTA sequence.
	  | For each detected haplotype, difference in sequence length compared to the reference Window sequence length (haplotype length - ref Window length) is listed as \`Length Difference with Reference´ \ or **LDR**. For each haplotype with an LDR = 0, exact matches between the haplotype sequence and the reference sequence of the respective Window, are assigned an LDR value of \'ref\'. 
	  | This procedure detects unique haplotypes in Windows enclosed by two known Border Sequences consisting of any (*a priori* unknown) combination of InDels and/or SNPs, *without* using the BAM alignment itself for the detection of InDels and/or SNPs. The `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ alignment is merely used for efficiently sorting reads across Windows. 
	  | After LDR allocations, haplotype counts are converted into frequencies which can then be filtered (options ``-f`` and ``-m``).
	  |
	  | **Step 4**
	  | The final step of **SMAP haplotype-window** is only applicable on individuals and concerns the conversion of haplotype frequencies into discrete calls. 
	  | Using customizable frequency intervals, haplotype frequencies can either be transformed into dominant calls (0/1) or dosage calls (0/1/2/..).
	  
	  
   .. tab:: commands
      
	  The complete list of commands can be found at the bottom of this page or on the :ref:`Summary of Commands <SMAPwindowquickstart>` page, the latter also includes examples for several kinds of data.

----
	  
Output
------ 

**Tabular output**

.. tabs::

   .. tab:: General output

      By default, **SMAP haplotype-window** will return two .tsv files.  
 
      :purple:`haplotype counts`
      
      **counts_cx_fx_mx.tsv** (with x the value per option used in the analysis) contains the read counts (``-c``) and haplotype frequency (``-f``) filtered and/or masked (``-m``) read counts per haplotype per locus as defined in the BED file from **SMAP delineate**.  
      This is the file structure:
	  
		  ========= ========== ======= ======= ======= ========
		  Locus     Haplotypes LDR     Sample1 Sample2 Sample..
		  ========= ========== ======= ======= ======= ========
		  Window_1  ACGTCGTCGC ref     60      13      34
		  Window_1  ACGTCGTCAC 0       19      90      51
		  Window_2  GCTCATCG   ref     70      63      87
		  Window_2  GCTCTCG    -1      108     22      134
		  ========= ========== ======= ======= ======= ========

      :purple:`relative haplotype frequency`
      
      **haplotypes_cx_fx_mx.tsv** contains the relative frequency per haplotype per locus in sample (based on the corresponding count table: counts_cx_fx_mx.tsv). The transformation to relative frequency per locus-sample combination inherently normalizes for differences in total number of mapped reads across samples, and differences in amplification efficiency across loci.  
      This is the file structure:

		  ========= ========== ======= ======= ======= ========
		  Locus     Haplotypes LDR     Sample1 Sample2 Sample..
		  ========= ========== ======= ======= ======= ========
		  Window_1  ACGTCGTCGC ref     0.76    0.13    0.40
		  Window_1  ACGTCGTCAC 0       0.24    0.87    0.60
		  Window_2  GCTCATCG   ref     0.39    0.74    0.39
		  Window_2  GCTCTCG    -1      0.61    0.26    0.61
		  ========= ========== ======= ======= ======= ========

	  | Additionally **freqs_unfiltered.tsv** can be further filtered using the options ``-j`` (minimum distinct haplotypes) and ``-k`` (maximum distinct haplotypes), resulting in the file **freqs_distinct_haplotypes_filter.tsv**

   .. tab:: Additional output for individuals
   
	  | For individuals, if the option ``--discrete_calls`` is used, the program will return three additional .tsv files. Their order of creation and content is shown in the scheme :ref:`above <SMAPhaplostep4>`.
	  | The first file is called **haplotypes_cx_fx_mx_total_discrete_calls.tsv** and this file contains the total sum of discrete calls, obtained after transforming haplotype frequencies into discrete calls, using the defined ``--frequency_interval_bounds``. The total sum of discrete dosage calls is expected to be 2 in diploids and 4 in tetraploids.
	  | The second file is **haplotypes_cx_fx_mx_call.tsv**, which incorporates the filter ``--dosage_filter`` to remove loci per sample with an unexpected number of haplotype calls in **haplotypes_cx_fx_mx_total_discrete_calls.tsv**. The expected number of calls is set with option ``-z`` [use 2 for diploids, 4 for tetraploids].
	  | The third file, **haplotypes_cx_fx_mx_AF.tsv**, lists the population haplotype frequencies (over all individual samples) based on the total number of discrete haplotype calls relative to the total number of calls per Window.

**Graphical output**

under development


----
	  
Summary of Commands
-------------------

::

	smap haplotype-window -genome /path/to/RefGenome/ -borders /path/to/GFF/ -reads_dir /path/to/FASTQ/ -alignments_dir /path/to/BAM/ -c 10 -f 5 -m 1 -p 8 --min_distinct_haplotypes 2 
 
.. tabs::

   .. tab:: general options

	  | ``-genome`` :white:`###################` *(str)* :white:`###` FASTA file with the reference genome sequence.
	  | ``–borders`` :white:`##################` *(str)* :white:`###` GFF file with the coordinates of pairs of Borders that enclose a Window. Must contain NAME=<> in column 9 to denote the Window name.
	  | ``–reads_dir`` :white:`#################` *(str)* :white:`###` Path to the directory containing FASTQ files with the reads mapped to the reference genome to create the BAM files. The FASTQ file names must have the same prefix as the BAM files specified in ``-alignments_dir`` [no default].
	  | ``-alignments_dir`` :white:`#############` *(str)* :white:`###` Path to the directory containing BAM and BAI alignment files. All BAM files should be in the same directory [no default].
	  | ``-–guides`` :white:`##################` *(str)* :white:`###` Optional FASTA file containing the sequences from sgRNAs used in CRISPR genome editing. Useful when amplicons on the CRISPR/sgRNA delivery vector are included in the HiPlex amplicon mixture.
	  | ``-p``, ``--processes`` :white:`############` *(int)* :white:`###` Number of parallel processes [1].
	  | ``-o``, ``--out`` :white:`################` *(str)* :white:`###` Basename of the output file without extension [SMAP_haplotype_window].
	  | ``-u``, ``--undefined_representation`` :white:`#` *(str)* :white:`###` Value to use for non-existing or masked data [NaN].
	  | ``-h``, ``--help`` :white:`######################` Show the full list of options. Disregards all other parameters.
	  | ``-v``, ``--version`` :white:`####################` Show the version. Disregards all other parameters.
	  | ``--debug`` :white:`#########################` Enable verbose logging.
	  |
	  | Options may be given in any order.
	  
   .. tab:: filtering options
   
	  | ``-q``, ``--min_mapping_quality`` :white:`####` *(int)* :white:`###` Minimum .bam mapping quality for reads to be included in the analysis [30].   
	  | ``-c``, ``--min_read_count`` :white:`#######` *(int)* :white:`###` Minimum total number of reads per locus per sample [0].
	  | ``-d``, ``--max_read_count`` :white:`#######` *(int)* :white:`###` Maximum number of reads per locus per sample, read depth is calculated after filtering out the low frequency haplotypes (``-f``) [inf].
	  | ``-f``, ``--min_haplotype_frequency`` :white:`#` *(int)* :white:`###` Set minimum haplotype frequency (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the samples are retained. Haplotypes that never reach this threshold in any of the samples are removed [0].
	  | ``-m``, ``--mask_frequency`` :white:`#######` *(float)* :white:`##` Mask haplotype frequency values below this threshold for individual samples. Can be used to mask noise. Haplotypes are not removed based on this value, use ``--min_haplotype_frequency`` for this purpose instead.
	  | ``-j``, ``--min_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Set minimum number of distinct haplotypes per locus across all samples. Loci that do not fit this criteria are removed from the final output [0].
	  | ``-k``, ``--max_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Set maximum number of distinct haplotypes per locus across all samples. Loci that do not fit this criteria are removed from the final output [inf].
	  |
	  | Options may be given in any order.
	  
   .. tab:: options for discrete calling in individual samples
	  
	   This option is primarily supported for diploids and tetraploids, nevertheless it is available for species with a higher ploidy, however this is not recommended as these generally require more complex models.
	  
	  ``-e``, ``–-discrete_calls`` :white:`###` *(str)* :white:`###` Set to "dominant" to transform haplotype frequency values into presence(1)/absence(0) calls per allele, or "dosage" to indicate the allele copy number.
	  
	  ``-i``, ``--frequency_interval_bounds`` :white:`##` Frequency interval bounds for classifying the read frequencies into discrete calls. Custom thresholds can be defined by passing one or more space-separated integers which represent relative frequencies in percentage. For dominant calling, one value should be specified. For dosage calling, an even total number of four or more thresholds should be specified. The usage of defaults can be enabled by passing either "diploid" or "tetraploid". The default value for dominant calling (see discrete_calls argument) is 10, regardless whether or not "diploid" or "tetraploid" is used. For dosage calling, the default for diploids is "10 10 90 90" and for tetraploids "12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5"
	  
	  ``-z``, ``--dosage_filter`` :white:`###` *(int)* :white:`###` Mask dosage calls in the loci for which the total allele count for a given locus at a given sample differs from the defined value. For example, in diploid organisms the total allele copy number must be 2, and in tetraploids the total allele copy number must be 4. (default no filtering).
	  			
	  ``--frequency_interval_bounds`` **in practical examples and additional information on the dosage filter:**
	  
	  .. tabs::

		 .. tab:: diploid dosage
			
			**discrete dosage calls for diploids (0/1/2)**
			
			Use this option if you want to customize discrete calling thresholds. Haplotype calls with frequency below the lowerbound percentage are considered not detected and receive dosage \`0´ \. Haplotype calls with a frequency between the lowerbound and the next percentage are considered heterozygous and receive haplotype dosage \`1´\.  Haplotype calls with frequency above the upperbound percentage are considered homozygous and scored as haplotype dosage \`2´ \. default \<10, [10:90], >90 \. Should be written with spaces between percentages, percentages may be written as floats or as integers [10 10 90 90].
			
			*e.g.* ``--discrete_calls dosage --frequency_interval_bounds 10 10 90 90`` translates to: haplotype frequency < 10% = 0, haplotype frequency > 10% & < 90% = 1, haplotype frequency > 90% = 2.
			
			Visualized examples of these thresholds can be found in the tabs :ref:`here <SMAPhaplofreq>`.	
			
		 .. tab:: diploid dominant
			
			**discrete dominant calls for diploids (0/1)**
			
			LowerBound frequency for dominant call haplotypes. Haplotypes with frequency above this percentage are scored as dominant present haplotype [10]. 	
			
			*e.g.* ``--discrete_calls dominant --frequency_interval_bounds 10`` translates to: haplotype frequency < 10% = 0, haplotype frequency > 10% = 1
			
			Visualized examples of these thresholds can be found in the tabs :ref:`here <SMAPhaplofreq>`.

		 .. tab:: tetraploid dosage
			
			**discrete dosage calls for tetraploids (0/1/2/3/4)**
			
			Use this option if you want to customize discrete calling thresholds, haplotype calls with frequency below the lowerbound percentage are considered not detected and receive dosage \`0´ \. Haplotype calls with frequency between the lowerbound and next percentage are considered present in 1 out of 4 alleles and scored as haplotype dosage \`1´ \, haplotype frequencies in the next frequency interval are scored as haplotype dosage \`2´ \, and so on. Haplotype calls with frequency above the upperbound percentage are considered homozygous and scored as haplotype dosage \`4´ \ default \<12.5, [12.5:37.5], [37.5:62.5], [62.5:87.5], >87.5 \. Should be written with spaces between percentages, percentages may be written as floats or as integers [12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5].
			
			*e.g.* ``--discrete_calls dosage --frequency_interval_bounds 12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5`` translates to: haplotype frequency < 12.5% = 0, haplotype frequency > 12.5% & < 37.5% = 1, haplotype frequency > 37.5.5% & < 62.5% = 2, haplotype frequency > 62.5% & < 87.5% = 3, haplotype frequency > 87.5% = 4.
			
			Visualized examples of these thresholds can be found in the tabs :ref:`here <SMAPhaplofreq>`.
			
		 .. tab:: tetraploid dominant
			
			**discrete dominant calls for tetraploids (0/1)**
			
			LowerBound frequency for dominant call haplotypes. Haplotypes with frequency above this percentage are scored as dominant present haplotype [10].
			
			*e.g.* ``--discrete_calls dominant --frequency_interval_bounds 10`` translates to: haplotype frequency < 10% = 0, haplotype frequency > 10% = 1.
			
			Visualized examples of these thresholds can be found in the tabs :ref:`here <SMAPhaplofreq>`.

		 .. tab:: Why dosage filter (-z)?

			| The dosage filter ``-z`` is an additional filter specifically for dosage calls in individuals. It removes loci within samples from the dataset (replaced by ``-u`` or ``--undefined_representation``) based on total dosage calls (= total allele count calculated from haplotype frequencies using frequency interval bounds). 
			| It is important to make a distinction between allele count (= total dosage call) and number of unique alleles. A tetraploid individual for example always contains 4 alleles (*e.g.* aabb) but can contain 1 up to 4 unique alleles (*e.g.* abcd, accd, aaab, aaaa, ..). The dosage filter does **not** look at unique allele counts but at actual allele counts calculated from haplotype frequencies.
			| In general the expected total dosage call for any locus is equal to the ploidy of the individual (except in exceptional cases such as aneuploidy).
			| Consider the examples of a single locus in the tabs below for a better understanding.
			
			.. tabs::

			   .. tab:: diploid dosage
				  
				  # .. image:: ../images/window/dosage_filter_2n.png
			   
			   .. tab:: tetraploid dosage
			
				  # .. image:: ../images/window/dosage_filter_4n.png
			
			
			| The dosage filter is applied after every other filter, and therefore the number of values substituted by ``-u`` depends on previous filters. 
			| An adequate value for the filter ``-f`` (minimum haplotype frequency) is especially useful to reduce the number of NA's, for example in Sample2 in the diploid example above a haplotype (c) persisted at 4.7%. If this had been filtered out using the option ``-f``, the other haplotype values would have been recalculated and the total dosage would have become 2 (haplotype aa).
			| Additionally the ``--frequency_interval_bounds`` can be tuned to the users liking at the hand of the :external+haplotype-sites:ref:`haplotype frequency graphs <SMAPhaplofreq>` in order to reduce the number of within sample loci filtered out by ``--dosage_filter``.