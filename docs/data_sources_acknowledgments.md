# Data Sources and Acknowledgments

## Visual Narrator Research: Complete Source Attribution

This document provides comprehensive attribution for all data sources used across Study 0 (FPS Signal Extraction Thresholds) and Study 1 (Frame Rate Matching Principle Validation).

---

## Study 0: FPS Signal Extraction Thresholds

**Total Videos**: 303

### 1. FineVideo Dataset (Web/UGC Tier)

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 170 |
| **Institution** | Hugging Face |
| **URL** | https://huggingface.co/datasets/HuggingFaceFV/finevideo |
| **License** | CC-BY |
| **Resolution** | 360p (authentic UGC quality) |
| **Content Type** | User-generated web content across 7 categories |

**Citation**:
```bibtex
@dataset{finevideo2024,
  title={FineVideo: A Large-Scale Dataset for Fine-Grained Video Understanding},
  author={Hugging Face Team},
  year={2024},
  publisher={Hugging Face},
  url={https://huggingface.co/datasets/HuggingFaceFV/finevideo}
}
```

**Acknowledgment**: We thank Hugging Face for making the FineVideo dataset publicly available under CC-BY license.

---

### 2. AVE Dataset (Cinema Tier)

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 65 (55 core + 10 validation) |
| **Institution** | Originally sourced from MovieClips YouTube |
| **URL** | https://github.com/dawitmureja/AVE |
| **License** | Research use |
| **Resolution** | 720p |
| **Content Type** | Film clips (Drama, Action, Comedy, Thriller, Romance) |

**Citation**:
```bibtex
@inproceedings{tian2018ave,
  title={Audio-Visual Event Localization in Unconstrained Videos},
  author={Tian, Yapeng and Shi, Jing and Li, Bochen and Duan, Zhiyao and Xu, Chenliang},
  booktitle={European Conference on Computer Vision (ECCV)},
  year={2018}
}
```

**Acknowledgment**: We thank Yapeng Tian et al. for creating the AVE dataset and making it available for research purposes.

---

### 3. Produced Digital (Professional Tier)

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 68 (37 commercials + 31 music videos) |
| **Sources** | YouTube (Super Bowl ads, Cannes Lions, Vevo, official artist channels) |
| **License** | Fair use (research) |
| **Resolution** | 720p-1080p |
| **Content Type** | High-production commercials and music videos |

**Specific Sources**:
- **Commercials (37)**: Super Bowl advertisement archives, Cannes Lions award winners, brand official channels
- **Music Videos (31)**: Vevo, official artist YouTube channels

**Acknowledgment**: Commercial and music video content was sourced from YouTube for academic research purposes under fair use provisions. We acknowledge the original creators and distributors of this content.

---

## Study 1: Frame Rate Matching Principle Validation

**Total Videos**: 138 (222 clips)

### 4. UVG Dataset (Ultra Video Group)

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 7 sequences |
| **Institution** | Tampere University, Finland |
| **URL** | https://ultravideo.fi/#testsequences |
| **License** | CC-BY |
| **Resolution** | 3840×2160 (4K) |
| **Frame Rate** | 120fps |
| **Format** | HEVC/H.265 |

**Sequences Used**:
- Beauty, Bosphorus, HoneyBee, Jockey, ReadySetGo, ShakeNDry, YachtRide

**Citation**:
```bibtex
@inproceedings{mercat2020uvg,
  title={UVG Dataset: 50/120fps 4K Sequences for Video Codec Analysis and Development},
  author={Mercat, Alexandre and Viitanen, Marko and Vanne, Jarno},
  booktitle={ACM Multimedia Systems Conference (MMSys)},
  pages={297--302},
  year={2020},
  doi={10.1145/3339825.3394937}
}
```

**Acknowledgment**: We thank the Ultra Video Group at Tampere University for providing high-quality 4K 120fps test sequences under CC-BY license.

---

### 5. BVI-HFR Dataset (Bristol Vision Institute)

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 22 sequences |
| **Institution** | University of Bristol, UK |
| **URL** | https://data.bris.ac.uk/data/dataset/18fhbi1yl5j152aob7pyz1pb8 |
| **License** | Academic research |
| **Resolution** | 1920×1080 (1080p) |
| **Frame Rate** | 120fps |
| **Format** | H.264 |

**Sequences Used**:
- bobblehead, books, bouncyball, catch, catch_track, cyclist, flowers, golf_side, guitar_focus, hamster, joggers, lamppost, leaves_wall, library, martial_arts, plasma, pond, pour, sparkler, typing, water_ripples, water_splashing

