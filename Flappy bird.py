import pygame
import random


pygame.init()




screen_width = 500
screen_height = 700

screen = pygame.display.set_mode(
    (screen_width, screen_height)
)

pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()




Sky_blue = (135, 206, 235)
White = (255, 255, 255)
Black = (0, 0, 0)

Green = (34, 177, 76)
Dark_Green = (0, 120, 40)

Yellow = (255, 220, 0)
Orange = (255, 140, 0)

Red = (220, 50, 50)

Brown = (139, 90, 43)
Light_Green = (100, 200, 70)



Ground_height = 100
Ground_Y = screen_height - Ground_height



bird_x = 100
bird_y = 300

bird_width = 40
bird_height = 30

bird_velocity = 0

Gravity = 0.5
Jump_Strength = -8



bird_frame = 0

animation_timer = 0
animation_speed = 100




Pipe_Width = 70

Base_Pipe_speed = 3
Base_Pipe_Gap = 170

Max_Pipe_speed = 7
Min_Pipe_Gap = 120

Pipe_Interval = 1500

pipe_timer = 0

pipes = []




score = 0
high_score = 0



Start = "start"
Playing = "playing"
Game_Over = "game_over"

game_state = Start



title_font = pygame.font.SysFont(
    "Times New Roman",
    55,
    bold=True
)

score_font = pygame.font.SysFont(
    "Times New Roman",
    45,
    bold=True
)

small_font = pygame.font.SysFont(
    "Times New Roman",
    22
)

game_over_font = pygame.font.SysFont(
    "Times New Roman",
    50,
    bold=True
)



flap_sound = None
hit_sound = None
point_sound = None
game_over_sound = None

try:

    pygame.mixer.init()

    flap_sound = pygame.mixer.Sound(
        "assets/Audio/sfx_wing.wav"
    )

    hit_sound = pygame.mixer.Sound(
        "assets/Audio/sfx_hit.wav"
    )

    point_sound = pygame.mixer.Sound(
        "assets/Audio/sfx_point.wav"
    )

    game_over_sound = pygame.mixer.Sound(
        "assets/Audio/sfx_die.wav"
    )

except pygame.error as e:

    print("Sound could not be loaded:", e)



Clouds = [
    [50, 100, 70],
    [300, 150, 90],
    [180, 70, 60],
    [400, 250, 80]
]



def get_difficulty():

    speed = min(
        Base_Pipe_speed + score * 0.15,
        Max_Pipe_speed
    )

    gap = max(
        Base_Pipe_Gap - score * 2,
        Min_Pipe_Gap
    )

    return speed, gap




def create_pipe():

    pipe_speed, pipe_gap = get_difficulty()

    max_height = Ground_Y - pipe_gap - 100

    top_height = random.randint(
        100,
        max_height
    )

    bottom_y = top_height + pipe_gap

    new_pipe = {

        "top": pygame.Rect(
            screen_width,
            0,
            Pipe_Width,
            top_height
        ),

        "bottom": pygame.Rect(
            screen_width,
            bottom_y,
            Pipe_Width,
            Ground_Y - bottom_y
        ),

        "speed": pipe_speed,

        "passed": False

    }

    pipes.append(new_pipe)

    print("PIPE CREATED")




def reset_game():

    global bird_y
    global bird_velocity
    global pipes
    global pipe_timer
    global score
    global bird_frame
    global animation_timer
    global game_state

    bird_y = 300
    bird_velocity = 0

    pipes = []

    pipe_timer = 0

    score = 0

    bird_frame = 0

    animation_timer = 0

    game_state = Playing


# ==========================================
# PLAY SOUND
# ==========================================

def play_sound(sound):

    if sound is not None:

        sound.play()




def draw_bird():

    pygame.draw.ellipse(

        screen,
        Yellow,

        (
            bird_x,
            int(bird_y),
            bird_width,
            bird_height
        )

    )


    if bird_frame == 0:

        wing_y = bird_y + 15

    else:

        wing_y = bird_y + 8


    pygame.draw.ellipse(

        screen,
        Orange,

        (
            bird_x + 5,
            int(wing_y),
            20,
            12
        )

    )


    

    pygame.draw.circle(

        screen,
        White,

        (
            bird_x + 28,
            int(bird_y + 9)
        ),

        7

    )


    pygame.draw.circle(

        screen,
        Black,

        (
            bird_x + 30,
            int(bird_y + 9)
        ),

        3

    )


    

    pygame.draw.polygon(

        screen,
        Orange,

        [

            (
                bird_x + 39,
                int(bird_y + 12)
            ),

            (
                bird_x + 52,
                int(bird_y + 17)
            ),

            (
                bird_x + 39,
                int(bird_y + 22)
            )

        ]

    )



def draw_pipe(pipe):

    top_pipe = pipe["top"]
    bottom_pipe = pipe["bottom"]


    pygame.draw.rect(
        screen,
        Green,
        top_pipe
    )


    top_cap = pygame.Rect(

        top_pipe.x - 5,
        top_pipe.bottom - 20,
        Pipe_Width + 10,
        20

    )


    pygame.draw.rect(
        screen,
        Dark_Green,
        top_cap
    )


    pygame.draw.rect(
        screen,
        Green,
        bottom_pipe
    )


    bottom_cap = pygame.Rect(

        bottom_pipe.x - 5,
        bottom_pipe.y,
        Pipe_Width + 10,
        20

    )


    pygame.draw.rect(
        screen,
        Dark_Green,
        bottom_cap
    )




