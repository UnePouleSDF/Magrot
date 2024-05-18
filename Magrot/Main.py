import pygame, sys, math

import pygame.sprite

# Initialiser Pygame
pygame.init()

# Sprites
IDLE = pygame.image.load("Asset\MIdle.png")
RUN1 = pygame.image.load("Asset\MRun1.png")
RUN2 = pygame.image.load("Asset\MRun2.png")
JUMP = pygame.image.load("Asset\Msaut.png")
# Constantes
LARGEUR,HAUTEUR = 800,600
FPS = 60
VITESSE = 5
VITESSE_MAX = 15
GRAVITE = 1.5
SAUT_H = -25

# Couleurs
BG = (0,0,0)
TRAP = (200,200,200)
BARREL = (139,69,19)
TERRAIN = (0,255,0)
END = (255,0,0)


# Ecran
ecran = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Magrot")

# Tick
clock = pygame.time.Clock()

# Divers
lvl = 0

# Joueur
class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IDLE
        self.surf = pygame.Surface((40,50))
        self.rect = self.surf.get_rect(center=(700,HAUTEUR - 100))
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.dash = 1
        self.frame_count = 0  # Pour gérer l'alternance entre RUN1 et RUN2

    def update(self,platformes,barrils,trap):
        if self.vx > 1:
            if self.vx > VITESSE_MAX:
                self.vx = VITESSE_MAX
            self.vx -= 1
            self.frame_count += 1
            if self.frame_count >= 10:
                if self.frame_count // 10 % 2 == 0:
                    self.image = pygame.transform.flip(RUN2,True,False)
                else:
                    self.image = pygame.transform.flip(RUN1,True,False)
                if self.frame_count == 20:
                    self.frame_count = 0
        elif self.vx < -1:
            if self.vx < -VITESSE_MAX:
                self.vx = -VITESSE_MAX
            self.vx += 1
            self.frame_count += 1
            if self.frame_count >= 10:
                if self.frame_count // 10 % 2 == 0:
                    self.image = RUN2  
                else:
                    self.image = RUN1
                if self.frame_count == 20:
                    self.frame_count = 0  
        else:
            self.vx = 0
            self.image = IDLE
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx -= VITESSE
        if keys[pygame.K_RIGHT]:
            self.vx += VITESSE
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = SAUT_H
            
        # Gestion des sprites en fonction des mouvements
        if not -1 < self.vy < 1:
            if self.vx > 0:
                self.image = pygame.transform.flip(JUMP,True,False)
            else:
                self.image = JUMP

        self.surf.blit(self.image, (0, 0))  # Update the sprite image

        self.rect.x += self.vx
        self.collision(self.vx,0,platformes,end,barrils,trap)
        self.vy += GRAVITE
        self.rect.y += self.vy
        self.on_ground = False
        self.collision(0,self.vy,platformes,end,barrils,trap)
        

    def collision(self,vx,vy,plateformes,end,barrils,traps):
        global lvl
        for plateforme in plateformes:
            if pygame.sprite.collide_rect(self,plateforme):
                if vx > 0:
                    self.rect.right = plateforme.rect.left
                elif vx < 0:
                    self.rect.left = plateforme.rect.right
                if vy > 0:
                    self.rect.bottom = plateforme.rect.top
                    self.on_ground = True
                    self.dash = 1
                    self.vy = 0
                elif vy < 0:
                    self.rect.top = plateforme.rect.bottom
                    self.vy = 0

        for trap in traps:
            if pygame.sprite.collide_rect(self,trap):
                self.rect.x = 750
                self.rect.y = HAUTEUR-100
        
        for i in end:
            if pygame.sprite.collide_rect(self,i):
                for i in level[lvl]:
                    all_sprites.remove(i)
                    if type(i) == Platforme:
                        plateformes.remove(i)
                    elif type(i) == Pique:
                        traps.remove(i)
                    else:
                        end.remove(i)
                lvl += 1
                Dessiner(lvl)   

        for barril in barrils:
            if pygame.sprite.collide_rect(self, barril):
                if vx > 0:
                    self.rect.right = barril.rect.left
                    self.vx = 0  # Arrêter le joueur s'il heurte un barril
                elif vx < 0:
                    self.rect.left = barril.rect.right
                    self.vx = 0

