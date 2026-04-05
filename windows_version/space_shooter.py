"""
Космический шутер - Версия для Windows
Игра с сохранением 20 значений в реестре Windows
Включая лучший счёт, который сохраняется между запусками
"""

import pygame
import random
import math
import os
import sys

# Инициализация Pygame
pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass  # Звук может быть недоступен в некоторых средах

# Константы экрана
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический Шутер - Windows Edition")
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

# Реестр ключ
REG_KEY_PATH = "Software\\SpaceShooter"
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

# Проверка платформы и импорт модулей Windows
IS_WINDOWS = sys.platform == 'win32'
if IS_WINDOWS:
    import winsound
    import winreg
else:
    # Заглушки для не-Windows платформ (для тестирования)
    winsound = None
    winreg = None


class RegistryManager:
    """Менеджер для работы с реестром Windows"""
    
    def __init__(self):
        self.key_path = REG_KEY_PATH
        self.values = {}
        self.load_from_registry()
    
    def load_from_registry(self):
        """Загрузка всех 20 значений из реестра"""
        if not IS_WINDOWS or winreg is None:
            self._initialize_missing_values()
            return
            
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ)
            
            # Читаем каждое значение по имени
            for name in REG_VALUE_NAMES:
                try:
                    value, type_ = winreg.QueryValueEx(key, name)
                    # Преобразуем значение в нужный тип
                    if name == "BestScore":
                        self.values[name] = int(value) if value else 0
                    elif name in ["AccuracyPercent"]:
                        self.values[name] = float(value) if value else 100.0
                    elif name in ["LastPlayedDate", "PlayerName"]:
                        self.values[name] = str(value) if value else ""
                    else:
                        self.values[name] = int(value) if value else 0
                except OSError:
                    # Значение не найдено, будет инициализировано позже
                    pass
                except Exception as e:
                    print(f"Ошибка чтения значения {name}: {e}")
                    pass
            
            winreg.CloseKey(key)
            
            # Инициализация отсутствующих значений
            self._initialize_missing_values()
            
            # Отладка: выводим загруженные значения
            print(f"Загружено BestScore из реестра: {self.values.get('BestScore', 'не найдено')}")
            
        except FileNotFoundError:
            # Ключ не существует, создаём его
            print("Ключ реестра не найден, создаём новый")
            self._create_registry_key()
            self._initialize_missing_values()
        except Exception as e:
            print(f"Ошибка загрузки из реестра: {e}")
            self._initialize_missing_values()
    
    def _create_registry_key(self):
        """Создание ключа реестра"""
        if not IS_WINDOWS or winreg is None:
            return
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.key_path)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Ошибка создания ключа реестра: {e}")
    
    def _initialize_missing_values(self):
        """Инициализация отсутствующих значений по умолчанию"""
        # Инициализируем только те значения, которых ещё нет в self.values
        if "BestScore" not in self.values:
            self.values["BestScore"] = 0
        if "TotalGamesPlayed" not in self.values:
            self.values["TotalGamesPlayed"] = 0
        if "TotalEnemiesDestroyed" not in self.values:
            self.values["TotalEnemiesDestroyed"] = 0
        if "TotalShotsFired" not in self.values:
            self.values["TotalShotsFired"] = 0
        if "PlayTimeSeconds" not in self.values:
            self.values["PlayTimeSeconds"] = 0
        if "MaxLevelReached" not in self.values:
            self.values["MaxLevelReached"] = 1
        if "PowerUpsCollected" not in self.values:
            self.values["PowerUpsCollected"] = 0
        if "DamageTaken" not in self.values:
            self.values["DamageTaken"] = 0
        if "BossesDefeated" not in self.values:
            self.values["BossesDefeated"] = 0
        if "ComboMax" not in self.values:
            self.values["ComboMax"] = 0
        if "AccuracyPercent" not in self.values:
            self.values["AccuracyPercent"] = 100.0
        if "LivesRemaining" not in self.values:
            self.values["LivesRemaining"] = 3
        if "BonusPoints" not in self.values:
            self.values["BonusPoints"] = 0
        if "SecretFound" not in self.values:
            self.values["SecretFound"] = 0
        if "AchievementsUnlocked" not in self.values:
            self.values["AchievementsUnlocked"] = 0
        if "LastPlayedDate" not in self.values:
            self.values["LastPlayedDate"] = ""
        if "PlayerName" not in self.values:
            self.values["PlayerName"] = "Player"
        if "DifficultyLevel" not in self.values:
            self.values["DifficultyLevel"] = 1
        if "SoundEnabled" not in self.values:
            self.values["SoundEnabled"] = 1
        if "GraphicsQuality" not in self.values:
            self.values["GraphicsQuality"] = 1
    
    def save_to_registry(self):
        """Сохранение всех 20 значений в реестр"""
        if not IS_WINDOWS or winreg is None:
            return
            
        try:
            # Сначала создаём ключ если его нет
            self._create_registry_key()
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
            
            for name, value in self.values.items():
                try:
                    if isinstance(value, int):
                        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                    elif isinstance(value, float):
                        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))
                    elif isinstance(value, str):
                        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
                except Exception as e:
                    print(f"Ошибка сохранения значения {name}: {e}")
            
            winreg.CloseKey(key)
            print("Значения успешно сохранены в реестр")
        except Exception as e:
            print(f"Ошибка сохранения в реестр: {e}")
    
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
    
    def shoot(self, registry):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            registry.increment_value("TotalShotsFired")
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
        self.registry = RegistryManager()
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
        
        self.registry.set_value("LastPlayedDate", pygame.time.get_ticks())
        self.registry.increment_value("TotalGamesPlayed")
        
        self.sound_enabled = self.registry.get_value("SoundEnabled")
    
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
    
    def play_sound(self, frequency, duration, volume=10000):
        """Воспроизведение звука"""
        if not self.sound_enabled or winsound is None:
            return
        try:
            winsound.Beep(frequency, duration)
        except:
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
        self.registry.set_value("PlayTimeSeconds", int(play_time))
        
        for star in self.stars:
            star.update()
        
        self.player.update()
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = self.player.shoot(self.registry)
            if bullet:
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                self.play_sound(800, 50, 5000)
        
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
            self.registry.increment_value("TotalEnemiesDestroyed")
            explosion = Explosion(hit.rect.center)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            self.play_sound(400, 100, 8000)
            
            if self.score % 100 == 0:
                self.level += 1
                self.registry.set_value("MaxLevelReached", self.level)
        
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.player.lives -= 1
            self.combo = 0
            self.registry.increment_value("DamageTaken")
            explosion = Explosion(hit.rect.center)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            self.play_sound(200, 300, 10000)
            
            if self.player.lives <= 0:
                self.game_over = True
                self.handle_game_over()
        
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            self.player.lives = min(5, self.player.lives + 1)
            self.score += 50
            self.registry.increment_value("PowerUpsCollected")
            self.play_sound(600, 150, 7000)
        
        self.registry.set_value("LivesRemaining", self.player.lives)
        self.registry.set_value("ComboMax", self.max_combo)
    
    def handle_game_over(self):
        """Обработка конца игры"""
        best_score = self.registry.get_value("BestScore")
        print(f"Текущий счёт: {self.score}, Лучший счёт из реестра: {best_score}")
        
        if self.score > best_score:
            self.registry.set_value("BestScore", self.score)
            print(f"Новый лучший счёт: {self.score}")
        
        self.registry.set_value("BonusPoints", self.score // 10)
        self.registry.save_to_registry()
    
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
        
        best_score = self.registry.get_value("BestScore")
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
        
        best_score = self.registry.get_value("BestScore")
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
        
        self.registry.save_to_registry()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
