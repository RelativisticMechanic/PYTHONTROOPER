import pygame

GlobalWindow = 0
GlobalScreen = 0
GlobalClock = 0
GlobalWidth = 0
GlobalHeight = 0
GlobalFont = 0 
InputArray = [False, False, False, False, False, False, False, False, False, False, False, False, False]
exitfunc = 0

BTN_UP = 0
BTN_DOWN = 1
BTN_RIGHT = 2
BTN_LEFT = 3
BTN_SPACE = 4
BTN_Z = 5
BTN_X = 6
BTN_C = 7
BTN_RETURN = 8
BTN_SHIFT = 9
BTN_CTRL = 10
BTN_MOUSE1 = 11
BTN_MOUSE2 = 12

class Image:
    image_data = 0
    w = 0 
    h = 0

    def __init__(self, file, w=0, h=0, image_data=0):
        if(not image_data):
            self.image_data = pygame.image.load(file)
            self.w = self.image_data.get_width()
            self.h = self.image_data.get_height()
        else:
            self.w = w
            self.h = h
            self.image_data = image_data
    
    def GetImageHeight(self):
        return self.h
    
    def GetImageWidth(self):
        return self.w

def Run(w, h, window_w, window_h, init, update, draw, onkeypress, onkeypressed, onkeyrelease, onmousemove, onexit, font='Arial', font_size=16):
    global GlobalScreen, GlobalWidth, GlobalHeight, GlobalClock, GlobalFont, GlobalWindow, exitfunc
    exitfunc = onexit
    pygame.init()
    GlobalFont = pygame.font.SysFont(font, font_size)
    if(w != window_w and h != window_h):
        GlobalScreen = pygame.Surface([w, h])
        GlobalWindow = pygame.display.set_mode([window_w, window_h])
    else:
        GlobalScreen = pygame.display.set_mode([window_w, window_h])
    GlobalWidth = w
    GlobalHeight = h
    GlobalClock = pygame.time.Clock()
    old_ticks = pygame.time.get_ticks()
    elapsed = 0
    mouse_x, mouse_y = pygame.mouse.get_pos()
    running = True
    init()
    while running:
        new_ticks = pygame.time.get_ticks()
        elapsed = pygame.time.get_ticks() - old_ticks
        old_ticks = new_ticks

        update(elapsed)
        draw(elapsed)

        if(GlobalWindow):
            GlobalWindow.blit(pygame.transform.scale(GlobalScreen, (window_w, window_h)), [0,0,window_w, window_h])

        pygame.display.flip()

        # Get inputs
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                onexit(elapsed)
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:        onkeypress(elapsed, BTN_UP); InputArray[BTN_UP] = True
                if event.key == pygame.K_DOWN:      onkeypress(elapsed, BTN_DOWN); InputArray[BTN_DOWN] = True
                if event.key == pygame.K_LEFT:      onkeypress(elapsed, BTN_LEFT); InputArray[BTN_LEFT] = True
                if event.key == pygame.K_RIGHT:     onkeypress(elapsed, BTN_RIGHT); InputArray[BTN_RIGHT] = True
                if event.key == pygame.K_z:         onkeypress(elapsed, BTN_Z); InputArray[BTN_Z] = True
                if event.key == pygame.K_x:         onkeypress(elapsed, BTN_X); InputArray[BTN_X] = True
                if event.key == pygame.K_c:         onkeypress(elapsed, BTN_C); InputArray[BTN_C] = True
                if event.key == pygame.K_SPACE:     onkeypress(elapsed, BTN_SPACE); InputArray[BTN_SPACE] = True
                if event.key == pygame.K_RETURN:    onkeypress(elapsed, BTN_RETURN); InputArray[BTN_RETURN] = True
                if event.key == pygame.K_LSHIFT:    onkeypress(elapsed, BTN_SHIFT); InputArray[BTN_SHIFT] = True
                if event.key == pygame.K_LCTRL:     onkeypress(elapsed, BTN_CTRL); InputArray[BTN_CTRL] = True
               
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_UP:        onkeyrelease(elapsed, BTN_UP); InputArray[BTN_UP] = False
                if event.key == pygame.K_DOWN:      onkeyrelease(elapsed, BTN_DOWN); InputArray[BTN_DOWN] = False
                if event.key == pygame.K_LEFT:      onkeyrelease(elapsed, BTN_LEFT); InputArray[BTN_LEFT] = False
                if event.key == pygame.K_RIGHT:     onkeyrelease(elapsed, BTN_RIGHT); InputArray[BTN_RIGHT] = False
                if event.key == pygame.K_z:         onkeyrelease(elapsed, BTN_Z); InputArray[BTN_Z] = False
                if event.key == pygame.K_x:         onkeyrelease(elapsed, BTN_X); InputArray[BTN_X] = False
                if event.key == pygame.K_c:         onkeyrelease(elapsed, BTN_C); InputArray[BTN_C] = False
                if event.key == pygame.K_SPACE:     onkeyrelease(elapsed, BTN_SPACE); InputArray[BTN_SPACE] = False
                if event.key == pygame.K_RETURN:    onkeyrelease(elapsed, BTN_RETURN); InputArray[BTN_RETURN] = False
                if event.key == pygame.K_LSHIFT:    onkeyrelease(elapsed, BTN_SHIFT); InputArray[BTN_SHIFT] = False
                if event.key == pygame.K_LCTRL:     onkeyrelease(elapsed, BTN_CTRL); InputArray[BTN_CTRL] = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:   onkeypress(elapsed, BTN_MOUSE1); InputArray[BTN_MOUSE1] = True
                if event.button == pygame.BUTTON_RIGHT:  onkeypress(elapsed, BTN_MOUSE2); InputArray[BTN_MOUSE2] = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:   onkeyrelease(elapsed, BTN_MOUSE1); InputArray[BTN_MOUSE1] = False
                if event.button == pygame.BUTTON_RIGHT:  onkeyrelease(elapsed, BTN_MOUSE2); InputArray[BTN_MOUSE2] = False
            
        for idx, i in enumerate(InputArray):
            if i == True:
                onkeypressed(elapsed, idx)
        
        new_mouse_x, new_mouse_y = pygame.mouse.get_pos()
        if new_mouse_x != mouse_x or new_mouse_y != mouse_y:
            mouse_x = new_mouse_x
            mouse_y = new_mouse_y
            onmousemove(elapsed, new_mouse_x, new_mouse_y)