**Citation**:
```bibtex
@inproceedings{mackin2018study,
  title={A Study of Subjective Video Quality at Various Frame Rates},
  author={Mackin, Alex and Zhang, Fan and Bull, David R.},
  booktitle={IEEE International Conference on Image Processing (ICIP)},
  pages={3523--3527},
  year={2018},
  doi={10.1109/ICIP.2018.8451755}
}
```

**Acknowledgment**: We thank Dr. Fan Zhang and the Bristol Vision Institute for providing access to the BVI-HFR dataset for academic research.

---

### 6. LIVE-YT-HFR Dataset (University of Texas at Austin)

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 16 sequences |
| **Institution** | University of Texas at Austin, LIVE Lab |
| **URL** | https://live.ece.utexas.edu/research/LIVE_YT_HFR/index.html |
| **License** | Academic research (password-protected) |
| **Resolution** | 1920×1080 to 3840×2160 |
| **Frame Rate** | 120fps |
| **Format** | VP9 lossless |

**Sequences Used**:
- 1Runner, 3Runners, Flips, Hurdles, LongJump, bobblehead, books, bouncyball, catchtrack, cyclist, hamster, lamppost, leaves, library, pour, watersplashing

**Citation**:
```bibtex
@article{madhusudana2021subjective,
  title={Subjective and Objective Quality Assessment of High Frame Rate Videos},
  author={Madhusudana, Pavan C. and Birkbeck, Neil and Wang, Yilin and Adsumilli, Balu and Bovik, Alan C.},
  journal={IEEE Access},
  volume={9},
  pages={108069--108082},
  year={2021},
  doi={10.1109/ACCESS.2021.3100292}
}
```

**Acknowledgment**: We thank Dr. Pavan C. Madhusudana and the LIVE Laboratory at UT Austin for granting access to the LIVE-YT-HFR dataset. Special thanks for providing the download password on January 12, 2026.

---

### 7. ARRI AMIRA Sample Footage

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 12 clips (6 @ 48fps + 6 @ 50fps) |
| **Institution** | ARRI (Arnold & Richter Cine Technik) |
| **URL** | ARRI FTP server (demo footage) |
| **License** | Demo/evaluation footage |
| **Resolution** | 1920×1080 to 2048×1152 |
| **Frame Rate** | 48fps and 50fps |
| **Format** | ProRes |

**Sequences Used**:
- F001C001-F001C006 (48fps), G001C001-G001C006 (50fps)

**Citation**:
```bibtex
@misc{arri2014amira,
  title={ARRI AMIRA Camera Sample Footage},
  author={{ARRI AG}},
  year={2014},
  howpublished={ARRI FTP Server},
  note={Professional camera demonstration footage}
}
```

**Acknowledgment**: We thank ARRI AG for providing professional camera test footage demonstrating native 48fps and 50fps capture capabilities.

---

### 8. YouTube HFR Content

| Attribute | Value |
|-----------|-------|
| **Videos Used** | 81 videos |
| **Brackets** | 48-50fps (9) + 60fps (72) |
| **License** | Fair use (research) |
| **Content Types** | Film trailers, sports broadcasts, gaming/esports |

**Content Categories**:

#### 48fps Film Content (9 videos)
- The Hobbit trilogy trailers (Peter Jackson, Warner Bros.)
- Avatar: The Way of Water trailers (James Cameron, 20th Century Studios)
- Peter Jackson HFR demonstration footage

#### 60fps Sports Content (72 videos)
| Sport | Videos | Sources |
|-------|--------|---------|
| NFL | 4 | Official NFL YouTube |
| NBA | 3 | Official NBA YouTube |
| NHL | 5 | Official NHL YouTube |
| MLB | 5 | Official MLB YouTube |
| Tennis | 4 | ATP/WTA official channels |
| Olympics | 2 | Olympic Channel |
| UFC | 1 | UFC official channel |
| F1 | 2 | Formula 1 official |
| Esports/Gaming | 14 | CS:GO, various esports |
| Cinema (60fps) | 32 | Billy Lynn, Gemini Man trailers, HFR demos |

**Acknowledgment**: YouTube content was sourced for academic research purposes under fair use provisions. We acknowledge the original content creators, studios, and sports leagues for producing high frame rate content.

---

## Software and Infrastructure Acknowledgments

### 9. Modal Cloud Computing

| Attribute | Value |
|-----------|-------|
| **Service** | Modal Labs cloud compute platform |
| **URL** | https://modal.com |
| **Usage** | Distributed video processing and signal extraction |
| **Compute Cost** | ~$600 total across both studies |

