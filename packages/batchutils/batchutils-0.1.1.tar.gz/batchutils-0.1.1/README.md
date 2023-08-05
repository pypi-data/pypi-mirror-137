# batchutils

## Overview

## Main Features

## Installation

## Usage

Use the following function as is.
Replace the paths with `[j1.ofile, j2.ofile, ...]`

```python
b = hb.Batch(
    default_image='hailgenetics/hail:0.2.77,
    backend=service_backend,
    name=f'combine-tsvs'
)
combined = batch_combine2(
    combine_tsvs_with_headers,
    combine_compressed_tsvs_with_headers,
    b,
    'combine-tsvs-with-headers',
    ['gs://bucket/input1.tsv', ...],
    final_location='gs://bucket/final-file.tsv.gz',
    branching_factor=25,
    suffix='.tsv.bgz')
```

`final_location` is where the output file is.

## Cite

## Maintainer

[Tarjinder Singh @ tsingh@broadinstitute.org](tsingh@broadinstitute.org)

## Acknowledgements

## Release Notes