# Qiime2 App

![Qiime2 App](./doc/screenshot.png)

### Server configuration

Create a `~/Qiime2App` in the user's home directory, which is the root directory of the Qiime2App.
A typical directory structure is shown below:

```
~/Qiime2App/
├── .profile
├── fastq/
├── qiime2_pipeline-1.0.0/
├── sample-sheet.csv
├── silva-138-99-nb-classifier.qza
├── silva-138-99-sequences.qza
└── silva-138-99-taxonomy.qza
```

The `.profile` defines all things needed to be activated to run the `qiime2_pipeline-1.0.0`.
An example of the `.profile` is shown below:

```bash
source $HOME/anaconda3/bin/activate qiime2-amplicon-2024.2
export QT_QPA_PLATFORM=offscreen
export UNIFRAC_USE_GPU=N
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

Other files/directories are described as follows:

- `fastq/`: Directory containing all fastq files
- `qiime2_pipeline-1.0.0/`: The executable `qiime2_pipeline` which can be downloaded from [here](https://github.com/linyc74/qiime2_pipeline/releases)
- `sample-sheet.csv`: The sample sheet file required by the `qiime2_pipeline`
- `silva-138-99-nb-classifier.qza`: The classifier file required for NB classifier
- `silva-138-99-sequences.qza`: The reference sequence file required for Vsearch classification
- `silva-138-99-taxonomy.qza`: The reference taxonomy file required for Vsearch classification
