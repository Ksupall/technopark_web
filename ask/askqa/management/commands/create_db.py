from django.core.management.base import BaseCommand, CommandError
from askqa.models import *
from random import randint, choice
from faker import Faker


faker = Faker()

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0)
        parser.add_argument('--questions', type=int, default=0)

    def create_profiles(self):
        for i in range(50):
            s = faker.word()
            user = User.objects.create_user(s + str(i),
                                            s + '@mail.ru',
                                            'password')
            user.save()
            p = Profile.objects.create(user=user)
            p.rating = randint(-5, 20)
            p.save()

    def create_tags(self):
        for i in range(50):
            tag = Tag.objects.create(title=faker.word(), unique_index=i)
            tag.save()

    def create_questions(self):
        tags = Tag.objects.all()
        profiles = Profile.objects.all()
        for i in range(100):
            s = str(i)
            question = Question.objects.create(title=faker.sentence(),
                                               text=faker.text(),
                                               author=choice(profiles),
                                               rating=randint(-5, 10))
            tag_number = randint(1, 4)
            for j in range(tag_number):
                tag = choice(tags)
                question.tags.add(tag)
            question.save()

    def create_answers(self):
        profiles = Profile.objects.all()
        for question in Question.objects.all():
            answer_count = randint(1, 10)
            for i in range(answer_count):
                a = Answer.objects.create(text=faker.text(), question=question,
                                          author=choice(profiles))
                a.save()

    def create_likes_obj(self, obj, profiles):
        rating = obj.rating
        if rating:
            like_count = randint(abs(rating), 2 * abs(rating))
            sign = rating / abs(rating)
            opposite_max = like_count - abs(rating)
            i = 0
            k = 0
            if sign > 0:
                while i > -opposite_max:
                    Like.objects.create(content_object=obj, is_positive=False,
                                        author=profiles[k])
                    i -= 1
                    k += 1
                while i < rating:
                    Like.objects.create(content_object=obj, is_positive=True,
                                        author=profiles[k])
                    i += 1
                    k += 1
            else:
                while i < opposite_max:
                    Like.objects.create(content_object=obj, is_positive=True,
                                        author=profiles[k])
                    i += 1
                    k += 1
                while i > rating:
                    Like.objects.create(content_object=obj, is_positive=False,
                                        author=profiles[k])
                    i -= 1
                    k += 1

    def create_likes(self):
        profiles = Profile.objects.all()
        questions = Question.objects.all()
        answers = Answer.objects.all()
        for question in questions:
            self.create_likes_obj(question, profiles)
        for answer in answers:
            self.create_likes_obj(answer, profiles)

    def handle(self, *args, **options):
        self.create_profiles()
        self.create_tags()
        self.create_questions()
        self.create_answers()
        self.create_likes()
