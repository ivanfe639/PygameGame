import pygame
import spritesheet
from defines import *

class AnimationSprites:
	
	def __init__(self, Name, pathSprite, sizeXSprite, sizeYSprite, scaleSprite, cooldown, flipX, flipY, positionX,positionY,
			     indexIdle, numFramesIdle,
				 indexHurt, numFrameHurt,
				 indexAttack, numFramesAttack):

		self.name = Name

		## Sprites atributes
		spriteSheetImage = pygame.image.load(pathSprite).convert_alpha()
		self.spriteSheet = spritesheet.SpriteSheet(spriteSheetImage, sizeXSprite, sizeYSprite, scaleSprite)  		#Objeto que carga los sprites para las animaciones

		self.idleAniFrames = self.extractAnimationFrames(indexIdle, numFramesIdle)				# Contain each frame of the animation 
		self.HurtAniFrames = self.extractAnimationFrames(indexHurt, numFrameHurt)	# Contain each frame of the animation 
		self.attackAniFrames = self.extractAnimationFrames(indexAttack, numFramesAttack)	# Contain each frame of the animation 

		if (flipX or flipY):
			self.flipSprite(flipX, flipY)
		
		self.ID_Animation = ID_ANIMATION_IDLE		#Starts in Idle
		self.currentAnimation = self.idleAniFrames

		self.currentTick = pygame.time.get_ticks()
		self.lastTick = pygame.time.get_ticks()
		self.coolDownTick = cooldown
		self.currentFrame = 0
		self.cyclesAnimation = 0		# Cuenta cuantos ciclos ha hecho la animación

		## Sprite Position atributes
		self.posX = positionX
		self.posY = positionY
		
		

	def extractAnimationFrames(self, indexFrameSheet, numFrames):
		arrayFrames = []	
		for i in range(indexFrameSheet,indexFrameSheet+numFrames,1):
			arrayFrames.append( self.spriteSheet.get_image(i, self.spriteSheet.sizeX, self.spriteSheet.sizeY, self.spriteSheet.scale, BLACK) )

		return arrayFrames

	def manageTicks(self):
		
		self.currentTick = pygame.time.get_ticks()

		if self.currentTick - self.lastTick >= self.coolDownTick:
			self.lastTick = self.currentTick
			self.currentFrame += 1

			if self.currentFrame >= len(self.currentAnimation):
				self.currentFrame = 0
				self.cyclesAnimation += 1

		

	def setAnimation(self, ID_ani):

		self.ID_Animation = ID_ani
		self.cyclesAnimation = 0
		self.currentFrame = 0
		 		
		if   ( ID_ani == ID_ANIMATION_IDLE ):
			self.currentAnimation = self.idleAniFrames

		elif ( ID_ani == ID_ANIMATION_HURT ):
			self.currentAnimation = self.HurtAniFrames

		elif ( ID_ani == ID_ANIMATION_ATTACK ):
			self.currentAnimation = self.attackAniFrames

	def setCooldown(self, coolD):
		self.coolDownTick = coolD


	def flipSprite(self, flipX, flipY):
		for frame in range(0,len(self.idleAniFrames),1):
			self.idleAniFrames[frame] = pygame.transform.flip(self.idleAniFrames[frame], flipX, flipY)

		for frame in range(0,len(self.HurtAniFrames),1):
			self.HurtAniFrames[frame] = pygame.transform.flip(self.HurtAniFrames[frame], flipX, flipY)

		for frame in range(0,len(self.attackAniFrames),1):
			self.attackAniFrames[frame] = pygame.transform.flip(self.attackAniFrames[frame], flipX, flipY)
		

	def getCyclesAnimation(self):
		return self.cyclesAnimation


## RenderSprite an manage th ticks
def renderSprites(screen, diccSprites):
	
	screen.fill(BLACK)	
	for sprites in diccSprites.values():
		# Render
		sprites.manageTicks()
		screen.blit(sprites.currentAnimation[sprites.currentFrame], (sprites.posX, sprites.posY))


