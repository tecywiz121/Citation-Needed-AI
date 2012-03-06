from copy import deepcopy
import random

def max_worse(self, other):
    '''
    Returns True if self is worse than other for a maximizing player
    '''
    if not self:
        return True
    return self.value < other.value or (self.value == other.value and self.max_depth > other.max_depth)


def min_worse(self, other):
    '''
    Returns True if self is worse than other for a minimizing player
    '''
    if not self:
        return True
    return self.value > other.value or (self.value == other.value and self.max_depth > other.max_depth)

class Minimax(object):
    '''
    Generic implementation of the minimax algorithm
    '''
    def itermoves(self):
        '''
        Returns an iterator of all possible moves for the current game state
        '''
        pass

    def is_won(self):
        '''
        Returns True if the current game state has been won
        '''
        pass

    def is_max(self):
        '''
        Returns True if the turn at the current game state should maximize.
        Maximizing players are usually the AI controlled ones
        '''
        pass

    def evaluate(self):
        '''
        Sets self.value to the value of the current game state
        '''
        self.value = 0
        return self

    def worse_func(self):
        '''
        Returns the correct worse function depending on if this game state is
        for a maximizing or a minimizing player
        '''
        return max_worse if self.is_max() else min_worse

    def longer(self, other):
        '''
        Returns True if the self has a greater maximum depth than other
        '''
        return not other or self.max_depth >= other.max_depth

    def shorter(self, other):
        '''
        Returns True if self has a shorter maximum depth than other
        '''
        return not other or self.max_depth < other.max_depth

    def minimax(self, depth=0):
        '''
        Runs the minimax algorithm on the current game state
        '''
        if self.is_won() or depth > 3:
            self.max_depth = depth
            return self.evaluate()
        else:
            depth += 1
            #print 'Depth:', depth, '\n'

        moves = self.itermoves()
        worse_than = self.worse_func()
        bestBoard = None
        longestBoard = None
        shortestBoard = None

        for move in moves:
            #print depth, 'Possible move:', move.action, move.value if hasattr(move, 'value') else '-'
            board = move.minimax(depth)
            if worse_than(bestBoard, board):
                bestBoard = move
            #else:
            #    print depth, 'Not replacing', 'None' if not bestBoard else str(bestBoard.action) + str(bestBoard.value), 'with', board.action, board.value
            if board.longer(longestBoard):
                longestBoard = move

        if not bestBoard:
            bestBoard = longestBoard
        self.value = bestBoard.value
        self.max_depth = longestBoard.max_depth
        #print depth, 'Best:', bestBoard.action, bestBoard.value
        return bestBoard

class Zombie:
    '''
    Represents a zombie player on the simulated game board.  Also is the base
    class for Humans
    '''
    HUMAN = 0
    ZOMBIE = 1
    TYPE = ZOMBIE

    HEALTH = 5.0
    RANGED = 0
    MELEE = 0.50
    BULLETS = 0

    def __init__(self, x, y):
        '''
        Creates an instance of a Zombie at position (x, y)
        '''
        self.type = self.TYPE
        self.ranged_attack = self.RANGED
        self.melee_attack = self.MELEE
        self.health = self.HEALTH
        self.bullets = self.BULLETS
        self.x = x
        self.y = y

class Human(Zombie):
    '''
    Represents a human player on the simulated game board.
    '''
    TYPE = Zombie.HUMAN
    HEALTH = 2.0
    RANGED = 0.5
    BULLETS = 30

# Offsets for valid Zombie/Player moves
MOVES = (
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
)

