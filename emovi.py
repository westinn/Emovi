import os, subprocess
import indicoio
import numpy
from math import sqrt
from PIL import Image
import requests
requests.packages.urllib3.disable_warnings()
indicoio.config.api_key = '78845ad351b86ed13eced5fad99ed78f'

happy = Image.open('emojis/happy.png')
happyPlus = Image.open('emojis/happyPlus.png')
sad = Image.open('emojis/sad.png')
sadPlus = Image.open('emojis/sadPlus.png')
angry = Image.open('emojis/angry.png')
angryPlus = Image.open('emojis/angryPlus.png')
fear = Image.open('emojis/fear.png')
fearPlus = Image.open('emojis/fearPlus.png')
surprise = Image.open('emojis/suprise.png')
surprisePlus = Image.open('emojis/suprisePlus.png')
neutral = Image.open('emojis/neutral.png')
neutralPlus = Image.open('emojis/neutralPlus.png')
happyFear = Image.open('emojis/happy+fear.png')
happySurprise = Image.open('emojis/happy+suprised.png')
happyNeutral = Image.open('emojis/happy+neutral.png')
sadAngry = Image.open('emojis/sad+angry.png')
sadFear = Image.open('emojis/sad+fear.png')
sadSurprise = Image.open('emojis/sad+suprised.png')
sadNeutral = Image.open('emojis/sad+neutral.png')
angryFear = Image.open('emojis/angry+fear.png')
angrySurprise = Image.open('emojis/angry+suprised.png')
angryNeutral = Image.open('emojis/angry+neutral.png')
fearSurprise = Image.open('emojis/fear+suprised.png')
fearNeutral = Image.open('emojis/neutral+fear.png')
neutralSurprise = Image.open('emojis/neutral+suprised.png')

# Image IndicoData -> None
# Effect: modifies image to include emojis
def pasteEmojis_effectful(img, faceInfo):
	(x1, y1) = faceInfo['location']['top_left_corner']
	(x2, y2) = faceInfo['location']['bottom_right_corner']
	emotions = sorted(faceInfo['emotions'].items(), key=lambda kv: -kv[1])
	first, second = emotions[0], emotions[1]

	if (first[1] + second[1]) / sum(faceInfo['emotions'].values()) >= .5 and second[1] / first[1] > .65: # 2 emotions
		if first[0] in ('Happy','Fear') and second[0] in ('Happy','Fear'):
			emoji = happyFear
		elif first[0] in ('Happy','Surprise') and second[0] in ('Happy','Surprise'):
			emoji = happySurprise
		elif first[0] in ('Happy','Neutral') and second[0] in ('Happy','Neutral'):
			emoji = happyNeutral
		elif first[0] in ('Sad','Angry') and second[0] in ('Sad','Angry'):
			emoji = sadAngry
		elif first[0] in ('Sad','Fear') and second[0] in ('Sad','Fear'):
			emoji = sadFear
		elif first[0] in ('Sad','Surprise') and second[0] in ('Sad','Surprise'):
			emoji = sadSurprise
		elif first[0] in ('Sad','Neutral') and second[0] in ('Sad','Neutral'):
			emoji = sadNeutral
		elif first[0] in ('Angry','Fear') and second[0] in ('Angry','Fear'):
			emoji = angryFear
		elif first[0] in ('Angry','Surprise') and second[0] in ('Angry','Surprise'):
			emoji = angrySurprise
		elif first[0] in ('Angry','Neutral') and second[0] in ('Angry','Neutral'):
			emoji = angryNeutral
		elif first[0] in ('Fear','Surprise') and second[0] in ('Fear','Surprise'):
			emoji = fearSurprise
		elif first[0] in ('Fear','Neutral') and second[0] in ('Fear','Neutral'):
			emoji = fearNeutral
		elif first[0] in ('Neutral','Surprise') and second[0] in ('Neutral','Surprise'):
			emoji = neutralSurprise
		else:
			emoji = neutral

	elif first[1] > 0.60: # strong emotion
		if first[0] == 'Happy':
			emoji = happyPlus
		elif first[0] == 'Sad':
			emoji = sadPlus
		elif first[0] == 'Angry':
			emoji = angryPlus
		elif first[0] == 'Fear':
			emoji = fearPlus
		elif first[0] == 'Surprise':
			emoji = surprisePlus
		else:
			emoji = neutralPlus

	else: # weak emotion
		if first[0] == 'Happy':
			emoji = happy
		elif first[0] == 'Sad':
			emoji = sad
		elif first[0] == 'Angry':
			emoji = angry
		elif first[0] == 'Fear':
			emoji = fear
		elif first[0] == 'Surprise':
			emoji = surprise
		else:
			emoji = neutral

	emoji = emoji.resize((x2-x1, y2-y1))
	img.paste(emoji, (x1,y1), emoji)