def draw_cloud(x, y, size):

    pygame.draw.circle(
        screen,
        White,
        (int(x), int(y)),
        int(size * 0.25)
    )

    pygame.draw.circle(
        screen,
        White,
        (
            int(x + size * 0.25),
            int(y - size * 0.1)
        ),
        int(size * 0.35)
    )

    pygame.draw.circle(
        screen,
        White,
        (
            int(x + size * 0.5),
            int(y)
        ),
        int(size * 0.28)
    )

    pygame.draw.rect(
        screen,
        White,
        (
            int(x - size * 0.05),
            int(y),
            int(size * 0.6),
            int(size * 0.25)
        )
    )



def draw_ground():

    pygame.draw.rect(

        screen,
        Light_Green,

        (
            0,
            Ground_Y,
            screen_width,
            15
        )

    )

    pygame.draw.rect(

        screen,
        Brown,

        (
            0,
            Ground_Y + 15,
            screen_width,
            Ground_height - 15
        )

    )



running = True


while running:

    
    dt = clock.tick(60)


   

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:



                if game_state == Start:

                    reset_game()

                    bird_velocity = Jump_Strength

                    play_sound(flap_sound)


                elif game_state == Playing:

                    bird_velocity = Jump_Strength

                    play_sound(flap_sound)


             

                elif game_state == Game_Over:

                    reset_game()

                    bird_velocity = Jump_Strength

                    play_sound(flap_sound)



    if game_state == Playing:


        # BIRD PHYSICS

        bird_velocity += Gravity

        bird_y += bird_velocity


        bird_rect = pygame.Rect(

            bird_x,
            int(bird_y),
            bird_width,
            bird_height

        )


        # TOP COLLISION

        if bird_rect.top <= 0:

            bird_y = 0

            game_state = Game_Over

            play_sound(hit_sound)


        # GROUND COLLISION

        if bird_rect.bottom >= Ground_Y:

            bird_y = Ground_Y - bird_height

            game_state = Game_Over

            play_sound(hit_sound)


        # ==================================
        # PIPE TIMER - FIXED
        # ==================================

        pipe_timer += dt


        if pipe_timer >= Pipe_Interval:

            create_pipe()

            pipe_timer = 0



        for pipe in pipes:

            pipe["top"].x -= pipe["speed"]

            pipe["bottom"].x -= pipe["speed"]



        for pipe in pipes:

            if bird_rect.colliderect(pipe["top"]):

                game_state = Game_Over

                play_sound(hit_sound)


            elif bird_rect.colliderect(pipe["bottom"]):

                game_state = Game_Over

                play_sound(hit_sound)



        for pipe in pipes:

            if (

                not pipe["passed"]

                and pipe["top"].right < bird_x

            ):

                pipe["passed"] = True

                score += 1

                play_sound(point_sound)


                if score > high_score:

                    high_score = score



        pipes = [

            pipe

            for pipe in pipes

            if pipe["top"].right > 0

        ]


    

        animation_timer += dt


        if animation_timer >= animation_speed:

            bird_frame += 1

            if bird_frame > 1:

                bird_frame = 0

            animation_timer = 0


   
    screen.fill(Sky_blue)



    for cloud in Clouds:

        draw_cloud(
            cloud[0],
            cloud[1],
            cloud[2]
        )



    for pipe in pipes:

        draw_pipe(pipe)


    

    draw_bird()


    

    draw_ground()


   

    if game_state == Start:

        title = title_font.render(

            "FLAPPY BIRD",

            True,

            Black

        )

        title_rect = title.get_rect(

            center=(
                screen_width // 2,
                200
            )

        )

        screen.blit(
            title,
            title_rect
        )


        instruction = small_font.render(

            "Press SPACE to Start",

            True,

            Black

        )

        instruction_rect = instruction.get_rect(

            center=(
                screen_width // 2,
                350
            )

        )

        screen.blit(
            instruction,
            instruction_rect
        )


  

    elif game_state == Playing:

        score_text = score_font.render(

            str(score),

            True,

            White

        )

        score_rect = score_text.get_rect(

            center=(
                screen_width // 2,
                50
            )

        )

        screen.blit(
            score_text,
            score_rect
        )


        current_speed, current_gap = get_difficulty()


        difficulty_text = small_font.render(

            f"Speed: {current_speed:.1f}",

            True,

            Black

        )

        screen.blit(
            difficulty_text,
            (10, 20)
        )


  

    elif game_state == Game_Over:

        game_over_text = game_over_font.render(

            "GAME OVER",

            True,

            Red

        )

        game_over_rect = game_over_text.get_rect(

            center=(
                screen_width // 2,
                250
            )

        )

        screen.blit(
            game_over_text,
            game_over_rect
        )


        score_text = small_font.render(

            f"Score: {score}",

            True,

            Black

        )

        score_rect = score_text.get_rect(

            center=(
                screen_width // 2,
                330
            )

        )

        screen.blit(
            score_text,
            score_rect
        )


        high_score_text = small_font.render(

            f"High Score: {high_score}",

            True,

            Black

        )

        high_score_rect = high_score_text.get_rect(

            center=(
                screen_width // 2,
                370
            )

        )

        screen.blit(
            high_score_text,
            high_score_rect
        )


        restart_text = small_font.render(

            "Press SPACE to Restart",

            True,

            Black

        )

        restart_rect = restart_text.get_rect(

            center=(
                screen_width // 2,
                430
            )

        )

        screen.blit(
            restart_text,
            restart_rect
        )


    

    pygame.display.update()



pygame.quit()

