#俄罗斯方块最终版本

from threading import currentThread
import pygame
import time
import sys
import random

from pygame.constants import KEYDOWN, KEYUP, QUIT

#绘制窗口变色函数
def tetrisChangeColor(r, g, b, changeR, changeG, changeB):
    if changeR == True:
        stepR = 0.2
    else:
        stepR = -0.2

    if changeG == True:
        stepG = 0.4
    else:
        stepG = -0.4

    if changeB == True:
        stepB = 0.8
    else:
        stepB = -0.8
    

    r += stepR
    g += stepG
    b += stepB

    if r > 200:
        changeR = False
    elif r < 100:
        changeR = True

    if g > 200:
        changeG = False
    elif g < 100:
        changeG = True

    if b > 200:
        changeB = False
    elif b < 100:
        changeB = True
    
    screen.fill((r, g, b))
    
    return r, g, b, changeR, changeG, changeB

#绘制框框，加载图片，打印字体
def tetrisFace():
    pygame.draw.rect(screen, (255,255,255), ((25,25),(500, 1000)), 1)   #游戏框
    pygame.draw.rect(screen, (255,255,255), ((550,25),(282,175)),1)     #分数框
    pygame.draw.rect(screen, (255,255,255), ((550,225),(282,275)),1)    #下一方块儿框
    pygame.draw.rect(screen, (255,255,255), ((550,525),(282,500)),1)    #图片框
    #添加图片
    screen.blit(picture, (550, 525))
    #打印字体
    text1 = font1.render("the score: ", True, (255,255,255))
    text2 = font1.render("the next:", True, (255,255,255))
    screen.blit(text1, (560, 35))
    screen.blit(text2, (560, 235))


#游戏框内的块儿打印
# 0 <= i <= 10; 0 <= j <= 20
def tetrisShowGamePots(i, j):
    pygame.draw.rect(screen, (0,0,0),(((26 + i * 50), (26 + j * 50)),(50, 50)),0)       #实心黑
    pygame.draw.rect(screen, (255,255,255),(((25 + i * 50), (25 + j * 50)),(50, 50)),1) #边框白

#下一方块提示的打印
# 0 <= i <= 4; 0 <= j <= 4
def tetrisShowNext(i,j):
    pygame.draw.rect(screen, (0,0,0),(((592 + i * 50), (281 + j * 50)),(50, 50)),0)       #实心黑
    pygame.draw.rect(screen, (255,255,255),(((591 + i * 50), (280 + j * 50)),(50, 50)),1) #边框白

#分数打印
def tetrisScore(i):
    score = font2.render(str(i), True, (255,255,255))
    screen.blit(score, (600, 100))

#方块位置集合的函数
def thisTetrisItem(nextItem, poseOfItem):
    #第一个方块：田
    if nextItem == 1:
        #方块的位置集合,田只有一种姿态
        positionOfIterm = {(4,0),(5,0),(4,1),(5,1)}

    #第二个方块：长条
    elif nextItem == 2:
        #不同的形状之横着
        if poseOfItem == 1 or poseOfItem == 2:
            positionOfIterm = {(3,0),(4,0),(5,0),(6,0)}
        #竖着
        else:
            positionOfIterm = {(4,0),(4,1),(4,2),(4,3)}

    #第三个方块：只有一折那个
    elif nextItem == 3:
        if poseOfItem == 1:
            positionOfIterm = {(4,0),(5,0),(5,1),(5,2)}

        elif poseOfItem == 2:
            positionOfIterm = {(3,1),(4,1),(5,1),(5,0)}

        elif poseOfItem == 3:
            positionOfIterm = {(4,0),(4,1),(4,2),(5,2)}

        else:
            positionOfIterm = {(3,0),(4,0),(5,0),(5,1)}

    #第四个方块：与三对称
    elif nextItem == 4:
        if poseOfItem == 1:
            positionOfIterm = {(4,0),(4,1),(4,2),(5,0)}

        elif poseOfItem == 2:
            positionOfIterm = {(4,0),(4,1),(5,1),(6,1)}

        elif poseOfItem == 3:
            positionOfIterm = {(4,2),(5,2),(5,1),(5,0)}

        else:
            positionOfIterm = {(3,1),(3,0),(4,0),(5,0)}

    #第五个方块：两折那个
    elif nextItem == 5:
        if poseOfItem == 1 or poseOfItem == 2:
            positionOfIterm = {(4,0),(4,1),(5,1),(5,2)}

        else:
            positionOfIterm = {(3,1),(4,1),(4,0),(5,0)}


    #第六个方块：和5对称那个
    elif nextItem == 6:
        if poseOfItem == 1 or poseOfItem == 2:
            positionOfIterm = {(5,0),(5,1),(4,1),(4,2)}

        else:
            positionOfIterm = {(4,0),(5,0),(5,1),(6,1)}

    #第七个方块：土那个
    else:
        if poseOfItem == 1:
            positionOfIterm = {(4,1),(5,1),(5,0),(6,1)}

        elif poseOfItem == 2:
            positionOfIterm = {(4,1),(5,0),(5,1),(5,2)}

        elif poseOfItem == 3:
            positionOfIterm = {(4,0),(5,0),(5,1),(6,0)}

        else:
            positionOfIterm = {(4,0),(4,1),(4,2),(5,1)}
    return positionOfIterm

