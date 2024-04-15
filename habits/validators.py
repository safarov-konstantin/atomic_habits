from rest_framework.serializers import ValidationError


class RelateAndRewardValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)
        reward = dict(value).get(self.field2)

        if related_habit and reward:
            raise ValidationError('Нельзя использовать одновременно связанную привычку и вознаграждение')


class HabitRelatedHabitIsPleasantValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)
        is_pleasant = dict(value).get(self.field2)

        if related_habit and not is_pleasant:
            raise ValidationError('Связанной привычкой может быть только приятная привычка')


class HabitPleasantValidator:

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)
        reward = dict(value).get(self.field2)
        is_pleasant = dict(value).get(self.field3)

        if is_pleasant and reward and related_habit:
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')


class HabitTimeDurationValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = dict(value).get(self.field)

        if duration and duration > 120:
            raise ValidationError('Выполнение привычки не может превышать 120 секунд')


class CheckHabitValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = dict(value).get(self.field)

        if isinstance(periodicity, int) and (periodicity > 7 or periodicity < 1):
            raise ValidationError('Периодичность привычки не может быть больше 7 и меньше 1')
