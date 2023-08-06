# CLASSIX

#### Fast and explainable clustering based on sorting

[![Build Status](https://app.travis-ci.com/nla-group/classix.svg?token=SziD2n1qxpnRwysssUVq&branch=master)](https://app.travis-ci.com/nla-group/classix)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ClassixClustering.svg)](https://pypi.python.org/pypi/ClassixClustering/)
[![!pypi](https://img.shields.io/pypi/v/ClassixClustering?color=orange)](https://pypi.org/project/ClassixClustering/)
[![Documentation Status](https://readthedocs.org/projects/classix/badge/?version=latest)](https://classix.readthedocs.io/en/latest/?badge=latest)
[![Anaconda-Server Badge](https://anaconda.org/nla.stefan.xinye/classix/badges/version.svg)](https://anaconda.org/nla.stefan.xinye/classix)
[![Anaconda-Server Badge](https://anaconda.org/nla.stefan.xinye/classix/badges/downloads.svg)](https://anaconda.org/nla.stefan.xinye/classix)
[![Anaconda-Server Badge](https://anaconda.org/nla.stefan.xinye/classix/badges/latest_release_date.svg)](https://anaconda.org/nla.stefan.xinye/classix)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/nla-group/classix/HEAD)

CLASSIX is a fast and explainable clustering algorithm based on sorting. Here are a few highlights:

- A novel clustering algorithm which exploits the sorting of data points.
- Ability to  cluster low and high-dimensional data of arbitrary shape efficiently.
- Ability to detect and deal with outliers in the data.
- Ability to provide textual explanations for the generated clusters.
- Full reproducibility of all tests in the accompanying paper.
- Support of Cython compilation.

The detailed documentation, including tutorials, is available at [CLASSIX DOCS](https://classix.readthedocs.io/en/latest/)

``CLASSIX`` is a contrived acronym of ``CLustering by Aggregation with Sorting-based Indexing`` and the letter ``X`` for ``explainability``. CLASSIX clustering consists of two phases, namely a greedy aggregation phase of the sorted data into groups of nearby data points, followed by a merging phase of groups into clusters. The algorithm is controlled by two parameters, namely the distance parameter for the aggregation and another parameter controlling the minimal cluster size. 

## Install

CLASSIX requires the following essential dependencies for clustering:

- cython>=0.29.4
- numpy>=1.20.0
- scipy>1.6.0

while requires the following dependencies for data visualization:

- matplotlib
- scikit-learn

To install the current release via PIP use:
```
$ pip install ClassixClustering
```

Download this repository via:
```
$ git clone https://github.com/nla-group/classix.git
```
## Quick Start

```Python
from sklearn import datasets
from classix import CLASSIX

# Generate synthetic data
X, y = datasets.make_blobs(n_samples=1000, centers=2, n_features=2, random_state=1)

# Employ CLASSIX clustering
clx = CLASSIX(sorting='pca', radius=0.5, verbose=0)
clx.fit(X)
```

Get the clustering result by ``clx.labels_`` and visualize the clustering:  
```Python
plt.figure(figsize=(10,10))
plt.rcParams['axes.facecolor'] = 'white'
plt.scatter(X[:,0], X[:,1], c=clx.labels_)
plt.show()
```

## The explain method

CLASSIX provides an API for the easy visualization of clusters, and to explain the assignment of data points to their clusters.
Now we demonstrate this functionality with some simple data:

```Python
classix.explain(plot=True)
```
<img src=https://raw.githubusercontent.com/nla-group/classix/master/docs/source/images/explain_viz.png width=500 />

The output summarizes the computed groups and clusters:

```
A clustering of 5000 data points with 2 features has been performed. 
The radius parameter was set to 0.50 and MinPts was set to 0. 
As the provided data has been scaled by a factor of 1/6.01,
data points within a radius of R=0.50*6.01=3.01 were aggregated into groups. 
In total 7903 comparisons were required (1.58 comparisons per data point). 
This resulted in 14 groups, each uniquely associated with a starting point. 
These 14 groups were subsequently merged into 2 clusters. 
A list of all starting points is shown below.
----------------------------------------
 Group  NrPts  Cluster  Coordinates 
   0     398      0     -1.19 -1.09 
   1    1073      0     -0.65 -1.15 
   2     553      0     -1.17 -0.56 
   3     466      0     -0.67 -0.65 
   4       6      0     -0.19 -0.88 
   5       3      0     -0.72 -0.03 
   6       1      0     -0.22 -0.28 
   7     470      1       0.31 0.21 
   8     675      1       0.18 0.71 
   9     579      1       0.86 0.19 
  10     763      1       0.69 0.67 
  11       6      1       0.42 1.35 
  12       5      1       1.24 0.59 
  13       2      1        1.0 1.08 
----------------------------------------
In order to explain the clustering of individual data points, 
use .explain(ind1) or .explain(ind1, ind2) with indices of the data points. 
```

In the columns of the above table, ``Group`` denotes the group label, ``NrPts`` denotes the number of data points in the associated group, ``Cluster`` is the cluster label assigned to the corresponding group,  and ``Coordinates`` are the coordinates of starting point associated with the group. In order to explain the cluster assignment of a particular data point, we just have to provide its index to the explain method:

```Python
clx.explain(0,  plot=True)
```
<img src=https://raw.githubusercontent.com/nla-group/classix/master/docs/source/images/None0.png width=720 />
Output:

```
The data point 0 is in group 2, which has been merged into cluster #0.
```

```Python
clx.explain(0, 2000,  plot=True)
```
<img src=https://raw.githubusercontent.com/nla-group/classix/master/docs/source/images/None0_2000.png width=720 />
Output:

```
The data point 0 is in group 2, which has been merged into cluster 0.
The data point 2000 is in group 10, which has been merged into cluster 1.
There is no path of overlapping groups between these clusters.
```



## Citation
Here is the full CLASSIX paper. If you find CLASSIX useful in a scientific publication, we would appreciate a citation:

```bibtex
@misc{CLASSIX,
      title={Fast and explainable clustering based on sorting}, 
      author={Xinye Chen and G\"{u}ttel, Stefan},
      year={2022},
      eprint={},
      archivePrefix={arXiv},
      primaryClass={}
}
```