# Pique
class Pique(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__()
        self.surf = pygame.Surface((width,height))
        self.surf.fill(TRAP)
        self.rect = self.surf.get_rect(center=(x,y))

# Barril
class Barril(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((30, 30))  # Taille du barril
        self.surf.fill(BARREL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.vx = 3  # Vitesse initiale du barril sur l'axe x

    def update(self):
        self.rect.x += self.vx

# Plateforme
class Platforme(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__()
        self.surf = pygame.Surface((width,height))
        self.surf.fill(TERRAIN)
        self.rect = self.surf.get_rect(center=(x,y))

# Fin
class End(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.surf = pygame.Surface((50,50))
        self.surf.fill(END)
        self.rect = self.surf.get_rect(center=(x,y))

# Groupes
all_sprites = pygame.sprite.Group()
platformes = pygame.sprite.Group()
barrils = pygame.sprite.Group()
end = pygame.sprite.Group()
traps = pygame.sprite.Group()

# Joueur
Joueur = Joueur()
all_sprites.add(Joueur)

# Plateformes
level = [
[
    Platforme(400,595,800,10),#sOL
    Platforme(815,300,10,1000),#Barrière droite
    Platforme(-15,300,10,1000),#Barrière gauche
    Platforme(400,590,20,200),
    Barril(50,550),
    Pique(450,570,20,200),
    End(50,565)
],
[
    Platforme(400,595,800,10),#Sol
    Platforme(-5,300,10,1000),#MurG
    Platforme(805,300,10,1000),#MurD
    Platforme(150,380,200,5),
    Platforme(650,450,200,5),
    Platforme(400,300,150,5),
    End(150,353)
],
[
    Platforme(400,595,800,10),#sOL
    Platforme(810,300,10,1000),#Barrière droite
    Platforme(-5,300,10,1000),#Barrière gauche
    Platforme(150,400,200,20),
    Platforme(400,450,200,20),
    Platforme(650,300,150,20),
    Platforme(400,200,150,20),
    Platforme(150,200,100,20),
    End(600,0)
],
[
    Platforme(400,595,800,10),#Sol
    Platforme(-5,300,10,1000),#MurG
    Platforme(815,300,10,1000),#MurD
    Platforme(150,550,50,5),
    Platforme(250,500,50,5),
    Platforme(350,450,50,5),
    Platforme(450,400,50,5),
    Platforme(550,350,50,5),
    Platforme(650,300,50,5),
    Platforme(750,250,25,5),
    Platforme(650,200,50,5),
    Platforme(550,150,50,5),
    Platforme(450,100,50,5),
    Platforme(250,50,250,5),
    End(600,0)
],
[
    Platforme(400,595,800,10),#sOL
    Platforme(815,300,10,1000),#Barrière droite
    Pique(200,585,550,10),
    Pique(0,300,10,800),
    Platforme(500,590,20,200),
    Platforme(400,590,20,300),
    Platforme(300,590,20,400),
    Platforme(200,590,20,500),
    Platforme(100,590,20,600),
    Platforme(15,590,20,700),
    Platforme(100,60,50,5),
    Platforme(200,60,50,5),
    Pique(300,70,70,10),
    End(300,45)
],
[
    Platforme(400,595,800,10),#sOL
    Platforme(815,300,10,1000),#Barrière droite
    Platforme(-15,300,10,1000),#Barrière gauche
]
]

def Dessiner(lvl):
    for i in level[lvl]: 
        if type(i) == Platforme :
            all_sprites.add(i)
            platformes.add(i)
        elif type(i) == Barril:
            all_sprites.add(i)
            barrils.add(i)
        elif type(i) == Pique:
            all_sprites.add(i)
            traps.add(i)
        else :
            all_sprites.add(i)
            end.add(i)
        

# Game loop
running = True
Dessiner(lvl)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    Joueur.update(platformes,barrils,traps)
    barrils.update()

    # Draw
    ecran.fill(BG)
    for entity in all_sprites:
        ecran.blit(entity.surf,entity.rect)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()