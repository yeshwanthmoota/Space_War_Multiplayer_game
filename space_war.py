import pygame,sys
import os
import math

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.font.init()
pygame.mixer.init()


# GAME SCREEN PROPERTIES
WIDTH = 1080
HEIGHT = 600


# Creating the display named gameDisplay and naming it Space War
gameDisplay=pygame.display.set_mode((WIDTH,HEIGHT)) # takes in a tuple.
pygame.display.set_caption("Space War")



# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN= (0,255,0)




# Frames Per Second => 1/FPS delay_time or sleep time
FPS = 100



# SPACESHIP PROPERTIES
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 60
SPACESHIP_SPEED = 3



# BULLETS PROPERTIES
MAX_BULLETS_ON_SCREEN = 3
BULLET_SPEED = 10
BULLET_RADIUS = 10


# Logic for getting all on the correct path in execution point of view
# Very important code

##

#----------------------code for working on terminal----------
final_path = os.getcwd()
path_list = final_path.split("/")
if path_list[-1] == "Space_war_Multiplayer" or  path_list[-1] == "Space_War_Multiplayer_game-master":
    final_path = final_path + "/Assets/"
#----------------------code for working on terminal----------

#----------------------code for working on vs code----------
else:
    final_path = os.path.dirname(__file__) + "/" + "Assets" + "/"
#----------------------code for working on vs code----------



# LOADING ALL THE IMAGES
GREEN_SPACESHIP_IMG = pygame.image.load(final_path + "spaceship_green_2.png")

GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMG, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

RED_SPACESHIP_IMG = pygame.image.load(final_path + "spaceship_red_2.png")

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

BACKGROUND_IMG = pygame.image.load(final_path + "space2.jpg").convert()
BACKGROUND_IMG= pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))




# CENTRAL BORDER
BORDER = pygame.Rect(WIDTH/2-5,0,10,HEIGHT)  # Middle Border




# User defined events
GREEN_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BULLETS_HIT = pygame.USEREVENT + 3


# Font properties
HEALTH_FONT = pygame.font.SysFont("consolas", 40)
WINNER_FONT = pygame.font.SysFont("Times New Roman",50)



# Music channels

# argument must be int
channel1 = pygame.mixer.Channel(0) # Background music channel
channel2 = pygame.mixer.Channel(1) # sound effects music channel



BULLET_FIRE_SOUND = pygame.mixer.Sound(final_path + "bullet_fire_sound.ogg") 
BULLET_HIT_IMPACT = pygame.mixer.Sound(final_path + "bullet_hit_impact.ogg")
BOTH_BULLETS_HIT_IMPACT = pygame.mixer.Sound(final_path + "both_bullets_collision_impact3.ogg")
BACKGROUND_MUSIC = pygame.mixer.Sound(final_path + "epic_music_tension.ogg")

BULLET_FIRE_SOUND.set_volume(1)
BULLET_HIT_IMPACT.set_volume(1)
BOTH_BULLETS_HIT_IMPACT.set_volume(1)
BACKGROUND_MUSIC.set_volume(0.10)





class Circle_Bullet:
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
    @staticmethod
    def Draw(color, bullets):
        pygame.draw.circle(gameDisplay, color, (int(bullets.x),int(bullets.y)), int(bullets.radius))
    
    @staticmethod
    def collide_Circle_Bullet(obj1,obj2):
        x=obj1.x
        y=obj1.y
        r1=obj1.radius

        h=obj2.x
        k=obj2.y
        r2=obj2.radius

        dist_bw_centers = math.sqrt( pow(x-h,2) + pow(y-k,2) )
        radius_add = r1+r2

        if(dist_bw_centers < radius_add):
            return True
        else:
            return False
    
    @staticmethod
    def collide_Circle_Bullet_with_Rect(circle_obj,rect_obj):
        obj = pygame.Rect(circle_obj.x - circle_obj.radius, circle_obj.y - circle_obj.radius, BULLET_RADIUS, BULLET_RADIUS)
        return obj.colliderect(rect_obj)

        


def draw_winner(winner_text):
    if winner_text =="GREEN SPACESHIP WINS!":
        draw_text = WINNER_FONT.render(winner_text,1,GREEN)
        gameDisplay.blit(draw_text,(WIDTH/2-(draw_text.get_width())/2, HEIGHT/2-(draw_text.get_height())/2))
    elif winner_text == "RED SPACESHIP WINS!":
        draw_text = WINNER_FONT.render(winner_text,1,RED)
        gameDisplay.blit(draw_text,(WIDTH/2-(draw_text.get_width())/2, HEIGHT/2-(draw_text.get_height())/2))
    pygame.display.update()
    pygame.time.delay(1000*3) # 3 seconds


