'''
This file needs to be merged with min_max.py
'''

ADJACENT = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
#   (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)

def evaluate(self):
    '''
    -(40 - (Distance to zombie * 5)) + 20*(Count of X) + 30*(Count of *) + 10*(Count of +) + (Health) - (Total Zombie Health) + 5(if searched)
    '''
    zombies = self.get_zombies()
    if self.is_max():
        human = self.human
        square = human.getSquare()
        row = square.GetRow()
        col = square.GetColumn()

        totalValue = 0

        # Stick to safe squares
        for dRow, dCol in ADJACENT:
            tRow = dRow + row
            tCol = dCol + col
            tSquare = self.getSquare(tCol, tRow)

            value = 0
            if not tSquare.isPassible():
                value += 2

            if not tSquare.blocksLOS():
                value += 1

            totalValue += value

            # Avoid adjacent zombies
            for zombie in zombies:
                zSquare = zombie.getSquare()
                zRow = zSquare.getRow()
                zCol = zSquare.getColumn()

                if zRow == tRow and zCol == tCol:
                    # TODO: Add non-adjacent zombies
                    totalValue -= 40

    else:
        totalValue = float('-inf')


    return totalValue
