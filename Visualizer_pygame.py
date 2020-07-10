import sys
import math
import pygame
from serial import*
class Arduino:
	def __init__(self,port="COM3",baudrate=115200):
		self.port = port
		self.baudrate = baudrate
		self.msg = "Arduino ready"
		self.connected = False
		self.board = None
		
	def connect(self):
		try:
			msg =""
			self.board = Serial(self.port,self.baudrate)
			while msg.find(self.msg) == -1:
				while self.board.inWaiting() == 0:
					pass
				msg = self.board.readline().decode('utf-8')
			
			self.connected =True
			self.board.flush()
			return self.connected 
		except Exception as e:
			print(e)
			return self.connected 
			
	def send(self,d):
		if type(d) != str:
			d =str(d)
		msg = d + '\n'
		msg = msg.encode('utf-8')
		self.board.write(msg)
		while(self.board.inWaiting()==0):
			pass
		data = self.board.readline().decode('utf-8').split(',')
		data[len(data) - 1] = data[len(data) - 1].rstrip()
		return data

	def disconnect(self):
		self.board.close()
		self.connected = False
		
		
		
class Gauge:
	def __init__(self,screen,x=0,y=0,r=1,text = 'dial'):
		self.x = int(x)
		self.y = int(y)
		self.r = int(r)
		self.screen = screen
		self.linewidth = 2
		self.fontsize = 30
		self.text = text + ':'
	def render(self,angle):
		x1 = self.r*math.cos(math.radians(angle)) + self.x 
		y1 = self.r*math.sin(math.radians(angle)) + self.y
		x2 = self.r*math.cos(math.radians(angle + 180)) + self.x
		y2 = self.r*math.sin(math.radians(angle + 180)) + self.y
		pygame.draw.line(self.screen, (127,127,127), (x1,y1), (x2,y2), self.linewidth)
		pygame.draw.circle(self.screen, (127,127,127), (self.x,self.y), self.r+self.linewidth,self.linewidth) 
		text = self.text + '{:.2f}'.format(angle)#str(float(angle))
		font = pygame.font.SysFont(None, self.fontsize)
		img = font.render(text , True, (127,127,127))
		self.screen.blit(img, (self.x  -self.r +self.linewidth +self.fontsize, self.y +self.r + self.linewidth +self.fontsize))
		
		
		
class Visualizer:
	def __init__(self,width=640,height=480):
        self.mouseX,self.mouseY = 0,0
		pygame.init()
		self.clock = clock = pygame.time.Clock()
		self.fps = 60
		self.width, self.height = width, height
		self.display = pygame.display
		self.screen = self.display.set_mode((self.width, self.height))
		self.display.set_caption('Visualizer_pygame')
		self.icon = pygame.image.load('SPCX.ico')
		self.display.set_icon(self.icon)
		self.running = True
		self.background_colour = (255, 255, 255)
		self.debug = False
		self.dial1 = Gauge(self.screen,self.width/5,self.height/2,self.width/10,'roll')
		self.dial2 = Gauge(self.screen,self.width/2,self.height/2,self.width/10,'pitch')
		self.dial3 = Gauge(self.screen,self.width*4/5,self.height/2,self.width/10,'yaw')
		self.Mega = Arduino()
		self.connection = self.Mega.connect()

		
		
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				self.Mega.disconnect()
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if self.debug:
					print(pygame.key.name(event.key),"DOWN")
				else:
					pass
			if event.type == pygame.KEYUP:
				if self.debug:
					print(pygame.key.name(event.key),"UP")
				else:
					pass
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.debug:
					print(event.pos,event.button)
				else:
					pass
			if event.type == pygame.MOUSEBUTTONUP:
				if self.debug:
					print(event.pos,event.button)
				else:
					pass
			if event.type == pygame.MOUSEMOTION:	
				self.mouseX = event.pos[0]
				self.mouseY = event.pos[1]			
				if self.debug:
					print(event.pos,event.rel,event.buttons)

				else:
					pass

	def run(self):
		while self.running:
			self.handle_events()
			self.screen.fill(self.background_colour)
			color = (0,0,0)
			center = self.mouseX,self.mouseY
			radius = 10 
			angle = self.Mega.send(0)
			#print(angle)
			#angle = math.degrees(math.atan2(self.mouseY-self.height/2,self.mouseX-self.width/2))
			self.dial1.render(float(angle[1]))
			self.dial2.render(float(angle[0]))
			self.dial3.render(float(angle[2]))
            pygame.draw.circle(self.screen, color, center, radius) 

			#self.display.update()#UPDATE WHOLE SCREEN,IF NO ARGUMENTS GIVEN SAME AS FLIP
			self.display.flip()# UPDATE ENTIRE SCREEN
			#print(angle,end="\r")
			self.clock.tick(self.fps)
			#print("FPS:",int(round(self.clock.get_fps())),end="\r")
			
			
V = Visualizer()
V.run()


















'''	
pygame.init()
clock = pygame.time.Clock()
(width, height) = (640, 480)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GUI')
programIcon = pygame.image.load('SPCX.ico')
pygame.display.set_icon(programIcon)

running = True
while running:
	background_colour = (0,0,0)
	screen.fill(background_colour)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			print(pygame.key.name(event.key),"DOWN")
		if event.type == pygame.KEYUP:
			print(pygame.key.name(event.key),"UP")
		if event.type == pygame.MOUSEBUTTONDOWN:
			print(event.pos,event.button)
		if event.type == pygame.MOUSEBUTTONUP:
			print(event.pos,event.button)
		if event.type == pygame.MOUSEMOTION:
			print(event.pos,event.rel,event.buttons)
	clock.tick(60) 
pygame.quit()
sys.exit()
'''