#下一个方块位置提示的函数
def nextTetrisItem(nextItem, poseOfItem):
    #第一个方块：田
    if nextItem == 1:
        #方块的位置集合,田只有一种姿态
        positionOfIterm = {(1,1),(2,1),(1,2),(2,2)}

    #第二个方块：长条
    elif nextItem == 2:
        #不同的形状之横着
        if poseOfItem == 1 or poseOfItem == 2:
            positionOfIterm = {(0,1),(1,1),(2,1),(3,1)}
        #竖着
        else:
            positionOfIterm = {(1,0),(1,1),(1,2),(1,3)}

    #第三个方块：只有一折那个
    elif nextItem == 3:
        if poseOfItem == 1:
            positionOfIterm = {(1,0),(2,0),(2,1),(2,2)}

        elif poseOfItem == 2:
            positionOfIterm = {(0,1),(1,1),(2,1),(2,0)}

        elif poseOfItem == 3:
            positionOfIterm = {(1,0),(1,1),(1,2),(2,2)}

        else:
            positionOfIterm = {(0,0),(1,0),(2,0),(2,1)}

    #第四个方块：与三对称
    elif nextItem == 4:
        if poseOfItem == 1:
            positionOfIterm = {(1,0),(1,1),(1,2),(2,0)}

        elif poseOfItem == 2:
            positionOfIterm = {(0,0),(0,1),(1,1),(2,1)}

        elif poseOfItem == 3:
            positionOfIterm = {(1,2),(2,2),(2,1),(2,0)}

        else:
            positionOfIterm = {(0,1),(0,0),(1,0),(2,0)}

    #第五个方块：两折那个
    elif nextItem == 5:
        if poseOfItem == 1 or poseOfItem == 2:
            positionOfIterm = {(1,0),(1,1),(2,1),(2,2)}

        else:
            positionOfIterm = {(0,1),(1,1),(1,0),(2,0)}


    #第六个方块：和5对称那个
    elif nextItem == 6:
        if poseOfItem == 1 or poseOfItem == 2:
            positionOfIterm = {(2,0),(2,1),(1,1),(1,2)}

        else:
            positionOfIterm = {(0,0),(1,0),(1,1),(2,1)}

    #第七个方块：土那个
    else:
        if poseOfItem == 1:
            positionOfIterm = {(0,1),(1,1),(1,0),(2,1)}

        elif poseOfItem == 2:
            positionOfIterm = {(1,1),(2,0),(2,1),(2,2)}

        elif poseOfItem == 3:
            positionOfIterm = {(0,0),(1,0),(1,1),(2,0)}

        else:
            positionOfIterm = {(1,0),(1,1),(1,2),(2,1)}
    return positionOfIterm

#方块下落
def tetrisChangeFalling(fallingCubes, landingCubes):
    tempCubes = set()
    for each in fallingCubes:
        temp = (each[0], (each[1] + 1))
        if temp in landingCubes or (each[1]+1) == 20:
            return False, fallingCubes
        else:
            tempCubes.add(temp)
    return True, tempCubes

#左移动下落方块
def tetrisGotoLeft(fallingCubes, landingCubes):
    tempCubes = set()
    for each in fallingCubes:
        temp = ((each[0] - 1), each[1])
        if temp in landingCubes or temp[0] < 0:
            return fallingCubes
        else:
            tempCubes.add(temp)
    return tempCubes

#右移动下落方块
def tetrisGotoRight(fallingCubes, landingCubes):
    tempCubes = set()
    for each in fallingCubes:
        temp = ((each[0] + 1), each[1])
        if temp in landingCubes or temp[0] > 9:
            return fallingCubes
        else:
            tempCubes.add(temp)
    return tempCubes
    
