import SimpleGraphics
import math
import random

screen_width = 320
screen_height = 200
window_width = screen_width * 4
window_height = screen_height * 4

# 40x40 canon
canon_base_size = 30
# 20x10 canon tower
canon_tower_length = 10
canon_tower_width = 10

canon_angle = 0

canon_base_x = 0
canon_base_y = 0
canon_end_x = 0
canon_end_y = 0

canon_angle = 0
canon_length = 10
BULLET_LAUNCH_FACTOR = 60
BULLET_COOLDOWN = 0.1

# bullet information
# bullet_x, bullet_y, bullet_vx, bullet_vy
bullet_array = []
BULLET_ARRAY_IDX_X = 0
BULLET_ARRAY_IDX_Y = 1
BULLET_ARRAY_IDX_VX = 2
BULLET_ARRAY_IDX_VY = 3

helicopter_array = []
HELICOPTER_ARRAY_IDX_X = 0
HELICOPTER_ARRAY_IDX_Y = 1
HELICOPTER_ARRAY_IDX_DIRECTION = 2
HELICOPTER_ARRAY_IDX_FRAME = 3
HELICOPTER_TYPE = 4

HELITYPE_HELICOPTER = 0
HELITYPE_PLANE = 1

helispawn_cooldown = 0
MAX_HELIS = 15
HELI_HEIGHT = 10
HELI_WIDTH = 20
HELI_Y_CHOICES = [HELI_HEIGHT/2, HELI_HEIGHT/2 + HELI_HEIGHT, HELI_HEIGHT/2 + 2*HELI_HEIGHT]
HELI_SPEED = 50
HELISPAWN_COOLDOWN_FACTOR = 2
HELI_SPRITE_FPS = 15
seconds_since_longspawn = 0

particles = []
PARTICLE_ARRAY_IDX_X = 0
PARTICLE_ARRAY_IDX_Y = 1
PARTICLE_ARRAY_IDX_VX = 2
PARTICLE_ARRAY_IDX_VY = 3
gravity = 2

missiles = []
missile_cooldown = 0
MISSILE_ARRAY_IDX_X = 0
MISSILE_ARRAY_IDX_Y = 1
MISSILE_ARRAY_IDX_VX = 2
MISSILE_ARRAY_IDX_VY = 3
MISSILE_RADIUS = 4
MISSILE_DAMAGE = 34

paratroopers = []
landed_paratroopers = []
MAX_PARATROOPERS = 5
PARATROOPER_ARRAY_IDX_X = 0
PARATROOPER_ARRAY_IDX_Y = 1
PARATROOPER_ARRAY_IDX_IS_PARACHUTE = 2
PARATROOPER_ARRAY_IDX_HAS_LANDED = 3
PARATROOPER_ARRAY_IDX_PARACHUTE_Y = 4
PARATROOPER_ARRAY_IDX_ISHIT = 5

PARATROOPER_WIDTH = 5
PARATROOPER_HEIGHT = 10
PARACHUTE_SIZE = 21

PARATROOPER_SPEED = 20
ground_y = screen_height - 10

MISSILE_SPEED = 100
MISSILE_COOLDOWN_FACTOR = 10
MISSILE_PROBABILITY = 0.9

heli_image = 0
heli_image_flipped = 0
plane_image = 0
plane_image_flipped = 0

background_image = 0
paratrooper_image = 0
parachute_image = 0

shoot_sound = 0
explosion_sound = 0
bomb_sound = 0
jump_sound = 0
game_over_sound = 0

# Player's health & score
player_health = 100
player_score = 0


game_running = False
game_over = False
canon_destroyed = False
# Start screen
start_screen_current_frame = 0
start_screen_fps = 10
end_scene_fps = 4
start_screen_frames = ["P", "PY", "PYT", "PYTH", "PYTHO", "PYTHON", "PYTHONT", "PYTHONTR", "PYTHONTRO", "PYTHONTROO", "PYTHONTROOP", "PYTHONTROOPE", "PYTHONTROOPER"]

# Killer screen
has_paratrooper_reached = False
killer_x = 0
killer_y = 0
killer_scene_frame = 0

def draw_start_screen(elapsed):
    global start_screen_current_frame, start_screen_frames
    SimpleGraphics.DrawString(start_screen_frames[int(start_screen_current_frame)], screen_width/2 - 48, screen_height/2 - 10, 255, 255, 255)
    if(start_screen_current_frame >= len(start_screen_frames)-1):
        SimpleGraphics.DrawString("PRESS SPACE TO CONTINUE", screen_width/2 - 80, screen_height/2, 255, 255, 255)
        SimpleGraphics.DrawString("By S. Gautam (RelativisticMechanic)", screen_width/2 - 100, screen_height/2 + 10, 255, 255, 255)
    else:
        start_screen_current_frame += start_screen_fps*(elapsed/1000)

    
