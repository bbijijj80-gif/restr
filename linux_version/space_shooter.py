"""
Космический шутер - Версия для Linux
Игра с сохранением 20 значений в файле конфигурации ~/.config/spaceshooter/settings.ini
Включая лучший счёт, который сохраняется между запусками
"""

import pygame
import random
import math
import os
import sys
import configparser
from pathlib import Path

# Инициализация Pygame
pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass  # Звук может быть недоступен в некоторых средах

# Константы экрана
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический Шутер - Linux Edition")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Путь к файлу конфигурации
CONFIG_DIR = Path.home() / ".config" / "spaceshooter"
CONFIG_FILE = CONFIG_DIR / "settings.ini"

# 20 значений для сохранения
REG_VALUE_NAMES = [
    "BestScore",
    "TotalGamesPlayed",
    "TotalEnemiesDestroyed",
    "TotalShotsFired",
    "PlayTimeSeconds",
    "MaxLevelReached",
    "PowerUpsCollected",
    "DamageTaken",
    "BossesDefeated",
    "ComboMax",
    "AccuracyPercent",
    "LivesRemaining",
    "BonusPoints",
    "SecretFound",
    "AchievementsUnlocked",
    "LastPlayedDate",
    "PlayerName",
    "DifficultyLevel",
    "SoundEnabled",
    "GraphicsQuality"
]

class ConfigManager:
    """Менеджер для работы с конфигурационным файлом (аналог реестра для Linux)"""
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.values = {}
        self.config_path = CONFIG_FILE
        self.load_from_file()
    
    def load_from_file(self):
        """Загрузка всех 20 значений из файла конфигурации"""
        # Создаём директорию если не существует
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        if self.config_path.exists():
            self.config.read(self.config_path)
        
        if 'GameData' not in self.config:
            self.config['GameData'] = {}
        
        # Чтение всех значений
        for name in REG_VALUE_NAMES:
            if name in self.config['GameData']:
                value = self.config['GameData'][name]
                # Попытка преобразовать в число
                try:
                    if '.' in value:
                        self.values[name] = float(value)
                    else:
                        self.values[name] = int(value)
                except ValueError:
                    self.values[name] = value
            else:
                self.values[name] = 0
        
        # Инициализация отсутствующих значений
        self._initialize_missing_values()
    
    def _initialize_missing_values(self):
        """Инициализация отсутствующих значений по умолчанию"""
        defaults = {
            "BestScore": self.values.get("BestScore", 0),
            "TotalGamesPlayed": self.values.get("TotalGamesPlayed", 0),
            "TotalEnemiesDestroyed": self.values.get("TotalEnemiesDestroyed", 0),
            "TotalShotsFired": self.values.get("TotalShotsFired", 0),
            "PlayTimeSeconds": self.values.get("PlayTimeSeconds", 0),
            "MaxLevelReached": self.values.get("MaxLevelReached", 1),
            "PowerUpsCollected": self.values.get("PowerUpsCollected", 0),
            "DamageTaken": self.values.get("DamageTaken", 0),
            "BossesDefeated": self.values.get("BossesDefeated", 0),
            "ComboMax": self.values.get("ComboMax", 0),
            "AccuracyPercent": self.values.get("AccuracyPercent", 100.0),
            "LivesRemaining": self.values.get("LivesRemaining", 3),
            "BonusPoints": self.values.get("BonusPoints", 0),
            "SecretFound": self.values.get("SecretFound", 0),
            "AchievementsUnlocked": self.values.get("AchievementsUnlocked", 0),
            "LastPlayedDate": self.values.get("LastPlayedDate", ""),
            "PlayerName": self.values.get("PlayerName", "Player"),
            "DifficultyLevel": self.values.get("DifficultyLevel", 1),
            "SoundEnabled": self.values.get("SoundEnabled", 1),
            "GraphicsQuality": self.values.get("GraphicsQuality", 1)
        }
        
        for key, value in defaults.items():
            if key not in self.values:
                self.values[key] = value
    
    def save_to_file(self):
        """Сохранение всех 20 значений в файл конфигурации"""
        try:
            # Создаём директорию если не существует
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            if 'GameData' not in self.config:
                self.config['GameData'] = {}
            
            for name, value in self.values.items():
                if isinstance(value, (int, float)):
                    self.config['GameData'][name] = str(value)
                elif isinstance(value, str):
                    self.config['GameData'][name] = value
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
                
        except Exception as e:
            print(f"Ошибка сохранения в файл: {e}")
    
    def get_value(self, name):
        return self.values.get(name, 0)
    
    def set_value(self, name, value):
        self.values[name] = value
    
    def increment_value(self, name, amount=1):
        current = self.get_value(name)
        if isinstance(current, (int, float)):
            self.set_value(name, current + amount)


