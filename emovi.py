import indicoio
from PIL import Image
indicoio.config.api_key = '78845ad351b86ed13eced5fad99ed78f'

# happy1 = Image.open('happy1.png')
# happy2 = Image.open('happy2.png')
# sad1 = Image.open('sad1.png')
# sad2 = Image.open('sad2.png')
# angry1 = Image.open('angry1.png')
# angry2 = Image.open('angry2.png')
# fear1 = Image.open('fear1.png')
# fear2 = Image.open('fear2.png')
# surprise1 = Image.open('surprise1.png')
# surprise2 = Image.open('surprise2.png')
# neutral1 = Image.open('neutral1.png')
# neutral2 = Image.open('neutral2.png')

def pasteEmojis(imgUrl):

	for faceInfo in indicoio.fer(imgUrl, detect=True):
		(x1, y1) = faceInfo['location']['top_left_corner']
		(x2, y2) = faceInfo['location']['bottom_right_corner']

		emotions = sorted(faceInfo['emotions'].items(), key=lambda kv: -kv[1])
		first, second = emotions[0], emotions[1]

		if ((emotions.first + emotions.second) /
            (emotions.first + emotions.second + emotions.third + emotions.fourth
            + emotions.fifth) >= .5
            and (emotions.second / emotions.first) > .65) : # 2 emotions
			if first in ('Happy','Sad') and second in ('Happy','Sad'):
				emoji =
			elif first in ('Happy','Angry') and second in ('Happy','Angry'):
				emoji =
			elif first in ('Happy','Fear') and second in ('Happy','Fear'):
				emoji =
			elif first in ('Happy','Surprise') and second in ('Happy','Surprise'):
				emoji =
			elif first in ('Happy','Neutral') and second in ('Happy','Neutral'):
				emoji =
			elif first in ('Sad','Angry') and second in ('Sad','Angry'):
				emoji =
			elif first in ('Sad','Fear') and second in ('Sad','Fear'):
				emoji =
			elif first in ('Sad','Surprise') and second in ('Sad','Surprise'):
				emoji =
			elif first in ('Sad','Neutral') and second in ('Sad','Neutral'):
				emoji =
			elif first in ('Angry','Fear') and second in ('Angry','Fear'):
				emoji =
			elif first in ('Angry','Surprise') and second in ('Angry','Surprise'):
				emoji =
			elif first in ('Angry','Neutral') and second in ('Angry','Neutral'):
				emoji =
			elif first in ('Fear','Surprise') and second in ('Fear','Surprise'):
				emoji =
			elif first in ('Fear','Neutral') and second in ('Fear','Neutral'):
				emoji =
			elif first in ('Neutral','Surprise') and second in ('Neutral','Surprise'):
				emoji =

		elif first > 0.60: # strong emotion
			if first == 'Happy':
				emoji = happyPlus
			elif first == 'Sad':
				emoji = sadPlus
			elif first == 'Angry':
				emoji = angryPlus
			elif first == 'Fear':
				emoji = fearPlus
			elif first == 'Surprise':
				emoji = surprisePlus
			else:
				emoji = neutralPlus

		else: # weak emotion
			if first == 'Happy':
				emoji = happy
			elif first == 'Sad':
				emoji = sad
			elif first == 'Angry':
				emoji = angry
			elif first == 'Fear':
				emoji = fear
			elif first == 'Surprise':
				emoji = surprise
			else:
				emoji = neutral


	for box in indicoio.facial_localization(imgUrl):
		(x1, y1) = box['top_left_corner']
		(x2, y2) = box['bottom_right_corner']
		curEmoji = emoji.resize((x2-x1, y2-y1))
		img.paste(curEmoji, (x1,y1), curEmoji)

face = Image.open('stock6.png')
pasteEmojis(face)
face.show()

# print(list(indicoio.fer('many.jpg', detect=True)[0]['emotions']))

# happy, sad, angry, fear, surprise, neutral
