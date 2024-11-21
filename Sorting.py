import math

import pygame
import random
pygame.init()

class DrawInfo:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]

    FONT = pygame.font.SysFont('Comic Sans', 20)
    LARGE_FONT = pygame.font.SysFont('Comic Sans', 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self,width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sorting Visualization')
        self.set_list(list)

    def set_list(self,list):
        self.list = list
        self.max_value = max(list)
        self.min_value = min(list)
        self.block_width = round((self.width - self.SIDE_PAD) / len(list))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD // 2


def create_list(length, min_value, max_value):
    list = []
    for i in range(length):
        value = random.randint(min_value, max_value)
        list.append(value)
    return list

def draw(drawInfo, sortingAlgorithmName, ascending):
    drawInfo.window.fill(drawInfo.BACKGROUND_COLOR)

    title = drawInfo.LARGE_FONT.render(f"{sortingAlgorithmName} - {'Ascending' if ascending else 'Descending'}", 1, drawInfo.RED)
    drawInfo.window.blit(title, ((drawInfo.width / 2) - (title.get_width() / 2), 5))

    controls = drawInfo.FONT.render("R - RESET | SPACE - Start Sorting | A - Ascending | D - Descending", 1, drawInfo.BLACK)
    drawInfo.window.blit(controls, ((drawInfo.width/2) - (controls.get_width() / 2), 45))

    sorting = drawInfo.FONT.render("I - Insetion Sort | B - Bubble Sort | S - Selection Sort", 1, drawInfo.BLACK)
    drawInfo.window.blit(sorting, ((drawInfo.width / 2) - (sorting.get_width() / 2), 75))

    drawList(drawInfo)
    pygame.display.update()


def drawList(drawInfo, colorPositions = {}, clearBackground=False):
    list = drawInfo.list

    if clearBackground:
        clearRectangle = (drawInfo.SIDE_PAD/2, drawInfo.TOP_PAD, drawInfo.width - drawInfo.SIDE_PAD, drawInfo.height - drawInfo.TOP_PAD)
        pygame.draw.rect(drawInfo.window, drawInfo.BACKGROUND_COLOR, clearRectangle)

    for i, value in enumerate(list):
        x = drawInfo.start_x + i*drawInfo.block_width
        y = drawInfo.height - (value - drawInfo.min_value)*drawInfo.block_height
        color = drawInfo.GRADIENTS[i%3]

        if i in colorPositions:
            color = colorPositions[i]

        pygame.draw.rect(drawInfo.window, color, pygame.Rect(x, y, drawInfo.block_width, drawInfo.height))

    if clearBackground:
        pygame.display.update()



def bubbleSort(drawInfo, ascending = True):
    list = drawInfo.list

    for i in range(len(list)-1):
        for j in range(len(list)-1 - i):
            num1 = list[j]
            num2 = list[j+1]
            if num1 > num2 and ascending or (num1 < num2 and not ascending):
                list[j], list[j+1] = list[j+1], list[j]
                drawList(drawInfo, {j: drawInfo.GREEN, j+1: drawInfo.RED}, True)
                yield True #Doesn't matter what we yield, just need to pause the function
    return list

def insertionSort(drawInfo, ascending = True):
    list = drawInfo.list

    for i in range(1,len(list)):
        current = list[i]

        while True:
            ascending_sort = i > 0 and list[i - 1] > current and ascending
            descending_sort = i > 0 and list[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            list[i] = list[i-1]
            i = i-1
            list[i] = current
            drawList(drawInfo, {i - 1: drawInfo.GREEN, i: drawInfo.RED}, True)
            yield True

    return list


def selectionSort(drawInfo, ascending = True):
    list = drawInfo.list

    if ascending:
        for i in range(len(list) - 1):
            minValue = list[i]
            minValuePosition = i
            for j in range(i + 1, len(list)):
                if list[j] < minValue:
                    minValue = list[j]
                    minValuePosition = j
            list[minValuePosition], list[i] = list[i], list[minValuePosition]
            drawList(drawInfo, {i: drawInfo.GREEN, minValuePosition: drawInfo.RED}, True)
            yield True

    if not ascending:

        for i in range(len(list) - 1):
            maxValue = list[i]
            maxValuePosition = i
            for j in range(i + 1, len(list)):
                if list[j] > maxValue:
                    maxValue = list[j]
                    maxValuePosition = j
            list[maxValuePosition], list[i] = list[i], list[maxValuePosition]
            drawList(drawInfo, {i: drawInfo.GREEN, maxValuePosition: drawInfo.RED}, True)
            yield True
    return list




def main():
    run = True
    clock = pygame.time.Clock()
    sorting = False
    ascending = True
    sortingAlgorithm = bubbleSort
    sortingAlgorithmName = "Bubble Sort"
    sortingAlgorithmGenerator = None

    n = 50
    min_value = 0
    max_value = 100

    list = create_list(n, min_value, max_value)

    drawInfo = DrawInfo(800, 600, list)


    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                sorting = False
        else:
            draw(drawInfo, sortingAlgorithmName, ascending)


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                list = create_list(n,min_value,max_value)
                drawInfo.set_list(list)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sortingAlgorithmGenerator = sortingAlgorithm(drawInfo, ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
            elif event.key == pygame.K_b and sorting == False:
                sortingAlgorithm = bubbleSort
                sortingAlgorithmName = "Bubble Sort"
            elif event.key == pygame.K_i and sorting == False:
                sortingAlgorithm = insertionSort
                sortingAlgorithmName = "Insertion Sort"
            elif event.key == pygame.K_s and sorting == False:
                sortingAlgorithm = selectionSort
                sortingAlgorithmName = "Selection Sort"



    pygame.quit()



if __name__ == '__main__':
    main()

