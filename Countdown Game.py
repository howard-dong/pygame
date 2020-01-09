import pygame, random, sys, math


pygame.init()

# Constants
windowHeight = 400
windowWidth = 600
clock = pygame.time.Clock()
FPS = 60


class Colour:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    gray = (120, 120, 120)
    background = (100, 100, 200)


class Text:

    def __init__(self, text, size, surface, font=0, board=False, isList=False):
        posX = 0

        # Start screen font
        if font == 0:
            self.surface = surface.copy()
            (width, height) = surface.get_size()
            self.surface.fill(Colour.background)
            rect = pygame.font.SysFont(None, 1000).render(text, True, Colour.white)
            if board:
                rect = pygame.transform.scale(rect, (width, int(width/10)))
                self.surface.blit(rect, (0, size))
            else:
                rect = pygame.transform.scale(rect, (width, height))
                self.surface.blit(rect, (0, 0))

        # Numbers
        if font == 1:
            self.surface = surface.copy()
            edge = int(size / 6)
            if not isList:
                text_list = list(str(text))
            else:
                text_list = text
            (width, height) = surface.get_size()
            self.surface.fill(Colour.background)
            for t in text_list:
                pygame.draw.rect(self.surface, Colour.white, (posX, 0, size*2 - edge, height), edge)
                rect = pygame.font.SysFont(None, 1000).render(str(t), True, Colour.white)
                rect = pygame.transform.scale(rect, (int(size*1.5), int(size*1.5)))
                self.surface.blit(rect, (posX + edge, edge * 2))
                posX += size*2 - edge

        # Answers
        if font == 3:
            pass


class _Numbers:

    def __init__(self, bigs):
        self._numList = []
        self.numList = []
        self._answer = 0
        self.answerList = []
        self.bigs = bigs
        self.smalls = 6 - bigs

    def generateNumbers(self, big, small):
        # Make numbers
        self._numList = []
        for i in range(big):
            number = random.randrange(25, 101, 25)
            self._numList.append(number)
        for j in range(small):
            number = random.randint(1, 10)
            self._numList.append(number)
        self.numList = self._numList
        random.shuffle(self.numList)

        # make combo
        # Add operations
        self.operationsList = []
        operations = ["+", "-", "*", "/"]
        for new in self.numList:
            sign = operations[random.randint(0, 3)]
            self.operationsList.append(sign + str(new))
            if sign == "+":
                self._answer += new
            elif sign == "-":
                self._answer -= new
            elif sign == "*":
                self._answer *= new
            elif sign == "/":
                self._answer /= new
            self.answerList.append(self._answer)

    def getQuestion(self):
        self.generateNumbers(self.bigs, self.smalls)
        if not(1000 > self._answer > 100) or not(float(self._answer).is_integer()):
            # print(self.operationsList)
            self._answer = 0
            self.getQuestion()
            return
        print(self._answer)
        print(self.operationsList)

    def getGoal(self):
        return int(self._answer)

    def getAns(self):
        ansList = [0]
        ansList.extend(self.answerList)
        for num in range(6):
            a = str(ansList[num])
            b = str(self.operationsList[num])
            c = str(' = ')
            d = str(self.answerList[num])
            print(a + b + c + d)
        return


class Screen:

    def __init__(self, width=0.0, height=0.0, x=0.0, y=0.0, unit=1.0, mode=1):
        if mode == 0:
            self.screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
            self.width, self.height = pygame.display.get_surface().get_size()
        if mode == 1:
            self.width = width * unit
            self.height = height * unit
            self.screen = pygame.Surface([self.width, self.height])
            self.posX = x * unit
            self.posY = y * unit

    def fill(self, colour):
        self.screen.fill(colour)

    def update(self):
        pygame.display.update(self.screen.get_rect())

    def blit(self, surface, pos):
        self.screen.blit(surface, pos)

    def get_size(self):
        (width, height) = self.screen.get_size()
        return (width, height)


window = Screen(mode=0)