def draw_window(green,red,green_bullets,red_bullets,GREEN_HEALTH,RED_HEALTH):
    gameDisplay.blit(BACKGROUND_IMG, (0, 0))
    pygame.draw.rect(gameDisplay, BLACK, BORDER)

    green_health_text = HEALTH_FONT.render("HEALTH: {}".format(GREEN_HEALTH), 1, WHITE)
    red_health_text = HEALTH_FONT.render("HEALTH: {}".format(RED_HEALTH), 1, WHITE)

    gameDisplay.blit(green_health_text,(WIDTH/2 -100-green_health_text.get_width(),10))
    gameDisplay.blit(red_health_text,((WIDTH/2 + 100),10))

    gameDisplay.blit(GREEN_SPACESHIP, (green.x,green.y))
    gameDisplay.blit(RED_SPACESHIP, (red.x,red.y))
    handle_bullets(green,red,green_bullets,red_bullets)
    pygame.display.update()





def green_handle_movement(keys_pressed,green):
    if keys_pressed[pygame.K_a] and green.x>0: # LEFT
        green.x-=SPACESHIP_SPEED
    if keys_pressed[pygame.K_d] and green.x<BORDER.x-SPACESHIP_WIDTH: # RIGHT
        green.x+=SPACESHIP_SPEED
    if keys_pressed[pygame.K_w] and green.y>0: # UP
        green.y-=SPACESHIP_SPEED
    if keys_pressed[pygame.K_s] and green.y<HEIGHT-SPACESHIP_HEIGHT-25: # DOWN
        green.y+=SPACESHIP_SPEED


def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width + 10: # LEFT
        red.x-=SPACESHIP_SPEED
    if keys_pressed[pygame.K_RIGHT] and  red.x < WIDTH-SPACESHIP_WIDTH: # RIGHT
        red.x+=SPACESHIP_SPEED
    if keys_pressed[pygame.K_UP] and red.y>0: # UP
        red.y-=SPACESHIP_SPEED
    if keys_pressed[pygame.K_DOWN] and red.y<HEIGHT-SPACESHIP_HEIGHT-25: # DOWN
        red.y+=SPACESHIP_SPEED




def handle_bullets(green, red, green_bullets, red_bullets):
    """
    Handles Creating the bullets,collisions,bullets off screen,
    sending event signal if the bullet collides with the spaceship
    doesn't control display for display relys on draw_window() function
    """

    # code for creating new green bullets
    for bullets in green_bullets:
        Circle_Bullet.Draw(GREEN, bullets)

    # code for creating new red bullets
    for bullets in red_bullets:
        Circle_Bullet.Draw(RED, bullets)
    
    
    # code for collision of green bullet and red ship
    for bullets in green_bullets: # Do this for all the bullets in green_bullets.
        if(bullets.x < WIDTH):  # Checks if the bullet's x-coordinate is less than WIDTH.
            if Circle_Bullet.collide_Circle_Bullet_with_Rect(bullets,red):  # Checking for collisons of red spaceship and green bullets.
                pygame.event.post(pygame.event.Event(RED_HIT))
                green_bullets.remove(bullets)    
            bullets.x+=BULLET_SPEED
        else:
            green_bullets.remove(bullets)

    # # code for collision of red bullet and green ship
    for bullets in red_bullets:
        if(bullets.x > 0-BULLET_RADIUS):
            if Circle_Bullet.collide_Circle_Bullet_with_Rect(bullets,green): # Checking for collisons of green spaceship and red bullets.
                pygame.event.post(pygame.event.Event(GREEN_HIT))
                red_bullets.remove(bullets)
            bullets.x-=BULLET_SPEED
        else:
            red_bullets.remove(bullets)

    # # code for collision of both the Bullets
    for bullet,bullets in  [(bullet,bullets) for bullet in green_bullets for bullets in red_bullets]: # Do this for all the green and red bullets.
        if(bullet.x and bullets.x < WIDTH):  # Checks if the bullet's x-coordinate is less than WIDTH.
            if Circle_Bullet.collide_Circle_Bullet(bullet, bullets):  # Checking for collisons of red spaceship and green bullets.
                pygame.event.post(pygame.event.Event(BULLETS_HIT))
                green_bullets.remove(bullet)
                red_bullets.remove(bullets)    







