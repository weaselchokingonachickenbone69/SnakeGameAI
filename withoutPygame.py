import random as r
import neat
import os

#drawing board on terminal
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
    dangerc = [snake[0][0]+0, snake[0][1]+0]
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

def main(genomes, config):
    global generation
    #change hieght and width of the board
    h = 20
    w = 30

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


                if snakes[n][0][0] + y in [-1, h] or snakes[n][0][1] + x in [-1, w] or [snakes[n][0][0] + y, snakes[n][0][1] + x] in snakes[n][1:-1]  or counters[n] > h*w:
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

        fitness = []
        for gen in genome_snakes :
            fitness.append(gen.fitness)
        index = fitness.index(max(fitness))
        #index = 0

        if generation > 195 :
            draw(h,w,foods[index],snakes[index])

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
