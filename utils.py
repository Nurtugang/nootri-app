def calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    """
    Вычисляет базальный уровень метаболизма (BMR) на основе пола, веса (кг), роста (см) и возраста (лет).
    Формула Миффлина-Сан Жеора:
    - Для мужчин: BMR = 88.36 + (13.4 * вес в кг) + (4.8 * рост в см) - (5.7 * возраст)
    - Для женщин: BMR = 447.6 + (9.2 * вес в кг) + (3.1 * рост в см) - (4.3 * возраст)
    """
    if gender.lower() == 'мужской':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    elif gender.lower() == 'женский':
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
    else:
        raise ValueError("Пол должен быть 'мужской' или 'женский'")
    return bmr

def calculate_calories(goal: str, bmr: float) -> float:
    """
    Рассчитывает рекомендуемое количество калорий на основе цели:
    - 'Сброс' (снижение веса): BMR * 0.8
    - 'Поддержание' (поддержание веса): BMR
    - 'Набор' (увеличение веса): BMR * 1.2
    """
    goal = goal.lower()
    if goal == 'сброс':
        return bmr * 0.8
    elif goal == 'поддержание':
        return bmr
    elif goal == 'набор':
        return bmr * 1.2
    else:
        raise ValueError("Цель должна быть 'Сброс', 'Поддержание' или 'Набор'")

def calculate_macros(calories: float, goal: str) -> dict:
    """
    Рассчитывает суточную норму макронутриентов на основе цели и общего количества калорий.
    Возвращает значения для белков, жиров и углеводов в граммах.
    """
    goal = goal.lower()
    if goal == 'сброс':
        protein_percentage = 0.4
        fat_percentage = 0.3
        carb_percentage = 0.3
    elif goal == 'поддержание':
        protein_percentage = 0.3
        fat_percentage = 0.3
        carb_percentage = 0.4
    elif goal == 'набор':
        protein_percentage = 0.25
        fat_percentage = 0.25
        carb_percentage = 0.5
    else:
        raise ValueError("Цель должна быть 'Сброс', 'Поддержание' или 'Набор'")

    protein_grams = (calories * protein_percentage) / 4
    fat_grams = (calories * fat_percentage) / 9
    carb_grams = (calories * carb_percentage) / 4

    return {
        'Белки (г)': round(protein_grams, 2),
        'Жиры (г)': round(fat_grams, 2),
        'Углеводы (г)': round(carb_grams, 2)
    }
