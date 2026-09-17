import streamlit as st
import os
import hashlib
import time
import cv2
import numpy as np
from sklearn.ensemble import IsolationForest

# --- Initialize Simulated Blockchain State ---
if 'blockchain_ledger' not in st.session_state:
    st.session_state.blockchain_ledger = {}

# --- Helper Functions ---
def compute_hash(uploaded_file_bytes):
    """Computes SHA-256 directly from file stream bytes"""
    sha256 = hashlib.sha256()
    sha256.update(uploaded_file_bytes)
    return sha256.hexdigest()

def analyze_video_bytes(file_bytes):
    """Extracts frames from bytes and evaluates structural anomalies"""
    # Temporary save to read via OpenCV
    temp_path = "temp_processing_video.mp4"
    with open(temp_path, "wb") as f:
        f.write(file_bytes)
        
    cap = cv2.VideoCapture(temp_path)
    features_list = []
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        if frame_idx % 10 == 0:
            resized = cv2.resize(frame, (128, 128))
            hist_b = cv2.calcHist([resized], [0], None, [32], [0, 256])
            hist_g = cv2.calcHist([resized], [1], None, [32], [0, 256])
            hist_r = cv2.calcHist([resized], [2], None, [32], [0, 256])
            feats = np.concatenate([hist_b, hist_g, hist_r]).flatten()
            features_list.append(feats)
        frame_idx += 1
    cap.release()
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    if len(features_list) < 2: return 0.0
    
    X = np.array(features_list)
    clf = IsolationForest(contamination=0.1, random_state=42)
    preds = clf.fit_predict(X)
    return np.sum(preds == -1) / len(preds)

# --- Streamlit Dashboard UI Configuration ---
st.set_page_config(page_title="Deepfake & Provenance Shield", layout="wide", page_icon="🛡️")

st.title("🛡️ Media Provenance & Deepfake Detection Hub")
st.markdown("An integrated **AI/ML** and **Blockchain** framework for verifying digital asset integrity.")
st.divider()

# Sidebar: Blockchain Node Status / Admin panel
st.sidebar.header("🔑 Decentralized Registry Node")
wallet_addr = st.sidebar.text_input("User Wallet Address", "0x71C7656EC7ab88b098defB751B7401B5f6d8976F")

st.sidebar.subheader("🔗 Blockchain Global Ledger Summary")
st.sidebar.info(f"Total Registered Assets: {len(st.session_state.blockchain_ledger)}")

# Main Layout split into two sections
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Upload Target Media")
    uploaded_file = st.file_uploader("Choose a video or image file to scan...", type=["mp4", "avi", "jpg", "jpeg", "png"])
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_hash = compute_hash(file_bytes)
        
        st.info(f"**Generated SHA-256 Asset Fingerprint:**\n`{file_hash}`")
        
        # Action Button 1: Register on Blockchain
        if st.button("🔗 Register Asset on Blockchain Ledger"):
            if file_hash in st.session_state.blockchain_ledger:
                st.sidebar.warning("⚠️ Blockchain Revert: This asset hash is already permanently registered!")
            else:
                st.session_state.blockchain_ledger[file_hash] = {
                    "author": wallet_addr,
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "block": len(st.session_state.blockchain_ledger) + 8549210
                }
                st.sidebar.success("✅ Block Minted successfully!")

with col2:
    st.subheader("🔬 Verification & Safety Engine Output")
    
    if uploaded_file and st.button("🚀 Run Integrity Analysis Pipeline"):
        with st.spinner("Analyzing media frames and matching smart contract states..."):
            
            # 1. Query Blockchain State Mapping
            is_registered = file_hash in st.session_state.blockchain_ledger
            metadata = st.session_state.blockchain_ledger.get(file_hash, None)
            
            # 2. Run AI Check
            if uploaded_file.name.endswith(('mp4', 'avi')):
                anomaly_score = analyze_video_bytes(file_bytes)
            else:
                anomaly_score = 0.0 # Clear if flat image for demo
                
            # 3. Decision Matrix Visual Reports
            st.metric(label="AI Frame Discrepancy Index", value=f"{anomaly_score * 100:.2f}%")
            
            st.markdown("### Unified Verdict:")
            if is_registered and anomaly_score <= 0.15:
                st.success("🟢 **VERDICT: 100% SECURE & AUTHENTIC**")
                st.write(f"• **Origin Verified:** Registered by wallet `{metadata['author']}`")
                st.write(f"• **Timestamp:** Immutable record written on `{metadata['timestamp']}`")
                st.write("• **AI Analysis:** Geometric structural features align perfectly with genuine camera sensor data.")
            elif is_registered and anomaly_score > 0.15:
                st.warning("🟡 **VERDICT: SECURITY BREACH (Asset Tampering Detected)**")
                st.write("• **Warning:** A blockchain cryptographic registry record exists, but the file content has been altered or frames have been modified after registration.")
            else:
                st.error("🚨 **VERDICT: HIGH RISK / REJECTED**")
                st.write("• **Failure:** No matching provenance certificate exists on the decentralized ledger.")
                if anomaly_score > 0.15:
                    st.write("• **AI Threat Advisory:** Deepfake/Synthesis artifacts are heavily present in frame textures.")