channel1.play( BACKGROUND_MUSIC, -1 )
def main():
    # Health properties
    GREEN_HEALTH = 10  # Initially
    RED_HEALTH = 10 # Initially
    
    global EXIT_CODE
    EXIT_CODE = 0 # User set for convenience

    green_bullets=[]
    red_bullets=[]
    bullets=[]

    green = pygame.Rect(0,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT) # Initial position
    red = pygame.Rect(850,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT) # Initial position


    clock = pygame.time.Clock()

    running = True

    while running:     #Game Loop

        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN: # event because it denotes the key is pressed once
                # Even holding down the key registers as one single event.


# Putting K_1 and K_9 instead of K_LCTRL and K_RCTRL
# Because they hang if keys are spammed where as 1 and 9 can work together.
                if event.key == pygame.K_1 and len(green_bullets) < MAX_BULLETS_ON_SCREEN:
                    bullets=Circle_Bullet((green.x+SPACESHIP_WIDTH-20), (green.y+SPACESHIP_HEIGHT/2+5), BULLET_RADIUS)
                    green_bullets.append(bullets)
                    # pygame.mixer.music.load(r"pygame_projects\Assets\Assets_for_Space_war_Multiplayer\bullet_fire_sound.mp3"))
                    # pygame.mixer.music.play()
                    # pygame.mixer.music.unload()
                    # BULLET_FIRE_SOUND.play()
                    channel2.play( BULLET_FIRE_SOUND )

                if event.key == pygame.K_9 and len(red_bullets) < MAX_BULLETS_ON_SCREEN:
                    bullets=Circle_Bullet(red.x-5, red.y+SPACESHIP_HEIGHT/2+5, BULLET_RADIUS)
                    red_bullets.append(bullets)
                    # pygame.mixer.music.load(r"pygame_projects\Assets\Assets_for_Space_war_Multiplayer\bullet_fire_sound.mp3"))
                    # pygame.mixer.music.play()
                    # pygame.mixer.music.unload()
                    # BULLET_FIRE_SOUND.play()
                    channel2.play( BULLET_FIRE_SOUND )


            if event.type == GREEN_HIT:
                GREEN_HEALTH-=1
                # pygame.mixer.music.load(r"pygame_projects\Assets\Assets_for_Space_war_Multiplayer\bullet_hit_impact.mp3"))
                # pygame.mixer.music.play()
                # pygame.mixer.music.unload()
                # BULLET_HIT_IMPACT.play()
                channel2.play( BULLET_HIT_IMPACT )
            if event.type == RED_HIT:
                RED_HEALTH-=1
                # pygame.mixer.music.load(r"pygame_projects\Assets\Assets_for_Space_war_Multiplayer\bullet_hit_impact.mp3"))
                # pygame.mixer.music.play()
                # pygame.mixer.music.unload()
                # BULLET_HIT_IMPACT.play()
                channel2.play( BULLET_HIT_IMPACT )
            
            if event.type == BULLETS_HIT:
                # pygame.mixer.music.load(r"pygame_projects\Assets\Assets_for_Space_war_Multiplayer\both_bullets_collision_impact3.mp3"))
                # pygame.mixer.music.play()
                # pygame.mixer.music.unload()
                # BOTH_BULLETS_HIT_IMPACT.play()
                channel2.play( BOTH_BULLETS_HIT_IMPACT )





            winner_text=""
            if GREEN_HEALTH<=0:
                winner_text="RED SPACESHIP WINS!"
            if RED_HEALTH<=0:
                winner_text="GREEN SPACESHIP WINS!"

            if winner_text!="":
                draw_winner(winner_text)
                EXIT_CODE=1 # Break from the for loop
                break



        green_handle_movement(keys_pressed,green)
        red_handle_movement(keys_pressed,red)
        draw_window(green,red,green_bullets,red_bullets,GREEN_HEALTH,RED_HEALTH)
        # print(RED_HEALTH)
        # print(GREEN_HEALTH)    
        if(EXIT_CODE==1): 
            break # Break out of the while loop
    main()

    

if __name__=="__main__":
    main()








# Now For rectangular bullets comment out the code above and uncomment out the code below:


# import pygame,sys
# import os
# import math


# pygame.init()
# pygame.font.init()
# pygame.mixer.init()


