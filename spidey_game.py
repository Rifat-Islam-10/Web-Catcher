import tkinter as tk
import random
import os

WIDTH = 600
HEIGHT = 700
PLAYER_SPEED = 25
BASE_FALL_SPEED = 7

# Images must sit in the same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CATCHER_IMG_PATH = os.path.join(SCRIPT_DIR, "Spider-Man-PNG.png")
FALLING_IMG_PATH = os.path.join(SCRIPT_DIR, "Gwen_Stacy_PNG.png")
BG_IMG_PATH=os.path.join(SCRIPT_DIR,"SM-FALL.png")


class CatcherGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Catcher Game")
        self.root.resizable(False, False)
        self.root.state("zoomed")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()
        
        self.bg_img=tk.PhotoImage(file=BG_IMG_PATH)
        self.bg=self.canvas.create_image(0,0,anchor="nw",image=self.bg_img)
        self.canvas.tag_lower(self.bg)

        self.score = 0
        self.game_over = False
        self.fall_speed = BASE_FALL_SPEED

        self.score_text = self.canvas.create_text(
            10, 10, anchor="nw", text=f"Score: {self.score}",
            font=("Arial", 14, "bold"), fill="light blue"
        )

        # Keep references to images so they aren't garbage-collected
        self.catcher_img = tk.PhotoImage(file=CATCHER_IMG_PATH)
        self.falling_img = tk.PhotoImage(file=FALLING_IMG_PATH)
        
        

        # Bottom catcher character
        self.player_y = HEIGHT - 50
        self.player = self.canvas.create_image(
            WIDTH // 2, self.player_y, image=self.catcher_img
        )

        # Falling character
        self.falling_object = self.create_falling_object()

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<KeyPress-a>", self.move_left)
        self.root.bind("<KeyPress-d>", self.move_right)
        self.root.focus_set()

        self.game_loop()

    def create_falling_object(self):
        x = random.randint(40, WIDTH - 40)
        return self.canvas.create_image(x, 0, image=self.falling_img)

    def move_left(self, event):
        if self.game_over:
            return
        self.canvas.move(self.player, -PLAYER_SPEED, 0)
        x1, y1, x2, y2 = self.canvas.bbox(self.player)
        if x1 < 0:
            self.canvas.move(self.player, -x1, 0)

    def move_right(self, event):
        if self.game_over:
            return
        self.canvas.move(self.player, PLAYER_SPEED, 0)
        x1, y1, x2, y2 = self.canvas.bbox(self.player)
        if x2 > WIDTH:
            self.canvas.move(self.player, WIDTH - x2, 0)

    def reset_object(self):
        self.canvas.delete(self.falling_object)
        self.falling_object = self.create_falling_object()
        # Gradually increase difficulty as score grows
        self.fall_speed = BASE_FALL_SPEED + self.score // 5

    def check_collision(self):
        p = self.canvas.bbox(self.player)
        o = self.canvas.bbox(self.falling_object)
        if not p or not o:
            return False
        px1, py1, px2, py2 = p
        ox1, oy1, ox2, oy2 = o
        # Standard axis-aligned bounding box overlap test
        return px1 < ox2 and px2 > ox1 and py1 < oy2 and py2 > oy1

    def game_loop(self):
        if self.game_over:
            return

        self.canvas.move(self.falling_object, 0, self.fall_speed)
        o = self.canvas.coords(self.falling_object)

        if self.check_collision():
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            self.reset_object()
        elif o[1] > HEIGHT:  # missed - fell past the bottom
            self.end_game()
            return

        self.root.after(30, self.game_loop)

    def end_game(self):
        self.game_over = True
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2,
            text="In every other Universe Gwen Stacy falls for SpiderMan!",
            font=("Comic Sans MS", 14, "bold"),
            fill="red"
        )
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2 + 40,
            text=f"Total Catches: {self.score}",
            font=("Arial", 19),
            fill="blue"
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = CatcherGame(root)
    root.mainloop()