# Kaggle Hub — Consolidated Environments, Datasets & Reviews

This directory centralizes all Kaggle CLI artifacts, remote GPU training setups, and verification jobs:

```text
kaggle/
├── datasets/                 # 📦 Input datasets for Kaggle remote runs
│   ├── chronic_training_backup/
│   ├── fcy_dishwasher_kaggle/
│   ├── fcy_ears_ltx_jobs/
│   ├── fcy_fingers_kaggle/
│   ├── fcy_fingers_ltx_jobs/
│   ├── fingers_anim_inputs/
│   ├── fingers_final_inputs/
│   ├── fingers_final_kit/
│   ├── kaggle_raazvik_handoff/
│   ├── kaggle_roman_short/
│   └── kaggle_roman_verify/
│
├── kernels/                  # ⚙️ Code kernels & execution scripts
│   ├── fcy_ears_edit_kernel/
│   ├── fcy_ears_edit_v2_kernel/
│   ├── fcy_ears_edit_v3_kernel/
│   ├── fcy_ears_ltx_kernel/
│   ├── fcy_fingers_ltx_kernel/
│   ├── fingers_anim_kernel/
│   ├── fingers_final_kernel/
│   └── kaggle_hold_verification/
│
└── reviews/                  # 🔍 Verification, logs & review kits
    ├── chronic_training_backup_verify/
    ├── fingers_coded_review/
    ├── fingers_final_review/
    └── kaggle_ltx_check/
```

### Usage
- To push a kernel: `kaggle kernels push -p kaggle/kernels/<kernel_folder>`
- To update/push a dataset: `kaggle datasets version -p kaggle/datasets/<dataset_folder> -m "update message"`