class Entity(AnimationSprites):

	def __init__(self, Name, pathSprite, sizeXSprite, sizeYSprite, scaleSprite, cooldown, flipX, flipY, positionX,positionY,
			     indexIdle, numFramesIdle,
				 indexHurt, numFrameHurt,
				 indexAttack, numFramesAttack):
		
		super().__init__(Name, pathSprite, sizeXSprite, sizeYSprite, scaleSprite, cooldown, flipX, flipY, positionX,positionY,indexIdle, numFramesIdle,indexHurt, numFrameHurt,indexAttack, numFramesAttack)

		# Aqui iran los atributos de las entidades

		




pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

BG = (50, 50, 50)
BLACK = (0, 0, 0)

screen.fill(BLACK)

# Extract Idle Animation

# To delay the animation
lastTick = pygame.time.get_ticks()
coolDownTick = 100
currentFrameIdle = 0



#Define Animation Sprites
mushroom = Entity('Mushroom','sprites/mushroom.png', 48,48,2,100, False, False, 200,200,     0,4,  9,3,  4,5)
dragonVerdeAni2 = Entity('DragonVerdeFlip','sprites/dinoGreen.png', 24,24,5,100, True, False, 500,200,     0,4,  14,3,  18,6)
arrowAni = AnimationSprites('Arrow','sprites/arrowA.png', 48,48,1.9,70, False, False, 0,0,     0,4,  0,4,  0,4)

spritesDicc = {"Mushroom" 			: mushroom,
 		   	   "DragonVerdeFlip" 	: dragonVerdeAni2,
			   "Arrow" 				: arrowAni,
			   }

diccSteps = []

run = True
state = STATE_IDLE
entity = ""
keyPressed = None

holdAnimation = 0
finishStateHold = 0

while run:

	##################################################################################################
	## Maquina de estados
	##################################################################################################
	if   ( state == STATE_IDLE ):

		for entities in spritesDicc:
			print(entities)
			spritesDicc[entities].setAnimation(ID_ANIMATION_IDLE)
							
		state = STATE_RENDER

		
	elif (state == STATE_ATTACK):

		if (holdAnimation != 1):
			holdAnimation = 1
			spritesDicc[entity].setAnimation(ID_ANIMATION_ATTACK)
			state = STATE_RENDER

		print("getCycles",spritesDicc[entity].getCyclesAnimation())
		if (holdAnimation == 1 and spritesDicc[entity].getCyclesAnimation() > ATTACK_CYCLE):
			holdAnimation = 0
			finishStateHold = 1

			state = STATE_RUN_LIST
		else:
			state = STATE_RENDER


	elif (state == STATE_RECIEVE_ATTACK):

		if (holdAnimation != 1):
			holdAnimation = 1
			spritesDicc[entity].setAnimation(ID_ANIMATION_HURT)
			state = STATE_RENDER

		print("getCycles",spritesDicc[entity].getCyclesAnimation())
		if (holdAnimation == 1 and spritesDicc[entity].getCyclesAnimation() > HURT_CYCLE):
			holdAnimation = 0
			finishStateHold = 1

			state = STATE_RUN_LIST
		else:
			state = STATE_RENDER
	
	elif (state == STATE_RENDER):

		renderSprites(screen, spritesDicc)
		state = STATE_RUN_LIST


	elif (state == STATE_RUN_LIST):
		
		if (len(diccSteps) > 0):
			state = diccSteps[0][0]
			entity = diccSteps[0][1]

			if (finishStateHold == 1):
				finishStateHold = 0
				diccSteps.pop(0)
				state = STATE_IDLE	
						
		else:
			state = STATE_RENDER	

		
	##################################################################################################

	#dummy_count += 1
	#print("dummy_count=",dummy_count)
	#if( dummy_count%10000 == 0):
	#	if ( status == STATUS_SORT_SPELLS_ANI ):
	#		status = STATUS_IDLE
	#	elif ( status == STATUS_IDLE ):
	#		status = STATUS_SORT_SPELLS_ANI
	

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN and holdAnimation == 0:
			keyPressed = pygame.key.get_pressed()
			print("A key has been pressed")
			
			if keyPressed[pygame.K_SPACE]: 	# Space bar as attack
				diccSteps = [
							 [STATE_ATTACK , "Mushroom"],
							 [STATE_RECIEVE_ATTACK , "DragonVerdeFlip"],
							 [STATE_ATTACK , "DragonVerdeFlip"],
							 [STATE_RECIEVE_ATTACK , "Mushroom"],							 
				  			]
				
				state = STATE_RUN_LIST

		
		
			



	pygame.display.update()

pygame.quit()