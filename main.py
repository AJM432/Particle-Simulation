import pygame
from pygame import Vector2
from particle import Particle
import config
import random

pygame.init()

WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Collision Detection")
clock = pygame.time.Clock()
dt = 0

particle_list = [Particle(x=config.WIDTH//2 + random.randint(-config.WIDTH//2, config.WIDTH//2), y=config.HEIGHT//2+random.randint(-config.HEIGHT//2, config.HEIGHT//2), vx=random.randint(-100, 100), vy=random.randint(-100, 100), ax=0, ay=-100, radius=config.PARTICLE_SIZE, mass=1, color = (random.randint(0, 255), 0, 0)) for x in range(config.NUM_PARTICLES)]
# particle_list = [Particle(x=config.WIDTH//2, y=config.HEIGHT//2, vx=0, vy=50, ax=0, ay=0, radius=10, mass=10, color=(0, 255, 255)), Particle(x=config.WIDTH//2, y=config.HEIGHT//2+500, vx=0, vy=-100, ax=0, ay=0, radius=10, mass=10, color=(0, 255, 255))]

def convert_ranges(value, value_min, value_max, new_min, new_max):
    return (((value - value_min) * (new_max - new_min)) / (value_max - value_min)) + new_min


def check_object_collision():
    sorted_particles_x_axis = sorted(particle_list, key=lambda particle: particle.pos.x) # sorts particles by order on x-axis
    possible_collisions = [] # stores possible collision pairs
    for index, particle in enumerate(sorted_particles_x_axis): # loop through all particles

        # particle.color = (convert_ranges(particle.pos.y, 0, config.HEIGHT, 20, 255), 0, 50)
        particle.acc.y = -convert_ranges(particle.pos.y, 0, config.HEIGHT, -500, 500)
        particle.acc.x = convert_ranges(particle.pos.y, 0, config.WIDTH, -500, 500)

        active_interval = [particle.pos.x-particle.radius, particle.pos.x+particle.radius] # create a interval to compare adjacent particle positions
        for y in range(index+1, len(sorted_particles_x_axis)): # loop through rest of particles
            if sorted_particles_x_axis[y].pos.x <= active_interval[1] and sorted_particles_x_axis[y].pos.x >= active_interval[0]: # check if intervals collide
                possible_collisions.append([particle, sorted_particles_x_axis[y]])
            else:
                break
    
    for particle in possible_collisions:
        if particle[0].pos.distance_to(particle[1].pos) <= particle[0].radius + particle[1].radius:
            particle[0].vel, particle[1].vel = particle[0].get_speed_after_collision(particle[1]), particle[1].get_speed_after_collision(particle[0]) # must use same line assignment, otherwise second particle uses new velocity of first particle
            
running = True
while running:
    clock.tick(config.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    WIN.fill(config.BLACK)
    dt = clock.tick(config.FPS)/1000
    for x in particle_list:
        x.update_all(dt)
        line = x.get_vel_line()
        pygame.draw.circle(WIN, x.color, x.pos, x.radius)
    
    check_object_collision()

    pygame.display.flip()
pygame.quit()
