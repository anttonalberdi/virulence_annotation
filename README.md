# Virulence annotation
Virulence factor annotation for MAGs

### Run pipeline
On a screen session, launch the snakefile to generate the SBMLs
```
screen -S virulence
cd virulence_annotation
module purge && module load snakemake/7.20.0 mamba/1.3.1
snakemake \
  -j 20 \
  --cluster 'sbatch -o results/log/{params.jobname}-slurm-%j.out --mem {resources.mem_gb}G --time {resources.time} -c {threads} --job-name={params.jobname} -v' \
  --use-conda --conda-frontend mamba --conda-prefix conda \
  --latency-wait 600
```
