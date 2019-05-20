
Data
----

Patient data should be organized in subfolders as described in the tree example below.
- Raw Nerualynx or Blackrock files are in /hospital/patient/Raw
- The transformed raw into mat files are in /hospital/patient/ChannelsCSC
- Epochs are spike_clusters are subfolders containing extracted features, later used for decoding analyses and ERSPs.

```bash
Data/
└── UCLA
    ├── patient_479
    │   ├── ChannelsCSC
    │   ├── Epochs
    │   ├── Logs
    │   ├── Raw
    │   ├── Spike_clusters
    │   └── Spike_clusters_Ariel
    ├── patient_482
    │   ├── ChannelsCSC
    │   ├── Logs
    │   ├── Raw
    │   │   └── nev_files
    │   └── Spike_clusters
    ├── patient_487
    │   ├── ChannelsCSC
    │   ├── Epochs
    │   ├── Logs
    │   └── Raw
    ├── patient_493
    │   ├── ChannelsCSC
    │   ├── Logs
    │   └── Raw
    ├── patient_502
    │   ├── ChannelsCSC
    │   ├── log_patient
    │   ├── Logs
    │   └── Raw
    │       └── nev_files
    ├── patient_504
    │   └── Logs
    │       └── original
    └── patient_505
        ├── ChannelsCSC
        ├── Logs
        └── Raw
```
l