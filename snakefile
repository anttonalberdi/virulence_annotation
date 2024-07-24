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
        expand("results/{sample}/prodigal/{sample}.genes.gff", sample=samples)

rule prodigal:
    input:
        "genomes/{sample}.fa"
    output:
        fna=temp("results/{sample}/prodigal/{sample}.genes.fna"),
        faa=temp("results/{sample}/prodigal/{sample}.genes.faa"),
        gff=temp("results/{sample}/prodigal/{sample}.genes.gff")
    params:
        jobname="{sample}.pr"
    conda:
        "environment.yml"
    threads:
        1
    resources:
        mem_gb=8,
        time='01:00:00'
    shell:
        """
        prodigal -i {input} -d {output.fna} -a {output.faa} -o {output.gff} -p meta
        """