**Acknowledgment**: Signal extraction was performed using Modal's serverless cloud computing platform, which enabled efficient parallel processing of 4,545+ extraction tasks.

---

### 10. YOLO (You Only Look Once)

| Attribute | Value |
|-----------|-------|
| **Version** | YOLOv8 (Ultralytics) |
| **URL** | https://github.com/ultralytics/ultralytics |
| **License** | AGPL-3.0 |
| **Usage** | Object and person detection for signal extraction |

**Citation**:
```bibtex
@software{jocher2023yolov8,
  title={Ultralytics YOLOv8},
  author={Jocher, Glenn and Chaurasia, Ayush and Qiu, Jing},
  year={2023},
  url={https://github.com/ultralytics/ultralytics},
  license={AGPL-3.0}
}
```

---

### 11. PySceneDetect

| Attribute | Value |
|-----------|-------|
| **Version** | 0.6+ |
| **URL** | https://github.com/Breakthrough/PySceneDetect |
| **License** | BSD-3-Clause |
| **Usage** | Scene boundary and transition detection |

**Citation**:
```bibtex
@software{pyscenedetect,
  title={PySceneDetect: Video Scene Cut Detection and Analysis Tool},
  author={Breakthrough},
  url={https://github.com/Breakthrough/PySceneDetect},
  license={BSD-3-Clause}
}
```

---

### 12. OpenCV

| Attribute | Value |
|-----------|-------|
| **Version** | 4.8+ |
| **URL** | https://opencv.org |
| **License** | Apache 2.0 |
| **Usage** | Frame extraction, optical flow, color analysis |

**Citation**:
```bibtex
@article{bradski2000opencv,
  title={The OpenCV Library},
  author={Bradski, Gary},
  journal={Dr. Dobb's Journal of Software Tools},
  year={2000}
}
```

---

## Summary Table: All Data Sources

| Source | Study | Videos | FPS | Type | License | Citation Required |
|--------|-------|--------|-----|------|---------|-------------------|
| **FineVideo** | 0 | 170 | Various | Web/UGC | CC-BY | Yes |
| **AVE Dataset** | 0 | 65 | Various | Cinema | Research | Yes |
| **Produced Digital** | 0 | 68 | Various | Professional | Fair use | Acknowledge |
| **UVG Dataset** | 1 | 7 | 120fps | Academic | CC-BY | Yes |
| **BVI-HFR** | 1 | 22 | 120fps | Academic | Research | Yes |
| **LIVE-YT-HFR** | 1 | 16 | 120fps | Academic | Research | Yes |
| **ARRI AMIRA** | 1 | 12 | 48-50fps | Professional | Demo | Acknowledge |
| **YouTube HFR** | 1 | 81 | 48-60fps | Mixed | Fair use | Acknowledge |

**Total Unique Sources**: 8

---

## Paper Acknowledgments Section (Template)

```
ACKNOWLEDGMENTS

We gratefully acknowledge the following data sources and their contributors:

For Study 0 (FPS Signal Extraction), we thank Hugging Face for the FineVideo dataset
(CC-BY), and Yapeng Tian et al. for the AVE dataset.

For Study 1 (Frame Rate Matching Principle), we thank: the Ultra Video Group at
Tampere University for the UVG 4K 120fps sequences (CC-BY); Dr. Fan Zhang and the
Bristol Vision Institute for access to the BVI-HFR dataset; and Dr. Pavan C.
Madhusudana and the LIVE Laboratory at UT Austin for granting access to the
LIVE-YT-HFR dataset.

We also acknowledge ARRI AG for professional camera demonstration footage, and the
various content creators, studios, and sports leagues whose high frame rate content
on YouTube enabled testing across diverse content types.

Signal extraction was performed using Modal cloud computing. Object detection used
YOLOv8 (Ultralytics), scene detection used PySceneDetect, and frame processing used
OpenCV.

This research was conducted under fair use provisions for academic purposes.
```

---

## Contact Information for Dataset Access

| Dataset | Contact | Access Type |
|---------|---------|-------------|
| FineVideo | N/A (public) | Direct download |
| AVE | GitHub | Direct download |
| UVG | N/A (public) | Direct download |
| BVI-HFR | fan.zhang@bristol.ac.uk | Request access |
| LIVE-YT-HFR | pavan.madhusudana@utexas.edu | Request password |

---

**Document Version**: 1.0
**Last Updated**: January 13, 2026
