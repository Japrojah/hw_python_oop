from typing import Dict, Type
from dataclasses import dataclass


@dataclass(init=True)
class InfoMessage:
    """Информационное сообщение о тренировке.
    определяет атрибуты такие как:
    training_type: str - тип тренировки,
    duration: float - длительность тренировки в часах,
    distance: float - расстояние преодолённое за тренировку в км.,
    speed: float - средняя скорость в км/ч,
    calories: float - колличество затраченных каллорий."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Функция выводит информационное сообщение о тренировке.
        возвращает f-строку с данными типа str,
        Атрибуты функции: training_type: str, duration: float,
        distance: float, speed: float, calories: float."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки.
    определяет константы: LEN_STEP: float - расстояние,
    преодолеваемое за один шаг(в метрах), M_IN_KM: int -
    коэффициент перевода метров в км., MIN_IN_H: int -
    коэффициент перевода часов в минуты, CM_IN_M: int -
    коэффициент перевода сантиметров в метры."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """Определяет атрибуты Базового класса, такие как:
        action: int - кол-во совершенных действий(шагов/гребков),
        duration: float - длительность тренировки в формате часа,
        weight: float - вес пользователя в килограммах."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км.
        возвращает данные типа float,
        Атрибуты: action: int,
        константы LEN_STEP: float, M_IN_KM: int"""
        return ((self.action * self.LEN_STEP) / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
        Возвращает данные типа float,
        Атрибуты: get_distance() -> float,
        duration: float"""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Возвращает данные типа float"""
        pass

    def training_duration_in_min(self) -> float:
        """После замены операци умножения на эту формулу в функциях
        pytest выдаёт ошибки в результатах - триллиардные и миллионные доли
        числа в ответе считались неправильно.
        эти проблемы возникали и раньше, но мне удалось решить
        их путём двухдневного поиска ответов в обсуждениях чата project, и
        обращения за помощью к наставникам. В один момент я просто наудачу
        скопировал кусок кода который в обсуждении написал наставник
        (код на вид вообще не отличался от моего, ни знаком, ни скобкой)
        для функции get_spent_calories и это каким-то чудом помогло,
        триллиардная доля числа посчиталась. Если это не критично,
        ради бога, давайте оставим так"""
        return (self.duration * self.MIN_IN_H)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке.
        Возвращает объект класса InfoMessage.
        Атрибуты функции: __clas__.__name__: str,
        duration: float, данные от функций get_distance() -> float,
        get_mean_speed() -> float, get_spent_calories() -> float."""
        return (InfoMessage(self.__class__.__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79

    def get_spent_calories(self) -> float:
        """Вычисляет кол-во затраченных клорий,
        возвращает данные типа float"""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    Определяет новые константы, такие как:
    CALORIES_WEIGHT_MULTIPLIER: float,
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float.
    KMH_IN_MSEC: float - коэффициент перевода из км/ч в м/сек
    CM_IN_M: int - для перевода сантиметров в метры."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """Переопределяет атрибуты родительского класса.
        А именно: self.height: float - рост пользователя в сантиметрах"""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Возвращает данные типа float
        Атрибуты метода: CALORIES_WEIGHT_MULTIPLIER: float,
        CALORIES_SPEED_HEIGHT_MULTIPLIER: float
        self.weight: float, height: float, duration: float,
        KMH_IN_MSEC: float, CM_IN_M: int, MIN_IN_H: int,
        вызывает функцию get_mean_speed() -> float."""

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                    / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание.
    Переопределяет константу: LEN_STEP: float = 1.38 -
    расстояние, которое проходит пользователь за один гребок
    константы: CALORIES_MEAN_SPEED_SHIFT: float и
    CALORIES_WEIGHT_MULTIPLIER: float нужны для функции подсчета каллорий."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        """Переопределяет атрибуты родительского класса,
        конкретно length_pool: float - длинна бассейна в метрах,
        count_pool: float - кол-во раз как пользователь переплыл бассейн."""
        super().__init__(action,
                         duration,
                         weight
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределяет функцию родительского класса,
        возвращает среднюю скорость в км/ч(данные типа float).
        В процессе вычислания исползует атрибуты:
        self.duration, self.M_IN_KM(константа родительского класса),
        self.count_pool и self.length_pool."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Переопределяет функцию подсчёта каллорий
        родительского класса.
        В вычислениях использует константы определённые в классе -
        такие как CALORIES_MEAN_SPEED_SHIFT: float,
        CALORIES_WEIGHT_MULTIPLIER: float,
        Также атрибуты weight: float и duration: float
        И вызывает функцию get_mean_speed()
        Возвращает данные типа float, а именно:
        затраченные каллории."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков.
    Принимает workout_type: str с буквенными кодами тренировок
    И data:list с данными этих тренировок
    Имеет словарь с классами тренировок, которые вызывает
    для создения объектов
    Объекты классов возвращает в функцию main()."""
    workout_type_dict: Dict[str, Type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking
    }
    try:
        return (workout_type_dict[workout_type](*data))
    except KeyError:
        raise KeyError(f'Тренировка {workout_type} не найдена.')


def main(training: Training) -> None:
    """Главная функция.
    Получает объект класса зависящий от кода треннировки
    Вызывает функцию, возвращающую объект класса InfoMessage,
    и после применения функции создания информационного сообщения
    выводит сообщение в консоль."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
