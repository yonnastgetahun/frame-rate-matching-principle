# The Frame Rate Matching Principle

**Video Signal Extraction Reliability Across Frame Rates**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18274658.svg)](https://doi.org/10.5281/zenodo.18274658)
[![Pre-registration](https://img.shields.io/badge/OSF-Pre--registered-blue)](https://osf.io/8jz3b)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Key Finding

**Signal Capture Rate (SCR) = min(f_extraction / f_source, 1.0)**

When extracting narrative signals from video using Vision-Language Models, extraction rates beyond the source video's frame rate provide no additional signal capture benefit.

## Abstract

This research establishes the Frame Rate Matching Principle for video understanding systems. Through systematic analysis of 4,429 signal extractions across 15 frame rates (0.5-240fps), we demonstrate that signal capture efficiency follows a predictable ceiling function bounded by source frame rate. Study 0 validates the principle on standard 24fps content, while Study 1 extends validation to native high frame rate (48-60fps) content, confirming the principle generalizes across frame rates.

## Repository Structure

```
frame-rate-matching-principle/
├── README.md                    # This file
├── paper/
│   ├── manuscript.md            # Full paper text
│   └── figures/                 # Publication figures (14 PNGs)
├── data/
│   ├── study0_signals.zip       # 4,042 signals from 24fps content (70MB)
│   └── study1_signals.zip       # 387 signals from HFR content (19MB)
├── analysis/
│   ├── signals_df.parquet       # Combined signal dataframe
│   ├── metrics_by_fps.parquet   # Aggregated metrics by frame rate
│   └── signal_stability.parquet # Stability analysis results
├── code/
│   ├── process_results.py       # Data processing pipeline
│   ├── statistical_analysis.py  # Statistical tests
│   └── visualize_results.py     # Figure generation
├── docs/
│   ├── reproducibility_package.md
│   ├── data_sources_acknowledgments.md
│   └── osf_deviation_justification.md
└── reproduction/
    ├── verify_completion.py     # Verification script
    ├── request_academic.md      # HFR video acquisition guide
    └── video_manifest.csv       # Study 1 video metadata
```

## Quick Start

```python
import pandas as pd
import zipfile

# Load analysis results
df = pd.read_parquet('analysis/signals_df.parquet')

# Extract signal data
with zipfile.ZipFile('data/study0_signals.zip', 'r') as z:
    z.extractall('signals/')

# View metrics by frame rate
metrics = pd.read_parquet('analysis/metrics_by_fps.parquet')
print(metrics[['fps', 'mean_signals', 'scr']])
```

## Key Results

### Study 0: Standard Video (24fps source)
- **N = 4,042** signal extractions
- **15 frame rates** tested (0.5-240fps)
- Signal saturation confirmed at source frame rate
- **Effect size:** η² = 0.847 (large)

### Study 1: HFR Validation (48-60fps source)
- **N = 387** signals from native HFR content
- Principle validated: higher native fps = higher saturation threshold
- Cross-dataset replication successful

### The Principle Visualized

```
Signal Capture Rate (SCR)
    1.0 |............●━━━━━━━━━━━━━━━━
        |        ●
        |      ●
        |    ●
        |  ●
    0.0 |●
        └─────────────────────────────→
         0    12    24    48    96   fps
              ↑
         Source FPS (ceiling)
```

## Pre-registration

This study was pre-registered on OSF: [https://osf.io/8jz3b](https://osf.io/8jz3b)

## Citation

```bibtex
@misc{getahun2026framerate,
  author       = {Getahun, Yonnas},
  title        = {The Frame Rate Matching Principle: Video Signal
                  Extraction Reliability Across Frame Rates},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/yonnastgetahun/frame-rate-matching-principle}},
  doi          = {10.5281/zenodo.18274658}
}
```

## Links

- **Pre-registration:** [osf.io/8jz3b](https://osf.io/8jz3b)
- **GitHub:** [github.com/yonnastgetahun](https://github.com/yonnastgetahun)
- **LinkedIn:** [linkedin.com/in/yonnasgetahun](https://linkedin.com/in/yonnasgetahun)
- **Twitter/X:** [x.com/yonnastgetahun](https://x.com/yonnastgetahun)

## Related Projects

This research is part of the Visual Narrator project:
- **Model:** [HuggingFace Visual Narrator](https://huggingface.co/spaces/yonnastgetahun/visual-narrator-comparison)
- **Live Demo:** [visual-narrator-demo.vercel.app](https://visual-narrator-demo.vercel.app)

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Data sources are acknowledged in [docs/data_sources_acknowledgments.md](docs/data_sources_acknowledgments.md).
