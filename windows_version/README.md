# Космический Шутер - Версия для Windows

## Описание
Космический шутер с сохранением прогресса в реестре Windows (HKCU\Software\SpaceShooter).

## Требования
- Python 3.8+
- pygame
- Windows OS

## Установка зависимостей
```bash
pip install pygame
```

## Запуск игры
```bash
python space_shooter.py
```

## Управление
- **Стрелки** - Перемещение корабля
- **Пробел** - Стрельба
- **ESC** - Пауза
- **R** - Рестарт (после Game Over)

## Сохранение данных
Игра сохраняет 20 значений в реестре Windows по пути:
`HKEY_CURRENT_USER\Software\SpaceShooter`

### Список сохраняемых значений:
1. BestScore - Лучший счёт
2. TotalGamesPlayed - Всего сыграно игр
3. TotalEnemiesDestroyed - Всего уничтожено врагов
4. TotalShotsFired - Всего выпущено пуль
5. PlayTimeSeconds - Время игры (секунды)
6. MaxLevelReached - Максимальный уровень
7. PowerUpsCollected - Собрано бонусов
8. DamageTaken - Получено урона
9. BossesDefeated - Побеждено боссов
10. ComboMax - Максимальное комбо
11. AccuracyPercent - Точность (%)
12. LivesRemaining - Осталось жизней
13. BonusPoints - Бонусные очки
14. SecretFound - Найдено секретов
15. AchievementsUnlocked - Открыто достижений
16. LastPlayedDate - Дата последнего запуска
17. PlayerName - Имя игрока
18. DifficultyLevel - Уровень сложности
19. SoundEnabled - Звук включён
20. GraphicsQuality - Качество графики

## Особенности
- Красивый анимированный фон со звёздами
- Градиентный космический фон
- Звуковые эффекты (выстрелы, взрывы, бонусы)
- Система комбо
- Прогрессирующая сложность
- Сохранение лучшего счёта между запусками
