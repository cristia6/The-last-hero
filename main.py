#pgzero
import random

# Campo do jogo
cell = Actor('border')
cell1 = Actor('floor')
cell2 = Actor("crack")
cell3 = Actor("bones")
shot = Actor("ball" , size =(50,50))

size_w = 9
size_h = 10
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h
loser = Actor("loser", size =(WIDTH, HEIGHT))
winner = Actor("win" , size =(WIDTH, HEIGHT))
win = 0
mode = "game"
colli = 0
TITLE = "WeCode e Dragões"
FPS = 30  # CORRIGIDO (era 3 + erro)

my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 2, 1, 3, 1, 1, 0],
          [0, 1, 1, 1, 2, 1, 1, 1, 0],
          [0, 1, 3, 2, 1, 1, 3, 1, 0],
          [0, 1, 1, 1, 1, 3, 1, 1, 0],
          [0, 1, 1, 3, 1, 1, 2, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]]

# Personagem principal
char = Actor('stand', size=(50,50))
char.top = cell.height
char.left = cell.width
char.health = 100
char.attack = 5

# salvar posição antiga (CORRIGIDO)
old_x = char.x
old_y = char.y

# boss
boss = Actor("boss", topleft=(200, 200), size=(100, 100))
boss.top = cell.height * 2
boss.left = cell.width * 2
boss.health = 75
boss.attack = 15

# direção
char.dir = 1

# Inimigos
enemies = []
for i in range(5):
    x = random.randint(1, 7) * cell.width
    y = random.randint(1, 7) * cell.height
    enemy = Actor("enemy", topleft = (x, y) , size=(50,50))
    enemy.health = random.randint(10, 20)
    enemy.attack = random.randint(5, 10)
    enemy.bonus = random.randint(1, 3)
    enemies.append(enemy)

# Bônus
hearts = []
swords = []
balls = []
shots = []
powers = 0

def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width*j
                cell.top = cell.height*i
                cell.draw()
            elif my_map[i][j] == 1:
                cell1.left = cell.width*j
                cell1.top = cell.height*i
                cell1.draw()
            elif my_map[i][j] == 2:
                cell2.left = cell.width*j
                cell2.top = cell.height*i
                cell2.draw()
            elif my_map[i][j] == 3:
                cell3.left = cell.width*j
                cell3.top = cell.height*i
                cell3.draw()

def draw():
    if mode == 'game' or mode == "level_2":
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        screen.draw.text("HP:", center=(25, 475), color = 'white', fontsize = 20)
        screen.draw.text(char.health, center=(75, 475), color = 'white', fontsize = 20)
        screen.draw.text("AP:", center=(375, 475), color = 'white', fontsize = 20)
        screen.draw.text(char.attack, center=(425, 475), color = 'white', fontsize = 20)

        for i in range(len(enemies)):
            enemies[i].draw()
            screen.draw.text(enemies[i].health, topleft=(enemies[i].x + 5, enemies[i].y - 30), color='white', fontsize=18)

        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
        for ball in balls:
            ball.draw()
        for shot in shots:
            shot.draw()

    elif mode == "level_3":
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        screen.draw.text("HP:", center=(25, 475), color = 'white', fontsize = 20)
        screen.draw.text(char.health, center=(75, 475), color = 'white', fontsize = 20)
        screen.draw.text("AP:", center=(375, 475), color = 'white', fontsize = 20)
        screen.draw.text(char.attack, center=(425, 475), color = 'white', fontsize = 20)

        boss.draw()
        screen.draw.text(boss.health, topleft=(boss.left + 5, boss.top - 30), color='white', fontsize=18)

        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
        for ball in balls:
            ball.draw()
        for shot in shots:
            shot.draw()



    elif mode == "end":

        if win == 3:
            screen.fill("white")
            winner.draw()
            
            screen.draw.text("You win!", center=(WIDTH/2, HEIGHT/2), color = 'white', fontsize = 46)
        else:
            loser.draw()
            screen.draw.text("Game over!", center=(WIDTH/2, HEIGHT/2), color = 'white', fontsize = 46)
            
