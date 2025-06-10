# ASR Microservice with `wav2vec2-large-960h`

## 📖 Overview

This repository implements an Automatic Speech Recognition (ASR) microservice using Facebook's [`wav2vec2-large-960h`](https://huggingface.co/facebook/wav2vec2-large-960h) model. It includes functionalities for:

- Hosting an ASR inference API
- Fine-tuning on the Common Voice dataset
- Detecting hotwords and semantically similar phrases

## 📁 Repository Structure

```
├── asr/                                # Task 2: Hosted ASR microservice + inference client
│   ├── asr_api.py                      # ASR inference service
│   └── cv-decode.py                    # Transcribes Common Voice samples via the API
│
├── asr-train/                          # Task 3: Fine-tune wav2vec2-large-960h
│   ├── cv-train-2a.ipynb               # Preprocessing, training, evaluation
│   └── output/                         # Fine-tuned model artifacts
│
├── hotword-detection/                  # Task 5: Hotword detection & semantic similarity
│   ├── cv-hotword-5a.ipynb             # Hotword matching notebook
│   ├── cv-hotword-similarity-5b.ipynb  # Embedding-based similarity detection
│   └── detected.txt                    # Matched filenames
│
├── training-report.pdf                 # Task 4: Model comparison and improvement proposals
├── essay-ssl.pdf                       # Task 6: Essay on self-supervised learning
│
├── requirements.txt                    # Python dependencies
│
├── Dockerfile                          # Containerization of the ASR service
│
├── .gitignore                          # Ignored files
│
└── README.md                           # Readme file
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/featherineaugustus/Automatic-Speech-Recognition-Fine-Tuning.git
cd Automatic-Speech-Recognition-Fine-Tuning
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run ASR Service (Task 2)

```bash
cd asr
python asr_api.py
```

Test the API:

```bash
curl http://localhost:8001/ping
# Should return "pong"

curl -F "file=@path/to/file.mp3" http://localhost:8001/asr
```

Example response:

```json
{
  "transcription": "hello world",
  "duration": 3.21
}
```

## 📊 Dataset Transcription

### 4. Transcribe Common Voice Samples

```bash
cd asr
python cv-decode.py
```

- Reads `cv-valid-dev/*.mp3`
- Calls `/asr` API
- Appends `generated_text` column to `cv-valid-dev.csv`

## 🐳 Docker Usage

### 5. Containerize ASR Service

```bash
cd asr
docker build -t asr-api .
docker run -p 8001:8001 asr-api
```

- The service will run inside a container
- Processed files are deleted to maintain cleanliness

## 🧠 Fine-Tuning the Model

### 6. Fine-Tune (Task 3)

Open and run:

```bash
asr-train/cv-train-2a.ipynb
```

- 70/30 train-validation split
- Uses `wav2vec2-large-960h` as base
- Trained using PyTorch or TensorFlow
- Outputs model to `asr-train/output/`
- Logs training/validation metrics and includes test transcriptions

## 📈 Evaluate & Compare Models

### 7. Model Comparison (Task 4)

Open `training-report.pdf`:

- Compares base model vs. fine-tuned performance
- Offers improvement strategies

## 🔍 Hotword Detection

### 8. Detect Target Phrases (Task 5A)

Open:

```bash
hotword-detection/cv-hotword-5a.ipynb
```

- Searches for:
  - “be careful”
  - “destroy”
  - “stranger”
- Results saved in `detected.txt`

### 9. Semantic Similarity (Task 5B)

Open:

```bash
hotword-detection/cv-hotword-similarity-5b.ipynb
```

- Uses `hkunlp/instructor-large` for embedding-based similarity
- Adds `similarity` boolean column to `cv-valid-dev.csv`

## 📝 Extras

- `essay-ssl.pdf`: 500-word essay on self-supervised learning (Task 6)

## ✅ Status

- [x] ASR service
- [x] Common Voice decoding
- [x] Docker support
- [x] Model fine-tuning
- [x] Evaluation & report
- [x] Hotword detection
- [x] Semantic similarity detection