def IsPressed(key):
    return InputArray[key]

def SetCaption(caption):
    pygame.display.set_caption(caption)

def GetHeight():
    return GlobalHeight

def GetWidth():
    return GlobalWidth

def Clear(r, g, b):
    global GlobalScreen
    GlobalScreen.fill((r, g, b))

def PutPixel(x, y, r, g, b):
    GlobalScreen.set_at((x, y), pygame.Color((int(r), int(g), int(b))))

def DrawCircle(x, y, radius, r, g, b, filled = False, linewidth = 1):
    if(filled):
        pygame.draw.circle(GlobalScreen, pygame.Color(int(r), int(g), int(b)), (x,y), radius, 0)
    else:
        pygame.draw.circle(GlobalScreen, pygame.Color(int(r), int(g), int(b)), (x,y), radius, linewidth)

def DrawTriangle(x1, y1, x2, y2, x3, y3, r, g, b, filled = False, linewidth = 1):
    if(filled):
        pygame.draw.polygon(GlobalScreen, pygame.Color(int(r), int(g), int(b)), [(x1,y1), (x2, y2), (x3, y3)], 0)
    else:
        pygame.draw.polygon(GlobalScreen, pygame.Color(int(r), int(g), int(b)), [(x1,y1), (x2, y2), (x3, y3)], linewidth)

def DrawBlock(x, y, w, h, r, g, b, filled = False, linewidth = 1):
    if(filled):
        pygame.draw.rect(GlobalScreen, pygame.Color(int(r), int(g), int(b)), pygame.Rect(x, y, w, h), 0)
    else:
        pygame.draw.rect(GlobalScreen, pygame.Color(int(r), int(g), int(b)), pygame.Rect(x, y, w, h), linewidth)

def LoadImage(file):
    return Image(file)

def GetHeightImage(img):
    return img.h

def GetWidthImage(img):
    return img.w

def DuplicateImage(img):
    new_image_data = img.image_data.copy()
    return Image("", img.w, img.h, new_image_data)

def DrawImage(img, x, y, pivotx=0, pivoty=0, angle=0):
    if(not angle):
        GlobalScreen.blit(img.image_data, (x,y))

def CropImage(img, x, y, w, h):
    new_img = DuplicateImage(img)
    cropped_image = pygame.Surface((w,h))
    cropped_image.blit(new_img.image_data, (x,y), (x,y,w,h))
    new_img.image_data = cropped_image
    new_img.w = w 
    new_img.h = h
    return new_img

def MakeTransparentImage(img, r,g,b):
    new_img = DuplicateImage(img)
    new_img.image_data.set_colorkey(pygame.Color(int(r), int(g), int(b)))
    new_img.image_data.convert_alpha()
    return new_img

def ResizeImage(img, w, h):
    new_img = DuplicateImage(img)
    new_img.w = w
    new_img.h = h
    new_img.image_data = pygame.transform.scale(img.image_data, (w,h))
    return new_img

def FlipImage(img, horizontal=False, vertical=False):
    new_img = DuplicateImage(img)
    new_img.image_data = pygame.transform.flip(new_img.image_data, horizontal, vertical)
    return new_img

def DrawString(str, x, y, r,g,b):
    textsurface = GlobalFont.render(str, False, (int(r), int(g), int(b)))
    GlobalScreen.blit(textsurface, (x,y))

def DrawLine(x1, y1, x2, y2, r, g, b, width=1):
    pygame.draw.line(GlobalScreen, pygame.Color(int(r),int(g),int(b)), (x1, y1), (x2, y2), width)

def FrameCap(frames):
    GlobalClock.tick(frames)

def LoadSound(filename):
    return pygame.mixer.Sound(filename)

def PlaySound(snd):
    snd.play()

def Quit():
    exitfunc(0)
    pygame.quit()
    exit()
