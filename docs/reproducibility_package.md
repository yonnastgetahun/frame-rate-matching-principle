# Research Reproducibility Package

## Visual Narrator Research: FPS Signal Extraction Studies

**Version**: 1.0
**Date**: January 13, 2026
**Repository**: [To be assigned - OSF/Zenodo]

---

## Overview

This package provides complete reproducibility materials for two studies investigating frame rate effects on video signal extraction for Audio Description and Audio Cinema applications.

| Study | Research Question | Videos | Tasks | Status |
|-------|-------------------|--------|-------|--------|
| **Study 0** | FPS thresholds for signal extraction | 303 | 4,545 | Complete |
| **Study 1** | Frame Rate Matching Principle | 222 clips | 888 | Complete |

---

## Package Contents (Hosted on OSF/Zenodo)

### What We Host (~2 GB total)

```
reproducibility_package/
├── README.md                           # This document
├── LICENSE                             # CC-BY-4.0
│
├── data/
│   ├── study0/
│   │   ├── signals/                    # 4,619 extracted signal JSONs (~600 MB)
│   │   ├── analysis/                   # Aggregated results, tables
│   │   └── metadata/
│   │       ├── video_manifest.csv      # Video IDs, sources, metadata
│   │       └── download_results.json   # Acquisition timestamps
│   │
│   ├── study1/
│   │   ├── signals/                    # 818 extracted signal JSONs (~700 MB)
│   │   ├── analysis/                   # SCR metrics, statistical results
│   │   │   ├── all_results.csv
│   │   │   ├── scr_metrics.csv
│   │   │   ├── statistical_results.json
│   │   │   └── tables/                 # Summary tables 1-4
│   │   ├── figures/                    # Visualization PNGs
│   │   └── metadata/
│   │       ├── study1_clip_registry.json
│   │       └── master_registry.json
│   │
│   └── shared/
│       └── signal_schema.json          # Signal format specification
│
├── code/
│   ├── extraction/
│   │   ├── frame_extractor.py          # Core extraction logic
│   │   ├── signal_extractors/          # YOLO, scene detection, etc.
│   │   ├── study0_modal.py             # Study 0 Modal runner
│   │   └── study1_modal.py             # Study 1 Modal runner
│   │
│   ├── analysis/
│   │   ├── study0_analysis.py          # FPS threshold analysis
│   │   └── study1_phase3_analysis.py   # SCR analysis
│   │
│   └── utils/
│       └── verification.py             # Frame rate verification
│
├── reproduction/
│   ├── study0/
│   │   ├── README.md                   # Study 0 reproduction guide
│   │   ├── download_ave.py             # AVE dataset downloader
│   │   ├── download_finevideo.py       # FineVideo downloader
│   │   ├── download_produced_digital.py # Commercials/MVs downloader
│   │   └── video_urls.csv              # All source URLs/IDs
│   │
│   ├── study1/
│   │   ├── README.md                   # Study 1 reproduction guide
│   │   ├── download_youtube_hfr.sh     # YouTube HFR content
│   │   ├── download_arri_samples.sh    # ARRI camera tests
│   │   ├── request_academic.md         # BVI-HFR, LIVE-YT-HFR, UVG access
│   │   └── video_ids.csv               # YouTube IDs, academic refs
│   │
│   ├── verify_downloads.py             # Verify frame rates
│   └── environment.yml                 # Conda environment
│
└── docs/
    ├── osf_preregistration.md          # Original pre-registration
    ├── osf_deviation_justification.md  # Documented deviations
    ├── phase1_assessment.md            # Dataset quality assessment
    ├── phase2_final_report.md          # Extraction completion report
    └── signal_taxonomy.md              # Signal definitions
```

### What We DON'T Host (Reproduction Required)

| Data Type | Size | Why Not Hosted | How to Reproduce |
|-----------|------|----------------|------------------|
| Study 0 raw videos | ~890 MB | Copyright (YouTube) | `reproduction/study0/` scripts |
| Study 1 raw videos | ~456 GB | Copyright + size | `reproduction/study1/` scripts |
| Modal volume data | ~500 GB | Redundant | Re-run extraction |

