import json
import math
import os
import random
import time

import pygame


# ============================================================
# AIM PARADIGM
# Programming Paradigms final project
# Enhanced Python/Pygame version
# ============================================================

pygame.init()

GAME_TITLE = "AIM PARADIGM"
START_WIDTH = 1280
START_HEIGHT = 920
MIN_WIDTH = 1060
MIN_HEIGHT = 820
FPS = 60

screen = pygame.display.set_mode((START_WIDTH, START_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()


# ----------------------------
# Theme
# ----------------------------

DARK = (8, 12, 25)
PANEL = (16, 24, 48)
PANEL_2 = (23, 34, 66)
PANEL_3 = (31, 45, 82)
TEXT = (246, 250, 255)
MUTED = (205, 216, 235)
DIM = (135, 150, 180)

CYAN = (62, 220, 255)
BLUE = (75, 135, 255)
PURPLE = (157, 97, 255)
PINK = (255, 77, 166)
RED = (255, 72, 105)
GREEN = (82, 232, 158)
GOLD = (255, 204, 75)
ORANGE = (255, 143, 73)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ACCENTS = [GREEN, CYAN, RED, PURPLE, GOLD, ORANGE]


# ----------------------------
# Fonts
# ----------------------------

def make_fonts():
    return {
        "title": pygame.font.SysFont("Segoe UI", 64, bold=True),
        "mode": pygame.font.SysFont("Segoe UI", 38, bold=True),
        "large": pygame.font.SysFont("Segoe UI", 42, bold=True),
        "big": pygame.font.SysFont("Segoe UI", 32, bold=True),
        "medium": pygame.font.SysFont("Segoe UI", 24, bold=True),
        "small": pygame.font.SysFont("Segoe UI", 19),
        "caption": pygame.font.SysFont("Segoe UI", 17),
        "tiny": pygame.font.SysFont("Segoe UI", 16),
        "heart": pygame.font.SysFont("Segoe UI Symbol", 30, bold=True),
    }


FONTS = make_fonts()


# ----------------------------
# Game data
# ----------------------------

MODES = {
    "Classic": {
        "accent": CYAN,
        "short": "Balanced mode with hearts, scoring, combos, and penalties.",
        "description": "The core Aim Paradigm experience. Click targets before they expire, protect your hearts, and build combos for higher scores.",
        "rules": [
            "Start with a limited number of hearts.",
            "Clicking a target gives score and increases your combo.",
            "Missing a click or letting a target expire costs a heart.",
            "The round ends when time runs out or hearts reach zero.",
        ],
        "uses_lives": True,
        "penalizes_click_misses": True,
        "penalizes_expired": True,
        "score_penalty": False,
        "sudden_death": False,
        "zen": False,
    },
    "Time Attack": {
        "accent": GOLD,
        "short": "No hearts, but mistakes subtract points.",
        "description": "A speed-focused challenge. Score aggressively before time runs out, but avoid careless misses because they reduce your score.",
        "rules": [
            "There are no hearts in this mode.",
            "Wrong clicks subtract points and break your combo.",
            "Expired targets also subtract points and break your combo.",
            "The round ends only when the timer reaches zero.",
        ],
        "uses_lives": False,
        "penalizes_click_misses": True,
        "penalizes_expired": True,
        "score_penalty": True,
        "miss_penalty": 75,
        "expired_penalty": 50,
        "sudden_death": False,
        "zen": False,
    },
    "Sudden Death": {
        "accent": RED,
        "short": "One heart. One mistake ends the run.",
        "description": "A high-pressure precision mode. Every click matters and there is no room for careless mistakes.",
        "rules": [
            "You only have one heart.",
            "One wrong click ends the round.",
            "One expired target ends the round.",
            "Higher pressure, higher bragging rights.",
        ],
        "uses_lives": True,
        "penalizes_click_misses": True,
        "penalizes_expired": True,
        "score_penalty": False,
        "sudden_death": True,
        "zen": False,
    },
    "Zen": {
        "accent": GREEN,
        "short": "Relaxed practice with no punishment for mistakes.",
        "description": "A calmer practice mode made for warming up and improving mouse control without pressure.",
        "rules": [
            "There are no hearts in this mode.",
            "Misses do not punish you.",
            "Expired targets simply move to a new target.",
            "The round ends when the timer reaches zero.",
        ],
        "uses_lives": False,
        "penalizes_click_misses": False,
        "penalizes_expired": False,
        "score_penalty": False,
        "sudden_death": False,
        "zen": True,
    },
}

DIFFICULTIES = {
    "Casual": {
        "target_lifetime": 1.55,
        "target_radius": 40,
        "lives": 5,
        "round_seconds": 60,
        "description": "Bigger targets and more hearts.",
    },
    "Standard": {
        "target_lifetime": 1.10,
        "target_radius": 31,
        "lives": 3,
        "round_seconds": 60,
        "description": "Balanced default challenge.",
    },
    "Tryhard": {
        "target_lifetime": 0.72,
        "target_radius": 23,
        "lives": 3,
        "round_seconds": 45,
        "description": "Fast, small, and unforgiving.",
    },
    "Custom": {
        "target_lifetime": 1.10,
        "target_radius": 31,
        "lives": 3,
        "round_seconds": 60,
        "description": "Your own lives, speed, size, and time.",
    },
}

HIGH_SCORE_FILE = "high_scores.json"


# ----------------------------
# Utility
# ----------------------------

def window_size():
    return screen.get_size()


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def lerp_color(a, b, t):
    t = clamp(t, 0, 1)
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def format_time(seconds):
    seconds = max(0, int(math.ceil(seconds)))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def draw_text(surface, text, font, color, x, y, center=False, right=False):
    rendered = font.render(str(text), True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    elif right:
        rect.topright = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)
    return rect


def wrap_text(text, font, max_width):
    words = str(text).split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_wrapped_text(surface, text, font, color, x, y, max_width, line_height=22, center=False):
    lines = wrap_text(text, font, max_width)
    for index, line in enumerate(lines):
        if center:
            draw_text(surface, line, font, color, x + max_width // 2, y + index * line_height, center=True)
        else:
            draw_text(surface, line, font, color, x, y + index * line_height)
    return y + len(lines) * line_height


def draw_background(surface, pulse=0):
    width, height = window_size()

    for y in range(height):
        t = y / max(1, height)
        color = lerp_color(DARK, (11, 8, 28), t)
        pygame.draw.line(surface, color, (0, y), (width, y))

    grid_color = (24, 35, 70)
    grid = 64
    offset = int((pulse * 10) % grid)

    for x in range(-grid + offset, width, grid):
        pygame.draw.line(surface, grid_color, (x, 0), (x, height), 1)
    for y in range(-grid + offset, height, grid):
        pygame.draw.line(surface, grid_color, (0, y), (width, y), 1)

    decorations = [
        (110, 105, 175, PURPLE),
        (width - 80, 130, 145, BLUE),
        (width - 240, height - 90, 210, PINK),
        (145, height - 120, 135, CYAN),
    ]

    for x, y, radius, color in decorations:
        soft = tuple(int(c * 0.18) for c in color)
        pygame.draw.circle(surface, soft, (int(x), int(y)), int(radius))


def draw_panel(surface, rect, color=PANEL, border=(58, 86, 145), radius=24):
    shadow = pygame.Rect(rect.x, rect.y + 7, rect.w, rect.h)
    pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=radius)
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, width=2, border_radius=radius)


def draw_heart(surface, x, y, filled=True):
    color = RED if filled else (70, 78, 105)
    rendered = FONTS["heart"].render("♥", True, color)
    surface.blit(rendered, (x, y))


def load_high_scores():
    if not os.path.exists(HIGH_SCORE_FILE):
        return {}
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}


