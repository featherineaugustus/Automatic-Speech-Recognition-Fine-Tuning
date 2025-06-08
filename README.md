# ASR Microservice with wav2vec2-large-960h

## Overview

This repository implements an Automatic Speech Recognition (ASR) microservice using Facebook's `wav2vec2-large-960h` model. It includes functionalities for transcribing audio files, fine-tuning the model on the Common Voice dataset, and detecting specific hotwords.


   ```bash
   ├── asr/                         # Task 2: Hosted ASR microservice + inference client
   │   ├── asr_api.py              # ASR inference service using wav2vec2-large-960h
   │   ├── cv-decode.py           # Script to transcribe Common Voice samples via the service
   │   ├── Dockerfile             # Containerization of the ASR service
   │   └── ...                     # e.g. requirements.txt if separate
   ├── asr-train/                  # Task 3: Fine‑tune wav2vec2-large-960h
   │   ├── cv-train-2a.ipynb       # Jupyter notebook: preprocessing, training, evaluation
   │   └── output/                 # Model artifacts (wav2vec2-large-960h-cv)
   ├── hotword-detection/          # Task 5: Hot‑word detection & semantic similarity
   │   ├── cv-hotword-5a.ipynb     # Hot‑word detection notebook
   │   ├── detected.txt            # Filenames containing hot words
   │   └── cv-hotword-similarity-5b.ipynb  # Notebook for semantic similarity detection
   ├── training-report.pdf         # Task 4: Comparison & improvement proposals
   ├── essay-ssl.pdf               # Task 6: 500-word self-supervised learning essay
   ├── Dockerfile             # Containerization of the ASR service
   ├── requirements.txt            # Python dependencies
   ├── .gitignore                  # Files to be ignored (e.g. model artifacts, __pycache__, LFS pointers)
   └── README.md                   # This instructions file
   ```


## Setup Instructions

1. **Clone the repository**:

   ```bash
   https://github.com/featherineaugustus/Automatic-Speech-Recognition-Fine-Tuning
   cd Automatic-Speech-Recognition-Fine-Tuning

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Run ASR Service (Task 2)**:
   ```bash
   cd asr
   python asr_api.py

   curl http://localhost:8001/ping # should return "pong".
   curl -F "file=@path/to/file.mp3" http://localhost:8001/asr

Response JSON contains:
- "transcription": the model output text
- "duration": file duration in seconds

4. **Transcribe Common Voice Dataset**:
   ```bash
   cd asr
   python cv-decode.py

Reads cv-valid-dev/*.mp3, calls the /asr API.
- Appends a generated_text column to cv-valid-dev.csv.
- Saves the augmented CSV file in the same folder.

5. **Containerize ASR Service**:
   ```bash
   cd asr
   docker build -t asr-api .
   docker run -p 8001:8001 asr-api

The ASR service runs within a Docker container, deleting processed files to maintain cleanliness.

6. **Fine-Tune ASR Model (Task 3)**:
   ```bash
   asr-train/cv-train-2a.ipynb

- Implements 70/30 train-validation split on cv-valid-train.csv + audio.
- Uses wav2vec2-large-960h as a base, fine-tunes with PyTorch or TensorFlow.
- Documents preprocessing, tokenizer, feature extraction, hyperparameters.
- Visualizes training and validation metrics and reports interpretations.
- Outputs the fine-tuned model: wav2vec2-large-960h-cv. Also includes transcription on test set and performance metrics.

7. **Compare Models (Task 4)**:
See training-report.pdf:
- Comparison against original wav2vec2 output on dev set.

8. **Compare Models (Task 4)**:
   ```bash
   hotword-detection/cv-hotword-5a.ipynb

- Searches for occurrences of words: “be careful”, “destroy”, “stranger”
- Outputs matched filenames in detected.txt.

   ```bash
   hotword-detection/cv-hotword-similarity-5b.ipynb

- Uses hkunlp/instructor-large for embedding-based similarity.
- Appends Boolean similarity column to cv-valid-dev.csv.