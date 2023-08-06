<h1 align="center">
  <a href="bio2byte.be/b2btools" target="_blank" ref="noreferrer noopener">
  <img src="https://pbs.twimg.com/profile_images/1247824923546079232/B9b_Yg7n_400x400.jpg" width="224px"/>
  </a>
  <br/>
  Bio2Byte Tools
</h1>
<p align="center">This package provides you structural predictions for protein sequences made by Bio2Byte group.</p>
<p align="center">
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/version.svg" /></a>&nbsp;
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/latest_release_relative_date.svg" /></a>&nbsp;
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/platforms.svg" /></a>&nbsp;
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/downloads.svg" /></a>&nbsp;
</p>

## 🧪 List of available predictors

| Predictor | Usage       |
|-----------|-------------|
| Dynamine  | Fast predictor of protein backbone dynamics using only sequence information as input. The version here also predicts side-chain dynamics and secondary structure predictors using the same principle. |
| Disomine  | Predicts protein disorder with recurrent neural networks not directly from the amino acid sequence, but instead from more generic predictions of key biophysical properties, here protein dynamics, secondary structure and early folding. |
| EfoldMine | Predicts from the primary amino acid sequence of a protein, which amino acids are likely involved in early folding events. |
| AgMata    | Single-sequence based predictor of protein regions that are likely to cause beta-aggregation. |