#landing方块判断减行、加分。
def tetrisLandingCubesJudge(landingCubes):
    scoreCount = 0

    #判断消行
    for i in range(0,20):   #range左闭右开
        originLand = landingCubes.copy()
        count = True
        for j in range(0,10):
            if (j,i) not in originLand:
                count = False
        #消行
        if count == True:
            scoreCount += 1
            #删掉满的一行
            tempCubes = landingCubes.copy()
            for each in tempCubes:
                if each[1] == i:
                    landingCubes.remove(each)
            #上面的归整
            for line in range(i-1, -1, -1):
                for lineEach in range(0,10):
                    if (lineEach, line) in landingCubes:
                        landingCubes.remove((lineEach, line))
                        landingCubes.add((lineEach, (line + 1)))

    #判断分数并直接返回值
    if scoreCount == 0:
        return landingCubes, 0
    elif scoreCount == 1:
        return landingCubes, 100
    elif scoreCount == 2:
        return landingCubes, 300
    elif scoreCount == 3:
        return landingCubes, 600
    elif scoreCount == 4:
        return landingCubes, 1000

#方块儿变形
#这个变形真的是废了一点劲，因为设计问题，导致只能通过下落的四个点左边来转换
#不过，聪明如我，虽然废了点周折，还是实现了
def tetrisChangePos(fallingCubes, landingCubes):
    #找到中心点，小数都视为0.5,且，一个是整数，另一个也必须是整数
    centerLine = 0
    centerColumn = 0
    columnFlag = False
    lineFlag = False
    for each in fallingCubes:
        centerColumn += each[0]
        centerLine += each[1]

    centerColumn /= 4
    tempColumn = int(centerColumn)
    if tempColumn != centerColumn:
        centerColumn = tempColumn + 0.5
        columnFlag = True

    centerLine /= 4
    tempLine = int(centerLine)
    if tempLine != centerLine:
        centerLine = tempLine + 0.5
        lineFlag = True

    #这样可以让方块变形时不会左右移动
    if columnFlag == False or lineFlag == False:
        if tempColumn != centerColumn:
            centerColumn = centerColumn + 0.5
        if tempLine != centerLine:
            centerLine = centerLine - 0.5

    tempCube = set()

    #顺时针变动falling物品
    for each in fallingCubes:
        posiA = each[0] - centerColumn
        posiB = each[1] - centerLine

        tempPosi = ((centerColumn - posiB), (centerLine + posiA))
        tempCube.add(tempPosi)

    #但是这样会导致一些方块（杠、两折、土）变形时会整体上升，需要纠正一下
    #超过center右边，就下降一格
    isDown = False
    if tempColumn == centerColumn or tempLine == centerLine: #排除点一折和田
        for each in tempCube:
            if each[0] > centerColumn:
                isDown = True
    if isDown == True:
        isDown, tempCube = tetrisChangeFalling(tempCube, landingCubes)

    #判断是否超过10*20的游戏框或是否被landingCubes阻挡
    temp = set()
    direction = 0   #负数表示右移一位，正数表示左移一位
    outOfUp = 0
    for each in tempCube.copy():
        if each in landingCubes or each[1] > 19:
            return fallingCubes
        #变形左边后超出两格(测试中发现竖杠在最左边变形会有这个问题)
        if each[0] == -2:
            direction = -2
        #变形左边后超出一格
        if each[0] == -1 and direction != -2:
            direction = -1
        #变形后右边超出一格
        if each[0] > 9:
            direction = 1
        #变形后顶上超出（刚生成方块儿会有这个问题）
        if each[1] == -1:
            outOfUp = 1
        if each[1] == -2:
            outOfUp = 2
    #阻挡后对应左右移动
    if direction == -2:
        tempCube = tetrisGotoRight(tempCube, landingCubes)
        tempCube = tetrisGotoRight(tempCube, landingCubes)
    elif direction == -1:
        tempCube = tetrisGotoRight(tempCube, landingCubes)
    elif direction == 1:
        tempCube = tetrisGotoLeft(tempCube, landingCubes)
    if outOfUp == 1:
        outOfUp,tempCube = tetrisChangeFalling(tempCube, landingCubes)
    if outOfUp == 2:
        outOfUp,tempCube = tetrisChangeFalling(tempCube, landingCubes)
        outOfUp,tempCube = tetrisChangeFalling(tempCube, landingCubes)
    return tempCube

