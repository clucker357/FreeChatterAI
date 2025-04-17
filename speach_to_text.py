import assemblyai as aai

def speach_to_text(input_file): 
    aai.settings.api_key = "xxx"
    transcriber = aai.Transcriber()
    # 音声が含まれているファイルを処理
    transcript = transcriber.transcribe(input_file,config = aai.TranscriptionConfig(language_code="ja"))
    # transcript = transcriber.transcribe("./my-local-audio-file.wav")
    return transcript.text


if __name__ == "__main__":
    input_file = "sample_audio_data/BASIC5000_0010.wav"
    text = speach_to_text(input_file)
    print(text)