def draw_canon():
    global canon_end_x, canon_end_y
    # Draw Canon
    if(canon_destroyed != True):
        SimpleGraphics.DrawBlock((screen_width / 2) - (canon_base_size / 2), screen_height - canon_base_size, canon_base_size, canon_base_size, 80, 80, 80, True)
        SimpleGraphics.DrawBlock((screen_width / 2) - (canon_base_size / 2) + 2, screen_height - canon_base_size + 2, canon_base_size - 4, canon_base_size - 4, 255, 255, 255, True)
        SimpleGraphics.DrawLine((screen_width / 2) - (canon_base_size / 2), screen_height - canon_base_size, (screen_width / 2) - (canon_base_size / 2) + canon_base_size, screen_height - canon_base_size + canon_base_size, 80, 80, 80, True)
        SimpleGraphics.DrawBlock((screen_width/2) - (canon_tower_width /2), screen_height - canon_base_size - canon_tower_length, canon_tower_width, canon_tower_length, 80, 80, 80, True)
        # Calculate canon_end_x, canon_end_y
        canon_end_x = canon_base_x + math.cos(canon_angle) * canon_length
        canon_end_y = canon_base_y - math.sin(canon_angle) * canon_length
        SimpleGraphics.DrawLine(canon_base_x, canon_base_y, canon_end_x, canon_end_y, 255, 255, 0, 4)
        # Draw a circle at the base
        SimpleGraphics.DrawCircle(canon_base_x, canon_base_y, 4, 255, 0, 0, filled=True)
        # Draw one smaller one at the end
        SimpleGraphics.DrawCircle(canon_end_x, canon_end_y, 2, 255, 255, 0, filled=True)
    # Draw Ground
    SimpleGraphics.DrawBlock(0, ground_y, screen_width, 10, 110, 100, 60, True)
    SimpleGraphics.DrawBlock(0, ground_y, screen_width, 5, 100, 180, 100, True)
    

def draw_particles():
    for particle in particles:
        SimpleGraphics.PutPixel(int(particle[PARTICLE_ARRAY_IDX_X]), int(particle[PARTICLE_ARRAY_IDX_Y]), 255, 0, 0)

def draw_bullets():
    for bullet in bullet_array:
        SimpleGraphics.DrawCircle(int(bullet[BULLET_ARRAY_IDX_X]), int(bullet[BULLET_ARRAY_IDX_Y]), MISSILE_RADIUS, 255, 255, 0, True)

def draw_paratroopers():
    for paratrooper in paratroopers:
        x = paratrooper[PARATROOPER_ARRAY_IDX_X]
        y = paratrooper[PARATROOPER_ARRAY_IDX_Y]
        if(paratrooper[PARATROOPER_ARRAY_IDX_IS_PARACHUTE] == True):
            # Draw a parachute too
            SimpleGraphics.DrawImage(parachute_image, x - (int(PARACHUTE_SIZE/2)) + 2, y-PARACHUTE_SIZE)
            
        SimpleGraphics.DrawImage(paratrooper_image, x, y)
    
    for landed_paratrooper in landed_paratroopers:
        x = landed_paratrooper[PARATROOPER_ARRAY_IDX_X]
        y = landed_paratrooper[PARATROOPER_ARRAY_IDX_Y]
        SimpleGraphics.DrawImage(paratrooper_image, x, y)
    