**🔗 Related link:**
These listed tools and others are described on the Bio2Byte website inside the [Tools section](https://bio2byte.be/tool/).

## ⚡️Quick start
First of all, download and install the package:

```console
$ pip install b2bTools
```

Use this example as an entry point:

```python
from b2bTools import SingleSeq
single_seq = SingleSeq("/path/to/example.fasta")
single_seq.predict(tools=['dynamine', 'agmata'])
predictions = single_seq.get_all_predictions('SEQ001')

backbone_pred = predictions['SEQ001']['backbone']
sidechain_pred = predictions['SEQ001']['sidechain']
agmata_pred = predictions['SEQ001']['agmata']

plt.plot(range(len(backbone_pred)), backbone_pred, label = "Backbone")
plt.plot(range(len(backbone_pred)), sidechain_pred, label = "Sidechain")
plt.plot(range(len(backbone_pred)), agmata_pred, label = "Agmata")

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

**💡 Relevant idea:** Using the package from Jupyter Notebooks is a good idea to test the package. If you are using [Google Colab](https://colab.research.google.com), install the package directly from `pip` inside a _code block_

```python
!pip install b2bTools
```

### 🐳 Docker-way to quick start
> Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you can significantly reduce the delay between writing code and running it in production.

**🔗 Related link:** [Docker official documentation](https://www.docker.com/).

#### Preconditions
You have downloaded the source code of the Bio2Byte Tools in your local environment:

```console
$ git clone git@bitbucket.org:bio2byte/b2btools.git && cd b2btools
```

#### Steps

In order to import/export files from your host to the container and viceversa create a volume using the `-v $(pwd)/swap:/data` parameter.

**⚠️ Important note:** Be sure your input files are inside `$(pwd)/swap`.

```console
$ docker build --tag b2b-tools .
$ docker run -it -v $(pwd)/swap:/data b2b-tools -disomine -file /data/input_example.fasta -output /data/result.json -identifier test
```

**⚠️ Important note:**
- The output file titled `result.json` will be stored inshde `$(pwd)/swap`.
- The available parameters after `b2b-tools` are:

| Parameter    | Purpose                                                | Example                                |
|--------------|--------------------------------------------------------|----------------------------------------|
| `-file`      | Path to the input file                                 | `-input /path/to/input/file.fasta`     |
| `-output`    | Path to the output file (a JSON file with the results) | `-output /path/to/output/results.json` |
| `-dynamine`  | Run Dynamine predictor                                 | `-dynamine`                            |
| `-disomine`  | Run Disomine predictor                                 | `-disomine`                            |
| `-efoldmine` | Run EfoldMine predictor                                | `-efoldmine`                           |
| `-agmata`    | Run AgMata predictor                                   | `-agmata`                              |

## ⚙️ First time setup
The following steps are required in order to install the b2bTools package in your local environment:

### Conda package installation

> Conda is an open source package management system and environment management system that runs on Windows, macOS and Linux. Conda quickly installs, runs and updates packages and their dependencies. Conda easily creates, saves, loads and switches between environments on your local computer. It was created for Python programs, but it can package and distribute software for any language.

**🔗 Related link:** [Conda official documentation](https://docs.conda.io/).

To install this package with conda, run:

```console
$ conda install -c Bio2Byte b2bTools
```

**⚠️ Important note:** some Linux users might experience dependency conflicts during the conda installation. Please use the pip installation (described below) if you encounter them.

If you must use conda, use the following command:
```console
$ conda install --override-channels --channel defaults --channel conda-forge --channel Bio2Byte --channel pytorch b2btools
```

### Pip package installation
> pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes.

**🔗 Related link:** [Pip official documentation](https://pypi.org/).

```console
$ pip install b2bTools
```

## 🐍 Package usage

Given a predictor could be built on top of other, it is usual to get more output predictions than the expected:

| Predictor | Depends on            |
|-----------|-----------------------|
| Dynamine  | None                  |
| EfoldMine | [Dynamine]            |
| Disomine  | [EfoldMine, Dynamine] |
| AgMata    | [EfoldMine, Dynamine] |

### 🧭 Basic flow
This section will explain you in details the script mentioned inside the Quick start section.

1) Import the `SingleSeq` class from the `b2bTools` package:

```python
from b2bTools import SingleSeq
```

2) Instantiate an object by passing the path to the input file in FASTA format:

```python
single_seq = SingleSeq("/path/to/example.fasta")
```

3) Run the predictions you want to:

```python
single_seq.predict(tools=['dynamine', 'efoldmine'])
```

**⚠️ Important note:** These are all the available options to put inside the tools parameter:

| Predictor | string value     |
|-----------|------------------|
| Dynamine  | `"dynamine"`     |
| EfoldMine | `"efoldmine"`    |
| Disomine  | `"disomine"`     |
| AgMata    | `"agmata"`       |

4) Get the prediction values after running the selected predictors for a specific sequence identifier:

```python
predictions = single_seq.get_all_predictions('SEQ001')
```

**⚠️ Important note:** The method `get_all_predictions` will return a dictionary with the following structure:

```python
{
  "SEQUENCE_ID_000": {
    "seq": "the input sequence 0",
    "result001": [0.001, 0.002, ..., 0.00],
    "result002": [0.001, 0.002, ..., 0.00],
    "...": [...],
    "resultN": [0.001, 0.002, ..., 0.00]
  },
  "SEQUENCE_ID_001": {
    "seq": "the input sequence 1",
    "result001": [0.001, 0.002, ..., 0.00],
    "result002": [0.001, 0.002, ..., 0.00],
    "...": [...],
    "resultN": [0.001, 0.002, ..., 0.00]
  },
  "...": { ... },
  "SEQUENCE_ID_N": {
    "seq": "the input sequence N",
    "result001": [0.001, 0.002, ..., 0.00],
    "result002": [0.001, 0.002, ..., 0.00],
    "...": [...],
    "resultN": [0.001, 0.002, ..., 0.00]
  },
}
```

To know all the available result keys, please review this table:

| Predictor | Output key       | Output values (type) | Output values (example)       |
|-----------|------------------|----------------------|-------------------------------|
| None      | `"seq"`          | [Char]               | `['M', 'A', ..., 'S', 'T']`   |
| Dynamine  | `"backbone"`     | [Float]              | `[0.6786, 0.71, ..., 0.7219]` |
| Dynamine  | `"sidechain"`    | [Float]              | `[0.5823, 0.23, ..., 0.1995]` |
| Dynamine  | `"helix"`        | [Float]              | `[0.0122, 0.84, ..., 0.2345]` |
| Dynamine  | `"ppII"`         | [Float]              | `[0.0420, 0.69, ..., 0.5566]` |
| Dynamine  | `"coil"`         | [Float]              | `[0.6666, 0.13, ..., 0.9954]` |
| Dynamine  | `"sheet"`        | [Float]              | `[0.1992, 0.12, ..., 0.0020]` |
| EfoldMine | `"earlyFolding"` | [Float]              | `[0.1989, 0.08, ..., 0.0031]` |
| Disomine  | `"disoMine"`     | [Float]              | `[0.1996, 0.12, ..., 0.0019]` |
| AgMata    | `"agmata"`       | [Float]              | `[0.1954, 0.06, ..., 0.0007]` |

5) You are ready to use the sequence and predictions to work with them. Here is an example of plotting the data.

```python
backbone_pred = predictions['SEQ001']['backbone']
sidechain_pred = predictions['SEQ001']['sidechain']
agmata_pred = predictions['SEQ001']['agmata']

plt.plot(range(len(backbone_pred)), backbone_pred, label = "Backbone")
plt.plot(range(len(backbone_pred)), sidechain_pred, label = "Sidechain")
plt.plot(range(len(backbone_pred)), agmata_pred, label = "Agmata")

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

### ⌨️ Running as Python module (no Python code involved)
You are able to use this package directly from your console session with no Python code involved. Further details available on [the official Python documentation site](https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts)

```console
$ python -m b2bTools -file ./swap/input_example.fasta -dynamics -disomine -identifier test -output ./swap/result-from-package.json
```

**⚠️ Important note:**
- The output file titled `result.json` will be stored inshde `$(pwd)/swap`.
- The available parameters after `b2b-tools` are:

| Parameter    | Purpose                                                | Example                                |
|--------------|--------------------------------------------------------|----------------------------------------|
| `-file`      | Path to the input file                                 | `-input /path/to/input/file.fasta`     |
| `-output`    | Path to the output file (a JSON file with the results) | `-output /path/to/output/results.json` |
| `-dynamine`  | Run Dynamine predictor                                 | `-dynamine`                            |
| `-disomine`  | Run Disomine predictor                                 | `-disomine`                            |
| `-efoldmine` | Run EfoldMine predictor                                | `-efoldmine`                           |
| `-agmata`    | Run AgMata predictor                                   | `-agmata`                              |

### 📚 Package classes & methods
If you are interested in further details, please read the full documentation on [the Bio2Byte website](https://bio2byte.be/b2btools/package-documentation).

To generate locally the documentation you can follow the next steps described in this section.

#### Preconditions
You have downloaded the source code of the Bio2Byte Tools in your local environment:

```console
$ git clone git@bitbucket.org:bio2byte/b2btools.git && cd b2btools
```

#### Steps
1) Run the following command:
```console
$ make generate-docs
```

2) And then open folder `./wrapped_documentation`

