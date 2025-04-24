from django.core.management.base import BaseCommand
from octofit_tracker.models import AppUser, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Conectar a MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Eliminar colecciones existentes
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Crear usuarios
        users = [
            AppUser(_id=ObjectId(), username='thundergod', email='thundergod@merington.edu', password='thundergodpassword'),
            AppUser(_id=ObjectId(), username='metalgeek', email='metalgeek@merington.edu', password='metalgeekpassword'),
            AppUser(_id=ObjectId(), username='zerocool', email='zerocool@merington.edu', password='zerocoolpassword'),
            AppUser(_id=ObjectId(), username='crashoverride', email='crashoverride@merington.edu', password='crashoverridepassword'),
            AppUser(_id=ObjectId(), username='sleeptoken', email='sleeptoken@merington.edu', password='sleeptokenpassword'),
        ]
        AppUser.objects.bulk_create(users)

        # Crear equipos
        blue_team = Team(_id=ObjectId(), name='Blue Team')
        gold_team = Team(_id=ObjectId(), name='Gold Team')
        blue_team.save()
        gold_team.save()
        for user in users[:3]:
            blue_team.members.add(user)
        for user in users[3:]:
            gold_team.members.add(user)

        # Crear actividades
        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
            Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
            Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)

        # Crear entradas de leaderboard
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=users[0], score=100),
            Leaderboard(_id=ObjectId(), user=users[1], score=90),
            Leaderboard(_id=ObjectId(), user=users[2], score=95),
            Leaderboard(_id=ObjectId(), user=users[3], score=85),
            Leaderboard(_id=ObjectId(), user=users[4], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Crear entrenamientos
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Base de datos de octofit_db poblada con datos de prueba.'))
