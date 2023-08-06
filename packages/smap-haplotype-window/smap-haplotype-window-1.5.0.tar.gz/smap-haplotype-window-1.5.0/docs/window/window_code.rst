.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. _SMAPwindowcommands:

###################
Summary of Commands
###################

General Options
---------------

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
	  | ``--debug`` :white:`#########################` Enable verbose logging. Provides additional intermediate output-files used for sample-specific QC.
	  |
	  | Options may be given in any order.
	  
   .. tab:: filtering options
   
	  | ``-q``, ``--min_mapping_quality`` :white:`####` *(int)* :white:`###` Minimum .bam mapping quality to retain reads for analysis [30].
	  | ``-c``, ``--min_read_count`` :white:`#######` *(int)* :white:`###` Minimum total number of reads per locus per sample [0].
	  | ``-d``, ``--max_read_count`` :white:`#######` *(int)* :white:`###` Maximum number of reads per locus per sample, read depth is calculated after filtering out the low frequency haplotypes (``-f``) [inf].
	  | ``-f``, ``--min_haplotype_frequency`` :white:`#` *(int)* :white:`###` Set minimum haplotype frequency (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the samples are retained. Haplotypes that never reach this threshold in any of the samples are removed [0].
	  | ``-m``, ``--mask_frequency`` :white:`#######` *(float)* :white:`##` Mask haplotype frequency values below this threshold for individual samples. Can be used to mask noise. Haplotypes are not removed based on this value, use ``--min_haplotype_frequency`` for this purpose instead.
	  | ``-j``, ``--min_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Set minimum number of distinct haplotypes per locus across all samples. Loci that do not fit this criteria are removed from the final output [0].
	  | ``-k``, ``--max_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Set maximum number of distinct haplotypes per locus across all samples. Loci that do not fit this criteria are removed from the final output [inf].
	  |
	  | Options may be given in any order.
	  
   .. tab:: options for discrete calling in individual samples
	  
	   This option is primarily supported for diploids and tetraploids. Users can define their own custom frequency bounds for species with a higher ploidy, but this requires optimization based on the observed haplotype frequency distributions.
	  
	  ``-e``, ``–-discrete_calls`` :white:`###` *(str)* :white:`###` Set to "dominant" to transform haplotype frequency values into presence(1)/absence(0) calls per allele, or "dosage" to indicate the allele copy number.
	  
	  ``-i``, ``--frequency_interval_bounds`` :white:`##` Frequency interval bounds for classifying the read frequencies into discrete calls. Custom thresholds can be defined by passing one or more space-separated values (integer or float) which represent relative frequencies in percentage. For dominant calling, one value should be specified. For dosage calling, an even total number of four or more thresholds should be specified. The usage of defaults can be enabled by passing either "diploid" or "tetraploid". The default value for dominant calling (see discrete_calls argument) is 10, regardless whether or not "diploid" or "tetraploid" is used. For dosage calling, the default for diploids is "10 10 90 90" and for tetraploids "12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5"
	  
	  ``-z``, ``--dosage_mask`` :white:`###` *(int)* :white:`###` Mask dosage calls in the loci for which the total dosage call for a given locus at a given sample differs from the defined value. For example, in diploid organisms the total dosage call must be 2, and in tetraploids the total dosage call must be 4. (default no masking).
	 
	  ``--locus_correctness`` :white:`########` *(int)* :white:`###` Threshold value: % of samples with locus correctness. Create a new .bed file defining only the loci that were correctly dosage called (-z) in at least the defined percentage of samples (default no filtering).
	  
	  ``--frequency_interval_bounds`` **in practical examples and additional information on the dosage mask:**
	  
	  .. tabs::

		 .. tab:: diploid dosage
			
			**discrete dosage calls for diploids (0/1/2)**
			
			Use this option if you want to customize discrete calling thresholds. Haplotype calls with frequency below the lowerbound percentage are considered "not detected" and receive dosage \`0´\. Haplotype calls with a frequency between the lowerbound and the next percentage are considered heterozygous and receive haplotype dosage \`1´\.  Haplotype calls with frequency above the upperbound percentage are considered homozygous and scored as haplotype dosage \`2´\. default \<10, [10:90], >90 \. Should be written with spaces between percentages, percentages may be written as floats or as integers [10 10 90 90].
			
			*e.g.* ``--discrete_calls dosage --frequency_interval_bounds 10 10 90 90`` translates to: haplotype frequency < 10% = 0, haplotype frequency > 10% & < 90% = 1, haplotype frequency > 90% = 2.
			
			Visualized examples of these thresholds can be found in :ref:`these tabs <SMAPhaplofreq>`.
			
		 .. tab:: diploid dominant
			
			**discrete dominant calls for diploids (0/1)**
			
			LowerBound frequency for dominant call haplotypes. Haplotypes with frequency above this percentage are scored as dominant present haplotype [10]. 	
			
			*e.g.* ``--discrete_calls dominant --frequency_interval_bounds 10`` translates to: haplotype frequency < 10% = 0, haplotype frequency > 10% = 1
			
			Visualized examples of these thresholds can be found in :ref:`these tabs <SMAPhaplofreq>`.

		 .. tab:: tetraploid dosage
			
			**discrete dosage calls for tetraploids (0/1/2/3/4)**
			
			Use this option if you want to customize discrete calling thresholds, haplotype calls with frequency below the lowerbound percentage are considered not detected and receive dosage \`0´ \. Haplotype calls with frequency between the lowerbound and next percentage are considered present in 1 out of 4 alleles and scored as haplotype dosage \`1´ \, haplotype frequencies in the next frequency interval are scored as haplotype dosage \`2´ \, and so on. Haplotype calls with frequency above the upperbound percentage are considered homozygous and scored as haplotype dosage \`4´ \ default \<12.5, [12.5:37.5], [37.5:62.5], [62.5:87.5], >87.5 \. Should be written with spaces between percentages, percentages may be written as floats or as integers [12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5].
			
			*e.g.* ``--discrete_calls dosage --frequency_interval_bounds 12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5`` translates to: haplotype frequency < 12.5% = 0, haplotype frequency > 12.5% & < 37.5% = 1, haplotype frequency > 37.5.5% & < 62.5% = 2, haplotype frequency > 62.5% & < 87.5% = 3, haplotype frequency > 87.5% = 4.
			
			Visualized examples of these thresholds can be found in :ref:`these tabs <SMAPhaplofreq>`.
			
		 .. tab:: tetraploid dominant
			
			**discrete dominant calls for tetraploids (0/1)**
			
			LowerBound frequency for dominant call haplotypes. Haplotypes with frequency above this percentage are scored as dominant present haplotype [10].
			
			*e.g.* ``--discrete_calls dominant --frequency_interval_bounds 10`` translates to: haplotype frequency < 10% = 0, haplotype frequency > 10% = 1.
			
			Visualized examples of these thresholds can be found in :ref:`these tabs <SMAPhaplofreq>`.

		 .. tab:: Why dosage mask (-z)?

			| The dosage mask ``-z`` is an additional mask specifically for dosage calls in individuals. It masks loci within samples from the dataset (replaced by ``-u`` or ``--undefined_representation``) based on total dosage calls (= total allele count calculated from haplotype frequencies using frequency interval bounds). 
			| It is important to make a distinction between total dosage call and total number of unique alleles per locus per sample.
			| A tetraploid individual for example is expected to contain a total dosage call of 4 alleles, but can contain from 1 up to 4 unique (different) alleles:
			 
			===== = = = = ================= ================
			locus dosage  total dosage call number of unique
			                                alleles
			----- ------- -----------------	----------------
			.     a b c d .                 .               
			===== = = = = ================= ================
			aaaa  4 0 0 0 4                 1       
			aaab  3 1 0 0 4                 2       
			aabb  2 2 0 0 4                 2       
			abcc  1 1 2 0 4                 3       
			abcd  1 1 1 1 4                 4       
			===== = = = = ================= ================
			
			| The dosage mask ``-z`` evaluates the total dosage call against the expected number of alleles (2 in diploids, 4 in tetraploids), but does not consider the number of unique alleles.
			| In general the expected total dosage call for any locus is equal to the ploidy of the individual (except in exceptional cases such as aneuploidy).
			| Consider the examples of a single locus in the tabs below for illustration of the combined functions of ``-f`` (minimum haplotype frequency), ``--frequency_interval_bounds`` and ``-z`` (dosage_mask).
			
			.. tabs::

			   .. tab:: diploid dosage
				  
				  .. image:: ../images/window/dosage_mask_2n.png
			   
			   .. tab:: tetraploid dosage
			
				  .. image:: ../images/window/dosage_mask_4n.png
			
			
			| The dosage mask is applied last (after all other filters).
			| An adequate value for the filter ``-f`` (minimum haplotype frequency) is especially useful to reduce the number of masked calls across the sample set. 
			| For example, in Sample2 in the diploid example above a haplotype (c) persisted at 4.7%. If this had been filtered out using the option ``-f``, the other haplotype values would have been recalculated and the total dosage would have become 2 (haplotype aa).
			| Additionally the ``--frequency_interval_bounds`` can be tuned to the users liking at the hand of the :ref:`haplotype frequency graphs <SMAPhaplofreq>` in order to reduce the number of within sample loci filtered out by ``--dosage_mask``.

----

Examples
--------

:purple:`Pools`

.. tabs::

   .. tab:: diploid pool
	  
	  ::
			
			smap haplotype-window -borders /path/to/GFF/ -alignments_dir /path/to/BAM/ -reads_dir /path/to/FASTQ/ -genome /path/to/RefGenome/ --min_read_count 30 -f 2 -m 1 -p 8 --min_distinct_haplotypes 2 

   .. tab:: tetraploid pool

	  ::
			
			smap haplotype-window -borders /path/to/GFF/ -alignments_dir /path/to/BAM/ -reads_dir /path/to/FASTQ/ -genome /path/to/RefGenome/ --min_read_count 30 -f 2 -m 1 -p 8 --min_distinct_haplotypes 2 

	
:purple:`Individuals`

.. tabs::

   .. tab:: diploid individual, dominant
  
	  ::
		
			smap haplotype-window -borders /path/to/GFF/ -alignments_dir /path/to/BAM/ -reads_dir /path/to/FASTQ/ -genome /path/to/RefGenome/ --min_read_count 10 --discrete_calls dominant --frequency_interval_bounds 10 -f 5 -m 1 -p 8 --min_distinct_haplotypes 2

   .. tab:: diploid individual, dosage
  
	  ::
		
			smap haplotype-window -borders /path/to/GFF/ -alignments_dir /path/to/BAM/ -reads_dir /path/to/FASTQ/ -genome /path/to/RefGenome/ --min_read_count 10 --discrete_calls dosage --dosage_mask 2 --frequency_interval_bounds 10 10 90 90 -f 5 -m 1 -p 8 --min_distinct_haplotypes 2

  
   .. tab:: tetraploid individual, dominant
	  
	  ::
	  
			smap haplotype-window -borders /path/to/GFF/ -alignments_dir /path/to/BAM/ -reads_dir /path/to/FASTQ/ -genome /path/to/RefGenome/ --min_read_count 20 --discrete_calls dominant --frequency_interval_bounds 10 -f 5 -m 1 -p 8 --min_distinct_haplotypes 2

   .. tab:: tetraploid individual, dosage
	  
	  ::
	  
			smap haplotype-window -borders /path/to/GFF/ -alignments_dir /path/to/BAM/ -reads_dir /path/to/FASTQ/ -genome /path/to/RefGenome/ --min_read_count 20 --discrete_calls dosage --dosage_mask 4 --frequency_interval_bounds 12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5 -f 5 -m 1 -p 8 --min_distinct_haplotypes 2
	  
	  