def save_high_scores(scores):
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
            json.dump(scores, file, indent=2)
    except OSError:
        pass


# ----------------------------
# UI Components
# ----------------------------

class Button:
    def __init__(self, rect, text, subtext="", accent=CYAN, font_key="medium", hero=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.subtext = subtext
        self.accent = accent
        self.font_key = font_key
        self.hero = hero

    def hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface, mouse_pos, selected=False):
        hover = self.hovered(mouse_pos)

        fill = PANEL_2 if not selected else lerp_color(PANEL_3, self.accent, 0.22)
        if self.hero:
            fill = lerp_color(PANEL_3, self.accent, 0.20)
        if hover:
            fill = lerp_color(fill, self.accent, 0.18)

        shadow = self.rect.move(0, 8)
        pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=18)
        pygame.draw.rect(surface, fill, self.rect, border_radius=18)

        border = self.accent if selected or hover or self.hero else (68, 88, 135)
        width = 3 if self.hero else 2
        pygame.draw.rect(surface, border, self.rect, width=width, border_radius=18)

        accent_bar = pygame.Rect(self.rect.x, self.rect.y, 7, self.rect.h)
        pygame.draw.rect(surface, border, accent_bar, border_radius=18)

        label_y = self.rect.y + (self.rect.h // 2 if not self.subtext else 30)
        draw_text(surface, self.text, FONTS[self.font_key], TEXT, self.rect.centerx, label_y, center=True)

        if self.subtext:
            draw_wrapped_text(
                surface,
                self.subtext,
                FONTS["caption"],
                MUTED,
                self.rect.x + 28,
                self.rect.y + 60,
                self.rect.w - 56,
                line_height=21,
                center=True,
            )


class MiniButton:
    def __init__(self, rect, text, accent=CYAN):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.accent = accent

    def hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface, mouse_pos):
        hover = self.hovered(mouse_pos)
        fill = lerp_color(PANEL_2, self.accent, 0.20 if hover else 0.05)
        pygame.draw.rect(surface, fill, self.rect, border_radius=12)
        pygame.draw.rect(surface, self.accent if hover else (65, 83, 130), self.rect, width=2, border_radius=12)
        draw_text(surface, self.text, FONTS["medium"], TEXT, self.rect.centerx, self.rect.centery - 2, center=True)


