import random as r
import neat
import os
import pygame
import sys


def draw(h,w,food,snake) :
    board = []
    for i in range(h) :
        l = []
        for j in range(w) :
            if [i,j] == food :
                l.append('0')
            elif [i,j] in snake:
                l.append('X')
            else :
                l.append('.')
        board.append(l)
    for i in board:
        print(i)
    print("\n")

def danger(y,x,snake,h,w,food) :
    dangerc = list(tuple(snake[0]))
    dangerl = 1
    while [dangerc[0]+y,dangerc[1]+x] not in snake[1:-1] and [dangerc[0]+y,dangerc[1]+x] != food and dangerc[0]+y in range(h) and dangerc[1]+x in range(w) :
        dangerc[0] += y
        dangerc[1] += x
        dangerl += 1
    if [dangerc[0]+y,dangerc[1]+x] == food :
        return 1/dangerl
    else :
        return -1/dangerl

generation = 0
pygame.init()
hieght = 400
width = 600
snake_size = 40 #make snake_size 20 for doubling the board
screen = pygame.display.set_mode((600,450))
clock = pygame.time.Clock()
game_surface = pygame.Surface((width,hieght))
snake_skin = pygame.Surface((40,40))
snake_head = pygame.Surface((40,40))
h = hieght//snake_size
w = width//snake_size
tick_counter = 0

pygame.font.init()
score_font = pygame.font.SysFont('freesansbold', 40)
pygame.display.set_caption('Snake Game')

high_score = 0


