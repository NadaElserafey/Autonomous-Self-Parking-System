import pygame
import random
import math
from queue import PriorityQueue

# إعدادات الألوان المبهجة
COLOR_FLOOR = (236, 240, 241)    
COLOR_GRID = (189, 195, 199)     
COLOR_MAIN_CAR = (46, 204, 113)  
COLOR_LASER = (231, 76, 60)      
COLOR_TARGET = (241, 196, 15)    
BRIGHT_COLORS = [(52, 152, 219), (155, 89, 182), (230, 126, 34), (26, 188, 156), (255, 107, 129), (72, 52, 212)]

pygame.init()
WIDTH, HEIGHT = 1000, 750 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Smart Parking - Auto-Success Edition")

font_title = pygame.font.SysFont("Impact", 32)
font_stats = pygame.font.SysFont("Arial", 16, bold=True)
font_msg = pygame.font.SysFont("Impact", 50)

class ParkingSystem:
    def __init__(self):
        self.grid = 40
        self.g_width = random.randint(750, 850)
        self.g_height = random.randint(450, 520)
        self.origin_x = (WIDTH - self.g_width) // 2
        self.origin_y = (HEIGHT - self.g_height) // 2 + 40
        self.cols = self.g_width // self.grid
        self.rows = self.g_height // self.grid
        
        self.car_grid_pos = [random.randint(0, self.cols-1), random.randint(0, self.rows-1)]
        self.car_pixel_pos = [self.origin_x + self.car_grid_pos[0]*self.grid, 
                              self.origin_y + self.car_grid_pos[1]*self.grid]
        
        self.other_cars, self.pillars, self.target = [], [], None
        self.generate_assets()
        
        self.scanning = True
        self.scan_angle = 0
        self.scan_limit = 1080 # وقت طويل لليزر (3 لفات)
        self.sc_area_free, self.sc_area_occ = 0, 0
        self.path, self.path_index = [], 0
        self.is_moving, self.finished = False, False

    def generate_assets(self):
        occupied = [tuple(self.car_grid_pos)]
        for _ in range(random.randint(6, 10)):
            pos = (random.randint(0, self.cols-1), random.randint(0, self.rows-1))
            if pos not in occupied:
                self.pillars.append({'pos': pos, 'color': random.choice(BRIGHT_COLORS)})
                occupied.append(pos)
        for _ in range(random.randint(20, 30)):
            pos = (random.randint(0, self.cols-1), random.randint(0, self.rows-1))
            if pos not in occupied:
                self.other_cars.append({'pos': pos, 'color': random.choice(BRIGHT_COLORS)})
                occupied.append(pos)
        
        all_empty = []
        for c in range(self.cols):
            for r in range(self.rows):
                if (c, r) not in occupied:
                    d = math.hypot(c - self.car_grid_pos[0], r - self.car_grid_pos[1])
                    all_empty.append(((c, r), d))
        
        all_empty.sort(key=lambda x: x[1], reverse=True)
        if all_empty:
            self.target = random.choice(all_empty[:max(1, len(all_empty)//4)])[0]

    def draw_styled_car(self, x, y, color):
        w, h = self.grid * 0.8, self.grid * 0.6
        surf = pygame.Surface((self.grid, self.grid), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (4, 8, w, h), border_radius=6)
        pygame.draw.rect(surf, (44, 62, 80), (self.grid-15, 10, 8, h-4), border_radius=2)
        screen.blit(surf, (x, y))

    def solve_astar(self):
        start, end = tuple(self.car_grid_pos), self.target
        queue = PriorityQueue()
        queue.put((0, 0, start))
        came_from, g_score = {}, { (c, r): float("inf") for r in range(self.rows) for c in range(self.cols) }
        g_score[start] = 0
        obs = {c['pos'] for c in self.other_cars} | {p['pos'] for p in self.pillars}
        
        while not queue.empty():
            curr = queue.get()[2]
            if curr == end:
                p = []
                while curr in came_from: p.append(curr); curr = came_from[curr]
                return p[::-1]
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nb = (curr[0]+dx, curr[1]+dy)
                if 0 <= nb[0] < self.cols and 0 <= nb[1] < self.rows and nb not in obs:
                    tg = g_score[curr] + 1
                    if tg < g_score[nb]:
                        came_from[nb] = curr
                        g_score[nb] = tg
                        queue.put((tg + abs(nb[0]-end[0]) + abs(nb[1]-end[1]), id(nb), nb))
        return []

    def update(self):
        if self.scanning:
            self.scan_angle += 15 
            if self.scan_angle >= self.scan_limit:
                self.scanning = False
                occ = len(self.other_cars) + len(self.pillars)
                self.sc_area_occ = occ * 4; self.sc_area_free = (self.cols * self.rows - occ) * 4
                self.path = self.solve_astar(); self.is_moving = True
        
        if self.is_moving and self.path_index < len(self.path):
            tp = [self.origin_x + self.path[self.path_index][0]*self.grid, self.origin_y + self.path[self.path_index][1]*self.grid]
            dx, dy = tp[0] - self.car_pixel_pos[0], tp[1] - self.car_pixel_pos[1]
            dist = math.hypot(dx, dy)
            if dist > 2:
                self.car_pixel_pos[0] += dx * 0.18; self.car_pixel_pos[1] += dy * 0.18
            else:
                self.path_index += 1
                if self.path_index >= len(self.path): self.finished = True

    def draw(self):
        screen.fill((245, 246, 250)) 
        pygame.draw.rect(screen, COLOR_FLOOR, (self.origin_x, self.origin_y, self.g_width, self.g_height), border_radius=10)
        pygame.draw.rect(screen, COLOR_GRID, (self.origin_x, self.origin_y, self.g_width, self.g_height), 2, border_radius=10)

        for p in self.pillars:
            px, py = self.origin_x + p['pos'][0]*self.grid + self.grid//2, self.origin_y + p['pos'][1]*self.grid + self.grid//2
            pygame.draw.circle(screen, p['color'], (px, py), self.grid//3)
        for oc in self.other_cars:
            self.draw_styled_car(self.origin_x + oc['pos'][0]*self.grid, self.origin_y + oc['pos'][1]*self.grid, oc['color'])
        if self.target:
            pygame.draw.rect(screen, COLOR_TARGET, (self.origin_x + self.target[0]*self.grid+5, self.origin_y + self.target[1]*self.grid+5, self.grid-10, self.grid-10), 4, border_radius=6)
        
        if self.scanning:
            cx, cy = self.car_pixel_pos[0] + self.grid//2, self.car_pixel_pos[1] + self.grid//2
            for i in range(0, 360, 20):
                rad = math.radians(i + self.scan_angle)
                pygame.draw.line(screen, COLOR_LASER, (cx, cy), (cx + math.cos(rad)*1000, cy + math.sin(rad)*1000), 1)

        if not self.finished and self.path:
            for p in self.path[self.path_index:]:
                pygame.draw.circle(screen, (46, 204, 113), (self.origin_x + p[0]*self.grid + self.grid//2, self.origin_y + p[1]*self.grid + self.grid//2), 3)
        self.draw_styled_car(self.car_pixel_pos[0], self.car_pixel_pos[1], COLOR_MAIN_CAR)

        # Dashboard UI
        pygame.draw.rect(screen, (44, 62, 80), (0, 0, WIDTH, 110))
        screen.blit(font_title.render("AI SMART PARKING", True, (255, 255, 255)), (30, 15))
        stats = f"CARS: {len(self.other_cars)+1}  |  OCCUPIED: {self.sc_area_occ} m²  |  FREE: {self.sc_area_free} m²"
        screen.blit(font_stats.render(stats, True, COLOR_TARGET), (30, 70))

        if self.finished:
            # الكلمة المطلوبة: نجحت في الركنة لوحدها
            msg = font_msg.render("AUTO-PARKING SUCCESSFUL!", True, (46, 204, 113))
            rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
            pygame.draw.rect(screen, (255,255,255, 230), (rect.x-15, rect.y-10, rect.width+30, rect.height+20), border_radius=12)
            screen.blit(msg, rect)

def main():
    sim = ParkingSystem()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: sim = ParkingSystem()
        sim.update(); sim.draw(); pygame.display.flip(); clock.tick(60)

if __name__ == "__main__":
    main()