def draw_helis(elapsed):
    for heli in helicopter_array:
        direction = heli[HELICOPTER_ARRAY_IDX_DIRECTION]
        #SimpleGraphics.DrawBlock(int(heli[HELICOPTER_ARRAY_IDX_X]), int(heli[HELICOPTER_ARRAY_IDX_Y]), HELI_WIDTH, HELI_HEIGHT, 255, 255, 255, False)
        if(heli[HELICOPTER_TYPE] == HELITYPE_HELICOPTER):
            # Draw the helicopter itself
            if(heli[HELICOPTER_ARRAY_IDX_DIRECTION] == 1):
                SimpleGraphics.DrawImage(heli_image, int(heli[HELICOPTER_ARRAY_IDX_X]), int(heli[HELICOPTER_ARRAY_IDX_Y]))
            else:
                SimpleGraphics.DrawImage(heli_image_flipped, int(heli[HELICOPTER_ARRAY_IDX_X]), int(heli[HELICOPTER_ARRAY_IDX_Y]))
            
            # Draw the helicopter's bladees
            current_frame = int(heli[HELICOPTER_ARRAY_IDX_FRAME])
            if(current_frame > 4):
                current_frame = 0
                heli[HELICOPTER_ARRAY_IDX_FRAME] = 0
            frame_lines = [[6, 18], [8, 16], [10, 14], [8, 16], [6, 18]]
            if(direction != 1):
                for frame in frame_lines:
                    frame[0] = heli_image.w - frame[0]
                    frame[1] = heli_image.w - frame[1]
            SimpleGraphics.DrawLine(int(heli[HELICOPTER_ARRAY_IDX_X]) + frame_lines[current_frame][0], int(heli[HELICOPTER_ARRAY_IDX_Y]), int(heli[HELICOPTER_ARRAY_IDX_X]) + frame_lines[current_frame][1], heli[HELICOPTER_ARRAY_IDX_Y], 255 - 40*(current_frame), 0, 0)
        
        else:    
            if(heli[HELICOPTER_ARRAY_IDX_DIRECTION] == 1):
                SimpleGraphics.DrawImage(plane_image, int(heli[HELICOPTER_ARRAY_IDX_X]), int(heli[HELICOPTER_ARRAY_IDX_Y]))
            else:
                SimpleGraphics.DrawImage(plane_image_flipped, int(heli[HELICOPTER_ARRAY_IDX_X]), int(heli[HELICOPTER_ARRAY_IDX_Y]))
            
            # Draw three rotating pixel points
            current_frame = int(heli[HELICOPTER_ARRAY_IDX_FRAME])
            x = heli[HELICOPTER_ARRAY_IDX_X]
            y = heli[HELICOPTER_ARRAY_IDX_Y]

            # Where to draw the exhaust pixels relative to the sprite
            frame_exhausts = [ 
                [[-1,10], [0,8], [1, 10]], 
                [[1,8], [-1,10], [-1, 8]], 
                [[-1,8], [0, 10], [1, 8]],
                [[-1,9], [1, 8], [1, 10]]
            ]

            if(current_frame >= len(frame_exhausts)):
                heli[HELICOPTER_ARRAY_IDX_FRAME] = 0
                current_frame = 0

            if(direction != 1):
                for triangle in frame_exhausts:
                    for pixel in triangle:
                        pixel[0] = heli_image.w - pixel[0]
            
            # Draw the frame
            for pixel in frame_exhausts[current_frame]:
                SimpleGraphics.PutPixel(int(x+pixel[0]), int(y+pixel[1]), 255, 0, 0)

            
            
        heli[HELICOPTER_ARRAY_IDX_FRAME] += HELI_SPRITE_FPS*(elapsed/1000)

def draw_missiles():
    for missile in missiles:
        SimpleGraphics.DrawCircle(missile[MISSILE_ARRAY_IDX_X], missile[MISSILE_ARRAY_IDX_Y], MISSILE_RADIUS, 255, 0, 0, True)

def update_bullets(elapsed):
    for idx, bullet in enumerate(bullet_array):
        bullet[BULLET_ARRAY_IDX_X] += bullet[BULLET_ARRAY_IDX_VX]*(elapsed/1000)
        bullet[BULLET_ARRAY_IDX_Y] += bullet[BULLET_ARRAY_IDX_VY]*(elapsed/1000)
        if(bullet[BULLET_ARRAY_IDX_X] > screen_width) or (bullet[BULLET_ARRAY_IDX_X] < 0) or (bullet[BULLET_ARRAY_IDX_Y] > screen_height) or (bullet[BULLET_ARRAY_IDX_Y] < 0):
            del bullet_array[idx]

