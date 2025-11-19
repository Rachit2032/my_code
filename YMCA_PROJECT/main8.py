import random
import sys
import pygame
from pygame.locals import *

FPS = 32
TIME_LIMIT_SECONDS = 300

SCREENWIDTH = 0
SCREENHEIGHT = 0
SCREEN = None
GROUNDY = 0
GAME_SPRITES = {}
GAME_SOUNDS = {}
PIPE_SPACING = 0

PLAYER = 'image/birddown.png'
BACKGROUND = 'image/bgw-bc34.png'
HIGHSCORE_FILE = "highscore.txt"


LEVEL_UNLOCK_SCORES = {1: 0, 2: 10, 3: 20, 4: 35, 5: 50}
LEVEL_SPEED = {1: -5, 2: -7, 3: -9, 4: -11, 5: -13}
LEVEL_GAP = {1: 280, 2: 260, 3: 240, 4: 220, 5: 200}
# LEVEL_GAP = {1: 250, 2: 220, 3: 200, 4: 180, 5: 160}

CURRENT_LEVEL = 1


def welcomeScreen():
    messagex = 0
    messagey = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
        
        SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandompipe(gap):
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3.5
    max_y2 = int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset)
    if max_y2 < 0:
        max_y2 = 0
    y2 = offset + random.randrange(0, max_y2 + 1)
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + gap
    return [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]


def update_level_by_score(score):
    global CURRENT_LEVEL
    unlocked = 1
    for lvl, req in sorted(LEVEL_UNLOCK_SCORES.items()):
        if score >= req:
            unlocked = lvl
    CURRENT_LEVEL = unlocked


def show_level_up(level):
    # short level-up flash
    text = FONT_LARGE.render(f"LEVEL {level}", True, (255, 215, 0))
    SCREEN.blit(text, (SCREENWIDTH // 2 - text.get_width() // 2, SCREENHEIGHT // 4))
    pygame.display.update()
    pygame.time.delay(600)


def mainGame(highscore):
    global CURRENT_LEVEL, PIPE_SPACING

    # reset level at start of each game
    CURRENT_LEVEL = 1

    score = 0
    playerx = int(SCREENWIDTH / 2)
    playery = int(SCREENHEIGHT / 2)
    basex = 0

    backgroundx = 0

    bg_width = GAME_SPRITES['background'].get_width()
    base_width = GAME_SPRITES['base'].get_width()

    start_time = pygame.time.get_ticks()

    gap = LEVEL_GAP[CURRENT_LEVEL]
    pipeVelx = LEVEL_SPEED[CURRENT_LEVEL]
    PIPE_SPACING = int(SCREENWIDTH / 3.5)  

    newPipe1 = getRandompipe(gap)
    newPipe2 = getRandompipe(gap)

    upperpipes = [
        {'x': SCREENWIDTH + 100, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 100 + int(gap), 'y': newPipe2[0]['y']},
    ]
    lowerpipes = [
        {'x': SCREENWIDTH + 100, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 100 + int(gap), 'y': newPipe2[1]['y']},
    ]

    playerVely = -9
    playerMaxVely = 10
    playerAccy = 1
    playerFlapAccv = -8
    playerFlapped = False

    previous_level = CURRENT_LEVEL

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000
        remaining_time = TIME_LIMIT_SECONDS - elapsed_time

        if remaining_time <= 0:
            GAME_SOUNDS['die'].play()
            if score > highscore:
                highscore = score
            gameOverScreen(score, elapsed_time, highscore)
            return highscore

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    # play wing sound if available
                    if 'wing' in GAME_SOUNDS:
                        GAME_SOUNDS['wing'].play()

        if isCollide(playerx, playery, upperpipes, lowerpipes):
            if score > highscore:
                highscore = score
            gameOverScreen(score, elapsed_time, highscore)
            return highscore

        
        update_level_by_score(score)
        # apply level settings
        gap = LEVEL_GAP[CURRENT_LEVEL]
        pipeVelx = LEVEL_SPEED[CURRENT_LEVEL]

        # if player reached new level, flash
        if previous_level != CURRENT_LEVEL:
            show_level_up(CURRENT_LEVEL)
            previous_level = CURRENT_LEVEL

        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + abs(pipeVelx):
                score += 1
                if 'point' in GAME_SOUNDS:
                    GAME_SOUNDS['point'].play()

        if playerVely < playerMaxVely and not playerFlapped:
            playerVely += playerAccy
        if playerFlapped:
            playerFlapped = False
        
        backgroundx = (backgroundx - 1) % -bg_width

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipeVelx
            lowerpipe['x'] += pipeVelx

        # spawn new pipe using gap as spacing between pipe pairs horizontally
        if upperpipes[-1]['x'] < SCREENWIDTH - int(gap):
            newpipe = getRandompipe(gap)
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # --- DRAWING ---
        SCREEN.blit(GAME_SPRITES['background'], (backgroundx, 0))
        SCREEN.blit(GAME_SPRITES['background'], (backgroundx + bg_width, 0))
        SCREEN.blit(GAME_SPRITES['background'], (backgroundx - bg_width, 0))

        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['base'], (basex + base_width, GROUNDY))
        
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        score_text = FONT_SMALL.render(f"Score: {score}", True, (0, 25, 0))
        SCREEN.blit(score_text, (10, 10))

        timer_text = FONT_SMALL.render(f"Time: {int(remaining_time)}s", True, (0, 25, 0))
        SCREEN.blit(timer_text, (10, 40))

        level_text = FONT_SMALL.render(f"Level: {CURRENT_LEVEL}", True, (0, 25, 0))
        SCREEN.blit(level_text, (10, 70))

        high_text = FONT_SMALL.render(f"Highscore: {highscore}", True, (0, 25, 0))
        SCREEN.blit(high_text, (SCREENWIDTH - 220, 10))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def gameOverScreen(score, elapsed_time, highscore):
    SCREEN.fill((0, 0, 0))

    title = FONT_LARGE.render("GAME OVER", True, (255, 50, 50))
    score_text = FONT_MEDIUM.render(f"Your Score: {score}", True, (255, 255, 255))
    time_text = FONT_MEDIUM.render(f"Time Survived: {int(elapsed_time)}s", True, (255, 255, 255))
    high_text = FONT_MEDIUM.render(f"Highscore: {highscore}", True, (255, 215, 0))
    restart_text = FONT_SMALL.render("Press R to Restart or Q to Quit", True, (200, 200, 200))

    SCREEN.blit(title, (SCREENWIDTH / 2 - title.get_width() / 2, SCREENHEIGHT / 3))
    SCREEN.blit(score_text, (SCREENWIDTH / 2 - score_text.get_width() / 2, SCREENHEIGHT / 2))
    SCREEN.blit(time_text, (SCREENWIDTH / 2 - time_text.get_width() / 2, SCREENHEIGHT / 2 + 40))
    SCREEN.blit(high_text, (SCREENWIDTH / 2 - high_text.get_width() / 2, SCREENHEIGHT / 2 + 80))
    SCREEN.blit(restart_text, (SCREENWIDTH / 2 - restart_text.get_width() / 2, SCREENHEIGHT / 2 + 150))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    return
                if event.key in (K_q, K_ESCAPE):
                    saveHighScore(highscore)
                    pygame.quit()
                    sys.exit()


def isCollide(playerx, playery, upperpipes, lowerpipes):
    playerRect = pygame.Rect(playerx, playery, GAME_SPRITES['player'].get_width(), GAME_SPRITES['player'].get_height())
    if playery > GROUNDY - 25 or playery < 0:
        if 'hit' in GAME_SOUNDS:
            GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes + lowerpipes:
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], GAME_SPRITES['pipe'][0].get_width(), GAME_SPRITES['pipe'][0].get_height())
        if playerRect.colliderect(pipeRect):
            if 'hit' in GAME_SOUNDS:
                GAME_SOUNDS['hit'].play()
            return True
    return False


