######
# Virulence factor annotation generation script
# Antton alberdi
# 2023/07/24
# Description: the pipeline annotates virulence factors from MAGs
######

# 1) Copy this snakefile to the working directory
# 2) Store the genome sequences in the folder 'genomes' in the working directory with extension .fa, and without any "." or "/" in the file name besides the .fa.
# 3) Launch the snakemake using the following code:
# snakemake -j 20 --cluster 'sbatch -o logs/{params.jobname}-slurm-%j.out --mem {resources.mem_gb}G --time {resources.time} -c {threads} --job-name={params.jobname} -v'   --use-conda --conda-frontend mamba --conda-prefix conda --latency-wait 600

#List sample wildcards
samples, = glob_wildcards("genomes/{sample}.fa")

#Expand target files
rule all:
    input:
        expand("results/{sample}/hmmer/{sample}.csv", sample=samples),
        expand("results/{sample}/signalp/{sample}.csv", sample=samples),
        expand("results/{sample}/rf/{sample}.csv", sample=samples)

# Predict genes in genome sequences. 
rule prodigal:
    input:
        "genomes/{sample}.fa"
    output:
        fna="results/{sample}/prodigal/{sample}.fna",
        faa="results/{sample}/prodigal/{sample}.faa",
        gff="results/{sample}/prodigal/{sample}.gff"
    params:
        jobname="{sample}.pr"
    threads:
        1
    resources:
        mem_gb=8,
        time=30
    shell:
        """
        module load prodigal/2.6.3
        prodigal -i {input} -d {output.fna} -a {output.faa} -o {output.gff}
        """

# Search for virulence factors' hmm profiles in the PathoFact database
rule hmmscan:
    input:
        query="results/{sample}/prodigal/{sample}.faa",
        database="/projects/mjolnir1/people/jpl786/PathoFact/databases/virulence/Virulence_factor.hmm"
    output:
        "results/{sample}/hmmer/{sample}.hmmscan"
    params:
        jobname="{sample}.hm"
    threads:
        4
    resources:
        mem_gb=8,
        time=30
    shell:
        """
        module load hmmer/3.3.2
        hmmsearch --cpu {threads} --noali --notextw --tblout {output} {input.database} {input.query}
        """

# Reformat output into a tabular format
rule hmm_reformat:
    input:
        "results/{sample}/hmmer/{sample}.hmmscan"
    output:
        "results/{sample}/hmmer/{sample}.tsv"
    params:
        jobname="{sample}.rf"
    threads:
        1
    resources:
        mem_gb=8,
        time=5
    shell:
        """
        sed '/^#/ d' {input} | sed 's/ \+/;/g' | cut -d ';' -f 1,3,5,6 | tr ';' '\t' > {output}
        """

# Assign virulence classification to annotations
rule virulence_classification:
    input:
        hmm="results/{sample}/hmmer/{sample}.tsv",
        positive="/projects/mjolnir1/people/jpl786/PathoFact/databases/models_and_domains/positive_domains.tsv",
        negative="/projects/mjolnir1/people/jpl786/PathoFact/databases/models_and_domains/negative_domains.tsv",
        shared="/projects/mjolnir1/people/jpl786/PathoFact/databases/models_and_domains/shared_domains.tsv"
    output:
        "results/{sample}/hmmer/{sample}.csv"
    params:
        jobname="{sample}.cl"
    threads:
        1
    resources:
        mem_gb=8,
        time=5
    script:
        "scripts/virulence_classification.py"

# Predict virulence from RF models
rule AAC:
    input:
        "results/{sample}/prodigal/{sample}.faa"
    output:
        "results/{sample}/rf/{sample}_AAC.txt"
    params:
        jobname="{sample}.rf1"
    threads:
        1
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        python scripts/AAC.py --file {input} --out {output}
        """

rule DPC:
    input:
        "results/{sample}/prodigal/{sample}.faa"
    output:
        "results/{sample}/rf/{sample}_DPC.txt"
    params:
        jobname="{sample}.rf2"
    threads:
        1
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        python scripts/DPC.py --file {input} --out {output}
        """

rule CTDC:
    input:
        "results/{sample}/prodigal/{sample}.faa"
    output:
        "results/{sample}/rf/{sample}_CTDC.txt"
    params:
        jobname="{sample}.rf3"
    threads:
        1
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        python scripts/CTDC.py --file {input} --out {output}
        """

rule CTDT:
    input:
        "results/{sample}/prodigal/{sample}.faa"
    output:
        "results/{sample}/rf/{sample}_CTDT.txt"
    params:
        jobname="{sample}.rf4"
    threads:
        1
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        python scripts/CTDT.py --file {input} --out {output}
        """

rule CTDD:
    input:
        "results/{sample}/prodigal/{sample}.faa"
    output:
        "results/{sample}/rf/{sample}_CTDD.txt"
    params:
        jobname="{sample}.rf5"
    threads:
        1
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        python scripts/CTDD.py --file {input} --out {output}
        """

rule merge_RF:
    input:
        AAC="results/{sample}/rf/{sample}_AAC.txt",
        DPC="results/{sample}/rf/{sample}_DPC.txt",
        CTDC="results/{sample}/rf/{sample}_CTDC.txt",
        CTDT="results/{sample}/rf/{sample}_CTDT.txt",
        CTDD="results/{sample}/rf/{sample}_CTDD.txt",
        model="/projects/mjolnir1/people/jpl786/PathoFact/scripts/Virulence_factor_model.sav"
    output:
        all="results/{sample}/rf/{sample}_all.txt",
        final="results/{sample}/rf/{sample}.csv"
    params:
        jobname="{sample}.rf"
    threads:
        1
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        cat {input.AAC} {input.DPC} {input.CTDC} {input.CTDT} {input.CTDD} > {output.all}
        python scripts/virulence_prediction.py {output.all} {output.final} {input.model}
        """

# Define whether toxins are secreted or non-secreted.
rule signalp:
    input:
        "results/{sample}/prodigal/{sample}.faa"
    output:
        "results/{sample}/signalp/{sample}.csv"
    params:
        jobname="{sample}.sp",
        outputdir="results/{sample}/signalp/output"
    threads:
        8
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        module load signalp/6h
        signalp6 --fastafile {input} --output_dir {params.outputdir} --write_procs {threads}
        cp {params.outputdir}/output.gff3 {output}
        """