def update_helis(elapsed):
    global helicopter_array, helispawn_cooldown, missile_cooldown
    # spawn a helicopter if there are none
    if(len(helicopter_array) < MAX_HELIS and (not (helispawn_cooldown > 0))):
        # Get direction
        direction = random.choice([-1, 1])
        heli_x = 0
        heli_y = random.choice(HELI_Y_CHOICES)
        heli_type = random.choice([HELITYPE_HELICOPTER, HELITYPE_PLANE])

        # Now check if this slot is free
        do_not_spawn = False
        flip_direction = False

        # First check
        for heli in helicopter_array:
            if(heli[HELICOPTER_ARRAY_IDX_Y] == heli_y):
                if(heli[HELICOPTER_ARRAY_IDX_DIRECTION] != direction):
                     flip_direction = True
                # Check if we're spawning a plane on a helicopter airspace
                # It's not nice to have the plane over take the helicopter
                # it looks very shabby on gameplay
                if(heli_type == HELITYPE_PLANE and heli[HELICOPTER_TYPE] == HELITYPE_HELICOPTER):
                    do_not_spawn = True
        
        if(flip_direction == True): direction = -direction

        # Second check
        for heli in helicopter_array:
            if(heli[HELICOPTER_ARRAY_IDX_Y] == heli_y):
                if(heli[HELICOPTER_ARRAY_IDX_DIRECTION] != direction):
                     do_not_spawn = True

        # Problem! This slot is not free!
        if(do_not_spawn == False):
            if(direction == 1):
                heli_x = 0+random.randrange(0, 20)
            else:
                heli_x = screen_width - random.randrange(0,20)
            
            helicopter_array.append(
                [heli_x, heli_y, direction, 0, heli_type]
            )
            helispawn_cooldown = 3 + random.randrange(-1, 3)
            # Once in a while stop for a long time, do this when the player has reached a certain point
            if(player_score > 300):
                # Ensure a gap
                global seconds_since_longspawn
                if(seconds_since_longspawn > 30):
                    seconds_since_longspawn = 0
                    long_cooldown = random.choice([True, False, False, False, False])
                    if(long_cooldown):
                        helispawn_cooldown += 30
                else:
                    seconds_since_longspawn += (elapsed/1000)

    for idx, heli in enumerate(helicopter_array):
        # Multiply by HELICOPTER_TYPE to speed up if plane
        heli[HELICOPTER_ARRAY_IDX_X] += HELI_SPEED * (elapsed/1000) * heli[HELICOPTER_ARRAY_IDX_DIRECTION] * (1+(heli[HELICOPTER_TYPE]))
        if(heli[HELICOPTER_ARRAY_IDX_X] > screen_width or heli[HELICOPTER_ARRAY_IDX_X] < 0):
            del helicopter_array[idx]
        # Drop a missile or a paratrooper
        should_drop = random.randrange(0,100)
        if(should_drop < MISSILE_PROBABILITY*100 and (not (missile_cooldown > 0))):
            # Chooice b/w paratrooper and missile
            what_to_drop = heli[HELICOPTER_TYPE]
            # If we're right atop the gun don't drop the paratrooper
            if(heli[HELICOPTER_ARRAY_IDX_X] > screen_width/2 - canon_base_size/2 and heli[HELICOPTER_ARRAY_IDX_X] < screen_width/2 + canon_base_size/2):
                what_to_drop = 1
            if(what_to_drop == 0):
                # Drop paratrooper
                paratroopers.append(
                    [
                        heli[HELICOPTER_ARRAY_IDX_X] - (heli[HELICOPTER_ARRAY_IDX_X]%PARATROOPER_WIDTH),
                        heli[HELICOPTER_ARRAY_IDX_Y] + PARATROOPER_HEIGHT,
                        False,
                        False,
                        screen_height/2 - 10 - random.randrange(10, 30),
                        False
                    ]
                )
                SimpleGraphics.PlaySound(jump_sound)
            else:
                # Where's the player
                missile_dir_x = canon_base_x - heli[HELICOPTER_ARRAY_IDX_X]
                missile_dir_y = canon_base_y - heli[HELICOPTER_ARRAY_IDX_Y]
                magnitude = math.sqrt(missile_dir_x * missile_dir_x + missile_dir_y * missile_dir_y)

                missiles.append(
                    [
                        heli[HELICOPTER_ARRAY_IDX_X],
                        heli[HELICOPTER_ARRAY_IDX_Y] + MISSILE_RADIUS,
                        missile_dir_x / magnitude, 
                        missile_dir_y / magnitude
                    ]
                )
                SimpleGraphics.PlaySound(bomb_sound)
            
            missile_cooldown = 40 + random.randrange(-1, 3)
            
            

    missile_cooldown -= (elapsed/1000)*MISSILE_COOLDOWN_FACTOR
    helispawn_cooldown -= (elapsed/1000)*HELISPAWN_COOLDOWN_FACTOR


def create_explosion(x, y, radius):
    for k in range(0, random.randrange(100, 150)):
        particles.append([
            x + random.randrange(-int(radius/2), int(radius/2)),
            y + random.randrange(-int(radius/2), int(radius/2)),
            random.randrange(-100, 100),
            random.randrange(-200, 200)
        ])
    SimpleGraphics.PlaySound(explosion_sound)

