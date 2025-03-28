# QR NLP AI Extension Guide

## New AI Capabilities

### 1. AI Content Analysis
```python
from qr_nlp.ai_init import QRContentAnalyzer

analyzer = QRContentAnalyzer()
results = analyzer.analyze_content("Your QR code text")
```

### 2. Custom Model Training
```bash
python train_ai_model.py --data your_data.csv --epochs 5
```

### 3. Integration Points
- Works alongside existing QR/NLP functions
- Adds advanced content understanding
- Optional module (import separately)

### 4. Requirements
```text
torch>=2.0.0
transformers>=4.30.0
datasets>=2.0.0
```

### 5. Architecture
```
QR Code → Text Extraction → NLP Processing → AI Analysis → Results
```

This supplements the existing README without modifying it.