class Control:

    def __init__(self):
        w = window.width
        h = window.height
        unit = int(h / 30)
        center = int(w / (2 * unit))
        self.answer = Screen(12, 4, int(center - 6), 1, unit)
        self.numbers = Screen(24, 4, center - 12, 6, unit)
        self.board = Screen(int(w / unit - 4), int(h / unit * (2/3) - 2), 2, 11, unit)
        self.answerText = Text("[Goal]", unit * 4, self.answer.screen)
        self.numbersText = Text("[Numbers]", unit * 4, self.numbers.screen)
        self.boardText = Text("Press Space to start", unit * 4, self.board.screen, board=True)

    def renderScreen(self, mode, nums=[], ans=0):
        unit = int(windowHeight / 30)
        if mode == 0:
            self.answerText = Text("[Goal]", unit * 4, self.answer.screen)
            self.numbersText = Text("[Numbers]", unit * 4, self.numbers.screen)
            self.boardText = Text("Press Space to start", unit * 4, self.board.screen, board=True)
            self.board.screen.blit(self.boardText.surface, (0, 0))
            self.countdownClock = Screen(14, 14, 1, 1, self.board.height * 1 / 16)
        if mode == 1:
            self.numbersText = Text(nums, unit * 4, self.numbers.screen, font=1, isList=True)
            self.answerText = Text(ans, unit * 4, self.answer.screen, font=1)

        self.answer.screen.blit(self.answerText.surface, (0, 0))
        self.numbers.screen.blit(self.numbersText.surface, (0, 0))
        window.blit(self.answer.screen, (self.answer.posX, self.answer.posY))
        window.blit(self.numbers.screen, (self.numbers.posX, self.numbers.posY))
        window.blit(self.board.screen, (self.board.posX, self.board.posY))

    def showClock(self, secondsPassed=0):
        # Clock Face
        self.board.fill(Colour.background)
        clockCircle = (int(self.countdownClock.width / 2), int(self.countdownClock.width / 2))
        self.countdownClock.fill(Colour.background)
        pygame.draw.circle(self.countdownClock.screen, Colour.white, clockCircle,
                           int(self.countdownClock.width / 2), 5)

        # Clock Hand
        radius = int(self.countdownClock.width / 2)
        angle = (math.pi*3/2) - (math.pi/30) * secondsPassed
        y = radius * math.sin(angle)
        x = math.sqrt(radius**2 - y**2)
        pygame.draw.line(self.countdownClock.screen, Colour.white, (radius, radius), (x+radius, y+radius), 5)

        self.board.screen.blit(self.countdownClock.screen, (self.countdownClock.posX, self.countdownClock.posY))

## Show answers do not work
    # def showAnswers(self, obj):
    #     # Find relevant
    #     newOperationsList = []
    #
    #     for x in obj.operationsList:
    #         [a, b] = list(x)
    #         if len(newOperationsList) == 0 and (a == '/' or a == '*'):
    #             continue
    #         elif (a == '*' or a == '/') and b == '1':
    #             continue
    #         newOperationsList.append(a)
    #         newOperationsList.append(b)

    def showScreen(self):
        window.fill(Colour.background)

        start = False
        countdown = False
        numberlist = []
        answer = 0
        sec = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        pygame.quit()

                        sys.exit()

                    if event.key == pygame.K_SPACE:
                        start = True
                        numbers = _Numbers(0)
                        numbers.getQuestion()
                        numberlist = sorted(numbers.numList, reverse=True)

                        answer = numbers.getGoal()
                        sec = 30
                        countdown = True

                    ## show answers do not work
                    # if event.key == pygame.K_RETURN:
                    #     self.showAnswers(numbers)

            if not start:
                self.renderScreen(0)
            if start:
                self.renderScreen(1, nums=numberlist, ans=answer)
            if countdown:
                passed = int(30 - sec)
                self.showClock(passed)
                if FPS != 0:
                    if not(sec < 0):
                        sec -= 2 / FPS
                    else:
                        countdown = False

            pygame.display.flip()
            clock.tick(FPS)


numbers = _Numbers(0)


def main():
    # window stuff
    game = Control()
    game.showScreen()
    print(numbers.getQuestion())


while True:
    main()