def update_collisions(elapsed):
    global player_score, player_health
    for idx_bul, bullet in enumerate(bullet_array):
        for idx_heli, heli in enumerate(helicopter_array):
            # Check if bullet is in heli
            if(bullet[BULLET_ARRAY_IDX_X] > heli[HELICOPTER_ARRAY_IDX_X] and bullet[BULLET_ARRAY_IDX_X] < heli[HELICOPTER_ARRAY_IDX_X] + HELI_WIDTH):
                if(bullet[BULLET_ARRAY_IDX_Y] > heli[HELICOPTER_ARRAY_IDX_Y] and bullet[BULLET_ARRAY_IDX_Y] < heli[HELICOPTER_ARRAY_IDX_Y] + HELI_HEIGHT):
                    # We got collision
                    # Create explosion
                    explosion_centre_x = heli[HELICOPTER_ARRAY_IDX_X] + HELI_WIDTH/2
                    explosion_centre_y = heli[HELICOPTER_ARRAY_IDX_Y] + HELI_HEIGHT/2
                    create_explosion(explosion_centre_x, explosion_centre_y, HELI_WIDTH)
                    del helicopter_array[idx_heli]
                    del bullet_array[idx_bul]
                    if(heli[HELICOPTER_TYPE] == HELITYPE_PLANE):
                        player_score += 50
                    else:
                        player_score += 30

    for idx_bul, bullet in enumerate(bullet_array):
        for idx_para, paratrooper in enumerate(paratroopers):
            bullet_x = bullet[BULLET_ARRAY_IDX_X]
            bullet_y = bullet[BULLET_ARRAY_IDX_Y]
            paratrooper_x = paratrooper[PARATROOPER_ARRAY_IDX_X]
            paratrooper_y = paratrooper[PARATROOPER_ARRAY_IDX_Y]
            # Check if we hit paratrooper
            if(bullet_x > paratrooper_x and bullet_x < paratrooper_x + PARATROOPER_WIDTH):
                if(bullet_y > paratrooper_y and bullet_y < paratrooper_y + PARATROOPER_HEIGHT):
                    explosion_centre_x = paratrooper[PARATROOPER_ARRAY_IDX_X] + PARATROOPER_WIDTH/2
                    explosion_centre_y = paratrooper[PARATROOPER_ARRAY_IDX_Y] + PARATROOPER_HEIGHT/2
                    create_explosion(explosion_centre_x, explosion_centre_y, PARATROOPER_WIDTH)
                    del paratroopers[idx_para]
                    del bullet_array[idx_bul]
                    player_score += 10    
            # Check if paratrooper has a parachute
            if(paratrooper[PARATROOPER_ARRAY_IDX_IS_PARACHUTE] == True):
                parachute_x = paratrooper_x - int(PARACHUTE_SIZE/2) + 3
                parachute_y = paratrooper_y - PARACHUTE_SIZE
                if(bullet_x > parachute_x and bullet_x < parachute_x + PARACHUTE_SIZE):
                    if(bullet_y > parachute_y and bullet_y < parachute_y + PARACHUTE_SIZE):
                        paratrooper[PARATROOPER_ARRAY_IDX_ISHIT] = True
                        paratrooper[PARATROOPER_ARRAY_IDX_IS_PARACHUTE] = False
                        explosion_centre_x = paratrooper_x - int(PARACHUTE_SIZE/2) + 3 + PARACHUTE_SIZE/2
                        explosion_centre_y = paratrooper_y - PARACHUTE_SIZE/2
                        create_explosion(explosion_centre_x, explosion_centre_y, PARATROOPER_WIDTH)

    
    for idx_mis, missile in enumerate(missiles):
        for idx_bul, bullet in enumerate(bullet_array):
            distance_sq = (missile[MISSILE_ARRAY_IDX_X] - bullet[BULLET_ARRAY_IDX_X])*(missile[MISSILE_ARRAY_IDX_X] - bullet[BULLET_ARRAY_IDX_X]) + (missile[MISSILE_ARRAY_IDX_Y] - bullet[BULLET_ARRAY_IDX_Y])*(missile[MISSILE_ARRAY_IDX_Y] - bullet[BULLET_ARRAY_IDX_Y])
            if(distance_sq <= (MISSILE_RADIUS+8)*(MISSILE_RADIUS+8)):
                create_explosion(missile[MISSILE_ARRAY_IDX_X], missile[MISSILE_ARRAY_IDX_Y], MISSILE_RADIUS*2)
                del missiles[idx_mis]
                del bullet_array[idx_bul]
                player_score += 5

    # missile collisions
    for idx_mis, missile in enumerate(missiles):
        # Calculate distance b/w canon base and missile
        distance_sq = (missile[MISSILE_ARRAY_IDX_X] - canon_base_x)*(missile[MISSILE_ARRAY_IDX_X] - canon_base_x) + (missile[MISSILE_ARRAY_IDX_Y] - canon_base_y)*(missile[MISSILE_ARRAY_IDX_Y] - canon_base_y)
        if(distance_sq < MISSILE_RADIUS*MISSILE_RADIUS):
            player_health -= MISSILE_DAMAGE
            create_explosion(canon_base_x, canon_base_y, 20)
            del missiles[idx_mis]
                
def update_particles(elapsed):
    for idx, particle in enumerate(particles):
        particle[PARTICLE_ARRAY_IDX_X] += particle[PARTICLE_ARRAY_IDX_VX] * (elapsed/1000)
        particle[PARTICLE_ARRAY_IDX_Y] += particle[PARTICLE_ARRAY_IDX_VY] * (elapsed/1000)
        particle[PARTICLE_ARRAY_IDX_VY] += gravity
        if(particle[PARTICLE_ARRAY_IDX_X] > screen_width) or (particle[PARTICLE_ARRAY_IDX_X] < 0) or (particle[PARTICLE_ARRAY_IDX_Y] > screen_height) or (particle[PARTICLE_ARRAY_IDX_Y] < 0):
            del particles[idx]

