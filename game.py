# Imports
if __name__ == '__main__':
    import random

# Snake classes
class snake_obj:
    def __init__(self, head):
        self.head = head

    @property
    def length(self):
        length = 0
        part = self.head
        while part:
            part = part.next
            length += 1
        return length

class snake_part:
    def __init__(self, pos, direction) -> None:
        self.pos = pos
        self.direction = direction
        self.previous = None
        self.next = None

def draw(snake, apple, GAME_SIZE, score):
    for y in range(GAME_SIZE, 0, -1):
        for x in range(0, GAME_SIZE):
            item = "-"
            if apple[0] == x and apple[1] == y:
                item = "@"
            # Check snake positions
            part = snake.head
            while part:
                if part.pos[0] == x and part.pos[1] == y:
                    item = "*"
                    break
                part = part.next

            print (item, end="")
        print ("")
    print (f"\n {score}")

#draw(snake, apple, GAME_SIZE, score)
class game:
    rewards = 0
    head = snake_part([random.randint(0, GAME_SIZE), random.randint(0, GAME_SIZE)], [0, 0])
    snake = snake_obj(head)
    apple = [random.randint(0, GAME_SIZE), random.randint(0, GAME_SIZE)]
    eaten = False

    def __init__(self, game_size=20):
        self.game_size = game_size

    def get_input(self, input):
        return input

    def move_snake(self, snake, direction):
        # Move to last part
        part = snake.head
        while part.next:
            part = part.next

        # Change directions of all the parts
        while part.previous:
            part.direction = part.previous.direction
            part = part.previous

        # Change direction of snake head
        snake.head.direction = direction

        # Change part positions
        part = snake.head
        while part:
            x, y = part.direction
            part.pos[0] += x
            part.pos[1] += y
            part = part.next

    def check_collisions(self, snake, game_size):
        """Returns whether the snake has hit the wall or itself"""
        head = snake.head
        # Wall collisions
        if head.pos[0] > game_size or head.pos[0] < 0 or head.pos[1] > game_size or head.pos[1] < 0:
            return True

        head_x, head_y = head.pos
        # Check for snake collisions
        part = head.next
        while part:
            x, y = part.pos
            if head_x == x and head_y == y and snake.length > 2:
                return True
            part = part.next

    def run_cycle(self, move):
        scored = False
        died = False
        if self.eaten:
            self.apple = [random.randint(0, GAME_SIZE), random.randint(0, GAME_SIZE)]
            self.eaten = False

        if move == "u":
            direction = [0, 1]
        elif move == "d":
            direction = [0, -1]
        elif move == "r":
            direction = [1, 0]
        else:
            direction = [-1, 0]

        self.move_snake(snake, direction)
        # Check if apple has been eaten
        if self.snake.head.pos[0] == self.apple[0] and self.snake.head.pos[1] == self.apple[1]:
            self.eaten = True
            scored = True
            # Get to last part of snake
            part = self.snake.head
            while part.next:
                part = part.next

            # Add new snake part
            part.next = snake_part([part.pos[0] - part.direction[0], part.pos[1] - part.direction[1]], [0, 0])
            part.next.previous = part

        end = self.check_collisions(snake, GAME_SIZE)

        # Return whether the game is over
        if end:
            return True
        return False