---

## Study 0: FPS Signal Extraction Thresholds

### Research Question
> At what frame rate (0.5-240 fps) can video signals be reliably extracted for Audio Description and Audio Cinema generation?

### Dataset Composition

| Tier | Source | Videos | Resolution | Content Type |
|------|--------|--------|------------|--------------|
| **Web/UGC** | FineVideo (HuggingFace) | 170 | 360p | User-generated |
| **Produced Digital** | YouTube (curated) | 68 | 720-1080p | Commercials, MVs |
| **Cinema** | AVE Dataset | 65 | 720p | Film clips |
| **Total** | | **303** | | |

### Reproduction Steps

#### 1. Download Videos

```bash
# FineVideo (Web/UGC tier)
python reproduction/study0/download_finevideo.py \
  --output data/videos/finevideo \
  --count 170

# Produced Digital (manually curated URLs)
python reproduction/study0/download_produced_digital.py \
  --urls reproduction/study0/video_urls.csv \
  --output data/videos/produced_digital

# AVE (Cinema tier)
python reproduction/study0/download_ave.py \
  --output data/videos/ave
```

#### 2. Verify Downloads

```bash
python reproduction/verify_downloads.py \
  --manifest data/study0/metadata/video_manifest.csv \
  --video-dir data/videos
```

#### 3. Run Extraction (requires Modal account)

```bash
modal run code/extraction/study0_modal.py \
  --video-dir data/videos \
  --output-dir results/study0 \
  --fps-levels 0.5,1,2,3,5,8,10,12,15,24,30,45,60,120,240
```

### Data Sources

| Source | Access Method | License |
|--------|---------------|---------|
| FineVideo | `huggingface.co/datasets/HuggingFaceFV/finevideo` | CC-BY |
| AVE Dataset | `github.com/dawitmureja/AVE` | Research use |
| Produced Digital | YouTube (individual URLs in `video_urls.csv`) | Fair use (research) |

---

## Study 1: Frame Rate Matching Principle Validation

### Research Question
> Is Signal Capture Rate (SCR) maximized when extraction FPS matches native source FPS?

### Hypothesis
> **H1**: For high frame rate (HFR) video content, signal extraction quality peaks when the extraction frame rate matches the source's native frame rate.

### Dataset Composition

| Bracket | Source | Clips | Native FPS | Status |
|---------|--------|-------|------------|--------|
| **48-50fps** | YouTube trailers, ARRI | 21 | 47.95-50 | Exploratory |
| **60fps** | YouTube sports/cinema | 163 | 59.94-60 | Confirmatory |
| **120fps** | UVG, BVI-HFR, LIVE-YT-HFR | 38 | 120 | Confirmatory |
| **Total** | | **222** | | |

### Key Results

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Native SCR | 1.000 ± 0.000 | Perfect signal capture at native FPS |
| Non-native SCR | 0.832 ± 0.119 | 16.8% signal loss when mismatched |
| t-statistic | 18.68 | Highly significant |
| p-value | 1.57 × 10⁻⁶³ | p < 0.0001 |
| Cohen's d | 1.99 | Very large effect size |
| **Hypothesis** | **SUPPORTED** | |

### Reproduction Steps

#### 1. Request Academic Dataset Access

| Dataset | Contact | Expected Wait |
|---------|---------|---------------|
| UVG | ultravideo.fi | Public access |
| BVI-HFR | University of Bristol | 1-2 weeks |
| LIVE-YT-HFR | Dr. Pavan Madhusudana (UT Austin) | 1-2 weeks |

See `reproduction/study1/request_academic.md` for email templates.

#### 2. Download YouTube Content

```bash
# YouTube HFR trailers and sports
./reproduction/study1/download_youtube_hfr.sh \
  --ids reproduction/study1/video_ids.csv \
  --output data/videos/study1

# ARRI camera samples (FTP)
./reproduction/study1/download_arri_samples.sh \
  --output data/videos/study1/arri
```

#### 3. Verify Frame Rates

