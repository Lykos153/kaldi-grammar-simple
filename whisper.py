import requests
import pathlib
import io
import soundfile

import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

def whisper_dictation(utterance: bytes , **kwargs):
    with io.BytesIO(utterance) as raw, io.BytesIO() as encoded:
        data, sr = soundfile.read(raw, format="RAW", subtype="PCM_16",channels=1, samplerate=16000, dtype="int16")
        
        soundfile.write(encoded, data, sr, format="OGG", subtype="VORBIS")

        url = "http://localhost:9000"
        r = requests.post(f"{url}/asr", params={"task":"transcribe","encode":"true","output":"txt"}, files={"audio_file": encoded.getvalue()})
        return r.text

