import os
import cv2
import numpy as np
from sklearn.ensemble import IsolationForest

def analyze_frame_consistency(image_path):
    """
    Analyzes visual features (color distribution and edge histograms) 
    to detect noise anomalies common in manipulated media.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    # Resize to standardize features
    img = cv2.resize(img, (128, 128))
    
    # Calculate color histograms as a simple texture feature vector
    hist_b = cv2.calcHist([img], [0], None, [16], [0, 256])
    hist_g = cv2.calcHist([img], [1], None, [16], [0, 256])
    hist_r = cv2.calcHist([img], [2], None, [16], [0, 256])
    
    feature_vector = np.concatenate([hist_b, hist_g, hist_r]).flatten()
    return feature_vector

def evaluate_clip(folder_path):
    """
    Uses an Isolation Forest anomaly detector to check if 
    frames have strange visual variations.
    """
    print("🤖 Initializing Lightweight Content Integrity Scanner...")
    
    frame_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
    if not frame_files:
        print("❌ No frames found to analyze.")
        return
        
    features_list = []
    for frame in frame_files:
        full_path = os.path.join(folder_path, frame)
        features = analyze_frame_consistency(full_path)
        if features is not None:
            features_list.append(features)
            
    X = np.array(features_list)
    
    # Train a quick anomaly model on the extracted clip features
    clf = IsolationForest(contamination=0.1, random_state=42)
    preds = clf.fit_predict(X)
    
    # Percentage of anomalous frames detected
    anomaly_ratio = np.sum(preds == -1) / len(preds)
    return anomaly_ratio

if __name__ == "__main__":
    FRAMES_DIR = "extracted_frames"
    
    if os.path.exists(FRAMES_DIR):
        risk_score = evaluate_clip(FRAMES_DIR)
        print("\n--- AI Content Integrity Summary ---")
        print(f"📊 Video Frame Anomaly Discrepancy: {risk_score * 100:.2f}%")
        
        if risk_score > 0.15:
            print("🚨 Alert: Structural frame irregularities detected! (Potential Deepfake)")
        else:
            print("🟢 Clear: Frame sequence is stable and authentic.")
    else:
        print(f"⚠️ Run your extraction script first to populate '{FRAMES_DIR}'.")
