import socket
import pyaudio
import wave
import struct
import socket
import pickle

class asr_model():
	def __init__(self):
		self.a = 1
	def record(self):
		print('recording')
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 48000
		CHUNK = 512
		RECORD_SECONDS = 1.5
		WAVE_OUTPUT_FILENAME = "./cmd.wav"
		audio = pyaudio.PyAudio()
		
		# start Recording
		stream = audio.open(format=FORMAT, channels=CHANNELS,
						rate=RATE, input=True,
						frames_per_buffer=CHUNK)

		frames = []
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)

		# stop Recording
		stream.stop_stream()
		stream.close()
		audio.terminate()

		return [CHANNELS, audio.get_sample_size(FORMAT), RATE, frames]
	
	def send(self, sData):
		print('sending')
		HOST = '140.112.21.80'
		PORT = 8001
		skClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		skClient.connect((HOST, PORT))
		for i in range(3):
			data_string = pickle.dumps([sData[i]])
			skClient.send(data_string)
		
			rData = skClient.recv(25536)
			data_arr = pickle.loads(rData)
			
		for ss in sData[3]:
			data_string = pickle.dumps(ss)
			skClient.send(data_string)
		
			rData = skClient.recv(25536)
			data_arr = pickle.loads(rData)
		
		data_string = pickle.dumps(['Done'])
		skClient.send(data_string)
		while True:
			rData = skClient.recv(25536)
			res = pickle.loads(rData)
			if len(res) == 2 and res[1] == 'Done':
				break
		
		skClient.close()
		
		print(res[0])
		return res[0]
	
	def recognize(self):
		rec = self.record()
		res = self.send(rec)
		if res == 'zero':
			return 0
		elif res == 'one':
			return 1
		elif res == 'two':
			return 2
		elif res == 'three':
			return 3
		elif res == 'four':
			return 4
		elif res == 'five':
			return 5
		elif res == 'six':
			return 6
		elif res == 'seven':
			return 7
		elif res == 'eight':
			return 8
		elif res == 'nine':
			return 9
		else:
			return 10

if __name__ == '__main__':
	m = asr_model()
	r = m.recognize()