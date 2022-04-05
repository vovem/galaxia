from game.casting.bullet import Bullet
from game.casting.enemy import Enemy
from game.casting.banner import Banner
from game.shared.point import Point
from game.shared.gameconstants import *
import pygame
import time
import random

pygame.mixer.init()



class Director:
    """A person who directs the game. 

    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _display_service (DisplayService): For providing display output.
    """

    def __init__(self, keyboard_service, display_service):
        self.__game_over = False
        """Constructs a new Director using the specified keyboard and display services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            display_service (DisplayService): An instance of DisplayService.
        """
        self._keyboard_service = keyboard_service
        self._display_service = display_service

    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._display_service.open_window()
        self._init_t = time.perf_counter() # Set the initial time counter
        self._enemy_t = time.perf_counter() # Set the initial enemy time counter
        self._enemy_rate = 3 # Enemies will appear each 3 seconds

        run = True
        quit_game = False
        frame_duration = self._display_service.get_frame_duration() # Here we get the duration of each frame (in milliseconds).

        while run:
            pygame.time.delay(frame_duration) # This line determines the time of each frame (actually it says to the program to wait a certain amout of time before executing the next steps).
            for event in pygame.event.get():
                # If player press the window X set quit_game to true and stops this loop
                if event.type == pygame.QUIT:
                    pygame.mixer.music.fadeout(1000 * 2)
                    pygame.mixer.music.unload()

                    run = False
                    quit_game = True
                    pygame.mixer.music.load(TITLE_MUSIC)
                    pygame.mixer.music.play(-1)
                    

            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
            if self._is_over():
                pygame.mixer.music.fadeout(1000 * 2)
                pygame.mixer.music.unload()
                run = False
                pygame.mixer.music.load(TITLE_MUSIC)
                pygame.mixer.music.play(-1)
                

        # If the player had pressed X before then quit_game will be true and the game over message won't be displayed.
        if not quit_game:
            game_over_message = Banner(Point(0,0), 'Game Over', 60)
            max_x = self._display_service.get_width()
            max_y = self._display_service.get_height()
            game_over_message.set_center(Point(max_x / 2, max_y / 2))
            cast.add_actor("game_over_message", game_over_message)

            run = True
            while run:
                # This new loop don't get new inputs neither do new updates (so the game "freezes")
                pygame.time.delay(frame_duration)
                self._do_outputs(cast)
                # If the player press the window X this loop stops
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the players.

        Args:
            cast (Cast): The cast of actors.
        """

        player_ship = cast.get_first_actor("player_ship")
        vel = player_ship.get_direction()
        player_ship.set_velocity(vel)


    def _do_updates(self, cast):
        """Updates the players' positions and resolves any collisions with trails.

        Args:
            cast (Cast): The cast of actors.
        """
        player_ship = cast.get_first_actor("player_ship")

        max_x = self._display_service.get_width()
        
        max_y = self._display_service.get_height()
        player_ship.move_next(MAX_PLAYER_X, max_y)
        # level = 0 

        # #get level banner
        # level_banner = cast.get_first_actor("level_banner")


        # get score banner
        score_banner = cast.get_first_actor("score_banner")


        #Check if passed enough time to create a new enemy
        if (time.perf_counter() - self._enemy_t > self._enemy_rate):
            random_enemy = random.randint(1,4)
            if random_enemy == 1:
                e_image = ENEMY_IMAGE
                #print(1)
            elif random_enemy == 2:
                e_image = ENEMY_IMAGE1
                #print(2)
            elif random_enemy == 3:
                e_image = ENEMY_IMAGE2
            elif random_enemy == 4:
                e_image = ENEMY_IMAGE3

            new_enemy = Enemy(image = e_image)
            # Place the enemy at a random position
            pos_x = max_x
            pos_y = random.randrange(0, max_y - new_enemy.get_image_height())
            new_enemy.set_position(Point(pos_x, pos_y))
            cast.add_actor("enemies", new_enemy)
            self._enemy_t = time.perf_counter()



        # Add player shots
        if (player_ship.is_shooting() and player_ship.is_recharged()):
            new_bullet = Bullet(player_ship.get_center(), 0)
            cast.add_actor("player_bullets", new_bullet)
            player_ship.uncharge()

        # Remove player bullets that go outside screen boundaries
        player_bullets = cast.get_actors("player_bullets")
        for bullet in player_bullets:
            bullet.move_next(max_x, max_y)
            if (bullet.get_position().get_x() > max_x):
                cast.remove_actor("player_bullets", bullet)

        enemies = cast.get_actors("enemies")
        for enemy in enemies:
            enemy.move_next(max_x, max_y)
            # Add enemy shots
            if (enemy.is_recharged()):
                new_bullet = Bullet(enemy.get_center(), 1)
                cast.add_actor("enemy_bullets", new_bullet)
                enemy.uncharge()
            # Check if a player bullet hit the enemy 
            for bullet in player_bullets:
                if (self.check_collision(bullet, enemy)):
                    ENEMY_SHOT.play()
                    cast.remove_actor("player_bullets", bullet)
                    # Remove health from enemy
                    enemy.add_to_health(-10)
                    # Updates player points
                    player_ship.add_to_points(10)
                    score_banner.set_text("Score: " + str(player_ship.get_points()))

                    # Realign score banner on the right
                    score_banner.set_position(Point((max_x - 20) - score_banner.get_image_width(), 5))
                    if (enemy.get_health() == 0):
                        cast.remove_actor("enemies", enemy)

            


        enemy_bullets = cast.get_actors("enemy_bullets")
        for bullet in enemy_bullets:
            bullet.move_next(max_x, max_y)
            # Remove enemy bullets that go outside screen boundaries
            if (bullet.get_position().get_x() < bullet.get_image_width() * -1):
                cast.remove_actor("enemy_bullets", bullet)
            # Check if a enemy bullet hit the player 
            if (self.check_collision(bullet, player_ship)):
                HERO_SHOT.play()
                cast.remove_actor("enemy_bullets", bullet)
                # Remove health from player
                player_ship.add_to_health(-10)
                if (player_ship.get_health() == 0):
                    self.__game_over = True
        
        # get and update health banner
        health_banner = cast.get_first_actor("health_banner")
        health_banner.set_text("Health: " + str(player_ship.get_health()))

        
    def _is_over(self):
        return self.__game_over

    def _do_outputs(self, cast):
        """Draws the actors on the screen.

        Args:
            cast (Cast): The cast of actors.
        """
        actors = cast.get_all_actors()
        self._display_service.draw_actors(actors)

    def check_collision(self, actor_1, actor_2):
        """
        """

        # First, get the four corner points of actor_1's "collision box"
        point_1 = actor_1.get_position()
        point_2 = Point(point_1.get_x(), point_1.get_y() + actor_1.get_image_height())
        point_3 = Point(point_1.get_x() + actor_1.get_image_width(), point_1.get_y())
        point_4 = Point(point_2.get_x(), point_3.get_y())
        actor1_points = [point_1, point_2, point_3, point_4]

        # Then check if any of these points are inside actor_2's "collision box"
        for point in actor1_points:
            if self.is_inside_box(point, actor_2.get_position(), actor_2.get_image_width(), actor_2.get_image_height()):
                return True
        return False

    def is_inside_box(self, point_a, point_b, width, height):
        """
        """
        return (
            point_a.get_x() >= point_b.get_x() and
            point_a.get_x() <= point_b.get_x() + width and
            point_a.get_y() >= point_b.get_y() and
            point_a.get_y() <= point_b.get_y() + height
        )
