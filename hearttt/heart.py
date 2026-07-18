import tkinter as tk
import math
import random

WIDTH, HEIGHT = 600, 700

root = tk.Tk()
root.title("Kryztine")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack()

# Violet / purple / pink palette
colors = ["#9b30ff", "#a64dff", "#8a2be2", "#b266ff", "#d18cff",
          "#7a1fd1", "#c77dff", "#e0aaff", "#ff77ff", "#bf5fff", "#ffffff"]

GRAVITY = 0.06
AIR = 0.985  # air resistance so sparks slow down naturally


class Particle:
    def __init__(self, x, y, color, velocity):
        angle = random.uniform(0, 2 * math.pi)
        # slight randomness so the circle isn't perfect (more realistic)
        speed = velocity * random.uniform(0.6, 1.0)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed + (random.random() - 0.5) * 0.5
        self.vy = math.sin(angle) * speed + (random.random() - 0.5) * 0.5
        self.color = color
        self.life = random.randint(45, 80)
        self.age = 0
        self.size = random.uniform(1.5, 3.0)
        self.id = canvas.create_oval(x, y, x, y, fill=color, outline="")

    def update(self):
        self.vx *= AIR
        self.vy *= AIR
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        s = self.size
        canvas.coords(self.id, self.x - s, self.y - s, self.x + s, self.y + s)
        # twinkle / fade near the end of life
        if self.age > self.life * 0.55:
            if self.age % 3 == 0:
                canvas.itemconfig(self.id, fill="")
            else:
                canvas.itemconfig(self.id, fill=self.color)
        return self.age < self.life

    def destroy(self):
        canvas.delete(self.id)


class Rocket:
    def __init__(self):
        self.x = random.uniform(WIDTH * 0.15, WIDTH * 0.85)
        self.y = HEIGHT
        self.target_y = random.uniform(HEIGHT * 0.15, HEIGHT * 0.5)
        self.color = random.choice(colors)
        self.speed = random.uniform(8, 12)
        self.id = canvas.create_oval(self.x - 2, self.y - 2,
                                     self.x + 2, self.y + 2,
                                     fill="#ffffff", outline="")

    def update(self):
        self.y -= self.speed
        canvas.coords(self.id, self.x - 2, self.y - 2, self.x + 2, self.y + 2)
        return self.y > self.target_y

    def explode(self):
        canvas.delete(self.id)
        # bright flash at the burst point
        flash = canvas.create_oval(self.x - 20, self.y - 20,
                                   self.x + 20, self.y + 20,
                                   fill="#e0aaff", outline="")
        flashes.append([flash, 6])
        # full-circle burst (like the example's makeFullCircleFirework)
        velocity = random.uniform(4, 7)
        count = random.randint(50, 90)
        burst_color = random.choice(colors)
        new = []
        for _ in range(count):
            c = burst_color if random.random() < 0.7 else random.choice(colors)
            new.append(Particle(self.x, self.y, c, velocity))
        return new


rockets = []
particles = []
flashes = []
frame = 0
name_shown = False
name_id = None
name_glow = []


def show_name():
    global name_id, name_glow
    for off, col in [(5, "#2a0845"), (3, "#5b1a9c"), (1, "#8a2be2")]:
        g = canvas.create_text(WIDTH // 2 + off, HEIGHT // 2 + off,
                               text="Kryztine",
                               font=("Georgia", 48, "bold"), fill=col)
        name_glow.append(g)
    name_id = canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Kryztine",
                                 font=("Georgia", 48, "bold"), fill="#f0d6ff")


def tick():
    global frame, name_shown
    frame += 1

    # launch rockets continuously (sometimes two at once for a fuller sky)
    if frame % random.randint(8, 16) == 0:
        rockets.append(Rocket())
        if random.random() < 0.4:
            rockets.append(Rocket())

    for r in rockets[:]:
        if not r.update():
            particles.extend(r.explode())
            rockets.remove(r)

    for p in particles[:]:
        if not p.update():
            p.destroy()
            particles.remove(p)

    # shrink and remove burst flashes
    for f in flashes[:]:
        f[1] -= 1
        if f[1] <= 0:
            canvas.delete(f[0])
            flashes.remove(f)
        else:
            x0, y0, x1, y1 = canvas.coords(f[0])
            canvas.coords(f[0], x0 + 3, y0 + 3, x1 - 3, y1 - 3)

    if frame > 100 and not name_shown:
        show_name()
        name_shown = True

    if name_shown:
        for g in name_glow:
            canvas.tag_raise(g)
        canvas.tag_raise(name_id)

    root.after(20, tick)


tick()
root.mainloop()