# # GAME SCREEN PROPERTIES
# WIDTH = 1080
# HEIGHT = 600


# # Creating the display named gameDisplay and naming it Space War
# gameDisplay=pygame.display.set_mode((WIDTH,HEIGHT)) # takes in a tuple.
# pygame.display.set_caption("Space War")



# # COLORS
# WHITE = (255,255,255)
# BLACK = (0,0,0)
# YELLOW = (255,255,0)
# RED = (255,0,0)
# BLUE = (0,0,255)
# GREEN= (0,255,0)




# # Frames Per Second => 1/FPS delay_time or sleep time
# FPS = 100



# # SPACESHIP PROPERTIES
# SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 60
# SPACESHIP_SPEED = 3



# # BULLETS PROPERTIES
# MAX_BULLETS_ON_SCREEN = 3
# BULLET_SPEED = 10
# BULLET_WIDTH = 20
# BULLET_HEIGHT = 10


# # Logic for getting all on the correct path in execution point of view
# # Very important code

# ##


# file_path = os.getcwd() # Code for working on terminal
# path_list = file_path.split("/") # Code for working on terminal

# if path_list[-1] != "Space_war_Multiplayer": # Code for working in vs code 
#     file_path = os.path.dirname(__file__) # Code for working in vs code
#     path_list = file_path.split("/") # Code for working in vs code

# final_path = "/".join(path_list[0:-3])
# # print(final_path)
# final_path= final_path+ "/" + r"pygame_projects\Assets\Assets_for_Space_war_Multiplayer" + "/"
# print(final_path)




# # LOADING ALL THE IMAGES
# GREEN_SPACESHIP_IMG = pygame.image.load(final_path + "spaceship_green_2.png")

# GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMG, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

# RED_SPACESHIP_IMG = pygame.image.load(final_path + "spaceship_red_2.png")

# RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

# BACKGROUND_IMG = pygame.image.load(final_path + "space2.jpg").convert()
# BACKGROUND_IMG= pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))




# # CENTRAL BORDER
# BORDER = pygame.Rect(WIDTH/2-5,0,10,HEIGHT)  # Middle Border




# # User defined events
# GREEN_HIT = pygame.USEREVENT + 1
# RED_HIT = pygame.USEREVENT + 2
# BULLETS_HIT = pygame.USEREVENT + 3


# # Font properties
# HEALTH_FONT = pygame.font.SysFont("consolas", 40)
# WINNER_FONT = pygame.font.SysFont("Times New Roman",50)



# # Music channels

# # argument must be int
# channel1 = pygame.mixer.Channel(0) # Background music channel
# channel2 = pygame.mixer.Channel(1) # sound effects music channel



# BULLET_FIRE_SOUND = pygame.mixer.Sound(final_path + "bullet_fire_sound.ogg") 
# BULLET_HIT_IMPACT = pygame.mixer.Sound(final_path + "bullet_hit_impact.ogg")
# BOTH_BULLETS_HIT_IMPACT = pygame.mixer.Sound(final_path + "both_bullets_collision_impact3.ogg")
# BACKGROUND_MUSIC = pygame.mixer.Sound(final_path + "epic_music_tension.ogg")

# BULLET_FIRE_SOUND.set_volume(1)
# BULLET_HIT_IMPACT.set_volume(1)
# BOTH_BULLETS_HIT_IMPACT.set_volume(1)
# BACKGROUND_MUSIC.set_volume(0.10)






# def draw_winner(winner_text):
#     if winner_text =="GREEN SPACESHIP WINS!":
#         draw_text = WINNER_FONT.render(winner_text,1,GREEN)
#         gameDisplay.blit(draw_text,(WIDTH/2-(draw_text.get_width())/2, HEIGHT/2-(draw_text.get_height())/2))
#     elif winner_text == "RED SPACESHIP WINS!":
#         draw_text = WINNER_FONT.render(winner_text,1,RED)
#         gameDisplay.blit(draw_text,(WIDTH/2-(draw_text.get_width())/2, HEIGHT/2-(draw_text.get_height())/2))
#     pygame.display.update()
#     pygame.time.delay(1000*3) # 3 seconds


# def draw_window(green,red,green_bullets,red_bullets,GREEN_HEALTH,RED_HEALTH):
#     gameDisplay.blit(BACKGROUND_IMG, (0, 0))
#     pygame.draw.rect(gameDisplay, BLACK, BORDER)

