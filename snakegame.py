import pygame
import sys
import random

def movesnake () :
	global h
	global w
	global food
	global snake
	global motion
	#if motion in ['a','s','w','d'] :
	if motion == 'a' :
		x=-1
		y=0
	if motion == 's' :
		x=0
		y=1
	if motion == 'w' :
		x=0
		y=-1
	if motion == 'd' :
		x=1
		y=0
	if len(snake) == h*w :
		pass

	if [snake[0][0] + y , snake[0][1] + x] == snake[1] :
		if ([snake[0][0] - y , snake[0][1] - x] in snake and [snake[0][0] - y , snake[0][1] - x] != snake[-1]) or (snake[0][0] - y in [-1,h] or snake[0][1] - x in [-1,w]):
			snake = [[h-1,2],[h-1,1],[h-1,0]]
			l = []
			for i in range(int(h)):
				for j in range(int(w)):
					l.append([i,j])
			for i in snake:
				l.remove(i)
			if l != [] :
				food = random.choice(l)
			motion = 'd'
		else :
			snake.insert(0,[snake[0][0] - y , snake[0][1] - x])
			if [snake[0][0],snake[0][1]] == food :
				l = []
				for i in range(int(h)):
					for j in range(int(w)):
						l.append([i,j])
				for i in snake:
					l.remove(i)
				if l != [] :
					food = random.choice(l)
			else :
				snake.pop()
	else :
		if ([snake[0][0] + y , snake[0][1] + x] in snake and [snake[0][0] + y , snake[0][1] + x] != snake[-1]) or (snake[0][0] + y in [-1,h] or snake[0][1] + x in [-1,w]):
			snake = [[h-1,2],[h-1,1],[h-1,0]]
			l = []
			for i in range(int(h)):
				for j in range(int(w)):
					l.append([i,j])
			for i in snake:
				l.remove(i)
			if l != [] :
				food = random.choice(l)
			motion = 'd'
		else :
			snake.insert(0,[snake[0][0] + y , snake[0][1] + x])
			if [snake[0][0],snake[0][1]] == food :
				l = []
				for i in range(int(h)):
					for j in range(int(w)):
						l.append([i,j])
				for i in snake:
					l.remove(i)
				if l != [] :
					food = random.choice(l)
			else :
				snake.pop()


pygame.init()
hieght = 400
width = 600
snake_size = 20
screen = pygame.display.set_mode((600,450))
clock = pygame.time.Clock()
game_surface = pygame.Surface((width,hieght))
snake_skin = pygame.Surface((20,20))
snake_head = pygame.Surface((20,20))
h = hieght/snake_size
w = width/snake_size
tick_counter = 0

pygame.display.set_caption('Snake Game')

#game_surface.blit(snake_head , (snake[i][1],snake[i][0]))
#define snake
snake = [[h-1,2],[h-1,1],[h-1,0]]
snake_original = [[h-1,2],[h-1,1],[h-1,0]]
motion = 'd'

#define foodplace
food = [int(h/2),int(w/2)]

#write score
pygame.font.init()
score_font = pygame.font.SysFont('freesansbold', 40)
high_score = 3

#congrats message
cong_text = score_font.render("CONGRATS!", True, (255, 255, 255),(80,60,175))
cong_rect = cong_text.get_rect()
cong_rect.center = (480,25)

while True :
	if (tick_counter + 1) %  10 == 0 :
		movesnake()

	screen.fill((80,60,175))
	game_surface.fill((0,0,15))
	screen.blit(game_surface , (0,50))


	score_text = score_font.render("SCORE : " + str(len(snake)), True, (255, 255, 255),(80,60,175))
	score_rect = score_text.get_rect()
	score_rect.center = (280,25)
	screen.blit(score_text, score_rect)

	if len(snake) > high_score :
		high_score = len(snake)
	high_score_text = score_font.render("HIGH SCORE : " + str(high_score), True, (255, 255, 255),(80,60,175))
	high_score_rect = score_text.get_rect()
	high_score_rect.center = (70,25)
	screen.blit(high_score_text, high_score_rect)



	#draw snake
	for i in range(len(snake)) :
		if i == 0:
			b = pygame.Rect(snake[i][1]*20 ,50 + snake[i][0]*20 , 20,20)
			pygame.draw.rect(screen,(90,60,50),b)
		else :
			b = pygame.Rect(snake[i][1]*20 ,50 + snake[i][0]*20 , 20,20)
			pygame.draw.rect(screen,(180,120,100),b)
	
	#draw food
	food_pix = pygame.Rect(food[1]*20 ,50 + food[0]*20 , 20,20)
	pygame.draw.rect(screen,(0,120,100),food_pix)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w] :
		motion = 'w'
	if keys[pygame.K_a] :
		motion = 'a'
	if keys[pygame.K_d] :
		motion = 'd'
	if keys[pygame.K_s] :
		motion = 's'

	if len(snake) == h*w :
		if tick_counter%20 == 0 or (tick_counter+1)%20 == 0 or (tick_counter+2)%20 == 0 or (tick_counter+3)%20 == 0 or (tick_counter+4)%20 == 0 or (tick_counter+5)%20 == 0 or (tick_counter+6)%20 == 0 or (tick_counter+7)%20 == 0 or (tick_counter+8)%20 == 0 or (tick_counter+9)%20 == 0 :
			screen.blit(cong_text, cong_rect)

   
	pygame.display.update()
	tick_counter += 1
	clock.tick(60)
    
	
	
