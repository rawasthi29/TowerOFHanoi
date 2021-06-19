import pygame, sys, time

pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

game_done = False
framerate = 60

# game vars:
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0
g_mode = 0

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78,162,196) 
grey = (170, 170, 170)
green = (77, 206, 145)

##Auto
global frm
to = [[],"2"]
aux = [[],"1"]
moveText = ""

def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                    # font option is provided to save memory if font is
        font = pygame.font.SysFont(font_name, size)     # already loaded and needs to be reused many times
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def choosing_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:  # every screen/scene/level has its own loop
        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (323,122), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Towers of Hanoi', (320,120), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=blue)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 9:
                        n_disks = 9
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()
        clock.tick(60)

def menu_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done, g_mode
    menu_done = False
    while not menu_done:  # every screen/scene/level has its own loop
        screen.fill(white)
        blit_text(screen, 'Tower Of Hanoi', (323,122), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Tower Of Hanoi', (320,120), font_name='sans serif', size=90, color=gold)
        
        blit_text(screen, 'Press ', (225,205), font_name='sans serif', size=30, color=black)
        blit_text(screen, '1', (263,202), font_name='sans serif', size=35, color=blue)
        blit_text(screen, 'For auto-play', (343,205), font_name='sans serif', size=30, color=black)

        blit_text(screen, 'Press', (225,255), font_name='sans serif', size=30, color=black)
        blit_text(screen, '2', (263,252), font_name='sans serif', size=35, color=blue)
        blit_text(screen, 'For manual-play', (358,255), font_name='sans serif', size=30, color=black)


    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    g_mode = 1
                    choosing_screen = True
                    menu_done = True

                if event.key == pygame.K_2:
                    g_mode = 2
                    choosing_screen = True
                    menu_done = True
                    
                
        pygame.display.flip()
        clock.tick(60)

def game_over(): # game over screen
    global screen, steps
    screen.fill(white)
    min_steps = 2**n_disks-1
    blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'Your Steps: '+str(steps), (320, 360), font_name='mono', size=30, color=black)
    blit_text(screen, 'Minimum Steps: '+str(min_steps), (320, 390), font_name='mono', size=30, color=red)
    if min_steps==steps:
        blit_text(screen, 'You finished in minumum steps!', (320, 300), font_name='mono', size=26, color=green)
    pygame.display.flip()
    time.sleep(2)   # wait for 2 secs 
    pygame.quit()   #pygame exit
    sys.exit()  #console exit

def draw_towers():
    global screen
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160 , 20))
        pygame.draw.rect(screen, grey, pygame.Rect(xpos+75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)

def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    mod23 = 0
    if (n_disks <= 6):
        mod23 = 23 + (6-n_disks) * 10
        width = n_disks * mod23 
    else:
        mod23 = 23 - (n_disks - 6) * 3
        width = n_disks * mod23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks-i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= mod23


def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])
        blit_text(screen, str(disk['val']), disk['rect'].midtop, font_name='mono', size=14, color=black)
    return

def move_right():
    global pointing_at,floating,floater,disks,towers_midx

    pointing_at = (pointing_at+1)%3
    if floating:
        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
        disks[floater]['tower'] = pointing_at

def move_left():
    global pointing_at,floating,floater,disks,towers_midx

    pointing_at = (pointing_at-1)%3
    if floating:
        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
        disks[floater]['tower'] = pointing_at

def move_up():
    global pointing_at,floating,floater,disks,towers_midx
    
    for disk in disks[::-1]:
        if disk['tower'] == pointing_at:
            floating = True
            floater = disks.index(disk)
            disk['rect'].midtop = (towers_midx[pointing_at], 100)
            break

def move_down():
    global pointing_at,floating,floater,disks,towers_midx,steps
    
    for disk in disks[::-1]:
        if disk['tower'] == pointing_at and disks.index(disk)!=floater:
            if disk['val']>disks[floater]['val']:
                floating = False
                disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                steps += 1
            break
    else: 
        floating = False
        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
        steps += 1


def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)
    return

def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()

def reset():
    global steps,pointing_at,floating,floater,frm
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    # Auto Mode
    frm = [list(range(n_disks,0,-1)),"0"]
    to = [[],"2"]
    aux = [[],"1"]
    # Auto Mode
    
    menu_screen()
    #choosing_screen()
    make_disks()


def hanoiAuto(n,frmT,auxT,toT):
    global moveText

    if n==0:
        return
    hanoiAuto(n-1,frmT,toT,auxT)
    toT[0].append(frmT[0].pop())
    moveText = "Moving disk " + str(n) + " from tower " + frmT[1] + " to tower " + toT[1]
    movedisk(frmT,auxT,toT)
    hanoiAuto(n-1,auxT,frmT,toT)

def movedisk(frm,aux,to):
    if((int(frm[1]) - pointing_at) != 0 and not floating): adjustPtr(frm)
    move_up()
    refreshAutoMode()
    if ((abs(int(frm[1]) - int(to[1])))!= 0): move_left_right(frm,to)
    move_down()
    refreshAutoMode()

def adjustPtr(fromTower):
    if((int(fromTower[1]) - pointing_at) > 0 ):
        for i in range(int(fromTower[1]) - pointing_at):
            move_right()
    else:
        for i in range(abs(int(fromTower[1]) - pointing_at)):
            move_left()
    refreshAutoMode()

def move_left_right(fromTower,ToTower):
    for i in range(abs(int(fromTower[1]) - int(ToTower[1]))):
        if (fromTower[1] < ToTower[1] and floating):
            move_right()
        if (fromTower[1] > ToTower[1] and floating):
            move_left()
        refreshAutoMode()    

def autoplay():
    hanoiAuto(n_disks,frm,aux,to)

def refreshAutoMode():
    screen.fill(white)
    draw_towers()
    draw_disks()
    draw_ptr()
    time.sleep(0.4)
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    #blit_text(screen, moveText , (320-110, 20+35) , font_name='sans serif', size=25, color=black) #(towers_midx[0]+40, 403+50)
    pygame.display.flip()
    clock.tick(framerate)

menu_screen()
if(g_mode == 1):
    choosing_screen()
    make_disks()
    frm = [list(range(n_disks,0,-1)),"0"]
    autoplay()
if(g_mode == 2):
    choosing_screen()
    make_disks()

# main game loop:
while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_RIGHT and g_mode == 2:
                pointing_at = (pointing_at+1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT and g_mode == 2:
                pointing_at = (pointing_at-1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating and g_mode == 2:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            if event.key == pygame.K_DOWN and floating and g_mode == 2:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                        if disk['val']>disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                            steps += 1
                        break
                else: 
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1
            if event.key == pygame.K_SPACE and g_mode == 2:
                waiting = true
                
    screen.fill(white)
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    pygame.display.flip()
    if not floating:check_won()
    clock.tick(framerate)
pygame.quit()   #pygame exit
sys.exit()  #console exit