def update_missiles(elapsed):
    for idx, missile in enumerate(missiles):
        missile[MISSILE_ARRAY_IDX_X] += MISSILE_SPEED * (elapsed/1000) * missile[MISSILE_ARRAY_IDX_VX]
        missile[MISSILE_ARRAY_IDX_Y] += MISSILE_SPEED * (elapsed/1000) * missile[MISSILE_ARRAY_IDX_VY]
        if(missile[MISSILE_ARRAY_IDX_Y] > screen_height or missile[MISSILE_ARRAY_IDX_X] > screen_width or missile[MISSILE_ARRAY_IDX_X] < 0 or missile[MISSILE_ARRAY_IDX_Y] < 0):
            del missiles[idx]

def update_paratroopers(elapsed):
    global player_score

    for idx_para, paratrooper in enumerate(paratroopers):

        if(paratrooper[PARATROOPER_ARRAY_IDX_HAS_LANDED] == False):
            if(paratrooper[PARATROOPER_ARRAY_IDX_IS_PARACHUTE]):
                paratrooper[PARATROOPER_ARRAY_IDX_Y] += PARATROOPER_SPEED*(elapsed/1000)
            else:
                paratrooper[PARATROOPER_ARRAY_IDX_Y] += PARATROOPER_SPEED*2*(elapsed/1000)

            if(paratrooper[PARATROOPER_ARRAY_IDX_Y] > paratrooper[PARATROOPER_ARRAY_IDX_PARACHUTE_Y] and paratrooper[PARATROOPER_ARRAY_IDX_ISHIT] == False):
                paratrooper[PARATROOPER_ARRAY_IDX_IS_PARACHUTE] = True
                    
            
            # Check if we are colliding with a landed paratrooper
            for landed_paratrooper in landed_paratroopers:
                if(paratrooper[PARATROOPER_ARRAY_IDX_X] == landed_paratrooper[PARATROOPER_ARRAY_IDX_X]):
                    # Wait, just ensure that this is not this parachute itself
                    # otherwise we go in an infinite loop!
                    if(paratrooper[PARATROOPER_ARRAY_IDX_HAS_LANDED] == True):
                        pass
                    # Are we right above him?
                    else:

                        if(paratrooper[PARATROOPER_ARRAY_IDX_Y]+PARATROOPER_HEIGHT >= landed_paratrooper[PARATROOPER_ARRAY_IDX_Y]):
                            
                            # Is this paratrooper hit? 
                            if(paratrooper[PARATROOPER_ARRAY_IDX_ISHIT] == True):
                                # Destroy all paratroopers on this X-coordinate!
                                max_y = 0
                                for idx_landed, landed_paratrooper2 in enumerate(landed_paratroopers):
                                    if(landed_paratrooper2[PARATROOPER_ARRAY_IDX_X] == paratrooper[PARATROOPER_ARRAY_IDX_X]):
                                        if(max_y < landed_paratrooper2[PARATROOPER_ARRAY_IDX_Y]):
                                            max_y = landed_paratrooper2[PARATROOPER_ARRAY_IDX_X]
                                        del landed_paratroopers[idx_landed]
                                create_explosion(paratrooper[PARATROOPER_ARRAY_IDX_X], max_y/2 + 10, max_y/2 + 10)
                            # Otherwise stack em up!
                            else:
                                paratrooper[PARATROOPER_ARRAY_IDX_Y] = landed_paratrooper[PARATROOPER_ARRAY_IDX_Y]-PARATROOPER_HEIGHT
                                paratrooper[PARATROOPER_ARRAY_IDX_HAS_LANDED] = True
                                paratrooper[PARATROOPER_ARRAY_IDX_IS_PARACHUTE] = False
                                landed_paratroopers.append(paratrooper)
                                del paratroopers[idx_para]
            
            if(paratrooper[PARATROOPER_ARRAY_IDX_Y]+PARATROOPER_HEIGHT >= ground_y):
                if(paratrooper[PARATROOPER_ARRAY_IDX_ISHIT] == True):
                    explosion_centre_x = paratrooper[PARATROOPER_ARRAY_IDX_X] + PARATROOPER_WIDTH/2
                    explosion_centre_y = paratrooper[PARATROOPER_ARRAY_IDX_Y] + PARATROOPER_HEIGHT/2
                    create_explosion(explosion_centre_x, explosion_centre_y, PARATROOPER_WIDTH)
                    del paratroopers[idx_para]
                    player_score += 10
                else:
                    paratrooper[PARATROOPER_ARRAY_IDX_Y] = ground_y-PARATROOPER_HEIGHT
                    paratrooper[PARATROOPER_ARRAY_IDX_HAS_LANDED] = True
                    paratrooper[PARATROOPER_ARRAY_IDX_IS_PARACHUTE] = False
                    del paratroopers[idx_para]
                    landed_paratroopers.append(paratrooper)

