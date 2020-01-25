"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os

from flask import send_from_directory
from google.cloud import texttospeech

from lib.py.core.traces import print_exception_traces
from lib.py.misc.gcloud import service_key


def tts(text="Hello world"):
    with service_key() as service_key_unsecure:
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_key_unsecure
            # Instantiates a client
            client = texttospeech.TextToSpeechClient()
            # Set the text input to be synthesized
            synthesis_input = texttospeech.types.SynthesisInput(text=text)

            # Build the voice request, select the language code ("en-US") and the ssml
            # voice gender ("neutral")
            voice = texttospeech.types.VoiceSelectionParams(
                language_code='en-US',
                ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

            # Select the type of audio file you want returned
            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3)

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = client.synthesize_speech(synthesis_input, voice, audio_config)

            return str(response.audio_content)
        except Exception as e:
            print_exception_traces(e)


def tts_mp3(text="Hello world"):
    from lib.py.flask_app.app import app

    res = tts(text)

    # file_name = str(uuid.uuid4()) + ".mp3"
    file_name = text + ".mp3"
    file_path = os.path.join(app.static_folder, file_name)
    save_mp3(bytes(res, encoding='utf8'), file_path)

    print("Sending file path for tts: " + file_path)
    file_path = send_from_directory(app.static_folder, file_name)
    print("Sending file path for tts: " + file_path)

    return file_path


def save_mp3(data, path="output.mp3"):
    with open(os.path.join(path), 'wb') as out:
        # Write the response to the output file.
        out.write(data)


def play(file_path):
    import vlc
    p = vlc.MediaPlayer(file_path)
    p.play()
    # p.stop()
    pass


if __name__ == "__main__":
    res = tts("who's there in hut")
    save_mp3(res, "output.mp3")
    play("output.mp3")