def on_key_down(key):
    global win, colli, old_x, old_y

    old_x = char.x
    old_y = char.y

    if keyboard.right and char.x + cell.width < WIDTH - cell.width:
        char.x += cell.width
        char.image = 'stand'
        char.dir = 1

    elif keyboard.left and char.x - cell.width > cell.width:
        char.x -= cell.width
        char.image = 'left'
        char.dir = -1

    elif keyboard.down and char.y + cell.height < HEIGHT - cell.height*2:
        char.y += cell.height

    elif keyboard.up and char.y - cell.height > cell.height:
        char.y -= cell.height

    enemy_index = char.collidelist(enemies)
    if enemy_index != -1:
        char.x = old_x
        char.y = old_y
        colli = 1
        enemy = enemies[enemy_index]
        enemy.health -= char.attack
        char.health -= enemy.attack

        if enemy.health <= 0:
            if enemy.bonus == 1:
                heart = Actor('heart', size =(50,50))
                heart.pos = enemy.pos
                hearts.append(heart)
            elif enemy.bonus == 2:
                sword = Actor('sword', size =(12,30))
                sword.pos = enemy.pos
                swords.append(sword)
            elif enemy.bonus == 3:
                ball = Actor('ball', size =(50,50))
                ball.pos = enemy.pos
                balls.append(ball)

            enemies.pop(enemy_index)

def victory():
    global mode, win, boss

    if enemies == [] and char.health > 0 and mode == "game":
        mode = "level_2"
        win += 1
        char.health = 100

        for i in range(5):
            x = random.randint(1, 7) * cell.width
            y = random.randint(1, 7) * cell.height
            enemy = Actor("enemy_2", topleft = (x, y), size=(50,50))
            enemy.health = random.randint(15, 25)
            enemy.attack = random.randint(5, 10)
            enemy.bonus = random.randint(1, 3)
            enemies.append(enemy)

    elif enemies == [] and char.health > 0 and mode == "level_2":
        mode = "level_3"
        win += 1
        char.health = 100

        boss = Actor("boss", topleft=(200, 200), size=(100, 100))
        boss.top = cell.height * 2
        boss.left = cell.width * 2
        boss.health = 75
        boss.attack = 15

    elif mode == "level_3" and boss.health <= 0:
        win = 3
        mode = 'end'

    elif char.health <= 0:
        mode = "end"
        win = -1

def on_mouse_down(button, pos):
    global powers

    if (mode == 'game' or mode == "level_2" or mode == "level_3") and button == mouse.left:
        if powers > 0:
            shot = Actor("ball", size=(50,50))
            shot.pos = char.pos
            shot.dir = char.dir
            shots.append(shot)
            powers -= 1

def update(dt):
    global powers, win, mode, boss, old_x, old_y

    victory()

    # CORRIGIDO (verifica modo)
    if mode == "level_3" and char.colliderect(boss) and boss.health > 0:
        char.x = old_x
        char.y = old_y
        boss.health -= char.attack
        char.health -= boss.attack

        if boss.health <= 0:
            win = 3

    # CORRIGIDO (verifica modo)
    for shot in shots[:]:
        if mode == "level_3" and shot.colliderect(boss):
            boss.health -= 50
            shots.remove(shot)
            break

    for shot in shots[:]:
        for enemy in enemies[:]:
            if shot.colliderect(enemy):
                shots.remove(shot)
                enemies.remove(enemy)
                break

    for ball in balls[:]:
        if char.colliderect(ball):
            powers += 1
            balls.remove(ball)

    for shot in shots[:]:
        shot.x += 15 * shot.dir
        if shot.x < 0 or shot.x > WIDTH:
            shots.remove(shot)

    for i in range(len(hearts)):
        if char.colliderect(hearts[i]):
            char.health += 5
            hearts.pop(i)
            break

    for i in range(len(swords)):
        if char.colliderect(swords[i]):
            char.attack += 5
            swords.pop(i)
            break
