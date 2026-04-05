# Космический Шутер - Space Shooter Game

## Структура проекта

```
/workspace/
├── windows_version/          # Версия для Windows
│   ├── space_shooter.py      # Основной файл игры
│   └── README.md             # Документация
│
└── linux_version/            # Версия для Linux
    ├── space_shooter.py      # Основной файл игры
    └── README.md             # Документация
```

## Описание

Космический шутер с:
- Красивой графикой (градиентный фон, анимированные звёзды)
- Звуковыми эффектами
- Системой сохранения прогресса (20 значений)
- Лучшим счётом, который сохраняется между запусками

## Особенности по версиям

### Windows Version
- Сохранение данных в реестр Windows: `HKEY_CURRENT_USER\Software\SpaceShooter`
- Использование winsound для звуковых эффектов
- 20 сохраняемых значений включая BestScore

### Linux Version  
- Сохранение данных в файл: `~/.config/spaceshooter/settings.ini`
- Процедурная генерация звуков через pygame.sndarray
- 20 сохраняемых значений включая BestScore

## Запуск

### Windows
```bash
cd windows_version
pip install pygame
python space_shooter.py
```

### Linux
```bash
cd linux_version
pip install pygame
python space_shooter.py
```

## Управление
- **Стрелки** - Перемещение
- **Пробел** - Стрельба
- **ESC** - Пауза
- **R** - Рестарт
