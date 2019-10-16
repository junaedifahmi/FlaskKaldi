import pyaudio
import wave
from array import array
import tqdm

class RecordingVoice(object):
    """docstring for RecodingVoice."""

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 1

    def record(self):
        stream = self.audio.open(format=self.format, channels=self.channels,
                          rate=self.rate,
                          input=True,
                          frames_per_buffer=self.CHUNK)
        frames = []
        FILE_NAME = '/media/juunnn/EXOLyxion1/Intership/FlaskKaldi/model/tmp.wav'
        for i in tqdm.tqdm(range(0, int(self.rate/self.CHUNK*self.RECORD_SECONDS))):
            data = stream.read(self.CHUNK)
            data_chunk = array('h', data)
            vol = max(data_chunk)
            if(vol>0):
                frames.append(data)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        self.save(frames, FILE_NAME)
        return FILE_NAME

    def save(self, frames, FILE_NAME):
        wavfile=wave.open(FILE_NAME, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(self.audio.get_sample_size(self.format))
        wavfile.setframerate(self.rate)
        wavfile.writeframes(b''.join(frames)) #append frames recorded to file
        wavfile.close()
        return True


def record_sound():

    r = RecordingVoice()
    return r.record()


if __name__ == '__main__':
    r = RecordingVoice()
    print(r.record())
