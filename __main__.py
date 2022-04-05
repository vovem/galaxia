from game.shared.gameconstants import *
from game.casting.cast import Cast
from game.casting.main_ship import Main_ship
from game.casting.banner import Banner
from game.directing.director import Director
from game.services.keyboard_service import KeyboardService
from game.services.display_service import DisplayService
from game.shared.point import Point
import pathlib
import pygame
pygame.font.init()


def mainMenu():
    WIN = pygame.display.set_mode((MAX_X,MAX_Y))
    LOGO = pygame.image.load(LOGO_IMAGE)
    SPLASH = pygame.transform.scale(pygame.image.load(SPLASH_IMAGE), (MAX_X, MAX_Y))
    NEXT_SPLASH = pygame.transform.scale(pygame.image.load(SPLASH_INSTRUCTION), (MAX_X, MAX_Y)) 
    pygame.mixer.music.load(TITLE_MUSIC)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    #run 
    run = True

    #Menu loop
    while run:
        WIN.blit(SPLASH, (0,0))
        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(LOGO) 
        pygame.display.update()
        for event in pygame.event.get():
            #quit event 
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                WIN.blit(NEXT_SPLASH, (0,0))
                pygame.display.update()
                pygame.mixer.music.fadeout(1000 * 3)
                pygame.mixer.music.unload() 
                main()
    
    
    
    pygame.quit()

def main():

    # create the cast
    cast = Cast()

    # The next line is just a facy way of positioning proportionally to the screen size.
    position = Point(int(MAX_X / 20), int(MAX_Y / 2))
    player_ship = Main_ship(position)
    cast.add_actor("player_ship", player_ship)

    # The health banner
    health_banner = Banner(Point(20,5),'Health:')
    cast.add_actor("health_banner", health_banner)

    # The score banner
    score_banner = Banner(Point(0,0),'Score: 0')
    score_banner.set_position(Point((MAX_X - 20) - score_banner.get_image_width(), 5))
    cast.add_actor("score_banner", score_banner)


    # start the game
    keyboard_service = KeyboardService()
    display_service = DisplayService(
        CAPTION.format(CENTER), MAX_X, MAX_Y, FRAME_RATE)
    director = Director(keyboard_service, display_service)
    director.start_game(cast)


if __name__ == "__main__":
    mainMenu()