# [String] -> [Image]
# Effect: Calls the Indico API
def urlsToImages(imgUrls, directory):
	imgs = []
	i = 0
	denom = str(len(imgUrls))

	if not os.path.exists('Output/' + directory):
		os.makedirs('Output/' + directory)

	for i, url in enumerate(imgUrls):
		img = Image.open(url)

		try:
			imgInfo = indicoio.fer(url, detect=True)
			[ pasteEmojis_effectful(img, faceInfo) for faceInfo in imgInfo ]
			imgs.append(img)
			i += 1
			print(str(i) + '/' + denom)
		except indicoio.utils.errors.IndicoError:
			imgs.append(img)
			i += 1
			print(str(i) + '/' + denom)
		except requests.exceptions.ConnectionError:
			pass

	return imgs

# GifURL -> [Image]
# Effect: Calls the Indico API
def gifUrlToFrames(url):
	gif = Image.open(url)
	imgs = []
	i = 0

	try:
		while 1:
			gif.seek(i)
			frame = gif.copy()

			w, h = frame.size
			if w % 2: w -= 1
			if h % 2: h -= 1
			frame = frame.crop((0, 0, w, h)).convert('RGB')

			try:
				imgInfo = indicoio.fer(numpy.array(frame), detect=True)
				[ pasteEmojis_effectful(frame, faceInfo) for faceInfo in imgInfo ]
				imgs.append(frame)
				i += 1
			except indicoio.utils.errors.IndicoError:
				imgs.append(frame)
				i += 1
			except requests.exceptions.ConnectionError:
				pass

	except EOFError:
		return imgs


# String -> None
# Effect: saves gif frames to /output
# Effect: creates an mp4 of a gif and saves it in /output
def processGifUrl_effectful(url):
	framerate = Image.open(url).info['duration'] / 1000.0
	gifName = url.split('/')[-1].split('.')[0]
	frames = gifUrlToFrames(url)

	if not os.path.exists('Output/' + gifName):
		os.makedirs('Output/' + gifName)

	[ frame.save('Output/' + gifName + ('/%003d.png' % i)) for i, frame in enumerate(frames) ]

	subprocess.Popen('ffmpeg -framerate ' + str(1/framerate) + ' -i Output/' + gifName + '/%003d.png '
					 + '-c:v libx264 -r 30 -pix_fmt yuv420p Output/' + gifName + '.mp4')


def processMovieUrl_effectful(url):
	def call_command(command):
		subprocess.call(command.split(' '))

	movieName = url.split('/')[-1].split('.')[0]

	if not os.path.exists('Input/' + movieName):
		os.makedirs('Input/' + movieName)
	if not os.path.exists('Output/' + movieName):
		os.makedirs('Output/' + movieName)

	# movie to frames
	call_command('ffmpeg -i ' + url + ' -vf fps=10 Input/' + movieName + '/%09d.png')

	# movie to audio
	call_command('ffmpeg -ss 0 -i ' + url + ' Output/' + movieName + '/audio.mp3')

	i = 1
	urls = []
	while os.path.isfile('Input/' + movieName + ('/%09d.png' % i)):
		urls.append('Input/' + movieName + ('/%09d.png' % i))
		i += 1

	frames = urlsToImages(urls, movieName)

	for url, frame in zip(urls, frames):
		url = url.split('/')[-1]
		frame.save('Output/' + movieName + '/' + url)

	# frames to movie
	call_command('ffmpeg -framerate 10 -i Output/' + movieName + '/%09d.png -c:v libx264 -r 30 -pix_fmt yuv420p Output/_' + movieName + '_.mp4')

	# merge video and audio
	call_command('ffmpeg -i Output/_' + movieName + '_.mp4 -i Output/' + movieName + '/audio.mp3 -codec copy -shortest Output/' + movieName + '.mp4')

processMovieUrl_effectful('Input/officespace.mp4')

'''
cd c:/users/dan/documents/python/emovi
python emovi.py
'''
