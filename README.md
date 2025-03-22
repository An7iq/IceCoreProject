# 🧊 IceCoreProject: Volcanic Event Detection from Ice Core Records

This project aims to detect and classify volcanic eruption signals from ice core records using a combination of anomaly detection (PyOD), historical eruption databases (GVP, Sigl2015), and post-volcanic cooling evidence.

## 📁 Project Structure

```
IceCoreProject/
├── volcano_detection/
│   ├── config.py                 # File paths & config variables
│   ├── main.py                   # Main execution logic
│   ├── models/
│   │   └── pyod_detector.py      # Anomaly detection model (WIP)
│   ├── utils/
│   │   └── matching.py           # Matching functions (year-based)
│   ├── data/
│       ├── EDC_merged_4ML.csv                # Cleaned ice core dataset
│       ├── GVP_Volcano_List_Holocene.csv     # Global Volcanism Program
│       ├── sigl2015_events.csv               # Extracted from Nature 2015
│       └── sigl2015_cooling_support.csv      # Cooling evidence from Extended Data Table 5
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Containerized setup
├── docker-compose.yml           # Dev environment config
└── README.md
```

## 🧠 How it works

1. **Data Loading** – Ice core, GVP, and Sigl2015 datasets are loaded via `main.py`
2. **Preprocessing** – GVP is scored by evidence strength, Sigl is augmented with cooling support
3. **Labeling** – Each ice core year is matched against known eruptions and labeled for ML
4. **Detection (WIP)** – Anomaly detection using PyOD and XGBoost to classify signals

## 🐳 Docker Setup

```bash
docker compose build --no-cache
docker compose up
```

---

## 🧪 TODO

- [ ] Add PyOD anomaly detection
- [ ] Add XGBoost classifier with SHAP interpretation
- [ ] Align with SIGL bipolar list
- [ ] Refine reliability scoring

---

Made with ❤️ by Anqi