#     green_health_text = HEALTH_FONT.render("HEALTH: {}".format(GREEN_HEALTH), 1, WHITE)
#     red_health_text = HEALTH_FONT.render("HEALTH: {}".format(RED_HEALTH), 1, WHITE)

#     gameDisplay.blit(green_health_text,(WIDTH/2 -100-green_health_text.get_width(),10))
#     gameDisplay.blit(red_health_text,((WIDTH/2 + 100),10))

#     gameDisplay.blit(GREEN_SPACESHIP, (green.x,green.y))
#     gameDisplay.blit(RED_SPACESHIP, (red.x,red.y))
#     handle_bullets(green,red,green_bullets,red_bullets)
#     pygame.display.update()





# def green_handle_movement(keys_pressed,green):
#     if keys_pressed[pygame.K_a] and green.x>0: # LEFT
#         green.x-=SPACESHIP_SPEED
#     if keys_pressed[pygame.K_d] and green.x<BORDER.x-SPACESHIP_WIDTH: # RIGHT
#         green.x+=SPACESHIP_SPEED
#     if keys_pressed[pygame.K_w] and green.y>0: # UP
#         green.y-=SPACESHIP_SPEED
#     if keys_pressed[pygame.K_s] and green.y<HEIGHT-SPACESHIP_HEIGHT-25: # DOWN
#         green.y+=SPACESHIP_SPEED


# def red_handle_movement(keys_pressed,red):
#     if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width + 10: # LEFT
#         red.x-=SPACESHIP_SPEED
#     if keys_pressed[pygame.K_RIGHT] and  red.x < WIDTH-SPACESHIP_WIDTH: # RIGHT
#         red.x+=SPACESHIP_SPEED
#     if keys_pressed[pygame.K_UP] and red.y>0: # UP
#         red.y-=SPACESHIP_SPEED
#     if keys_pressed[pygame.K_DOWN] and red.y<HEIGHT-SPACESHIP_HEIGHT-25: # DOWN
#         red.y+=SPACESHIP_SPEED




# def handle_bullets(green, red, green_bullets, red_bullets):
#     """
#     Handles Creating the bullets,collisions,bullets off screen,
#     sending event signal if the bullet collides with the spaceship
#     doesn't control display for display relys on draw_window() function
#     """

#     # code for creating new green bullets
#     for bullets in green_bullets:
#         pygame.draw.rect(gameDisplay, GREEN, bullets)

#     # code for creating new red bullets
#     for bullets in red_bullets:
#         pygame.draw.rect(gameDisplay, RED, bullets)
    
    
#     # code for collision of green bullet and red ship
#     for bullets in green_bullets: # Do this for all the bullets in green_bullets.
#         if(bullets.x < WIDTH):  # Checks if the bullet's x-coordinate is less than WIDTH.
#             if red.colliderect(bullets):  # Checking for collisons of red spaceship and green bullets.
#                 pygame.event.post(pygame.event.Event(RED_HIT))
#                 green_bullets.remove(bullets)    
#             bullets.x+=BULLET_SPEED
#         else:
#             green_bullets.remove(bullets)

#     # code for collision of red bullet and green ship
#     for bullets in red_bullets:
#         if(bullets.x > 0-BULLET_WIDTH):
#             if green.colliderect(bullets): # Checking for collisons of green spaceship and red bullets.
#                 pygame.event.post(pygame.event.Event(GREEN_HIT))
#                 red_bullets.remove(bullets)
#             bullets.x-=BULLET_SPEED
#         else:
#             red_bullets.remove(bullets)

#     # code for collision of both the Bullets
#     for bullet,bullets in  [(bullet,bullets) for bullet in green_bullets for bullets in red_bullets]: # Do this for all the green and red bullets.
#         if(bullet.x and bullets.x < WIDTH):  # Checks if the bullet's x-coordinate is less than WIDTH.
#             if bullet.colliderect(bullets):  # Checking for collisons of red spaceship and green bullets.
#                 pygame.event.post(pygame.event.Event(BULLETS_HIT))
#                 green_bullets.remove(bullet)
#                 red_bullets.remove(bullets)    







# channel1.play( BACKGROUND_MUSIC, -1 )
# def main():
#     # Health properties
#     GREEN_HEALTH = 10  # Initially
#     RED_HEALTH = 10 # Initially
    
#     global EXIT_CODE
#     EXIT_CODE = 0 # User set for convenience

