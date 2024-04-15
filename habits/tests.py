from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email="test@test.ru",
            is_staff=True,
            is_active=True,
            is_superuser=False
        )
        self.user.set_password('test_user')
        self.user.save()

        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            place='test_place',
            action='test_action',
            owner=self.user
        )

    def test_create_habit(self):
        """Тестирование создания привычек"""

        data = {
            'place': 'test_create',
            'action': 'test_create',
            'owner': self.user.pk
        }

        response = self.client.post('/habits/create/', data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Habit.objects.all().count(), 2)

    def test_list_habit(self):
        """Тестирование вывода списка привычек"""

        response = self.client.get('/habits/')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results':
                    [
                        {
                            'id': self.habit.id,
                            'place': 'test_place',
                            'time': self.habit.time,
                            'date': self.habit.date,
                            'action': 'test_action',
                            'is_pleasant': self.habit.is_pleasant,
                            'reward': self.habit.reward,
                            'duration': self.habit.duration,
                            'periodicity': self.habit.periodicity,
                            'is_public': self.habit.is_public,
                            'owner': self.user.pk,
                            'related_habit': self.habit.related_habit
                        }
                    ]
            }
        )

    def test_update_habit(self):
        """Тестирование изменения привычки"""

        change_data = {
            'place': 'place_update',
            'action': 'action_update'
        }
        response = self.client.patch(f'/habits/update/{self.habit.id}/', data=change_data)
        self.maxDiff = None

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json(),
            {
                'id': self.habit.id,
                'place': 'place_update',
                'time': self.habit.time,
                'date': self.habit.date,
                'action': 'action_update',
                'is_pleasant': self.habit.is_pleasant,
                'reward': self.habit.reward,
                'duration': self.habit.duration,
                'periodicity': self.habit.periodicity,
                'is_public': self.habit.is_public,
                'owner': self.user.pk,
                'related_habit': self.habit.related_habit
            }
        )

    def test_duration_habit(self):
        """Тестирование создания привычки со временем исполнения более 2 минут"""

        data = {
            'place': 'test_place',
            'action': 'test_action',
            'duration': '130',
            'owner': self.user.pk,
        }
        response = self.client.post('/habits/create/', data=data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_habit(self):
        """Тестирование создания привычки с периодичностью менее одного раза в неделю"""

        data = {
            'place': 'test_place',
            'action': 'test_action',
            'periodicity': 8,
            'owner': self.user.pk
        }
        response = self.client.post('/habits/create/', data=data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reward_and_pleasant_habit(self):
        """Тестирование создания привычки с наградой и приятной привычкой одновременно"""

        data = {
            'place': 'test_place',
            'action': 'test_action',
            'reward': 'reward_test',
            'owner': self.user.pk,
            'related_habit': 1
        }
        response = self.client.post('/habits/create/', data=data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
