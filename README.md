# Epi-foundation-models

In this Repo, we make TiRex predictions of surveillance data, extracted from the Robert Koch Institute, the public health institute of Germany. We've gathered data on case counts for a range of diseases, over a range of time, per region per week from https://survstat.rki.de/. Queries can be made here: https://survstat.rki.de/Content/Query/Create.aspx. Inside our models, we aggregate on column ``'timestamp'`` and sum column ``'cases'``, which are the only two columns that need to be present for our pipeline to work. Store the data into ``data/epidemiology`` in the project root, under ``disease-name.csv``.

Make sure to have TiRex installed! For instructions, see https://github.com/NX-AI/tirex. Then, store ``model.ckpt`` into ``src/models/NX-AI/TiRex``.

## Project Structure
```
data/
└── epidemiology
    ├── ...
    └── campylobacter.csv
src/
├── models
│   ├── basemodel.py
│   └── tirexmodel.py
├── utils
│   ├── exceptions.py
│   └── pathmanager.py
└── dataloading.py
```