# Offsets for all adjacent squares
ADJACENT = MOVES + (
    (-1, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
)

class Field:
    '''
    Stores the state of the map including passability, opacity, and search status
    '''
    def __init__(self, width, height):
        '''
        Creates a new instance of Field with the given width and height
        '''
        self.width = width
        self.height = height

        # Stored in (y, x) aka (row, col)
        self.searched = {}
        self.unpassable = {}
        self.unseeable = {}

    def clone(self):
        '''
        Returns a copy of self.  Keeps the same references for immutable fields
        like the map, and creates new copies for mutable fields like searched
        '''
        new = self.__class__(self.width, self.height)

        # Searched can be modified, so copy it
        new.searched = dict(self.searched)

        # These cannot be changed, so only copy the reference
        new.unpassable = self.unpassable
        new.unseeable = self.unseeable
        return new

    def passable(self, x, y):
        '''
        Returns True if the square at (x, y) is passable
        '''
        return (y, x) not in self.unpassable

    def searchable(self, x, y):
        '''
        Returns True if the square at (x, y) is searchable
        '''
        return (y, x) not in self.searched

    def search(self, x, y):
        '''
        Marks a square at (x, y) as having been searched
        '''
        self.searched[(y, x)] = True

    def transparent(self, x, y):
        '''
        Returns True if the square at (x, y) is see-through
        '''
        return (y, x) not in self.unseeable

    def can_see(self, source, target):
        '''
        Returns True if the square source has line of sight to the square at
        target.
        '''
        dx = target.x - source.x
        dy = target.y - source.y

        maxSteps = float(max(abs(dx), abs(dy)))
        if maxSteps > 0:
            dy /= maxSteps
            dx /= maxSteps

        x = source.x
        y = source.y

        while (int(x) <> target.x and int(y) <> target.y):
            iX = int(x)
            iY = int(y)
            print (iX, iY), (target.x, target.y)

            if iX<0 or iX >= self.width or iY < 0 or iY > self.height:
                raise Exception('out of bounds')

            if (iX, iY) in self.unseeable:
                return False
            x+=dx
            y+=dy

        return True


    def ascii(self):
        '''
        Produces a pretty ascii string representation of the field
        '''
        output = []
        for y in range(0, self.height):
            line = []
            for x in range(0, self.width):
                passable = self.passable(x, y)
                transparent = self.transparent(x, y)
                searched = not self.searchable(x, y)

                if passable and transparent and searched:
                    v = ','
                elif passable and transparent:
                    v = '.'
                elif passable and not transparent and searched:
                    v = '+'
                elif passable and not transparent:
                    v = '*'
                elif not passable and transparent:
                    v = 'x'
                elif not passable and not transparent:
                    v = 'X'
                line.append(v)
            output.append(line)
        return output

    def __str__(self):
        return '\n'.join([' '.join(line) for line in self.ascii()])

class AmmoError(Exception):
    '''
    Thrown if a shoot command is given when a Human has no ammo
    '''
    pass

class ZombieBoard(Minimax):
    '''
    Implements the logic specific to the Zombie game
    '''
    def __init__(self, field):
        self.zombies = []
        self.humans = []
        self.entities = {}
        self.field = field.clone()
        self.n_turn = 0

    def add_zombie(self, x, y, health=Zombie.HEALTH, melee=Zombie.MELEE):
        '''
        Add a Zombie to the board at (x, y) with the given health and melee
        attack chance
        '''
        if not self.bounds(x, y):
            raise Exception('Invalid position')
        zombie = Zombie(x, y)
        zombie.health = health
        zombie.melee_attack = melee
        self.zombies.append(zombie)
        self.entities[(x, y)] = zombie

    def add_human(self, x, y, health=Human.HEALTH, bullets=Human.BULLETS, melee=Human.MELEE, ranged=Human.RANGED, id=0):
        '''
        Adds a human to the board at (x, y) with the given health, bullets, and
        given melee and ranged attack chance.  id is an optional argument to
        link the human to a human in the CS Games server.
        '''
        if not self.bounds(x, y):
            raise Exception('Invalid position')
        human = Human(x, y)
        human.health = health
        human.bullets = bullets
        human.melee_attack = melee
        human.ranged_attack = ranged
        human.id = 0
        self.humans.append(human)
        self.entities[(x, y)] = human

    def clone(self):
        '''
        Create a copy of the current game state
        '''
        new = self.__class__(self.field)
        new.zombies = deepcopy(self.zombies)
        new.humans = deepcopy(self.humans)
        new.entities = dict(((e.x, e.y), e) for e in new.zombies + new.humans)
        new.n_turn = self.n_turn
        return new

    def turn(self):
        '''
        Create a copy of the current game state and advance the turn counter
        '''
        new = self.clone()
        new.n_turn += 1
        if new.n_turn > len(new.humans)*2:
            new.n_turn = 0
        return new

    def human(self):
        '''
        If this game state represents a max turn, return the current human
        '''
        return self.humans[self.n_turn/2]

    def is_max(self):
        '''
        Returns True if the turn at the current state belongs to the AI
        '''
        return self.n_turn < len(self.humans)*2

    def is_won(self):
        '''
        Returns True if the game is over
        '''
        return len(self.zombies) <= 0 or len(self.humans) <= 0

    def evaluate(self):
        '''
        Calculate the value of the current game state
        '''
        if len(self.zombies) == 0:
            self.value = float('inf')
            return self
        elif len(self.humans) == 0:
            self.value = float('-inf')
            return self

        # Calculate the totals of some possible metrics
        bullets = sum(map(lambda x: x.bullets, self.humans))
        health = sum(map(lambda x: x.health, self.humans))
        ranged = sum(map(lambda x: x.ranged_attack, self.humans))
        melee = sum(map(lambda x: x.melee_attack, self.humans))
        zHealth = sum(map(lambda x: x.health, self.zombies))

        # Calculate a score depending on the number of adjacent edges
        edge = 0
        for h in self.humans:
            for x,y in MOVES:
                tX = x + h.x
                tY = y + h.y

                if not self.bounds(tX, tY) or not self.passable(tX, tY):
                    edge += 1


        self.value = health - 0.1*zHealth - 0.5*edge

        return self

    def bounds(self, x, y):
        '''
        Return True if (x, y) is a valid game tile
        '''
        return x >= 0 and x < self.field.width and y >= 0 and y < self.field.height

    def passable(self, x, y):
        '''
        Return True if the square at (x, y) is passable
        '''
        return self.field.passable(x, y) and (x, y) not in self.entities

    def search(self, x, y):
        '''
        Simulate searching a square by adding the expected value of each
        possible outcome to the related field of the Human doing the search

        Chances of various effects:

        20% bullets (5-10)
        20% food    (+1 hp)
        10% medical (+2 hp)
        5%  armor   (+5 hp)
        5%  ranged  (0.01 - 0.09 %ranged)
        5%  melee   (0.01 - 0.09 %melee)

        Expected Values:

        bullets = 0.2 * 7 = 1.4
        health  = (0.2 * 1) + (0.1 * 2) + (0.05 * 5) = 0.65
        ranged  = 0.05 * 0.05 = 0.0025
        melee   = 0.05 * 0.05 = 0.0025
        '''

        if not self.field.searchable(x, y):
            raise Exception('square already searched')

        human = self.entities[(x, y)]
        human.bullets += 1.4
        human.health += 0.65
        human.ranged_attack += 0.0025
        human.melee_attack += 0.0025
        self.field.search(human.x, human.y)

        self.action = ('search', x, y)


    def melee(self, aX, aY, dX, dY):
        '''
        Simulate an attack from (aX, aY) to (dX, dY).  The amount of damage done
        is the expected value from a melee attack, which is the chance to hit
        times the damage to deal.
        '''
        # TODO: Ensure valid melee attacks

        attacker = self.entities[(aX, aY)]
        defender = self.entities[(dX, dY)]
        defender.health -= attacker.melee_attack
        self.clear_bodies()

        self.action = ('melee', aX, aY, dX, dY)

    def shoot(self, aX, aY, dX, dY):
        '''
        Simulate a ranged attack from (aX, aY) to (dX, dY).
        '''
        # TODO: Ensure valid ranged attacks
        attacker = self.entities[(aX, aY)]
        defender = self.entities[(dX, dY)]

        if attacker.bullets <= 0:
            raise AmmoError()

        defender.health -= attacker.ranged_attack
        attacker.bullets -= 1
        self.clear_bodies()

        self.action = ('shoot', aX, aY, dX, dY)

    def clear_bodies(self):
        '''
        Remove all dead entities from the various lists used to track them.
        '''
        self.zombies = filter(lambda x: x.health > 0, self.zombies)
        self.humans = filter(lambda x: x.health > 0, self.humans)
        self.entities = dict(((e.x, e.y), e) for e in self.zombies + self.humans)

    def move(self, srcX, srcY, x, y):
        '''
        Move an entity from (srcX, srcY) to (x, y)
        '''
        dX = abs(srcX - x)
        dY = abs(srcY - y)

        if dX > 1 or dY > 1:
            raise Exception('Invalid move ' + str((srcX, srcY, x, y)))
        elif dX > 0 and dY > 0:
            raise Exception('Invalid move ' + str((srcX, srcY, x, y)))

        entity = self.entities[(srcX, srcY)]
        try:
            del self.entities[(entity.x, entity.y)]
        except KeyError:
            print (entity.x, entity.y), self.entities.keys()
            exit()
        self.entities[(x, y)] = entity
        entity.x = x
        entity.y = y

        self.action = ('move', srcX, srcY, x, y)

    def move_zombie(self, zombie):
        '''
        Simulate a zombie move according to the rules of the competition
        '''
        if zombie.health <= 0:
            return

        # Find all alive humans within sqrt(range2) spaces
        range2 = 5**2
        humans = filter(lambda x: x.health >= 0, self.humans)
        random.shuffle(humans)

        closestHuman = None
        shortestDistance2 = self.field.width**2 + self.field.height**2
        for h in humans:
            if self.field.can_see(zombie, h): # TODO: add adjacency test (Zombies can melee an adjacent human regardless of LOS)
                dx = zombie.x - h.x
                dy = zombie.y - h.y
                if dx**2 + dy**2 < shortestDistance2:
                    closestHuman = h
                    shortestDistance2 = dx**2 + dy**2

        # Chase the closest human
        move = None
        if closestHuman and shortestDistance2 < range2:
            zX = zombie.x
            zY = zombie.y
            dx = zombie.x - closestHuman.x
            dy = zombie.y - closestHuman.y
            if abs(dx) <= 1 and abs(dy) <= 1:
                self.melee(zombie.x, zombie.y, closestHuman.x, closestHuman.y)
            else:
                mX = (-dx)
                mY = (-dy)

                nY = 1 if mY > 0 else -1 if mY < 0 else 0
                nX = 1 if mX > 0 else -1 if mX < 0 else 0

                possibles = [(abs(mX), (nX+zX, zY)),
                                (abs(mY), (zX, nY+zY))]
                possibles = filter(lambda (s, (x, y)): self.bounds(x, y) and self.passable(x, y), possibles)

                if abs(mX) == abs(mY):
                    try:
                        move = random.choice(possibles)[1] # TODO: Return all possible moves, and not a random one
                    except IndexError:
                        pass
                elif len(possibles):
                    possibles.sort(lambda x, y: cmp(x[0], y[0]))
                    move = possibles[-1][1]
        else:
            # Move in a random direction
            choices = list(MOVES)
            random.shuffle(choices)
            while len(choices):
                option = choices.pop()
                mX = zombie.x + option[0]
                mY = zombie.y + option[1]
                if self.bounds(mX, mY) and self.passable(mX, mY):
                    move = (mX, mY)
                    break
        if move:
            if any(isinstance(x, tuple) for x in move):
                raise Exception(move)
            self.move(zombie.x, zombie.y, move[0], move[1])

    def itermoves(self):
        '''
        Generates all possible moves for a single human or all zombies
        '''
        if self.is_max():
            myHuman = self.human()
            hX = myHuman.x
            hY = myHuman.y

            # For whatever reason, this particular ordering of search, shoot,
            # melee, and move performs the best.  The ordering probably should
            # not matter, so this hints at a bug somewhere.

            # Do search
            if self.field.searchable(hX, hY):
                new = self.turn()
                #print 'original',(hX, hY), self.entities.keys(), [(h.x, h.y) for h in self.humans]
                new.search(hX, hY)
                yield new

            # Do Shooting
            for zombie in self.zombies:
                if myHuman.bullets >= 0 and self.field.can_see(myHuman, zombie):
                    new = self.turn()
                    try:
                        new.shoot(hX, hY, zombie.x, zombie.y)
                        yield new
                    except AmmoError:
                        pass

            # Do Melee
            for dX, dY in ADJACENT:
                x = hX + dX
                y = hY + dY
                try:
                    target = self.entities[(x, y)]
                    if target.type == Zombie.ZOMBIE:
                        new = self.turn()
                        new.melee(hX, hY, target.x, target.y)
                        yield new
                except KeyError:
                    pass

            # Do moves
            for dX, dY in MOVES:
                x = hX + dX
                y = hY + dY
                if self.bounds(x, y) and self.passable(x, y):
                    new = self.turn()
                    new.move(hX, hY, x, y)
                    yield new

            # Return the no-op possibility last
            nomove = self.turn()
            nomove.action = ('wait',)
            yield nomove
        else:
            # Calculate the zombie moves
            z = self.turn()
            for zombie in z.zombies:
                z.move_zombie(zombie)
            z.action = ('zombie',)
            yield z

    def __str__(self):
        '''
        Make a nice pretty string version of the game board
        '''
        ascii = self.field.ascii()
        for human in self.humans:
            ascii[human.y][human.x] = 'H'

        for zombie in self.zombies:
            ascii[zombie.y][zombie.x] = 'Z'

        return '\n'.join([' '.join(line) for line in ascii])

if __name__ == '__main__':
    # If we're running this file directly, put on a show!
    from time import sleep
    field = Field(10, 10)
    board = ZombieBoard(field)
    board.add_human(0, 1)
    board.add_human(0, 4)
    board.add_zombie(9, 6)
    board.add_zombie(9, 7)
    board.add_zombie(9, 8)
    board.add_zombie(9, 9)
    board.add_zombie(9, 0)
    board.add_zombie(9, 1)
    board.add_zombie(9, 2)
    board.add_zombie(9, 3)
    while not board.is_won():
        move = board.minimax()
        print board
        print
        print move
        print move.action
        print move.value
        sleep(0.05)
        board = move