# ----------------------------
# Gameplay objects
# ----------------------------

class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2.0, 7.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = random.uniform(3, 7)
        self.life = random.uniform(0.35, 0.75)
        self.max_life = self.life
        self.color = color

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.96
        self.vy *= 0.96
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return
        ratio = self.life / self.max_life
        color = tuple(int(c * ratio) for c in self.color)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.radius * ratio)))


class Target:
    def __init__(self, radius, lifetime, mode_name):
        width, height = window_size()
        self.radius = radius
        self.lifetime = lifetime
        self.spawn_time = time.time()

        self.kind = "bonus" if random.random() < 0.14 else "normal"
        if self.kind == "bonus":
            self.radius = max(14, int(radius * 0.75))
            self.color = GOLD
            self.value = 250
        else:
            self.color = random.choice([CYAN, PURPLE, PINK, GREEN, ORANGE])
            self.value = 100

        top_margin = 132
        margin = self.radius + 30
        self.x = random.randint(margin, max(margin + 1, width - margin))
        self.y = random.randint(top_margin + margin, max(top_margin + margin + 1, height - margin))

        speed = 1.0
        if mode_name == "Sudden Death":
            speed = 2.2
        elif mode_name == "Time Attack":
            speed = 1.4

        angle = random.uniform(0, math.tau)
        self.vx = math.cos(angle) * random.uniform(0.45, 1.25) * speed
        self.vy = math.sin(angle) * random.uniform(0.45, 1.25) * speed

    def age(self):
        return time.time() - self.spawn_time

    def remaining_ratio(self):
        return clamp(1 - self.age() / self.lifetime, 0, 1)

    def expired(self):
        return self.age() >= self.lifetime

    def update(self):
        width, height = window_size()
        self.x += self.vx
        self.y += self.vy

        top_margin = 132
        if self.x < self.radius + 20 or self.x > width - self.radius - 20:
            self.vx *= -1
        if self.y < top_margin + self.radius or self.y > height - self.radius - 20:
            self.vy *= -1

        self.x = clamp(self.x, self.radius + 20, width - self.radius - 20)
        self.y = clamp(self.y, top_margin + self.radius, height - self.radius - 20)

    def contains(self, pos):
        mx, my = pos
        return (self.x - mx) ** 2 + (self.y - my) ** 2 <= self.radius ** 2

    def draw(self, surface):
        ratio = self.remaining_ratio()
        pulse = 1 + 0.08 * math.sin(time.time() * 9)
        center = (int(self.x), int(self.y))
        radius = int(self.radius * pulse)

        glow = tuple(int(c * 0.25) for c in self.color)
        pygame.draw.circle(surface, glow, center, int(radius * 2.15))
        pygame.draw.circle(surface, tuple(int(c * 0.42) for c in self.color), center, int(radius * 1.5))

        pygame.draw.circle(surface, self.color, center, radius)
        pygame.draw.circle(surface, WHITE, center, max(4, radius // 4))
        pygame.draw.circle(surface, DARK, center, max(2, radius // 9))
        pygame.draw.circle(surface, WHITE, center, radius, 3)
        pygame.draw.circle(surface, DARK, center, max(4, int(radius * 0.62)), 2)

        arc_rect = pygame.Rect(0, 0, radius * 2 + 18, radius * 2 + 18)
        arc_rect.center = center
        start = -math.pi / 2
        end = start + math.tau * ratio
        pygame.draw.arc(surface, GOLD if self.kind == "bonus" else CYAN, arc_rect, start, end, 5)

        if self.kind == "bonus":
            draw_text(surface, "+", FONTS["medium"], DARK, center[0], center[1] - 1, center=True)


# ----------------------------
# Game
# ----------------------------

class AimParadigm:
    def __init__(self):
        self.state = "select_mode"
        self.selected_mode = "Classic"
        self.selected_difficulty = "Standard"
        self.custom_settings = dict(DIFFICULTIES["Custom"])
        self.high_scores = load_high_scores()
        self.dropdown_open = False
        self.fullscreen = False
        self.windowed_size = (START_WIDTH, START_HEIGHT)

        self.target = None
        self.particles = []
        self.feedback = ""
        self.feedback_timer = 0
        self.new_record = False

        self.reset_stats()

    def set_fullscreen(self, enabled):
        global screen
        self.fullscreen = enabled
        if enabled:
            self.windowed_size = screen.get_size()
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(self.windowed_size, pygame.RESIZABLE)

    def toggle_fullscreen(self):
        self.set_fullscreen(not self.fullscreen)

    def set_window_size(self, width, height):
        global screen
        self.fullscreen = False
        self.windowed_size = (max(MIN_WIDTH, width), max(MIN_HEIGHT, height))
        screen = pygame.display.set_mode(self.windowed_size, pygame.RESIZABLE)

    def settings(self):
        if self.selected_difficulty == "Custom":
            return self.custom_settings
        return DIFFICULTIES[self.selected_difficulty]

    def reset_stats(self):
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.combo = 0
        self.max_combo = 0
        self.best_reaction = None
        self.lives = 3
        self.round_seconds = 60
        self.round_start = time.time()

    def high_score_key(self):
        return f"{self.selected_mode} - {self.selected_difficulty}"

    def update_high_score(self):
        key = self.high_score_key()
        old = self.high_scores.get(key, 0)
        self.new_record = self.score > old
        if self.new_record:
            self.high_scores[key] = self.score
            save_high_scores(self.high_scores)

    def start_game(self):
        settings = self.settings()
        mode = MODES[self.selected_mode]

        self.reset_stats()
        self.new_record = False

        self.target_lifetime = settings["target_lifetime"]
        self.target_radius = settings["target_radius"]
        self.round_seconds = settings["round_seconds"]
        self.lives = settings["lives"]

        if mode["sudden_death"]:
            self.lives = 1
            self.target_lifetime = max(0.45, self.target_lifetime * 0.78)
        if mode["zen"]:
            self.round_seconds = 45
            self.target_lifetime = max(1.0, self.target_lifetime)

        self.round_start = time.time()
        self.particles = []
        self.feedback = "GO!"
        self.feedback_timer = 0.8
        self.target = Target(self.target_radius, self.target_lifetime, self.selected_mode)
        self.state = "playing"

    def spawn_target(self):
        self.target = Target(self.target_radius, self.target_lifetime, self.selected_mode)

    def end_game(self):
        self.update_high_score()
        self.state = "game_over"

    def time_remaining(self):
        return self.round_seconds - (time.time() - self.round_start)

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0
        return round((self.hits / total) * 100, 1)

    def register_hit(self):
        reaction = self.target.age()
        if self.best_reaction is None or reaction < self.best_reaction:
            self.best_reaction = reaction

        self.hits += 1
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)

        time_bonus = int(120 * self.target.remaining_ratio())
        combo_bonus = min(500, self.combo * 15)
        gain = self.target.value + time_bonus + combo_bonus
        self.score += gain

        for _ in range(30):
            self.particles.append(Particle(self.target.x, self.target.y, self.target.color))

        self.feedback = f"+{gain}"
        self.feedback_timer = 0.45
        self.spawn_target()

    def register_miss(self, reason="MISS"):
        mode = MODES[self.selected_mode]
        self.misses += 1
        self.combo = 0

        if mode.get("score_penalty", False):
            penalty = mode.get("expired_penalty", 50) if reason == "EXPIRED" else mode.get("miss_penalty", 75)
            self.score = max(0, self.score - penalty)
            self.feedback = f"-{penalty}"
        else:
            if mode["sudden_death"]:
                self.lives = 0
            elif mode["uses_lives"]:
                self.lives -= 1
            self.feedback = reason

        self.feedback_timer = 0.55
        self.spawn_target()

    def update_playing(self, dt):
        if self.target:
            self.target.update()

        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]

        if self.feedback_timer > 0:
            self.feedback_timer -= dt

        mode = MODES[self.selected_mode]

        if self.target and self.target.expired():
            if mode["penalizes_expired"]:
                self.register_miss("EXPIRED")
            else:
                self.combo = 0
                self.spawn_target()

        if self.time_remaining() <= 0:
            self.end_game()

        if mode["uses_lives"] and self.lives <= 0:
            self.end_game()

    # ----------------------------
    # Shared UI
    # ----------------------------

    def draw_mode_dropdown(self, mouse_pos):
        width, _ = window_size()
        mode = MODES[self.selected_mode]
        button = Button((width - 420, 28, 370, 58), f"MODE: {self.selected_mode} ▼", "", mode["accent"], "small")
        button.draw(screen, mouse_pos)

        items = []
        if self.dropdown_open:
            y = 90
            for mode_name, info in MODES.items():
                item = Button((width - 420, y, 370, 94), mode_name, info["short"], info["accent"], "small")
                item.draw(screen, mouse_pos, selected=(mode_name == self.selected_mode))
                items.append((mode_name, item))
                y += 108

        return button, items

    # ----------------------------
    # Screens
    # ----------------------------

    def draw_select_mode(self, mouse_pos):
        width, height = window_size()
        draw_background(screen, time.time())

        draw_text(screen, GAME_TITLE, FONTS["title"], TEXT, width // 2, 75, center=True)
        draw_text(screen, "SELECT GAMEMODE", FONTS["mode"], CYAN, width // 2, 135, center=True)
        draw_text(screen, "Choose how you want to play.", FONTS["small"], MUTED, width // 2, 175, center=True)

        card_w = min(520, (width - 180) // 2)
        card_h = 112
        gap_x = 34
        gap_y = 26
        start_x = width // 2 - card_w - gap_x // 2
        start_y = 220

        mode_buttons = []
        mode_names = list(MODES.keys())
        for i, mode_name in enumerate(mode_names):
            col = i % 2
            row = i // 2
            x = start_x + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)
            info = MODES[mode_name]
            button = Button((x, y, card_w, card_h), mode_name.upper(), info["short"], info["accent"], "big")
            button.draw(screen, mouse_pos)
            mode_buttons.append((mode_name, button))

        quit_button = Button((width // 2 - 150, height - 98, 300, 58), "QUIT", "", RED, "medium")
        quit_button.draw(screen, mouse_pos)

        return mode_buttons, quit_button

    def draw_mode_rules_card(self, x, y, w):
        mode = MODES[self.selected_mode]
        accent = mode["accent"]

        # Large readable card with real breathing room for the description and all rules.
        card_h = 330
        panel = pygame.Rect(x, y, w, card_h)
        draw_panel(screen, panel, (15, 23, 45), (55, 90, 155), 22)

        draw_text(screen, self.selected_mode.upper(), FONTS["mode"], accent, x + 38, y + 26)

        desc_end_y = draw_wrapped_text(
            screen,
            mode["description"],
            FONTS["small"],
            MUTED,
            x + 40,
            y + 84,
            w - 80,
            line_height=27,
        )

        rules_y = max(y + 152, desc_end_y + 22)
        draw_text(screen, "Rules", FONTS["medium"], TEXT, x + 40, rules_y)

        bullet_y = rules_y + 40
        for rule in mode["rules"]:
            draw_text(screen, "•", FONTS["small"], accent, x + 48, bullet_y)
            draw_wrapped_text(
                screen,
                rule,
                FONTS["caption"],
                MUTED,
                x + 76,
                bullet_y,
                w - 122,
                line_height=23,
            )
            bullet_y += 32

        return panel

    def draw_difficulty(self, mouse_pos):
        width, height = window_size()
        draw_background(screen, time.time())

        dropdown_data = self.draw_mode_dropdown(mouse_pos)

        content_w = min(960, width - 180)
        x = width // 2 - content_w // 2

        # Clean vertical order:
        # Title -> mode/rules -> START -> 3 difficulties -> Custom -> Quit.
        draw_text(screen, GAME_TITLE, FONTS["title"], TEXT, width // 2, 58, center=True)
        self.draw_mode_rules_card(x, 112, content_w)

        start_y = 470
        start_button = Button((x, start_y, content_w, 74), "START GAME", "Launch the selected setup.", GREEN, "big", hero=True)
        start_button.draw(screen, mouse_pos)

        diff_y = start_y + 104
        gap = 24
        diff_w = (content_w - gap * 2) // 3
        difficulty_buttons = []

        difficulty_order = [("Casual", GREEN), ("Standard", CYAN), ("Tryhard", RED)]
        for index, (name, color) in enumerate(difficulty_order):
            settings = DIFFICULTIES[name]
            button = Button(
                (x + index * (diff_w + gap), diff_y, diff_w, 112),
                name.upper(),
                settings["description"],
                color,
                "medium",
            )
            button.draw(screen, mouse_pos, selected=(self.selected_difficulty == name))
            difficulty_buttons.append((name, button))

        custom_y = diff_y + 142
        custom_button = Button(
            (x, custom_y, content_w, 74),
            "CUSTOM DIFFICULTY",
            "Customize lives, target size, target lifetime, and round time.",
            PURPLE,
            "medium",
        )
        custom_button.draw(screen, mouse_pos, selected=(self.selected_difficulty == "Custom"))

        quit_y = custom_y + 96
        quit_button = Button((x, quit_y, content_w, 58), "QUIT", "", RED, "medium")
        quit_button.draw(screen, mouse_pos)

        selected = DIFFICULTIES[self.selected_difficulty]
        stats = f"{self.selected_difficulty}: Target {selected['target_radius']}px | Lifetime {selected['target_lifetime']:.2f}s | Lives {selected['lives']} | Time {selected['round_seconds']}s"
        if self.selected_mode == "Time Attack":
            stats += " | Miss -75 | Expired -50"
        elif self.selected_mode == "Zen":
            stats += " | No penalties"
        draw_text(screen, stats, FONTS["caption"], MUTED, width // 2, min(height - 24, quit_y + 70), center=True)

        return {
            "dropdown": dropdown_data,
            "start": start_button,
            "difficulty_buttons": difficulty_buttons,
            "custom": custom_button,
            "quit": quit_button,
        }

    def draw_custom(self, mouse_pos):
        width, height = window_size()
        draw_background(screen, time.time())

        dropdown_data = self.draw_mode_dropdown(mouse_pos)

        content_w = min(860, width - 120)
        x = width // 2 - content_w // 2

        draw_text(screen, GAME_TITLE, FONTS["title"], TEXT, width // 2, 62, center=True)
        draw_text(screen, "CUSTOM DIFFICULTY", FONTS["mode"], PURPLE, width // 2, 124, center=True)
        draw_text(screen, "Adjust one setting per row. This keeps the editor clean and readable.", FONTS["small"], MUTED, width // 2, 162, center=True)

        panel = pygame.Rect(x, 200, content_w, 380)
        draw_panel(screen, panel, (15, 23, 45), (55, 90, 155), 24)

        fields = [
            ("Lives", "lives", 1, 10, 1, "", "How many mistakes you can survive in heart-based modes."),
            ("Target Size", "target_radius", 14, 65, 1, "px", "Smaller targets are harder to click."),
            ("Target Lifetime", "target_lifetime", 0.35, 2.60, 0.05, "s", "How long each target stays active."),
            ("Round Time", "round_seconds", 20, 180, 1, "s", "Total length of the round."),
        ]

        controls = []
        row_y = panel.y + 34
        for i, (label, key, minimum, maximum, step, suffix, helper) in enumerate(fields):
            accent = ACCENTS[i]
            row = pygame.Rect(panel.x + 28, row_y + i * 84, panel.w - 56, 64)
            pygame.draw.rect(screen, (21, 31, 60), row, border_radius=14)
            pygame.draw.rect(screen, (58, 78, 125), row, width=1, border_radius=14)

            draw_text(screen, label, FONTS["medium"], TEXT, row.x + 20, row.y + 19)

            value = self.custom_settings[key]
            value_text = f"{value:.2f}{suffix}" if isinstance(value, float) else f"{value}{suffix}"
            draw_text(screen, value_text, FONTS["big"], accent, row.right - 166, row.y + 32, center=True)

            minus = MiniButton((row.right - 285, row.y + 10, 46, 44), "-", RED)
            plus = MiniButton((row.right - 78, row.y + 10, 46, 44), "+", GREEN)
            minus.draw(screen, mouse_pos)
            plus.draw(screen, mouse_pos)

            controls.append((key, -step, minimum, maximum, minus))
            controls.append((key, step, minimum, maximum, plus))

        # Vertical button order
        start_y = 602
        start_button = Button((x, start_y, content_w, 64), "START CUSTOM GAME", "", GREEN, "big", hero=True)
        reset_button = Button((x, start_y + 78, content_w, 52), "RESET CUSTOM SETTINGS", "", PURPLE, "medium")
        back_button = Button((x, start_y + 144, (content_w - 20) // 2, 52), "BACK TO DIFFICULTY", "", CYAN, "medium")
        quit_button = Button((x + (content_w + 20) // 2, start_y + 144, (content_w - 20) // 2, 52), "QUIT", "", RED, "medium")

        for button in [start_button, reset_button, back_button, quit_button]:
            button.draw(screen, mouse_pos)

        return {
            "dropdown": dropdown_data,
            "controls": controls,
            "start": start_button,
            "reset": reset_button,
            "back": back_button,
            "quit": quit_button,
        }

    def draw_confirm_quit(self, mouse_pos):
        width, height = window_size()
        draw_background(screen, time.time())

        panel = pygame.Rect(width // 2 - 330, height // 2 - 150, 660, 300)
        draw_panel(screen, panel, (17, 25, 48), (90, 70, 130), 26)

        draw_text(screen, "QUIT AIM PARADIGM?", FONTS["large"], TEXT, width // 2, panel.y + 70, center=True)
        draw_text(screen, "Are you sure you want to close the program?", FONTS["small"], MUTED, width // 2, panel.y + 126, center=True)

        yes_button = Button((width // 2 - 230, panel.y + 190, 200, 58), "YES, QUIT", "", RED, "medium")
        no_button = Button((width // 2 + 30, panel.y + 190, 200, 58), "CANCEL", "", GREEN, "medium")
        yes_button.draw(screen, mouse_pos)
        no_button.draw(screen, mouse_pos)

        return yes_button, no_button

    def draw_playing(self):
        width, height = window_size()
        draw_background(screen, time.time())

        frame = pygame.Rect(28, 120, width - 56, height - 150)
        pygame.draw.rect(screen, (22, 34, 66), frame, width=2, border_radius=24)

        if self.target:
            self.target.draw(screen)

        for particle in self.particles:
            particle.draw(screen)

        if self.feedback_timer > 0 and self.feedback:
            color = GREEN if self.feedback.startswith("+") or self.feedback == "GO!" else RED
            draw_text(screen, self.feedback, FONTS["big"], color, width // 2, 155, center=True)

        header = pygame.Rect(28, 20, width - 56, 82)
        draw_panel(screen, header, (14, 20, 40), (45, 70, 120), 22)

        draw_text(screen, GAME_TITLE, FONTS["big"], TEXT, 56, 38)
        draw_text(screen, f"{self.selected_mode} | {self.selected_difficulty}", FONTS["tiny"], MUTED, 58, 75)

        draw_text(screen, "SCORE", FONTS["tiny"], MUTED, 350, 34)
        draw_text(screen, self.score, FONTS["big"], GOLD, 350, 53)

        draw_text(screen, "COMBO", FONTS["tiny"], MUTED, 500, 34)
        draw_text(screen, f"x{self.combo}", FONTS["big"], CYAN, 500, 53)

        timer_x = 650
        timer_y = 49
        timer_w = min(260, max(160, width - 1010))
        ratio = clamp(self.time_remaining() / self.round_seconds, 0, 1)
        color = GREEN if ratio > 0.45 else GOLD if ratio > 0.20 else RED

        draw_text(screen, "TIMER", FONTS["tiny"], MUTED, timer_x, 29)
        pygame.draw.rect(screen, (35, 45, 75), (timer_x, timer_y, timer_w, 24), border_radius=14)
        pygame.draw.rect(screen, color, (timer_x, timer_y, int(timer_w * ratio), 24), border_radius=14)
        pygame.draw.rect(screen, (80, 95, 140), (timer_x, timer_y, timer_w, 24), width=2, border_radius=14)
        draw_text(screen, format_time(self.time_remaining()), FONTS["medium"], TEXT, timer_x + timer_w + 60, timer_y + 12, center=True)

        mode = MODES[self.selected_mode]
        lives_x = width - 235
        if mode["uses_lives"]:
            draw_text(screen, "LIVES", FONTS["tiny"], MUTED, lives_x, 29)
            max_lives = 1 if mode["sudden_death"] else self.settings()["lives"]
            for i in range(max_lives):
                draw_heart(screen, lives_x + i * 31, 50, i < self.lives)
        else:
            draw_text(screen, "NO HEART LIMIT", FONTS["small"], GREEN, lives_x, 54)

        draw_text(screen, "Left click targets | ESC ends round | F11 fullscreen | Resize with window borders", FONTS["tiny"], MUTED, width // 2, height - 28, center=True)

    def draw_game_over(self, mouse_pos):
        width, height = window_size()
        draw_background(screen, time.time())

        title = "NEW RECORD!" if self.new_record else "GAME OVER"
        title_color = GOLD if self.new_record else TEXT

        draw_text(screen, GAME_TITLE, FONTS["title"], TEXT, width // 2, 62, center=True)
        draw_text(screen, title, FONTS["mode"], title_color, width // 2, 128, center=True)
        draw_text(screen, f"{self.selected_mode} | {self.selected_difficulty}", FONTS["small"], CYAN, width // 2, 166, center=True)

        panel_w = min(940, width - 120)
        panel = pygame.Rect(width // 2 - panel_w // 2, 205, panel_w, 295)
        draw_panel(screen, panel, (15, 23, 45), (55, 90, 155), 26)

        stats = [
            ("Score", str(self.score), GOLD),
            ("Hits", str(self.hits), GREEN),
            ("Misses", str(self.misses), RED),
            ("Accuracy", f"{self.accuracy()}%", CYAN),
            ("Max Combo", f"x{self.max_combo}", PURPLE),
            ("Best Reaction", "N/A" if self.best_reaction is None else f"{self.best_reaction:.2f}s", ORANGE),
        ]

        card_w = (panel.w - 90) // 3
        card_h = 76
        for i, (label, value, color) in enumerate(stats):
            col = i % 3
            row = i // 3
            rect = pygame.Rect(panel.x + 30 + col * (card_w + 15), panel.y + 40 + row * 104, card_w, card_h)
            pygame.draw.rect(screen, (22, 32, 62), rect, border_radius=16)
            pygame.draw.rect(screen, color, rect, width=2, border_radius=16)
            draw_text(screen, label, FONTS["tiny"], MUTED, rect.x + 16, rect.y + 12)
            draw_text(screen, value, FONTS["big"], color, rect.x + 16, rect.y + 33)

        high = self.high_scores.get(self.high_score_key(), self.score)
        draw_text(screen, f"Best score for this setup: {high}", FONTS["small"], MUTED, width // 2, panel.y + panel.h - 28, center=True)

        y = height - 110
        retry = Button((width // 2 - 440, y, 190, 60), "RETRY", "", GREEN, "medium")
        difficulty = Button((width // 2 - 220, y, 250, 60), "DIFFICULTY", "", CYAN, "medium")
        modes = Button((width // 2 + 60, y, 190, 60), "MODES", "", PURPLE, "medium")
        quit_button = Button((width // 2 + 280, y, 160, 60), "QUIT", "", RED, "medium")

        for button in [retry, difficulty, modes, quit_button]:
            button.draw(screen, mouse_pos)

        return retry, difficulty, modes, quit_button

    # ----------------------------
    # Events
    # ----------------------------

    def ask_quit(self):
        self.previous_state = self.state
        self.state = "confirm_quit"

    def handle_dropdown_click(self, pos, dropdown_data):
        button, items = dropdown_data
        if button.hovered(pos):
            self.dropdown_open = not self.dropdown_open
            return True

        if self.dropdown_open:
            for mode_name, item in items:
                if item.hovered(pos):
                    self.selected_mode = mode_name
                    self.dropdown_open = False
                    return True

        return False

    def run(self):
        running = True
        data = None

        while running:
            dt = clock.tick(FPS) / 1000
            mouse_pos = pygame.mouse.get_pos()

            if self.state == "select_mode":
                data = self.draw_select_mode(mouse_pos)
            elif self.state == "difficulty":
                data = self.draw_difficulty(mouse_pos)
            elif self.state == "custom":
                data = self.draw_custom(mouse_pos)
            elif self.state == "confirm_quit":
                data = self.draw_confirm_quit(mouse_pos)
            elif self.state == "playing":
                self.update_playing(dt)
                self.draw_playing()
                data = None
            elif self.state == "game_over":
                data = self.draw_game_over(mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ask_quit()

                elif event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.set_window_size(event.w, event.h)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

                    elif event.key == pygame.K_ESCAPE:
                        if self.state == "playing":
                            self.end_game()
                        elif self.state == "select_mode":
                            self.ask_quit()
                        elif self.state == "confirm_quit":
                            self.state = getattr(self, "previous_state", "select_mode")
                        elif self.state == "custom":
                            self.state = "difficulty"
                        else:
                            self.ask_quit()

                    elif event.key == pygame.K_SPACE:
                        if self.state in ["difficulty", "game_over"]:
                            self.start_game()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos

                    if self.state == "select_mode":
                        mode_buttons, quit_button = data
                        for mode_name, button in mode_buttons:
                            if button.hovered(pos):
                                self.selected_mode = mode_name
                                self.state = "difficulty"
                        if quit_button.hovered(pos):
                            self.ask_quit()

                    elif self.state == "difficulty":
                        if self.handle_dropdown_click(pos, data["dropdown"]):
                            continue
                        self.dropdown_open = False

                        if data["start"].hovered(pos):
                            self.start_game()

                        for diff_name, button in data["difficulty_buttons"]:
                            if button.hovered(pos):
                                self.selected_difficulty = diff_name

                        if data["custom"].hovered(pos):
                            self.selected_difficulty = "Custom"
                            self.state = "custom"
                        elif data["quit"].hovered(pos):
                            self.ask_quit()

                    elif self.state == "custom":
                        if self.handle_dropdown_click(pos, data["dropdown"]):
                            continue
                        self.dropdown_open = False

                        for key, delta, minimum, maximum, button in data["controls"]:
                            if button.hovered(pos):
                                value = self.custom_settings[key] + delta
                                value = clamp(value, minimum, maximum)
                                if key in ["lives", "target_radius", "round_seconds"]:
                                    value = int(value)
                                else:
                                    value = round(value, 2)
                                self.custom_settings[key] = value

                        if data["start"].hovered(pos):
                            self.selected_difficulty = "Custom"
                            self.start_game()
                        elif data["reset"].hovered(pos):
                            self.custom_settings = dict(DIFFICULTIES["Custom"])
                        elif data["back"].hovered(pos):
                            self.state = "difficulty"
                        elif data["quit"].hovered(pos):
                            self.ask_quit()

                    elif self.state == "confirm_quit":
                        yes_button, no_button = data
                        if yes_button.hovered(pos):
                            running = False
                        elif no_button.hovered(pos):
                            self.state = getattr(self, "previous_state", "select_mode")

                    elif self.state == "playing":
                        mode = MODES[self.selected_mode]
                        if self.target and self.target.contains(pos):
                            self.register_hit()
                        elif mode["penalizes_click_misses"]:
                            self.register_miss("MISS")
                        else:
                            self.combo = 0
                            self.feedback = "NO PENALTY"
                            self.feedback_timer = 0.4

                    elif self.state == "game_over":
                        retry, difficulty, modes, quit_button = data
                        if retry.hovered(pos):
                            self.start_game()
                        elif difficulty.hovered(pos):
                            self.state = "difficulty"
                        elif modes.hovered(pos):
                            self.state = "select_mode"
                        elif quit_button.hovered(pos):
                            self.ask_quit()

        pygame.quit()


if __name__ == "__main__":
    AimParadigm().run()
