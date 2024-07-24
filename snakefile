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
        expand("results/{sample}/hmmer/{sample}.hmmscan", sample=samples)

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
        time='01:00:00'
    shell:
        """
        module load prodigal/2.6.3
        prodigal -i {input} -d {output.fna} -a {output.faa} -o {output.gff}
        """

rule hmmscan:
    input:
        query="results/{sample}/prodigal/{sample}.faa"
        database="/projects/mjolnir1/people/jpl786/PathoFact/databases/virulence/Virulence_factor.hmm"
    output:
        "results/{sample}/hmmer/{sample}.hmmscan"
    params:
        jobname="{sample}.hm"
    threads:
        4
    resources:
        mem_gb=8,
        time='01:00:00'
    shell:
        """
        module load hmmer/3.3.2
        hmmsearch --cpu {threads} --noali --notextw --tblout {output} {input.database} {input.query}
        """
