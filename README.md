# 🛡️ Media Provenance & Deepfake Detection Hub

An integrated, hybrid **AI/ML** and **Blockchain** verification framework designed to safeguard digital media asset integrity and track asset provenance in real-time. Built as a Computer Science & Engineering 3rd-year (5th Semester) core project.

## 🚀 Overview
Traditional deepfake mitigation relies strictly on post-facto media forensics, which detects manipulations but fails to establish a secure historical record of origin. Conversely, blockchain verification ensures data ownership but cannot validate if the asset itself is genuine. 

This project bridges both technologies into a **dual-layer protection pipeline**:
1. **AI/ML Integrity Engine:** Ingests video streams, segments frames via OpenCV, and applies an unsupervised *Isolation Forest* anomaly tracking algorithm on localized color histograms to flag texture modifications.
2. **Blockchain Provenance Simulator:** Computes unique SHA-256 cryptographic fingerprints of uploaded media files and maps them onto an immutable decentralized state registry tracker.

---

## 🛠️ Project Architecture
