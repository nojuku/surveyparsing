import imutils
import numpy as np
from PyPDF2 import PdfFileReader, PdfFileWriter
import cv2
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import pytesseract



PAGES = 3


# dict { row: ((col fromY, toY), (opt1 fromX, toX), (opt2 fromX, toX), (opt3 fromX, toX), (opt4 fromX, toX), (opt5 fromX, toX))


ALLBOXES = {

1: ((1192, 1375), (990, 1098), (1106, 1194), (1228, 1336), (1347, 1443), (1455, 1578)),
2: ((1386, 1568), (990, 1098), (1106, 1194), (1228, 1336), (1347, 1443), (1455, 1578)),
3: ((1582, 1804), (990, 1098), (1106, 1194), (1228, 1336), (1347, 1443), (1455, 1578)),
4: ((1817, 1952), (990, 1098), (1106, 1194), (1228, 1336), (1347, 1443), (1455, 1578)),

5: ((204, 340), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
6: ((353, 573), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
7: ((583, 760), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
8: ((781, 956), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
9: ((975, 1102), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
10: ((1117, 1300), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
11: ((1311, 1444), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
12: ((1457, 1594), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
13: ((1604, 1785), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1443), (1458, 1578)),
14: ((1797, 1979), (993, 1098), (1103, 1194), (1225, 1336), (1344, 1451), (1458, 1578)),

15: ((206, 339), (1005, 1105), (1117, 1225), (1242, 1342), (1358, 1443), (1465, 1580)),
16: ((350, 529), (1005, 1105), (1117, 1225), (1242, 1342), (1358, 1443), (1465, 1580)),

}

reader = PdfFileReader(open('scan.pdf', 'rb'))
writer = PdfFileWriter()

# rotate pdf
for i in range (PAGES):
	page = reader.getPage(i)
	orientation = page.get('/Rotate')
	if(orientation == 0):
		page = page.rotateClockwise(180)

	writer.addPage(page)

# create rotated pdf
with open('output.pdf', 'wb') as output:
	writer.write(output)


# get image array from pdf
images = convert_from_path('output.pdf')

#print(ALLBOXES[1][0][0])

# convert to cv2
for curimage in images:

	cvimage = cv2.cvtColor(np.array(curimage), cv2.COLOR_RGB2BGR)

	#roi of pagenum / startX 2000 startY 1400 endX 2200 endY 1600
	#SHOULD BE Y:Y+H, X:X+W
	roi = cvimage[2000: 2200, 1400: 1600]
	text = pytesseract.image_to_string(roi, config="-l eng --oem 1 --psm 7")

	cv2.imwrite("%s.jpg" % text, cvimage)

	textasnum = int(float(text))


	if(textasnum == 1):

		print("PG1")

		for i in range(1-4):
			fromY = ALLBOXES[i][0][0]
			toY = ALLBOXES[i][0][1]

			for j in range(5):

					fromX = ALLBOXES[i][j+1][0]
					toX = ALLBOXES[i][j+1][1]


					checkbox = cvimage[fromY: toY, fromX: toX]
					cv2.imwrite("checbox pg1 %d - %d.jpg" % i, j)
					checkbox = cv2.threshold(checkbox, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

					print(cv2.countNonZero(checkbox))



	elif(textasnum == 2):

		print("PG2")

		for i in range(5,14):
			fromY = ALLBOXES[i][0][0]
			toY = ALLBOXES[i][0][1]

			print("something")
			
			for j in range(5):
					fromX = ALLBOXES[i][j+1][0]
					toX = ALLBOXES[i][j+1][1]

					checkbox = cvimage[fromY: toY, fromX: toX]
					cv2.imwrite("checbox pg2 - %d.jpg" % j, checkbox)
					checkbox = cv2.threshold(checkbox, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
					checkbox_gray = cv2.cvtColor(checkbox, cv2.COLOR_BGR2GRAY)
					mask = np.zeros(checkbox.shape, dtype = "uint8")
					mask = cv2.bitwise_and(checkbox, checkbox, mask=mask)

					print(cv2.countNonZero(mask))


	elif(textasnum == 3):

		print("PG3")

		for i in range(5-14):
			fromY = ALLBOXES[i][0][0]
			toY = ALLBOXES[i][0][1]

			for j in range(5):
					fromX = ALLBOXES[i][j+1][0]
					toX = ALLBOXES[i][j+1][1]

					checkbox = cvimage[fromY: toY, fromX: toX]					
					checkbox = cv2.threshold(checkbox, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
					cv2.imwrite("checbox pg3 %d - %d.jpg" % i, j, checkbox)
					print(cv2.countNonZero(checkbox))




	# if(textasnum == 1):
	# 	roi1 = cv2.cvtColor(np.array(curimage), cv2.COLOR_RGB2BGR)[1140: 1420, 960: 1620]






# detect contours within roi's
# calculate fulldoc relative location within roi?
# save bins in global location array (use network x?)



# gray = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(gray, 0,255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)

# for (j, c) in enumerate(cnts):

# 	mask = np.zeros(thresh.shape[:2], dtype="uint8")
# 	cv2.drawContours(mask, [c], -1, 255, -1)

	
# 	mask = cv2.bitwise_and(thresh, thresh, mask=mask)
# 	total = cv2.countNonZero(mask)

# cv2.drawContours(roi1, cnts, -1, (0,255,0), 3)

# cv2.imshow("cnts", roi1)
# cv2.waitKey(0)




#image = cv2.imread
#oi = orig[startY:endY, startX:endX]