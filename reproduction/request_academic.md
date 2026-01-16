# Academic Dataset Access Requests

## Study 1: 120fps Academic Datasets

To reproduce Study 1, you need access to three academic HFR datasets. Below are instructions and email templates for each.

---

## 1. UVG Dataset (Public Access)

**URL**: https://ultravideo.fi/#testsequences

**Access**: Public download - no request needed

**Download**:
```bash
# 4K 120fps sequences
wget https://ultravideo.fi/video/Beauty_3840x2160_120fps_420_8bit_YUV_RAW.7z
wget https://ultravideo.fi/video/Bosphorus_3840x2160_120fps_420_8bit_YUV_RAW.7z
wget https://ultravideo.fi/video/HoneyBee_3840x2160_120fps_420_8bit_YUV_RAW.7z
wget https://ultravideo.fi/video/Jockey_3840x2160_120fps_420_8bit_YUV_RAW.7z
wget https://ultravideo.fi/video/ReadySetGo_3840x2160_120fps_420_8bit_YUV_RAW.7z
wget https://ultravideo.fi/video/ShakeNDry_3840x2160_120fps_420_8bit_YUV_RAW.7z
wget https://ultravideo.fi/video/YachtRide_3840x2160_120fps_420_8bit_YUV_RAW.7z
```

**Citation**:
```bibtex
@article{mercat2020uvg,
  title={UVG dataset: 50/120fps 4K sequences for video codec analysis and development},
  author={Mercat, Alexandre and Viitanen, Marko and Vanne, Jarno},
  journal={ACM MMSys},
  year={2020}
}
```

---

## 2. BVI-HFR Dataset (Request Required)

**Institution**: University of Bristol, Vision Institute

**URL**: https://data.bris.ac.uk/data/dataset/18fhbi1yl5j152aob7pyz1pb8

**Contact**: Dr. Fan Zhang (fan.zhang@bristol.ac.uk)

### Email Template

```
Subject: Request for BVI-HFR Dataset Access - Academic Research

Dear Dr. Zhang,

I am a researcher at [Your Institution] conducting a study on frame rate effects
in video signal extraction for accessibility applications (Audio Description).

I am writing to request access to the BVI-HFR dataset for use in my research
project titled "[Your Project Title]".

Research Purpose:
- Investigating the Frame Rate Matching Principle for video signal extraction
- Testing whether signal quality is maximized when extraction FPS matches source FPS
- The dataset's 120fps sequences are essential for testing the high-frame-rate bracket

I confirm that:
1. The dataset will be used solely for academic research
2. The data will not be redistributed
3. All publications will cite the original dataset paper

Please let me know if you require any additional information.

Best regards,
[Your Name]
[Your Institution]
[Your Email]
```

**Expected Response Time**: 1-2 weeks

**Citation**:
```bibtex
@article{mackin2018bvi,
  title={A study of subjective video quality at various frame rates},
  author={Mackin, Alex and Zhang, Fan and Bull, David R},
  journal={IEEE ICIP},
  year={2018}
}
```

---

## 3. LIVE-YT-HFR Dataset (Password Required)

**Institution**: University of Texas at Austin, LIVE Lab

**URL**: https://live.ece.utexas.edu/research/LIVE_YT_HFR/index.html

**Contact**: Dr. Pavan C. Madhusudana (pavan.madhusudana@utexas.edu)

### Email Template

```
Subject: Request for LIVE-YT-HFR Dataset Password - Academic Research

Dear Dr. Madhusudana,

I am a researcher at [Your Institution] studying video quality and frame rate
effects for accessibility applications.

I am writing to request the download password for the LIVE-YT-HFR dataset
for use in my research project on frame rate matching in video signal extraction.

Research Purpose:
- Investigating optimal frame rates for video signal extraction
- Testing the Frame Rate Matching Principle hypothesis
- Your dataset's 120fps YouTube sequences provide essential ground truth data

I confirm that:
1. The dataset will be used solely for non-commercial academic research
2. The data will not be redistributed
3. All publications will properly cite your work

Thank you for making this valuable resource available to the research community.

Best regards,
[Your Name]
[Your Institution]
[Your Email]
```

**Expected Response Time**: 1-2 weeks

**Note**: The download page requires a password. Once granted, download the VP9
lossless 120fps versions for maximum quality.

**Citation**:
```bibtex
@article{madhusudana2021live,
  title={Subjective and objective quality assessment of high frame rate videos},
  author={Madhusudana, Pavan C and Birkbeck, Neil and Wang, Yilin and Adsumilli, Balu and Bovik, Alan C},
  journal={IEEE Access},
  year={2021}
}
```

---

## Timeline Summary

| Dataset | Access Type | Expected Wait | Files |
|---------|-------------|---------------|-------|
| UVG | Public | Immediate | 7 sequences |
| BVI-HFR | Request | 1-2 weeks | 22 sequences |
| LIVE-YT-HFR | Password | 1-2 weeks | 16 sequences |

**Total**: 45 sequences at 120fps

---

## After Receiving Access

Once you have all datasets, verify frame rates:

```bash
for f in *.mp4 *.webm *.yuv; do
  echo "$f: $(ffprobe -v error -select_streams v:0 \
    -show_entries stream=r_frame_rate \
    -of default=noprint_wrappers=1:nokey=1 "$f")"
done
```

All files should show `120/1` or `120000/1001` (119.88fps).