```bash
# All videos must pass frame rate verification
python reproduction/verify_downloads.py \
  --manifest data/study1/metadata/master_registry.json \
  --verify-fps
```

Accepted frame rates:
- 48fps: `48/1` or `48000/1001`
- 50fps: `50/1`
- 60fps: `60/1` or `60000/1001`
- 120fps: `120/1` or `120000/1001`

#### 4. Run Extraction

```bash
modal run code/extraction/study1_modal.py \
  --registry data/study1/metadata/study1_clip_registry.json \
  --output-dir results/study1 \
  --fps-levels 15,24,30,native
```

#### 5. Run Analysis

```bash
python code/analysis/study1_phase3_analysis.py \
  --results-dir results/study1 \
  --output-dir analysis/study1
```

### Data Sources

| Source | Access | License | Native FPS |
|--------|--------|---------|------------|
| UVG Dataset | ultravideo.fi | CC-BY | 120fps |
| BVI-HFR | bristol.ac.uk (request) | Academic | 120fps |
| LIVE-YT-HFR | live.ece.utexas.edu (password) | Academic | 120fps |
| YouTube HFR | Individual video IDs | Fair use | 48-60fps |
| ARRI AMIRA | ARRI FTP | Demo footage | 48-50fps |

---

## Signal Schema

All extracted signals follow this JSON schema:

```json
{
  "video_id": "string",
  "fps": "float",
  "duration": "float",
  "frame_count": "integer",
  "scene_signals": {
    "transitions": ["array of timestamps"],
    "scene_count": "integer",
    "scene_durations": ["array of floats"]
  },
  "character_signals": {
    "person_counts": ["array of integers per frame"],
    "total_detections": "integer"
  },
  "visual_signals": {
    "object_detections": "integer",
    "dominant_objects": ["array of strings"]
  },
  "atmosphere_signals": {
    "color_histogram": ["array"],
    "brightness_mean": "float"
  },
  "action_signals": {
    "motion_intensity": ["array of floats"],
    "motion_mean": "float"
  },
  "temporal_signals": {
    "flow_magnitude": ["array of floats"],
    "flow_mean": "float"
  }
}
```

---

## Verification Protocol

### Frame Rate Verification

```bash
# Verify native frame rate using ffprobe
ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate \
  -of default=noprint_wrappers=1:nokey=1 [filename]
```

### Checksum Verification

All hosted files include SHA256 checksums in `checksums.sha256`:

```bash
sha256sum -c checksums.sha256
```

---

## Software Requirements

### Environment Setup

```bash
# Create conda environment
conda env create -f reproduction/environment.yml
conda activate visual-narrator

# Or pip install
pip install -r reproduction/requirements.txt
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.10+ | Runtime |
| OpenCV | 4.8+ | Frame extraction |
| ultralytics | 8.0+ | YOLO object detection |
| scenedetect | 0.6+ | Scene boundary detection |
| pandas | 2.0+ | Data analysis |
| scipy | 1.11+ | Statistical tests |
| modal | 0.50+ | Cloud compute |

### Hardware Requirements

| Study | Local Analysis | Full Reproduction |
|-------|----------------|-------------------|
| Study 0 | 8 GB RAM, 50 GB disk | Modal account (~$600) |
| Study 1 | 8 GB RAM, 50 GB disk | Modal account (~$300) |

---

## Citation

If you use this data or code, please cite:

```bibtex
@misc{visualnarrator2026,
  title={Frame Rate Effects on Video Signal Extraction for Audio Description},
  author={[Author Names]},
  year={2026},
  publisher={OSF},
  doi={[DOI]}
}
```

---

## License

- **Code**: MIT License
- **Data (extracted signals)**: CC-BY-4.0
- **Documentation**: CC-BY-4.0
- **Raw videos**: Subject to original source licenses (not redistributed)

---

## Contact

For questions about reproduction:
- **Dataset access issues**: [email]
- **Code questions**: [GitHub Issues]
- **Academic collaboration**: [email]

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-13 | Initial release with Study 0 + Study 1 |