#     green_bullets=[]
#     red_bullets=[]
#     bullets=[]

#     green = pygame.Rect(0,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT) # Initial position
#     red = pygame.Rect(850,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT) # Initial position


#     clock = pygame.time.Clock()

#     running = True

#     while running:     #Game Loop

#         clock.tick(FPS)

#         keys_pressed = pygame.key.get_pressed()

#         for event in pygame.event.get():

#             if event.type == pygame.QUIT:
#                 running = False
#                 pygame.quit()
#                 sys.exit(0)

#             if event.type == pygame.KEYDOWN: # event because it denotes the key is pressed once
#                 # Even holding down the key registers as one single event.

# # Putting K_1 and K_9 instead of K_LCTRL and K_RCTRL
# # Because they hang if keys are spammed where as 1 and 9 can work together.
#                 if event.key == pygame.K_1 and len(green_bullets) < MAX_BULLETS_ON_SCREEN:
#                     bullets=pygame.Rect((green.x+SPACESHIP_WIDTH-20), (green.y+SPACESHIP_HEIGHT/2+5), BULLET_WIDTH,BULLET_HEIGHT)
#                     green_bullets.append(bullets)
#                     # pygame.mixer.music.load(os.path.join("pygame_projects", "Assets", "Assets_for_Space_war_Multiplayer","bullet_fire_sound.mp3"))
#                     # pygame.mixer.music.play()
#                     # pygame.mixer.music.unload()
#                     # BULLET_FIRE_SOUND.play()
#                     channel2.play( BULLET_FIRE_SOUND )

#                 if event.key == pygame.K_9 and len(red_bullets) < MAX_BULLETS_ON_SCREEN:
#                     bullets=pygame.Rect(red.x-5, red.y+SPACESHIP_HEIGHT/2+5, BULLET_WIDTH,BULLET_HEIGHT)
#                     red_bullets.append(bullets)
#                     # pygame.mixer.music.load(os.path.join("pygame_projects", "Assets", "Assets_for_Space_war_Multiplayer","bullet_fire_sound.mp3"))
#                     # pygame.mixer.music.play()
#                     # pygame.mixer.music.unload()
#                     # BULLET_FIRE_SOUND.play()
#                     channel2.play( BULLET_FIRE_SOUND )


#             if event.type == GREEN_HIT:
#                 GREEN_HEALTH-=1
#                 # pygame.mixer.music.load(os.path.join("pygame_projects", "Assets", "Assets_for_Space_war_Multiplayer","bullet_hit_impact.mp3"))
#                 # pygame.mixer.music.play()
#                 # pygame.mixer.music.unload()
#                 # BULLET_HIT_IMPACT.play()
#                 channel2.play( BULLET_HIT_IMPACT )
#             if event.type == RED_HIT:
#                 RED_HEALTH-=1
#                 # pygame.mixer.music.load(os.path.join("pygame_projects", "Assets", "Assets_for_Space_war_Multiplayer","bullet_hit_impact.mp3"))
#                 # pygame.mixer.music.play()
#                 # pygame.mixer.music.unload()
#                 # BULLET_HIT_IMPACT.play()
#                 channel2.play( BULLET_HIT_IMPACT )
            
#             if event.type == BULLETS_HIT:
#                 # pygame.mixer.music.load(os.path.join("pygame_projects", "Assets", "Assets_for_Space_war_Multiplayer","both_bullets_collision_impact3.mp3"))
#                 # pygame.mixer.music.play()
#                 # pygame.mixer.music.unload()
#                 # BOTH_BULLETS_HIT_IMPACT.play()
#                 channel2.play( BOTH_BULLETS_HIT_IMPACT )





#             winner_text=""
#             if GREEN_HEALTH<=0:
#                 winner_text="RED SPACESHIP WINS!"
#             if RED_HEALTH<=0:
#                 winner_text="GREEN SPACESHIP WINS!"

#             if winner_text!="":
#                 draw_winner(winner_text)
#                 EXIT_CODE=1 # Break from the for loop
#                 break



#         green_handle_movement(keys_pressed,green)
#         red_handle_movement(keys_pressed,red)
#         draw_window(green,red,green_bullets,red_bullets,GREEN_HEALTH,RED_HEALTH)
#         # print(RED_HEALTH)
#         # print(GREEN_HEALTH)    
#         if(EXIT_CODE==1): 
#             break # Break out of the while loop
#     main()

    

# if __name__=="__main__":
#     main()
