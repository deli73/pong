import pygame, random, sys
from pygame.locals import *
#==SETTINGS==#
MBLUR = True
ENEMYAI = 0 #enemy AI
			#0 = doesn't move
			#1 = back and forth (oddly enough, easier than 0)

#==SET CONSTANTS==#
FPS = 30
WSIZE = WWIDTH, WHEIGHT = (640,480)
POFFSET = 15 #horizontal margin of the paddle in pixels
PADWIDTH = 15
PADRATIO = 3 #paddle height is WHEIGHT / PADRATIO

BALLSIZE = 50 #diameter of the ball
BALLOUTLINE = 5 #width of the outline
BSPEED = 10

BALLCOLOR = (100,240,200) #a "sky blue"-ish color
BALLOUTLINECOLOR = (60,120,100) #darker color

WHITE = (255,255,255)
BLACK = (0,0,0)
BLACK_ALPHA = (0,0,0,180)

pygame.font.init()
DEFAULTFONT = pygame.font.Font("consolas.ttf",50)

def main():
	global CLOCK, DISPLAY, pPaddle, cPaddle, cPaddleSpeed, v #DON'T JUDGE ME
	pygame.init()
	CLOCK = pygame.time.Clock()
	DISPLAY = pygame.display.set_mode(WSIZE)

	pygame.display.set_caption("INSERT CAPTION HERE")


	ballRect = pygame.rect.Rect((WWIDTH/2,WHEIGHT/2,BALLSIZE,BALLSIZE))

	pPaddle  = pygame.rect.Rect((0, 0, PADWIDTH, WHEIGHT/PADRATIO))
	cPaddle = pygame.rect.Rect((0, 0, PADWIDTH, WHEIGHT/PADRATIO))
	pPaddle.centerx = POFFSET
	cPaddle.centerx = WWIDTH - POFFSET
	pPaddle.centery = cPaddle.centery = WHEIGHT/2

	cPaddleSpeed = 10

	v = (random.choice((-BSPEED,BSPEED)),random.choice((-BSPEED,BSPEED)))
	scores = [0,0] #player score, computer score

	pygame.time.delay(1000)
	while True:
		checkForQuit()
		#USER INPUT
		pPaddle = updatePPaddle(pPaddle)
		cPaddle = updateCPaddle(cPaddle,ballRect)

		#GAME STATE
		scores= checkForScore(scores,ballRect)
		v = bounce(ballRect, v) #bounce the ball if at wall
		dx,dy = v
		ballRect.move_ip(dx,dy) #move the ball

		#DISPLAY
		if MBLUR:
			dalpha = DISPLAY.convert_alpha()
			drect = DISPLAY.get_rect()
			dalpha.fill(BLACK_ALPHA)
			DISPLAY.blit(dalpha, drect)
		else:
			DISPLAY.fill(BLACK)
		
		pygame.draw.line(DISPLAY, WHITE, (WWIDTH/2,0), (WWIDTH/2,WHEIGHT)) #draw divider line
		pygame.draw.rect(DISPLAY, WHITE, pPaddle, 0)
		pygame.draw.rect(DISPLAY, WHITE, cPaddle, 5)
		drawBall(DISPLAY,ballRect) #draw the ball
		pScore = DEFAULTFONT.render(str(scores[0]),False,WHITE)
		pScoreRect = pScore.get_rect()
		cScore = DEFAULTFONT.render(str(scores[1]),False,WHITE)
		cScoreRect = cScore.get_rect()
		cScoreRect.right = WWIDTH
		DISPLAY.blit(pScore,pScoreRect)
		DISPLAY.blit(cScore,cScoreRect)

		pygame.display.update()
		CLOCK.tick(FPS)


def checkForQuit():
	for event in pygame.event.get(QUIT):
		pygame.quit()
		sys.exit()

#==SUPPORT FUNCTIONS==#
def drawBall(surf,rect):
	pos = rect.center
	rad = rect.width / 2
	pygame.draw.circle(surf, BALLCOLOR, pos, rad, 0)
	pygame.draw.circle(surf, BALLOUTLINECOLOR, pos, rad, BALLOUTLINE)

def bounce(rect, v): #reverses y where necessary
	x,y = v
	if rect.y < 0 or rect.bottom > WHEIGHT: #hits the top or bottom
		y *= -1

	if rect.colliderect(pPaddle): #hits a paddle
		x = abs(x)
		y += random.randint(-2,2)
	if rect.colliderect(cPaddle): #functions designed to prevent bouncing inside the paddles
		x = -abs(x)
	return x,y

def checkForScore(score,rect):
	if rect.right < 0:
		score[1] += 1
		resetBall(rect,1)
	elif rect.x > WWIDTH:
		score[0] += 1
		resetBall(rect,-1)
	return score

def resetBall(rect,direction):
	global v
	rect.center = WWIDTH/2, WHEIGHT/2

	DISPLAY.fill(BLACK)
	pygame.draw.line(DISPLAY, WHITE, (WWIDTH/2,0), (WWIDTH/2,WHEIGHT)) #draw divider line
	pygame.draw.rect(DISPLAY, WHITE, pPaddle, 0)
	pygame.draw.rect(DISPLAY, WHITE, cPaddle, 5)
	drawBall(DISPLAY,rect) #draw the ball
	pygame.display.update()

	pygame.time.delay(1000)
	v = ((BSPEED * direction),random.choice((-BSPEED,BSPEED)))

def updatePPaddle(paddle):
	for event in pygame.event.get(MOUSEMOTION):
		paddle.centery = event.pos[1]
	return paddle

#=====ENEMY AI=====#
def updateCPaddle(paddle, rect):
	global cPaddleSpeed

	if ENEMYAI == 0:
		pass		#enemy level 0 doesn't move

	if ENEMYAI == 1:
		paddle.y += cPaddleSpeed
		if paddle.y < 0 or paddle.bottom > WHEIGHT: #hits the top or bottom
			cPaddleSpeed *= -1

	return paddle



if __name__ == '__main__':
	main()