#game over
def tetrisGameOver():
    print("Your score is: " + str(scoreOfGame))
    text3 = font3.render("game over!", True, (0,0,0),(255,255,255))
    text4 = font3.render("score:"+ str(scoreOfGame), True, (0,0,0),(255,255,255))
    screen.blit(text3, (200, 400))
    screen.blit(text4, (200, 500))

################ 程序开始地方 ################
#初始化
pygame.init()
#建一个窗口
screen = pygame.display.set_mode((857, 1050), 0, 0)
#设置窗口标题
pygame.display.set_caption("Tetris-俄罗斯方块")
#加入图片对象
picture = pygame.image.load("pic.png").convert()
#字体
font1 = pygame.font.SysFont('arial', 28)
font2 = pygame.font.SysFont('arial', 48)
font3 = pygame.font.SysFont('arial', 72)

#设置一直不停按下键的移动
pygame.key.set_repeat(200, 50)   #单位ms,第一个参数:按键的灵敏度，第二个参数:按键的移动时间间隔。

#用来颜色渐变的
r = 50
g = 50
b = 50
colorChangeR = True
colorChangeG = True
colorChangeB = True

#已经落地的块儿的位置的集合
collectionOfLanding = set()
#正在落地的块儿的集合
collectionOfFalling = set()
#下一方块儿的预告集合
collectionOfNext = set()
#游戏的分数
scoreOfGame = 0

#此时的方块（元祖）第一个元素是哪个方块，第二个元素是方块的形态
cubeNow = ()
#下一个方块
cubeNext = (random.randint(1,7),random.randint(1,4))    #randint左闭右闭

#下落方块左移标志位
letfFlag = False
#下落方块右移标志位
rightFlag = False

#主循环判断的时间依据
loop = 0
loopTime = 15
#下一个方块儿的变化标志位
isChangeToNext = True


#主循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                collectionOfFalling = tetrisGotoLeft(collectionOfFalling, collectionOfLanding)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                collectionOfFalling = tetrisGotoRight(collectionOfFalling, collectionOfLanding)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                collectionOfFalling = tetrisChangePos(collectionOfFalling, collectionOfLanding)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                loopTime = 1
        if event.type == KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                loopTime = 15


    ####逻辑相关####
    #每一段时间执行一次
    loop += 1
    if loop >= loopTime:
        loop = 0

        #替换方块儿
        if isChangeToNext == True:
            cubeNow = cubeNext
            cubeNext = (random.randint(1,7),random.randint(1,4))
            isChangeToNext = False
            #下一个方块的集合显示
            collectionOfNext.clear()
            for each in nextTetrisItem(cubeNext[0], cubeNext[1]):
                collectionOfNext.add(each)
            #正在下落方块的集合显示
            collectionOfFalling.clear()
            for each in thisTetrisItem(cubeNow[0], cubeNow[1]):
                #游戏结束的判断
                if each in collectionOfLanding:
                    #把重复的那个块儿也打印出来
                    for positionOfFalling in thisTetrisItem(cubeNow[0], cubeNow[1]):
                        tetrisShowGamePots(positionOfFalling[0], positionOfFalling[1])
                    tetrisGameOver()
                    pygame.display.update()
                    time.sleep(3)
                    sys.exit()
                else:
                    collectionOfFalling.add(each)
        #方块下落
        else:
            isFallingSucce, collectionOfFalling = tetrisChangeFalling(collectionOfFalling, collectionOfLanding)
            #走到头了
            if isFallingSucce == False:
                isChangeToNext = True
                for each in collectionOfFalling:
                    collectionOfLanding.add(each)
                collectionOfFalling.clear()
                collectionOfLanding, tempScore = tetrisLandingCubesJudge(collectionOfLanding)
                scoreOfGame += tempScore


    ####图形相关####
    #颜色刷新时间
    time.sleep(0.02)
    #置颜色
    r, g, b, colorChangeR, colorChangeG, colorChangeB = tetrisChangeColor(r, g, b, colorChangeR, colorChangeG, colorChangeB)
    #绘制界面
    tetrisFace()
    #打印分数
    tetrisScore(scoreOfGame)
    #打印下一方块儿
    for positionNext in collectionOfNext:
        tetrisShowNext(positionNext[0], positionNext[1])
    #打印已经下落的块儿和正在下落的块儿的集合
    for positionOfFalling in collectionOfFalling:
        tetrisShowGamePots(positionOfFalling[0], positionOfFalling[1])
    for positionOfLanding in collectionOfLanding:
        tetrisShowGamePots(positionOfLanding[0], positionOfLanding[1])
    #刷新
    pygame.display.update()