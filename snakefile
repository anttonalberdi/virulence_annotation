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

localrules: virulence_classification

#Expand target files
rule all:
    input:
        expand("results/{sample}/hmmer/{sample}.csv", sample=samples)

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

rule signalp:
    input:
        "results/{sample}/prodigal/{sample}.faa"
    output:
        "results/{sample}/signalp/{sample}_summary.signalp6"
    params:
        jobname="{sample}.sp",
        outputdir="results/{sample}/signalp"
    threads:
        8
    resources:
        mem_gb=8,
        time=120
    shell:
        """
        module load signalp/6.0h.fast
        signalp6 --fastafile {input} --output_dir {params.outputdir} --write_procs {threads} --torch_num_threads {threads}
        """
