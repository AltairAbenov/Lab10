import pygame
import random
import psycopg2

conn = psycopg2.connect(
    dbname="snake_game",
    user="postgres",
    password="A2682772aa",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def create_user(username):
    cur.execute("INSERT INTO \"user\" (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT INTO user_score (user_id, score, level, snake_length) VALUES (%s, %s, %s, %s)", (user_id, 0, 1, 3))
    conn.commit()
    print(f"User {username} created with ID {user_id}.")
    return user_id


def get_user(username):
    cur.execute("SELECT id FROM \"user\" WHERE username = %s", (username,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None

def load_user_data(user_id):
    cur.execute("SELECT score, level, snake_length FROM user_score WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    if result:
        return result[0], result[1], result[2]
    else:
        return 0, 1, 3

def save_game(user_id, score, level, snake_length):
    cur.execute("UPDATE user_score SET score = %s, level = %s, snake_length = %s WHERE user_id = %s", (score, level, snake_length, user_id))
    conn.commit()

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

score = 0
level = 1
snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = (10, 0)
food = (200, 200)

def display_info(score, level):
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

def update_level(score, level):
    level = score // 50 + 1
    return level

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
    return True

def check_collisions(snake):
    if snake[0] in snake[1:]:
        return True
    if not (0 <= snake[0][0] < 600 and 0 <= snake[0][1] < 400):
        return True
    return False

def game_loop(user_id, score, level, snake_length):
    global snake, snake_dir, food

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if not pause_game():
                        return
                elif event.key == pygame.K_UP:
                    snake_dir = (0, -10)
                elif event.key == pygame.K_DOWN:
                    snake_dir = (0, 10)
                elif event.key == pygame.K_LEFT:
                    snake_dir = (-10, 0)
                elif event.key == pygame.K_RIGHT:
                    snake_dir = (10, 0)

        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake = [new_head] + snake[:-1]

        if check_collisions(snake):
            print("Game Over!")
            break

        if snake[0] == food:
            score += 10
            level = update_level(score, level)
            snake_length += 1
            snake.append(snake[-1])
            food = (random.randint(0, 59) * 10, random.randint(0, 39) * 10)

        display_info(score, level)

        for segment in snake:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0], food[1], 10, 10))

        pygame.display.flip()

        clock.tick(10 + level * 2)

        save_game(user_id, score, level, snake_length)


def main():
    username = input("Enter your username: ")
    user_id = get_user(username)

    if user_id is None:
        user_id = create_user(username)
        print(f"New user {username} created.")
        score, level, snake_length = 0, 1, 3
    else:
        score, level, snake_length = load_user_data(user_id)
        print(f"Welcome back {username}. Your current level is {level}, score is {score}, and snake length is {snake_length}.")

    game_loop(user_id, score, level, snake_length)


if __name__ == "__main__":
    main()