def main(genomes, config):
    global generation, h, w, screen, clock, game_surface,snake_size,snake_skin,snake_head,tick_counter,high_score

    networks = []
    genome_snakes = []
    snakes = []
    foods = []
    counters = []

    for genome_id, g in genomes:
        network = neat.nn.FeedForwardNetwork.create(g, config)
        networks.append(network)
        snakes.append([[h - 1, 2], [h - 1, 1], [h - 1, 0]])
        foods.append([h//2, w//2])
        counters.append(0)
        g.fitness = 0
        genome_snakes.append(g)

    deadsnakes =[]

    Run = True
    while (Run):
        if (tick_counter + 1) %  1 == 0 :
            for n in range(len(snakes)):
                if n not in deadsnakes:
                    foodx = (foods[n][1] - snakes[n][0][1])/w
                    foody = (foods[n][0] - snakes[n][0][0])/h
                    forward =[snakes[n][0][0]-snakes[n][1][0], snakes[n][0][1]-snakes[n][1][1]]
                    right = [snakes[n][0][1]-snakes[n][1][1], snakes[n][1][0] - snakes[n][0][0]]
                    left = [snakes[n][1][1]-snakes[n][0][1], snakes[n][0][0]-snakes[n][1][0]]
                    input = (foodx, -foodx, foody, -foody, (foodx**2+foody**2)**(1/2), snakes[n][0][0]/h, snakes[n][0][1]/w, 1 - snakes[n][0][0]/h, 1-snakes[n][0][1]/w, danger(forward[0], forward[1], snakes[n], h, w, foods[n]), danger(right[0], right[1], snakes[n], h, w, foods[n]), danger(left[0], left[1], snakes[n], h, w, foods[n]))#,danger(forward[0]+right[0],forward[1]+right[1], snakes[n], h, w),danger(forward[0]+left[0],forward[1]+left[1], snakes[n], h, w),danger(-forward[0]+right[0],-forward[1]+right[1], snakes[n], h, w),danger(-forward[0]+left[0],-forward[1]+left[1], snakes[n], h, w)]

                
                    output = networks[n].activate(input)


                    if max(output) == output[1]:
                        x, y = snakes[n][0][1] - snakes[n][1][1], snakes[n][0][0] - snakes[n][1][0]
                    if max(output) == output[2]:
                        x, y = snakes[n][1][0] - snakes[n][0][0], snakes[n][0][1] - snakes[n][1][1]
                    if max(output) == output[0]:
                        x, y = snakes[n][0][0] - snakes[n][1][0], snakes[n][1][1] - snakes[n][0][1]


                    if snakes[n][0][0] + y in [-1, h] or snakes[n][0][1] + x in [-1, w] or [snakes[n][0][0] + y, snakes[n][0][1] + x] in snakes[n][1:-1]  or counters[n] > h*w + 100:
                        genome_snakes[n].fitness -= 5
                        deadsnakes.append(n)
                    else:
                        if [snakes[n][0][0] + y, snakes[n][0][1] + x] != foods[n]:
                            snakes[n].pop()
                            snakes[n].insert(0, [snakes[n][0][0] + y, snakes[n][0][1] + x])
                            genome_snakes[n].fitness += 0.015
                            if counters[n] > 3.5*len(snakes[n]) :
                                genome_snakes[n].fitness -= (1.001**counters[n])/10
                            if (snakes[n][0][1] - foods[n][1])**2 + (snakes[n][0][0] - foods[n][0])**2 < (snakes[n][1][1] - foods[n][1])**2 + (snakes[n][1][0] - foods[n][0])**2 :
                                genome_snakes[n].fitness += 0.001
                            else :
                                genome_snakes[n].fitness -= 0.0011
                        else:
                            snakes[n].insert(0, [snakes[n][0][0] + y, snakes[n][0][1] + x])
                            genome_snakes[n].fitness += 20
                            counters[n] = 0
                            if len(snakes[n]) == h*w:
                                genome_snakes[n].fitness += h*w*10
                                deadsnakes.append(n)
                            l = []
                            for i in range(h):
                                for j in range(w):
                                    l.append([i, j])
                            for i in snakes[n]:
                                l.remove(i)
                            if l:
                                foods[n] = r.choice(l)

                        counters[n] += 1

            if len(deadsnakes) == len(snakes):
                Run = False
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((80,60,175))
        game_surface.fill((0,0,15))
        screen.blit(game_surface , (0,50))


        fitness = []
        for gen in genome_snakes :
            fitness.append(gen.fitness)
        index = fitness.index(max(fitness))
        #index = 0
        score_text = score_font.render("GEN HIGH : " + str(len(snakes[index])), True, (255, 255, 255),(80,60,175))
        score_rect = score_text.get_rect()
        score_rect.center = (260,25)
        screen.blit(score_text, score_rect)

        GEN_text = score_font.render("GEN : " + str(generation), True, (255, 255, 255),(80,60,175))
        GEN_rect = score_text.get_rect()
        GEN_rect.center = (105,25)
        screen.blit(GEN_text, GEN_rect)

        if len(snakes[index]) > high_score :
            high_score = len(snakes[index])
        high_score_text = score_font.render("HIGH SCORE : " + str(high_score), True, (255, 255, 255),(80,60,175))
        high_score_rect = score_text.get_rect()
        high_score_rect.center = (460,25)
        screen.blit(high_score_text, high_score_rect)

        #draw snake
	    
        for i in range(len(snakes[index])) :
            if i == 0:
                b = pygame.Rect(snakes[index][i][1]*snake_size ,50 + snakes[index][i][0]*snake_size ,snake_size,snake_size)
                pygame.draw.rect(screen,(90,60,50),b)
            else :
                b = pygame.Rect(snakes[index][i][1]*snake_size ,50 + snakes[index][i][0]*snake_size , snake_size,snake_size)
                pygame.draw.rect(screen,(180,120,100),b)
	
	    #draw food
        food_pix = pygame.Rect(foods[index][1]*snake_size ,50 + foods[index][0]*snake_size , snake_size,snake_size)
        pygame.draw.rect(screen,(0,120,100),food_pix)

        pygame.display.update()
        tick_counter+=1
        clock.tick(60)

    generation += 1


def run(config_path) :
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,200)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neatconfig.txt")
    run(config_path)
