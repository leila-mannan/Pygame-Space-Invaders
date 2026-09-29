from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

Grey = (29, 29, 27)
Yellow = (243, 216, 63)
level = 1
#text surfaces
font = pygame.font.Font("Gameplay.ttf", 30)
smaller_font = pygame.font.Font("Gameplay.ttf", 20)
level_text = "LEVEL 0" + str(level)
level_surface = font.render(level_text, False, Yellow)
game_over_surface = font.render("GAME OVER", False, Yellow)
score_text_surface = font.render("SCORE", False, Yellow)
highscore_text_surface = font.render("HIGH-SCORE", False, Yellow)
restart_surface = font.render("[ENTER] TO RESTART", False, Yellow)
play_again_surface = font.render("WINNER! NEXT LEVEL?", False, Yellow)
try_again_surface = font.render("TRY AGAIN!", False, Yellow)
instructions_surface = smaller_font.render("[SPACE] TO SHOOT", False, Yellow)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption('Space Invaders')

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT+1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

while True:
    #Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()
        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and game.run == False:
            if game.alien_count == 0:  # if the game is won
                game.next_level()
                level+=1
                if level>9:
                    level_text = "LEVEL " + str(level)
                else:
                    level_text = "LEVEL 0" + str(level)
            else:
                game.reset()
                level = 1
                level_text = "LEVEL 01"
                instructions_surface = smaller_font.render("[SPACE] TO SHOOT", False, Yellow)
            level_surface = font.render(level_text, False, Yellow)

    #Updating
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()
        game.check_aliens()

    # Drawing
    screen.fill(Grey)

    #UI
    pygame.draw.rect(screen, Yellow, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, Yellow, (25, 700), (775, 700), 3)
    #while the game is running, display:
    if game.run:
        screen.blit(level_surface, (590, 725, 50, 50))
        screen.blit(instructions_surface, (300, 725, 50, 50))
        if keys[pygame.K_SPACE]:
            instructions_surface = smaller_font.render("", False, Yellow)
    #once the game ends, display:
    else:
        screen.blit(game_over_surface, (540, 725, 50, 50))
        screen.blit(restart_surface, (230, 420, 50, 50))
        if game.alien_count == 0: #if the game is won
            screen.blit(play_again_surface, (230, 370, 50, 50))
        else:
            screen.blit(try_again_surface, (315, 370, 50, 50))

    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 700))
        x += 50
    #constantly display the score & highscore
    screen.blit(score_text_surface, (50,25,50,50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, Yellow)
    screen.blit(score_surface, (50, 70, 50, 50))
    screen.blit(highscore_text_surface, (550, 25, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, Yellow)
    screen.blit(highscore_surface, (660, 70, 50, 50))

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
