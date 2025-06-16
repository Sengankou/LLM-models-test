import time
import os

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_car(x):
    """Draws the pixel art car at a given x position."""
    car_art = [
        "   _______   ",
        "  / ______ \\  ",
        " /  ______  \\ ",
        "| |      | | |",
        "| |______| | |",
        "| |______| | |",
        "| |______| | |",
        " \\ \\______ / ",
        "  \\________/  ",
    ]

    # Calculate the width of the car art lines
    car_width = len(car_art[0])

    # Ensure the car doesn't go off the screen horizontally
    screen_width = 80 # Assuming a terminal width of 80 characters for simplicity
    if x < 0:
        output_x = 0  # Padding to the left
        
    elif x + car_width > screen_width:
        output_x = screen_width - car_width # Padding to the right
    else:
        output_x = x

    # Create the output string with padding
    output_lines = []
    for line in car_art:
        padded_line = " " * output_x + line
        output_lines.append(padded_line)

    return "\n".join(output_lines)

def main():
    """Main function to animate the car."""
    car_x = 0
    speed = 1  # How many characters the car moves each frame
    delay = 0.1 # Delay between frames (in seconds)

    try:
        while True:
            clear_screen()
            
            # Draw the car at the current position
            print(draw_car(car_x))
            
            # Move the car
            car_x += speed
            
            # Reset car position to the left if it goes off the right edge
            # This calculation assumes a fixed screen width (e.g., 80 characters)
            # For a robust solution, you'd need to get the actual terminal size.
            screen_width = 80
            car_width = len(draw_car(0).split('\n')[0]) # Get car width from the first line
            
            if car_x > screen_width:
                car_x = -car_width # Start off-screen again

            time.sleep(delay)

    except KeyboardInterrupt:
        print("\nAnimation stopped.")

if __name__ == "__main__":
    main()