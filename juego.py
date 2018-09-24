import pygame
import random
Ancho=1000
Alto=600
verde=[0,255,0]
blanco=[255,255,255]
azul=[0,0,255]
negro=[0,0,0]
imagen=[150,150]
poso=[450,50]
salud=100
cont=0

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([50,50])
        self.image.fill(verde)
        self.rect=self.image.get_rect()
        self.vel_y=0
        self.vel_x=0

    def update(self):
        self.rect.y+=self.vel_y
        self.rect.x+=self.vel_x


class Rival(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([30,30])
        self.image.fill(blanco)
        self.rect=self.image.get_rect()
        self.vel_x=-4
        self.tmp=random.randrange(550)

    def update(self):
        if self.rect.x > Ancho - self.rect.width:
            self.vel_x=-4
        self.rect.x+=self.vel_x
        self.tmp-=1


class Bala(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([10,5])
        self.image.fill(azul)
        self.rect=self.image.get_rect()
        self.vel_x=9

    def update(self):
        self.rect.x+=self.vel_x


if __name__ == '__main__':
    pygame.init()
    pantalla=pygame.display.set_mode([Ancho,Alto])
    jugadores=pygame.sprite.Group()
    j1=Jugador()
    j1.rect.x=100
    j1.rect.y=100
    jugadores.add(j1)

    n=10
    rivales=pygame.sprite.Group()
    for i in range(n):
        r=Rival()
        r.rect.x=random.randrange(Ancho,Ancho+400)
        r.rect.y=random.randrange(50,(Alto-r.rect.width))
        rivales.add(r)

    balas=pygame.sprite.Group()
    balas_rivales=pygame.sprite.Group()


    reloj=pygame.time.Clock()
    fin=False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_DOWN:
                    j1.vel_y=2
                if event.key==pygame.K_UP:
                    j1.vel_y=-2
                if event.key==pygame.K_RIGHT:
                    j1.vel_x=2
                if event.key==pygame.K_LEFT:
                    j1.vel_x=-2
                if event.key==pygame.K_SPACE:
                    b=Bala()
                    b.rect.x=j1.rect.x+j1.rect.width
                    b.rect.y=j1.rect.y+(j1.rect.width)/2
                    balas.add(b)

            if event.type==pygame.KEYUP:
                j1.vel_y=0
                j1.vel_x=0

        for b in balas:
            col_b=pygame.sprite.spritecollide(b,rivales,True)
            for r in col_b:
                balas.remove(b)
            for b in col_b:
                cont+=1
            if cont==50:
                fin=True
            if b.rect.x>(Ancho+50):
                balas.remove(b)

        for r in rivales:
            if r.rect.x<-10:
                r.rect.x=random.randrange(Ancho,Ancho+500)
            if r.tmp <0:
                b=Bala()
                b.rect.x=r.rect.x+j1.rect.width
                b.rect.y=r.rect.y
                b.vel_x=-7
                balas_rivales.add(b)
                r.tmp=random.randrange(550)

        for b in balas_rivales:
            col_j1=pygame.sprite.spritecollide(b,jugadores,True)
            for r in col_j1:
                balas_rivales.remove(b)
            for b in col_j1:
                salud-=5
            if salud==0:
                fin=True


            jugadores.add(j1)
            if b < -10:
                balas_rivales.remove(b)

        if len(rivales)<n:
            nr=n-len(rivales)
            for i in range(n):
                r=Rival()
                r.rect.x=random.randrange(Ancho,Ancho+400)
                r.rect.y=random.randrange(50,(Alto-r.rect.width))
                rivales.add(r)
        fuente = pygame.font.Font(None, 20)
        text = "SALUD : "
        vida = str(salud)
        text1 ="ENEMIGOS : "
        enemigo= str(cont)
        mensaje = fuente.render(text, 1, (255, 255, 255))
        pantalla.blit(mensaje, [15, 15])
        mensaje3 = fuente.render(text1, 1, (255, 255, 255))
        pantalla.blit(mensaje3, [200, 15])
        mensaje2 = fuente.render(vida, 1, (255, 255, 255))
        pantalla.blit(mensaje2, [20, 15])
        mensaje4 = fuente.render(enemigo, 1, (255, 255, 255))
        pantalla.blit(mensaje4, [300, 15])


        jugadores.update()
        rivales.update()
        balas.update()
        balas_rivales.update()
        pantalla.fill(negro)
        jugadores.draw(pantalla)
        rivales.draw(pantalla)
        balas.draw(pantalla)
        balas_rivales.draw(pantalla)
        pantalla.blit(mensaje, [15, 15])
        pantalla.blit(mensaje2, [80, 15])
        pantalla.blit(mensaje3, [200, 15])
        pantalla.blit(mensaje4, [300, 15])
        pygame.display.flip()
        reloj.tick(60)

    if salud==0:
        print "Game Over"
    if cont==50:
        print "Winner"
