import speech_recognition as sr 
import os 
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(audio_chunks_dir, path, language):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub

    pydub.AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
    sound = AudioSegment.from_wav(path)  
    print(len(sound))
    print(sound.dBFS)
    
    # split audio sound where silence is 700 miliseconds or more and get chunks
    # chunks = split_on_silence(sound,
    #     # experiment with this value for your target audio file
    #     min_silence_len = 200,
    #     # adjust this per requirement
    #     silence_thresh = sound.dBFS-20,
    #     # keep the silence for 1 second, adjustable as well
    #     keep_silence=100,
    # )

    chunks = split_on_silence(sound, silence_thresh=-80)    
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(audio_chunks_dir, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                # text = r.recognize_google(audio_listened, language='fr-FR', show_all=False)
                text = r.recognize_google(audio_listened, language=language, show_all=False)
            except sr.UnknownValueError as e:
                # print("Error:", str(e))
                pass
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text


if __name__=="__main__":
    filename = "out/2022-12-25_20:38:06_86471571031465984.wav"
    get_large_audio_transcription(filename)
