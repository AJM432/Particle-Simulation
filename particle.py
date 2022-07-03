from pygame import Vector2
import time
import config

dt_prev = time.time()
dt = time.time()

class Particle:
    def __init__(self, x, y, vx, vy, ax, ay, radius, mass, color):
        self.pos = Vector2(x, y)
        self.vel = Vector2(vx, vy)
        self.acc = Vector2(ax, ay)
        self.radius = radius
        self.mass = mass
        self.color = color

    def __repr__(self):
        return f'Position:{self.pos}, Velocity:{self.vel}'

    def get_vel_line(self):
        test_x_pos = self.pos.x + self.vel.x/10
        test_y_pos = self.pos.y + self.vel.y/10
        x1 = self.pos.x
        y1 = self.pos.y
        x2 = test_x_pos
        y2 = test_y_pos

        return ((x1, y1), (x2, y2))

    def check_wall_collision(self):
        if self.pos.distance_to(Vector2(config.WIDTH//2, config.HEIGHT//2)) >= 500:
            self.vel =  -self.vel
        # test_x_pos = self.pos.x + (self.vel.x + self.acc.x*config.DELTA_TIME)*config.DELTA_TIME
        # test_y_pos = self.pos.y + (self.vel.y + self.acc.y*config.DELTA_TIME)*config.DELTA_TIME

        # if test_x_pos - self.radius <= 0:
        #     self.vel.x *= -1
        #     self.pos.x=self.radius

        # if test_x_pos + self.radius >= config.WIDTH:
        #     self.vel.x *= -1
        #     self.pos.x = config.WIDTH-self.radius

        # if test_y_pos - self.radius <= 0:
        #     self.vel.y *= -1
        #     self.pos.y = self.radius

        # if test_y_pos + self.radius >= config.HEIGHT:
        #     self.vel.y *= -1
        #     self.pos.y = config.HEIGHT-self.radius

    def get_speed_after_collision(self, object_2): # from elastic collision formula
        return ((self.mass-object_2.mass)/(self.mass + object_2.mass))*self.vel + ((2*object_2.mass)/(self.mass + object_2.mass))*object_2.vel

    def update_pos(self):
        self.vel = self.vel + self.acc*(config.DELTA_TIME) - self.vel*config.MU_AIR # using friction
        self.pos = self.pos + self.vel*(config.DELTA_TIME)

    def update_all(self, dt):
        config.DELTA_TIME = dt
        self.check_wall_collision()
        self.update_pos()