def is_game_over():
    global game_over, has_paratrooper_reached, killer_x, killer_y
    if(game_over == True):
        return
    
    for landed_trooper in landed_paratroopers:
        if(landed_trooper[PARATROOPER_ARRAY_IDX_Y] < screen_height - MAX_PARATROOPERS * PARATROOPER_HEIGHT) or (player_health <= 0):
            game_over = True
            has_paratrooper_reached = True
            killer_x = landed_trooper[PARATROOPER_ARRAY_IDX_X]
            killer_y = landed_trooper[PARATROOPER_ARRAY_IDX_Y]
            SimpleGraphics.PlaySound(game_over_sound)
        
    if(player_health <= 0):
        game_over = True
        SimpleGraphics.PlaySound(game_over_sound)
        

def Create():
    global canon_base_x, canon_base_y 
    global heli_image, heli_image_flipped, background_image, paratrooper_image, parachute_image, plane_image, plane_image_flipped
    global shoot_sound, explosion_sound, bomb_sound, jump_sound, game_over_sound
    # calculate canon_base_x, and canon_base_y
    canon_base_x = screen_width/2
    canon_base_y = screen_height - canon_tower_length - canon_base_size

    heli_image = SimpleGraphics.LoadImage("./data/heli.png")
    heli_image = SimpleGraphics.MakeTransparentImage(heli_image, 0,0,0)
    heli_image_flipped = SimpleGraphics.FlipImage(heli_image, True, False)

    plane_image = SimpleGraphics.LoadImage("./data/plane.png")
    plane_image = SimpleGraphics.MakeTransparentImage(plane_image, 0,0,0)
    plane_image_flipped = SimpleGraphics.FlipImage(plane_image, True, False)

    paratrooper_image = SimpleGraphics.LoadImage("./data/paratrooper.png")
    paratrooper_image = SimpleGraphics.MakeTransparentImage(paratrooper_image, 0,0,0)
    parachute_image = SimpleGraphics.LoadImage("./data/parachute.png")
    parachute_image = SimpleGraphics.MakeTransparentImage(parachute_image, 0,0,0)

    background_image = SimpleGraphics.LoadImage("./data/background.png")

    shoot_sound = SimpleGraphics.LoadSound("./data/shoot.wav")
    explosion_sound = SimpleGraphics.LoadSound("./data/explosion.wav")
    bomb_sound = SimpleGraphics.LoadSound("./data/bomb.wav")
    jump_sound = SimpleGraphics.LoadSound("./data/jump.wav")
    game_over_sound = SimpleGraphics.LoadSound("./data/over.wav")
    return

def update_difficulty():
    global MISSILE_SPEED, MAX_HELIS, MISSILE_PROBABILITY, MISSILE_COOLDOWN_FACTOR, HELI_SPEED, HELISPAWN_COOLDOWN_FACTOR
    if(player_score >= 100): 
        MISSILE_SPEED = 100
        MAX_HELIS = 10
        MISSILE_COOLDOWN_FACTOR = 10
        MISSILE_PROBABILITY = 0.30
        HELI_SPEED = 60
        HELISPAWN_COOLDOWN_FACTOR = 3

    if(player_score >= 200):
        MISSILE_SPEED = 120
        MAX_HELIS = 15
        MISSILE_COOLDOWN_FACTOR = 20
        MISSILE_PROBABILITY = 0.40
        HELI_SPEED = 70
        HELISPAWN_COOLDOWN_FACTOR = 4

    if(player_score >= 500):
        MISSILE_SPEED = 140
        MAX_HELIS = 20
        MISSILE_COOLDOWN_FACTOR = 80
        MISSILE_PROBABILITY = 0.50
        HELI_SPEED = 80   
        HELISPAWN_COOLDOWN_FACTOR = 8

    if(player_score >= 1000):
        MISSILE_SPEED = 150
        MAX_HELIS = 25
        MISSILE_COOLDOWN_FACTOR = 100
        MISSILE_PROBABILITY = 0.60
        HELI_SPEED = 100
        HELISPAWN_COOLDOWN_FACTOR = 10
    
    if(player_score < 100):
        MISSILE_SPEED = 50
        MAX_HELIS = 5
        MISSILE_COOLDOWN_FACTOR = 5
        HELISPAWN_COOLDOWN_FACTOR = 2
        HELI_SPEED = 50

