import pygame
import serial
import threading
import time

# Arduino setup
arduino_port = '/dev/cu.usbmodem1101'  # Adjust this to your port
baud_rate = 9600

# Pygame setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player
player_width, player_height = 50, 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 10  # Pixels to move per frame

# Falling object
object_size = 20
object_x = width // 2
object_y = 0
object_speed = 5

# Game variables
score = 0
clock = pygame.time.Clock()

# Serial reading setup
reading = True
distance = 0
target_x = player_x

def read_sensor_data():
    global reading, distance, target_x
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Allow time for the connection to be established
    
    while reading:
        if ser.in_waiting > 0:
            try:
                raw_distance = float(ser.readline().decode('utf-8').strip())
                # Apply a simple moving average filter
                distance = 0.7 * distance + 0.3 * raw_distance
                # Calculate target position
                if 3 <= distance <= 20:
                    target_x = int((distance - 3) / 17 * (width - player_width))
                elif distance < 3:
                    target_x = 0
                elif distance > 20:
                    target_x = width - player_width
            except ValueError:
                pass  # Ignore any invalid data
        time.sleep(0.01)  # Reduced sleep time for more frequent updates
    
    ser.close()

# Start the sensor reading thread
sensor_thread = threading.Thread(target=read_sensor_data, daemon=True)
sensor_thread.start()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Smooth movement towards target position
    if abs(player_x - target_x) > player_speed:
        player_x += player_speed if target_x > player_x else -player_speed
    else:
        player_x = target_x

    # Move falling object
    object_y += object_speed
    if object_y > height:
        object_y = 0
        object_x = pygame.time.get_ticks() % (width - object_size)

    # Check for collision
    if (player_x < object_x + object_size and
        player_x + player_width > object_x and
        player_y < object_y + object_size and
        player_y + player_height > object_y):
        score += 1
        object_y = 0
        object_x = pygame.time.get_ticks() % (width - object_size)

    # Clear the screen
    screen.fill(BLACK)

    # Draw player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    # Draw falling object
    pygame.draw.rect(screen, RED, (object_x, object_y, object_size, object_size))

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
reading = False
pygame.quit()