def loadHighScore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0


def saveHighScore(highscore):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(highscore))


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')

    info = pygame.display.Info()
    SCREENWIDTH = info.current_w
    SCREENHEIGHT = info.current_h
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.NOFRAME)

    GROUNDY = SCREENHEIGHT * 0.75

    pygame.font.init()
    FONT_SMALL = pygame.font.SysFont('Arial', 25)
    FONT_MEDIUM = pygame.font.SysFont('Arial', 35)
    FONT_LARGE = pygame.font.SysFont('Arial', 60)

    highscore = loadHighScore()

    GAME_SPRITES['message'] = pygame.transform.scale(pygame.image.load('image/message4.png').convert_alpha(), (SCREENWIDTH, SCREENHEIGHT))

    GAME_SPRITES['base'] = pygame.transform.scale(pygame.image.load('image/ground.png').convert_alpha(), (SCREENWIDTH, SCREENHEIGHT//4))
    
    GAME_SPRITES['pipe'] = (
        pygame.transform.scale(pygame.image.load('image/pipedown.png').convert_alpha(), (65, 800)),
        pygame.transform.scale(pygame.image.load('image/pipeup.png').convert_alpha(), (65, 800))
    )
    
    GAME_SPRITES['background'] = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (SCREENWIDTH, SCREENHEIGHT))
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    GAME_SOUNDS['hit'] = pygame.mixer.Sound('sounds/assets_audio_hit.ogg')
    GAME_SOUNDS['die'] = pygame.mixer.Sound('sounds/assets_audio_die.ogg')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('sounds/assets_audio_point.ogg')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('sounds/assets_audio_swoosh.ogg')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('sounds/assets_audio_wing.ogg')

    while True:
        welcomeScreen()
        highscore = mainGame(highscore)
        saveHighScore(highscore)