**💡 Relevant idea:** At any moment, you can read the docs of a method invoking the `__doc__` method (e.g. `print(SingleSeq.predict.__doc__)`).

## 📖 How to cite
If you use this package or data in this package, please cite:

| Predictor | Cite                                                                                                                                                                 | Digital Object Identifier (DOI)            |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| Dynamine  | _Elisa Cilia, Rita Pancsa, Peter Tompa, Tom Lenaerts, and Wim Vranken._ From protein sequence to dynamics and disorder with DynaMine **Nature Communications 4:2741 (2013)** | https://www.nature.com/articles/ncomms3741                 |
| Disomine  | _Gabriele Orlando, Daniele Raimondi, Francesco Codice, Francesco Tabaro, Wim Vranken._ Prediction of disordered regions in proteins with recurrent Neural Networks and protein dynamics. **bioRxiv 2020.05.25.115253 (2020)**                                                        | https://www.biorxiv.org/content/10.1101/2020.05.25.115253v1   |
| EfoldMine | _Raimondi, D., Orlando, G., Pancsa, R. et al._ Exploring the Sequence-based Prediction of Folding Initiation Sites in Proteins. **Sci Rep 7, 8826 (2017)**                 | https://doi.org/10.1038/s41598-017-08366-3 |
| AgMata    | _Gabriele Orlando, Alexandra Silva, Sandra Macedo-Ribeiro, Daniele Raimondi, Wim Vranken._ Accurate prediction of protein beta-aggregation with generalized statistical potentials **Bioinformatics , Volume 36, Issue 7, 1 April 2020, Pages 2076–2081 (2020)**                                            | https://academic.oup.com/bioinformatics/article/36/7/2076/5670527      |

<!--
## 📝 License
Bio2Byte Tools is free and open-source software licensed under the Apache 2.0 License.
-->

## 📝 Terms of use

1. The Bio2Byte group aims to promote open science by providing freely available online services, database and software relating to the life sciences, with focus on proteins. Where we present scientific data generated by others we impose no additional restriction on the use of the contributed data than those provided by the data owner.
1. The Bio2Byte group expects attribution (e.g. in publications, services or products) for any of its online services, databases or software in accordance with good scientific practice. The expected attribution will be indicated in 'How to cite' sections (or equivalent).
1. The Bio2Byte group is not liable to you or third parties claiming through you, for any loss or damage.
1. Any questions or comments concerning these Terms of Use can be addressed to [Wim Vranken](mailto:wim.vranken@vub.be).

<hr/>
<p align="center">© Wim Vranken, Bio2Byte group, VUB</p>
<p align="center"><a href="https://bio2byte.be/b2btools/" target="_blank" ref="noreferrer noopener">https://bio2byte.be/b2btools/</a></p>
