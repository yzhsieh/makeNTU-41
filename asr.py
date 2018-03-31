import speech_recognition as sr
'''
import torch
from command_loader import CommandLoader
from model import LeNet, VGG
from torch.autograd import Variable

class_set = ['bed', 'bird', 'cat', 'dog', 'down', 'eight', 'five', 'four', 'go', 'happy', 'house', 'left', 'marvin', 'nine', 'no', 'off', 'on', 'one', 'right', 'seven', 'sheila', 'six', 'stop', 'three', 'tree', 'two', 'up', 'wow', 'yes', 'zero']
# Training settings
test_path = '../SSR2/test/four/0ea0e2f4_nohash_0.wav'
test_batch_size = 100
arc = 'LeNet'
cuda = True
seed = 1234
# feature extraction options
window_size = .02
window_stride = .01
window_type = 'hamming'
normalize = True

cuda = cuda and torch.cuda.is_available()
torch.manual_seed(seed)
if cuda:
	torch.cuda.manual_seed(seed)

# build model
if arc == 'LeNet':
	model = LeNet()
elif arc.startswith('VGG'):
	model = VGG(arc)
else:
	model = LeNet()

if cuda:
	model = torch.nn.DataParallel(model).cuda()

class asr_model():
	def __init__(self):
		model.load_state_dict(torch.load('./checkpoint/ckpt-'+arc+'.t7'))

	def recognize(self):
		# loading data
		data = CommandLoader(test_path, window_size=window_size, window_stride=window_stride,
									  window_type=window_type, normalize=normalize).getitem()

		# test model
		model.eval()

		if cuda:
			data = data.cuda()
		data = Variable(data, volatile=True)
		output = model(data)
		pred = output.data.max(1, keepdim=True)[1]
		print(class_set[int(pred)])
'''
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
				return '0'
			elif sttTXT_org == 'one' or sttTXT_org == 'One' or sttTXT_org == '1':
				return '1'
			elif sttTXT_org == 'two' or sttTXT_org == 'Two' or sttTXT_org == '2':
				return '2'
			else:
				return '9'
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			return '9'
		except sr.RequestError as e:
			print('Could not request results from Google Speech Recognition service; {0}'.format(e))
			return '9'