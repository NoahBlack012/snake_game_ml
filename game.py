# Imports
import random
import numpy as np

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

#draw(snake, apple, game_size, score)
class game:
    def __init__(self, game_size=20):
        self.game_size = game_size
        self.rewards = 0
        head = snake_part([random.randint(0, self.game_size), random.randint(0, self.game_size)], [0, 0])
        self.snake = snake_obj(head)
        self.apple = [random.randint(0, self.game_size), random.randint(0, self.game_size)]
        self.eaten = False

    def draw(self, score=0):
        for y in range(self.game_size, -1, -1):
            for x in range(0, self.game_size+1):
                item = "-"
                if self.apple[0] == x and self.apple[1] == y:
                    item = "@"
                # Check snake positions
                part = self.snake.head
                while part:
                    if part.pos[0] == x and part.pos[1] == y:
                        item = "*"
                        break
                    part = part.next

                print (item, end="")
            print ("")
        print (f"\n {score}")

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
        if head.pos[0] >= game_size or head.pos[0] < 0 or head.pos[1] >= game_size or head.pos[1] < 0:
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
        eaten = False 
        
        # Get inital distance to apple
        x1 = self.snake.head.pos[0]
        y1 = self.snake.head.pos[1]
        distance_to_apple1 = np.sqrt((self.apple[0] - x1)**2 + (self.apple[1] - y1)**2)
        if self.eaten:
            self.apple = [random.randint(0, self.game_size), random.randint(0, self.game_size)]
            self.eaten = False

        if move == "u":
            direction = [0, 1]
        elif move == "d":
            direction = [0, -1]
        elif move == "r":
            direction = [1, 0]
        else:
            direction = [-1, 0]

        self.move_snake(self.snake, direction)
        # Check if apple has been eaten
        if self.snake.head.pos[0] == self.apple[0] and self.snake.head.pos[1] == self.apple[1]:
            self.eaten = True
            eaten = True
            # Get to last part of snake
            part = self.snake.head
            while part.next:
                part = part.next

            # Add new snake part
            part.next = snake_part([part.pos[0] - part.direction[0], part.pos[1] - part.direction[1]], [0, 0])
            part.next.previous = part

        end = self.check_collisions(self.snake, self.game_size)
        
        # Get final distance to apple
        x2 = self.snake.head.pos[0]
        y2 = self.snake.head.pos[1]
        distance_to_apple2 = np.sqrt((self.apple[0] - x2)**2 + (self.apple[1] - y2)**2)
        
        # Calculate reward
        if eaten:
            reward = 0.7
        elif end:
            reward = -0.5
        else:
            if distance_to_apple2 < distance_to_apple1:
                reward = 0.1
            else:
                reward = -0.1

        # Return rewards, game state, and if the game is over
        return reward, self, end 
        
print ('done')

if __name__ == '__main__':
    a = game()
    while True:
        a.draw()
        move = input()
        end = a.run_cycle(move)
        print (end)