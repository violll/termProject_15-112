# taken from course website at
# https://www.kosbie.net/cmu/fall-15/15-112/notes/notes-strings.html#basicFileIO
# https://stackabuse.com/python-append-contents-to-a-file/
def updateHighScore(self):
    with open("highScoreList.txt", "a") as f:
        f.write(f"\n{self.userName}: {self.score}")


# taken from http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-graphics.html
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

# I wrote everything but lines 20 and 21, which are from https://stackabuse.com/python-append-contents-to-a-file/
class HighScoreList(object):
    def __init__ (self):
        self.list = []
        self.getOrderedList()

    def getOrderedList(self):
        with open("highScoreList.txt", 'r') as reader:
            for line in reader.readlines():
                placed = False
                line = line.strip()
                currName, currScore = line.split(": ")
                for i in range(len(self.list)):
                    name, score = self.list[i]
                    if int(currScore) > int(score):
                        self.list.insert(i, (currName, currScore))
                        placed = True
                    if placed == True: break
                if placed == False:
                    self.list.append((currName, currScore))