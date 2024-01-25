import pygame
import math

class Envir:
    def __init__(self,dimensions):
        #colors
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,255,0) 
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.yel = (255,255,0)

        #map dimensions
        self.height = dimensions[0]
        self.width = dimensions[1]

        #window settings
        pygame.display.set_caption("Differential Drive Robot")
        self.map = pygame.display.set_mode((self.width,self.height))

        #text variables
        self.text="default text"
        self.font=pygame.font.Font('freesansbold.ttf',50)
        self.text=self.font.render('default',True,self.white,self.black)
        self.textRect=self.text.get_rect()
        self.textRect.center=(dimensions[1]-600,dimensions[0]-150)

        #trail 
        self.trail_set=[]

    def write_info(self,vel_l,vel_r,theta):
        txt=f"vel_l={vel_l} vel_r={vel_r} theta={int(math.degrees(theta))}"
        self.text=self.font.render(txt,True,self.white,self.black)
        self.map.blit(self.text,self.textRect)
    
    def trail(self,pos):
        for i in range(0,len(self.trail_set)-1):
            pygame.draw.line(self.map,self.yel,(self.trail_set[i][0],self.trail_set[i][1]),(self.trail_set[i+1][0],self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__()>20000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)

    def robot_frame(self,pos,rotation):
        n=80

        centerx,centery=pos
        x_axis=(centerx+n*math.cos(rotation),centery+n*math.sin(rotation))
        y_axis=(centerx+n*math.cos(rotation+math.pi/2),centery+n*math.sin(rotation+math.pi/2))
        pygame.draw.line(self.map,self.red,(centerx,centery),x_axis,3)
        pygame.draw.line(self.map,self.blue,(centerx,centery),y_axis,3)

class Robot:
    def __init__(self,startpos,robotImg,width):
        self.m2p=3779.52 #meters to pixels (3779.52)
        
        #robot dimensions
        self.w=width
        self.x=startpos[0]
        self.y=startpos[1]
        self.theta=0
        self.vel_l=0.01*self.m2p
        self.vel_r=0.01*self.m2p #0.01 cms
        self.maxspeed=0.1*self.m2p
        self.minspeed=0.02*self.m2p

        #graphics
        self.img=pygame.image.load(robotImg)
        self.rotated=self.img
        self.rect=self.rotated.get_rect(center=(self.x,self.y))

    def draw(self,map):
        map.blit(self.rotated,self.rect)

    def move(self,event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.vel_l+=0.5*self.m2p
                elif event.key == pygame.K_a:
                    self.vel_l-=0.5*self.m2p
                elif event.key == pygame.K_s:
                    self.vel_r+=0.5*self.m2p
                elif event.key == pygame.K_d:
                    self.vel_r-=0.5*self.m2p
        #print(type(self.x))
        #print(type(self.vel_l))
        #print(type(self.vel_r))
        self.x += ((self.vel_l + self.vel_r) / 2.0)*math.cos(self.theta)*dt
        self.y += ((self.vel_l + self.vel_r) / 2.0)*math.sin(self.theta)*dt
        self.theta += (self.vel_r-self.vel_l)/self.w*dt
        #reset theta
        if self.theta > 2 * math.pi or self.theta < -2 * math.pi:
            self.theta=0
        #set max speed
        self.vel_r = max(self.vel_r,self.maxspeed)
        self.vel_l = max(self.vel_l,self.maxspeed)
        #set min speed
        self.vel_r = min(self.vel_r,self.minspeed)
        self.vel_l = min(self.vel_l,self.minspeed)

        self.rotated=pygame.transform.rotozoom(self.img,math.degrees(-  self.theta),1)
        self.rect=self.rotated.get_rect(center=(self.x,self.y))

#initialisation
pygame.init()

#start positions
start=(200,200)

#dimensions
dimensions=(800,1500)

#running or not
running=True

#the envir
environment=Envir(dimensions) 

#the robot
robot=Robot(start,r"D:\Coding\Python\robot.py\Differential_Drive_Sim\robot_image.png"  ,0.01*3779.52)

#dt
dt=0
lasttime=pygame.time.get_ticks()

#simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        robot.move(event)
        
    dt=(pygame.time.get_ticks()-lasttime)/1000
    lasttime=pygame.time.get_ticks()
    
    robot.move()
    
    pygame.display.update() 
    environment.map.fill(environment.black)
    environment.write_info(int(robot.vel_l),int(robot.vel_r),robot.theta)   
    robot.draw(environment.map)    
    environment.robot_frame((robot.x,robot.y),robot.theta)
    environment.trail((robot.x,robot.y))