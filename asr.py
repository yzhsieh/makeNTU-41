import speech_recognition as sr
class asr_model():
	def __init__(self):
		self.r = sr.Recognizer()
	
	def recognize(self):
		with sr.Microphone() as source:
			self.r.adjust_for_ambient_noise(source)
			print('Say something!')
			audio = self.r.listen(source)
		
		try:
			sttTXT_org = self.r.recognize_google(audio)
			print("Google Speech Recognition thinks you said: " + sttTXT_org)
			if sttTXT_org == 'zero' or sttTXT_org == 'Zero' or sttTXT_org == '0':
				return 0
			elif sttTXT_org == 'one' or sttTXT_org == 'One' or sttTXT_org == '1':
				return 1
			elif sttTXT_org == 'two' or sttTXT_org == 'Two' or sttTXT_org == '2':
				return 2
			else:
				return 9
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			return 9
		except sr.RequestError as e:
			print('Could not request results from Google Speech Recognition service; {0}'.format(e))
			return 9