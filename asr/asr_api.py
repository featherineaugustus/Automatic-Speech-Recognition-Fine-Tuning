# asr/asr_api.py
from flask import Flask, request, jsonify
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torchaudio
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load pre-trained model and tokenizer
model_name = "facebook/wav2vec2-base-960h"
# model_name = "facebook/wav2vec2-large-960h"
tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/asr', methods=['POST'])
def asr():
    try:
        print('Load Data')
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files['file']
        print(file)

    except Exception as e:
        app.logger.error(f"Error in /asr route: {e}")
        return jsonify(error="Internal Server Error"), 500
    
    # file_path = os.path.join("uploads", file.filename)
    # file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    # file.save(file_path)

    # Load and process audio
    print('Process Audio')
    # waveform, sample_rate = torchaudio.load(file_path)
    waveform, sample_rate = torchaudio.load(file)
    # Resample if necessary
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
    input_values = tokenizer(waveform.squeeze().numpy(), return_tensors="pt").input_values

    # Perform inference
    logits = model(input_values).logits
    predicted_ids = logits.argmax(dim=-1)
    transcription = tokenizer.decode(predicted_ids[0])

    # Calculate duration
    duration = waveform.shape[1] / 16000.0

    # Cleanup
    # os.remove(file_path)

    return jsonify({"transcription": transcription, "duration": str(duration)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)