class Star:
    """Класс для звёзд на фоне"""
    def __init__(self):
        self.reset()
        self.y = random.randint(0, HEIGHT)
    
    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = 0
        self.speed = random.uniform(1, 4)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(150, 255)
    
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()
    
    def draw(self, surface):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class Player(pygame.sprite.Sprite):
    """Игрок"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        self._draw_ship()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 7
        self.lives = 3
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()
    
    def _draw_ship(self):
        """Рисование космического корабля"""
        points = [(30, 0), (0, 80), (30, 60), (60, 80)]
        pygame.draw.polygon(self.image, CYAN, points)
        pygame.draw.polygon(self.image, WHITE, points, 2)
        
        # Двигатель
        pygame.draw.circle(self.image, ORANGE, (30, 75), 8)
        pygame.draw.circle(self.image, YELLOW, (30, 75), 4)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
    
    def shoot(self, config):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            config.increment_value("TotalShotsFired")
            return Bullet(self.rect.centerx, self.rect.top)
        return None


class Enemy(pygame.sprite.Sprite):
    """Враг"""
    def __init__(self, difficulty=1):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self._draw_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.uniform(2, 4) + difficulty * 0.5
        self.speed_x = random.uniform(-1, 1)
        self.health = 1 + difficulty // 2
    
    def _draw_enemy(self):
        """Рисование врага"""
        pygame.draw.circle(self.image, RED, (25, 25), 20)
        pygame.draw.circle(self.image, DARK_RED := (100, 0, 0), (25, 25), 20, 3)
        # Глаза
        pygame.draw.circle(self.image, YELLOW, (18, 20), 5)
        pygame.draw.circle(self.image, YELLOW, (32, 20), 5)
        pygame.draw.circle(self.image, BLACK, (18, 20), 2)
        pygame.draw.circle(self.image, BLACK, (32, 20), 2)
    
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        
        if self.rect.top > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """Пуля"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, YELLOW, (0, 0, 6, 20))
        pygame.draw.rect(self.image, WHITE, (2, 0, 2, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -12
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    """Бонус"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (15, 15), 15)
        pygame.draw.circle(self.image, WHITE, (15, 15), 15, 2)
        font = pygame.font.Font(None, 24)
        text = font.render("+", True, BLACK)
        self.image.blit(text, (10, 8))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-50, -30)
        self.speed = 3
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """Взрыв"""
    def __init__(self, center):
        super().__init__()
        self.frame = 0
        self.images = []
        for i in range(8):
            img = pygame.Surface((60, 60), pygame.SRCALPHA)
            radius = 10 + i * 5
            alpha = 255 - i * 30
            color = (*ORANGE[:3], alpha)
            pygame.draw.circle(img, color, (30, 30), radius)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.animation_speed = 3
    
    def update(self):
        self.frame += 1
        if self.frame >= len(self.images) * self.animation_speed:
            self.kill()
        else:
            self.image = self.images[self.frame // self.animation_speed]


class Game:
    """Основной класс игры"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.score = 0
        self.level = 1
        self.combo = 0
        self.max_combo = 0
        self.game_over = False
        self.paused = False
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 1500
        
        self.stars = [Star() for _ in range(150)]
        
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        self.start_time = pygame.time.get_ticks()
        
        self.config.set_value("LastPlayedDate", pygame.time.get_ticks())
        self.config.increment_value("TotalGamesPlayed")
        
        self.sound_enabled = self.config.get_value("SoundEnabled")
        
        # Инициализация звуков
        self._init_sounds()
    
    def _init_sounds(self):
        """Инициализация звуковых эффектов"""
        try:
            # Создаём простые звуковые эффекты
            sample_rate = 44100
            
            # Звук выстрела
            shoot_samples = []
            for i in range(int(sample_rate * 0.1)):
                t = i / sample_rate
                value = int(10000 * math.sin(2 * math.pi * 800 * t) * (1 - t / 0.1))
                shoot_samples.append(value)
            self.shoot_sound = pygame.sndarray.make_sound(
                pygame.surfarray.array2d(pygame.Surface((len(shoot_samples), 1), dtype=pygame.int16))
            )
            
            # Звук взрыва
            explosion_samples = []
            for i in range(int(sample_rate * 0.2)):
                t = i / sample_rate
                value = int(15000 * random.uniform(-1, 1) * (1 - t / 0.2))
                explosion_samples.append(value)
            self.explosion_sound = pygame.sndarray.make_sound(
                pygame.surfarray.array2d(pygame.Surface((len(explosion_samples), 1), dtype=pygame.int16))
            )
            
            # Звук бонуса
            bonus_samples = []
            for i in range(int(sample_rate * 0.15)):
                t = i / sample_rate
                value = int(8000 * math.sin(2 * math.pi * 600 * t) * (1 - t / 0.15))
                bonus_samples.append(value)
            self.bonus_sound = pygame.sndarray.make_sound(
                pygame.surfarray.array2d(pygame.Surface((len(bonus_samples), 1), dtype=pygame.int16))
            )
            
            # Звук повреждения
            damage_samples = []
            for i in range(int(sample_rate * 0.3)):
                t = i / sample_rate
                value = int(12000 * math.sin(2 * math.pi * 200 * t) * (1 - t / 0.3))
                damage_samples.append(value)
            self.damage_sound = pygame.sndarray.make_sound(
                pygame.surfarray.array2d(pygame.Surface((len(damage_samples), 1), dtype=pygame.int16))
            )
            
        except Exception as e:
            print(f"Предупреждение: Не удалось создать звуки: {e}")
            self.sound_enabled = False
    
    def spawn_enemy(self):
        if len(self.enemies) < 5 + self.level:
            enemy = Enemy(self.level)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
    
    def spawn_powerup(self):
        if random.random() < 0.02:
            powerup = PowerUp()
            self.all_sprites.add(powerup)
            self.powerups.add(powerup)
    
    def play_sound(self, sound_type):
        """Воспроизведение звука"""
        if not self.sound_enabled:
            return
        
        try:
            if sound_type == "shoot" and hasattr(self, 'shoot_sound'):
                self.shoot_sound.play()
            elif sound_type == "explosion" and hasattr(self, 'explosion_sound'):
                self.explosion_sound.play()
            elif sound_type == "bonus" and hasattr(self, 'bonus_sound'):
                self.bonus_sound.play()
            elif sound_type == "damage" and hasattr(self, 'damage_sound'):
                self.damage_sound.play()
        except Exception as e:
            pass
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()
        
        return True
    
    def update(self):
        if self.paused or self.game_over:
            return
        
        current_time = pygame.time.get_ticks()
        play_time = (current_time - self.start_time) / 1000
        self.config.set_value("PlayTimeSeconds", int(play_time))
        
        for star in self.stars:
            star.update()
        
        self.player.update()
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = self.player.shoot(self.config)
            if bullet:
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                self.play_sound("shoot")
        
        if current_time - self.enemy_spawn_timer > self.enemy_spawn_interval:
            self.spawn_enemy()
            self.spawn_powerup()
            self.enemy_spawn_timer = current_time
            self.enemy_spawn_interval = max(500, 1500 - self.level * 100)
        
        self.bullets.update()
        self.enemies.update()
        self.powerups.update()
        self.explosions.update()
        
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 10 * self.level
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            self.config.increment_value("TotalEnemiesDestroyed")
            explosion = Explosion(hit.rect.center)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            self.play_sound("explosion")
            
            if self.score % 100 == 0:
                self.level += 1
                self.config.set_value("MaxLevelReached", self.level)
        
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.player.lives -= 1
            self.combo = 0
            self.config.increment_value("DamageTaken")
            explosion = Explosion(hit.rect.center)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            self.play_sound("damage")
            
            if self.player.lives <= 0:
                self.game_over = True
                self.handle_game_over()
        
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            self.player.lives = min(5, self.player.lives + 1)
            self.score += 50
            self.config.increment_value("PowerUpsCollected")
            self.play_sound("bonus")
        
        self.config.set_value("LivesRemaining", self.player.lives)
        self.config.set_value("ComboMax", self.max_combo)
    
    def handle_game_over(self):
        """Обработка конца игры"""
        best_score = self.config.get_value("BestScore")
        if self.score > best_score:
            self.config.set_value("BestScore", self.score)
        
        self.config.set_value("BonusPoints", self.score // 10)
        self.config.save_to_file()
    
    def draw_background(self):
        """Рисование фона"""
        gradient_surface = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            color = (
                int(10 * ratio),
                int(10 * ratio),
                int(50 + 50 * ratio)
            )
            pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))
        screen.blit(gradient_surface, (0, 0))
        
        for star in self.stars:
            star.draw(screen)
    
    def draw_ui(self):
        """Рисование интерфейса"""
        score_text = self.font_small.render(f"Счёт: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        lives_text = self.font_small.render(f"Жизни: {self.player.lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))
        
        level_text = self.font_small.render(f"Уровень: {self.level}", True, WHITE)
        screen.blit(level_text, (10, 90))
        
        combo_text = self.font_small.render(f"Комбо: {self.combo}", True, YELLOW)
        screen.blit(combo_text, (10, 130))
        
        best_score = self.config.get_value("BestScore")
        best_text = self.font_small.render(f"Лучший: {best_score}", True, GREEN)
        screen.blit(best_text, (WIDTH - 200, 10))
    
    def draw_game_over(self):
        """Рисование экрана конца игры"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(game_over_text, text_rect)
        
        score_text = self.font_medium.render(f"Ваш счёт: {self.score}", True, WHITE)
        text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(score_text, text_rect)
        
        best_score = self.config.get_value("BestScore")
        best_text = self.font_medium.render(f"Лучший счёт: {best_score}", True, GREEN)
        text_rect = best_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(best_text, text_rect)
        
        restart_text = self.font_small.render("Нажмите R для рестарта", True, WHITE)
        text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(restart_text, text_rect)
    
    def draw_paused(self):
        """Рисование паузы"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        
        paused_text = self.font_large.render("ПАУЗА", True, WHITE)
        text_rect = paused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(paused_text, text_rect)
        
        continue_text = self.font_small.render("Нажмите ESC для продолжения", True, WHITE)
        text_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(continue_text, text_rect)
    
    def draw(self):
        self.draw_background()
        self.all_sprites.draw(screen)
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_paused()
        
        pygame.display.flip()
    
    def run(self):
        """Главный цикл игры"""
        running = True
        while running:
            clock.tick(60)
            running = self.handle_events()
            self.update()
            self.draw()
        
        self.config.save_to_file()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
