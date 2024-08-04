# Virulence annotation
Virulence factor annotation for MAGs. This pipeline based on the virulence workflow of [PathoFact](https://git-r3lab.uni.lu/laura.denies/PathoFact) classifies genes into 5 categories based on the results of [hmmer](https://www.ebi.ac.uk/Tools/hmmer/), the [random-forest classifier](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-020-00993-9) of Pathofact and [signalp](https://dtu.biolib.com/SignalP-6):

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