def paratrooper_kill_sequence(elapsed):
    global killer_scene_frame, has_paratrooper_reached, canon_destroyed, player_health
    if(canon_destroyed == True):
        return
    player_health -= 10 * end_scene_fps * (elapsed/1000)
    f = int(killer_scene_frame)
    if(f == 0 or f == 6 or f == 10):
        SimpleGraphics.DrawLine(killer_x, killer_y, canon_base_x, canon_base_y, 255, 0, 0, 1)
        killer_scene_frame += end_scene_fps * (elapsed/1000)
    elif(f == 1 or f == 5 or f == 9):
        SimpleGraphics.DrawLine(killer_x, killer_y, canon_base_x, canon_base_y, 255, 0, 0, 2)
        killer_scene_frame += end_scene_fps * (elapsed/1000)
    elif(f == 2 or f == 4 or f == 8):
        SimpleGraphics.DrawLine(killer_x, killer_y, canon_base_x, canon_base_y, 255, 0, 0, 3)
        killer_scene_frame += end_scene_fps * (elapsed/1000)
    elif(f == 3 or f == 7):
        SimpleGraphics.DrawLine(killer_x, killer_y, canon_base_x, canon_base_y, 255, 0, 0, 4)
        killer_scene_frame += end_scene_fps * (elapsed/1000)
    elif(f == 11):
        create_explosion(canon_base_x, canon_base_y, canon_base_size)
        canon_destroyed = True
        has_paratrooper_reached = False

def Update(elapsed):
    if(not (game_running)):
        return

    update_particles(elapsed)
    is_game_over()
    
    if(game_over == True):
        return
    
    update_difficulty()
    update_bullets(elapsed)
    update_helis(elapsed)
    update_collisions(elapsed)
    update_missiles(elapsed)
    update_paratroopers(elapsed)
    return

def OnKeyPress(elapsed, key):
    global player_score, game_running

    if(not game_running):
        if(key == SimpleGraphics.BTN_SPACE):
            game_running = True
        return
        
    if(key == SimpleGraphics.BTN_SPACE):
        # Calculate velocity direction
        bullet_vx = (canon_end_x - canon_base_x)*BULLET_LAUNCH_FACTOR
        bullet_vy = (canon_end_y - canon_base_y)*BULLET_LAUNCH_FACTOR

        bullet_array.append(
            [canon_end_x, canon_end_y, bullet_vx, bullet_vy]
        )
        if(player_score < 5):
            player_score = 0
        else:
            player_score -= 5
        SimpleGraphics.PlaySound(shoot_sound)
    
    return
def OnKeyPressed(elapsed, key):
    global canon_angle
    if(not game_running):
        return 

    if(key == SimpleGraphics.BTN_LEFT):
        canon_angle += 0.005*(elapsed)
    if(key == SimpleGraphics.BTN_RIGHT):
        canon_angle -= 0.005 * (elapsed)
    if(canon_angle < 0):
        canon_angle = 0
    elif(canon_angle > math.pi):
        canon_angle = math.pi
    return
def OnKeyRelease(elapsed, key):
    return
def Draw(elapsed):
    SimpleGraphics.Clear(0,0,0)
    if(not game_running):
        draw_start_screen(elapsed)
        return

    SimpleGraphics.DrawImage(background_image, 0, 0)
    draw_canon()
    draw_bullets()
    draw_helis(elapsed)
    draw_paratroopers()
    draw_particles()
    draw_missiles()

    if(has_paratrooper_reached):
        paratrooper_kill_sequence(elapsed)
    else:
        global canon_destroyed
        if(game_over == True and canon_destroyed == False):
            create_explosion(canon_base_x, canon_base_y, canon_base_size/2)
            canon_destroyed = True
        
        if(canon_destroyed == True):
            SimpleGraphics.DrawString("THE BAD GUYS DESTROYED YOUR BASE!", screen_width/2 - 96, screen_height/2 - 8, 255, 255, 255)

    # Draw HUD
    SimpleGraphics.DrawBlock(screen_width / 2 - canon_base_size, ground_y, canon_base_size * 2, 10, 255, 255, 255, True)
    SimpleGraphics.DrawBlock(screen_width / 2 - canon_base_size + 2, ground_y + 2, int((canon_base_size * 2 - 4) * (player_health/100)), 6, 255, 0, 0, True)
    SimpleGraphics.DrawString("SCORE: " + str(player_score), screen_width - 80, screen_height - 10, 255, 255, 255)
    return
def OnMouseMove(elapsed, x, y):
    return
def OnExit(elapsed):
    print("Your score: " + str(player_score))
    return

SimpleGraphics.Run(screen_width, screen_height, window_width, window_height, Create, Update, Draw, OnKeyPress, OnKeyPressed, OnKeyRelease, OnMouseMove, OnExit, 'Consolas', 10)
SimpleGraphics.Quit()