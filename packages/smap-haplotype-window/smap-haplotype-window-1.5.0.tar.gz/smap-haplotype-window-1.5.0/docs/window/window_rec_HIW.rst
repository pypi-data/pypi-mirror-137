####################################
Recommendations & Troubleshooting
####################################


.. _SMAPwindowrec:

Recommendations
----------------

Minimum read depth filter -c
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accurate haplotype frequency estimation requires a minimum read count which is different between sample type (individuals and Pool-Seq) and ploidy levels.

.. tabs::

   .. tab:: diploid individual
   
	  | For diploid individuals the odds of seeing both alleles **at least once** (which are the same if homozygous and different if heterozygous) is equal to 1 minus the odds of only seeing one allele.  
	  
	  .. image:: ../images/window/formula_diploid_1.png
	     :width: 200
		 
	  | with c the read count. This is visualized in the image below as the green line, the black lines represent a 95% chance (6 reads) and a 99% chance (8 reads).
	  | However due to the prevalence of sequencing errors it is advisable to see each allele **at least twice**, represented by the blue line. The formula for this curve is an extension of the one used for 1 sighting, on top of that formula, all combinations wherein an allele is seen only once are removed.
	  
	  .. image:: ../images/window/formula_diploid_2.png
	     :width: 300
		 
	  | For two sightings per allele, the 95% boundary is 9 reads and the 99% boundary is 12 reads.
	  | For >2 sightings per allele one can use the function:
	  
	  .. image:: ../images/window/formula_diploid_3.png
	     :width: 300
		 
	  # .. image:: ../images/sites/SMAP_haplotype_diploid_ind_read_count_requirement.png

   .. tab:: tetraploid individual

	  For tetraploid individuals, calculating the odds of seeing all 4 alleles at least once is a little more complicated than in diploids. A function that approximates this distribution is given by `Joly et al. (2006) <https://bsapubs.onlinelibrary.wiley.com/doi/epdf/10.3732/ajb.93.3.412>`_ as 
	  
	  .. image:: ../images/window/formula_tetraploid.png
	     :width: 200
	  
	  and results in a 95% chance to see all alleles at read count 15 and a 99% chance at around read count 20 (only the full black line should be considered). Figure and additional explanation `Griffin et al., 2011 <https://bmcbiol.biomedcentral.com/articles/10.1186/1741-7007-9-19>`_.
	  Just like in diploids, in order to see at least 2 copies of each allele it would be best to add a few reads to the results acquired for single copy sightings. 
	  
	  # .. image:: ../images/sites/SMAP_haplotype_tetraploid_ind_read_count_requirement.png

   .. tab:: Pool-Seq

	  For Pool-Seq data analysis the number of required reads depends on the ploidy as well as the number of samples in a pool, see `Raineri et al. (2012) <https://www.researchgate.net/publication/230884099_SNP_calling_by_sequencing_pooled_sample>`_, `Gautier et al. (2014) <https://www.researchgate.net/publication/237015120_Estimation_of_population_allele_frequencies_from_next-generation_sequencing_data_Pool-versus_individual-based_genotyping>`_, and `Schlötterer et al. (2014) <https://www.researchgate.net/publication/266029234_Sequencing_pools_of_individuals-mining_genome-wide_polymorphism_data_without_big_funding_Nature_Rev_Genet>`_. 

Therefore, the user is advised to use the read count threshold to ensure that the reported haplotype frequencies per locus are indeed based on sufficient read data. If a locus has a total haplotype count below the user-defined minimal read count threshold (option ``-c``; default 0, recommended 10 for diploid individuals, 20 for tetraploid individuals, and 30 for pools) then all haplotype observations are removed for that sample.

----

Troubleshooting
----------------

FASTQ Sequence identifier format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| SMAP haplotype-window does not support old Illumina sequence ID's like the example entry shown below, the reason being that the # blocks the read ID's cluster coordinates. In order to solve this it suffices to replace the # with a single whitespace, for example with the command ``sed -i 's|#| |g' *.fq`` .
| Also note that the quality encoding in the example below is in the old Phred+64 format, this does not present any issue.

.. tabs::

   .. tab:: old Seq_ID example
   
      ::
	  
			@ILLUMINA-52179E_0009:8:1:1057:18188#CAGATC/1
			ATCGCGGGCAACGGCAGCGCCAGNTAGGGCGGCGCCGGCTACGTTTCCTG
			+ILLUMINA-52179E_0009:8:1:1057:18188#CAGATC/1
			dcddddcZ`^Lb^bbccddTb^cBTLTbSPL_F_]Y`b_YL]\ILK_\[Z

   .. tab:: old Seq_ID example fixed
   
      ::
	  
			@ILLUMINA-52179E_0009:8:1:1057:18188 CAGATC/1
			ATCGCGGGCAACGGCAGCGCCAGNTAGGGCGGCGCCGGCTACGTTTCCTG
			+ILLUMINA-52179E_0009:8:1:1057:18188 CAGATC/1
			dcddddcZ`^Lb^bbccddTb^cBTLTbSPL_F_]Y`b_YL]\ILK_\[Z	  
	  
Output
~~~~~~

| When opening the output (Tab delimited) .tsv files in Microsoft Excel, one might encounter the error that certain rows contain 1 column and others 2 columns, making it impossible to use the built-in option Data -> Text to Columns.
| In order to circumvent this issue, it is best to open a new Excel-file and use the option Data -> Get Data -> From Text/CSV.

----

FAQ
----------------

text

