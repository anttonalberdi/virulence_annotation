# Virulence annotation
Virulence factor annotation for MAGs. This pipeline based on PathoFact classifies genes into 5 categories based on the results of hmmer, a random-forest classifier and signalp:

- 1: Secreted Virulence factor
- 2: Non-secreted Virulence factor
- 3: Potential Secreted Virulence factor
- 4: Potential Non-secreted Virulence factor
- 5: Not a Virulence factor

### Run pipeline
On a screen session, launch the snakefile to annotate virulence factors:

```
screen -S virulence
cd virulence_annotation
mamba env create -f workflow/envs/environment.yml
conda activate virulence_annotation_env
snakemake \
  -j 20 \
  --cluster 'sbatch -o results/log/{params.jobname}-slurm-%j.out --mem {resources.mem_gb}G --time {resources.time} -c {threads} --job-name={params.jobname} -v' \
  --latency-wait 600
```
