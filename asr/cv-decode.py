import os
import pandas as pd
import requests
from tqdm import tqdm

# Define the path to the CSV file and the folder containing MP3 files
print(os.getcwd())

CSV_PATH = r'C:\Users\Featherine\Downloads\HTX xData Assignment\common_voice\cv-valid-dev.csv'
SAVE_PATH = r'C:\Users\Featherine\Downloads\HTX xData Assignment\asr\cv-valid-dev-saved.csv'
AUDIO_FOLDER = r'C:\Users\Featherine\Downloads\HTX xData Assignment\common_voice\cv-valid-dev'
API_URL = 'http://localhost:8001/asr'  # Update this if your API is hosted elsewhere

def transcribe_audio(file_path):
    """
    Sends an audio file to the ASR API and returns the transcription.
    """
    try:
        with open(file_path, 'rb') as audio_file:
            files = {'file': audio_file}
            response = requests.post(API_URL, files=files)
            response.raise_for_status()
            return response.json().get('transcription', '')
    except requests.exceptions.RequestException as e:
        print(f"Error transcribing {file_path}: {e}")
        return ''

def main():
    # Load the CSV file into a DataFrame
    df = pd.read_csv(CSV_PATH)

    # Ensure there's a 'generated_text' column
    if 'generated_text' not in df.columns:
        df['generated_text'] = ''

    # Iterate over each row and transcribe the corresponding audio file
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Transcribing audio files"):
        mp3_filename = row.get('filename')
        if not mp3_filename:
            print(f"No filename found for row {index}. Skipping.")
            continue

        audio_path = os.path.join(AUDIO_FOLDER, mp3_filename)
        print(audio_path)
        if not os.path.isfile(audio_path):
            print(f"File {audio_path} does not exist. Skipping.")
            continue

        # Transcribe the audio file
        transcription = transcribe_audio(audio_path)
        print(transcription)
        df.at[index, 'generated_text'] = transcription

    # Save the updated DataFrame back to the CSV file
    df.to_csv(SAVE_PATH, index=False)
    print(f"Transcription complete. Updated CSV saved to {SAVE_PATH}.")

if __name__ == '__main__':
    main()
