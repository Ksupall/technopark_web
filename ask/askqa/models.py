from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ProfileManager(models.Manager):
    def best(self):
        return self.all()[:5]

    def is_email_taken(self, mail):
        return User.objects.filter(email=mail).count()

    def is_name_taken(self, name):
        return User.objects.filter(username=name).count()

    def is_exist(self, name, email):
        if self.is_email_taken(email):
            return True
        return self.is_name_taken(name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='uploads', default='askqa/static/img/test.jpg')

    def __str__(self):
        return self.user.username

    def new_name(self, new_name):
        if Profile.objects.is_name_taken(new_name):
            return False
        self.user.username = new_name
        self.user.save()
        return True

    def new_email(self, new_email):
        if Profile.objects.is_email_taken(new_email):
            return False
        self.user.email = new_email
        self.user.save()
        return True

    objects = ProfileManager()


class TagManager(models.Manager):
    def popular(self):
        return self.all()[:5]
    
    def add_tags(self, tags):
        ids = []
        for tag in tags:
            if self.filter(title=tag).count() == 0:
                ids.append(self.all().count())
                self.create(title=tag, unique_index=self.all().count())
        return ids


class Tag(models.Model):
    title = models.CharField(max_length=20)
    unique_index = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    objects = TagManager()


class QuestionManager(models.Manager):
    def newest(self):
        return self.order_by('-created')

    def hottest(self):
        return self.order_by('-rating')
    
    def tagged(self, tag):
        return self.filter(tags__title=tag)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = QuestionManager()
    
    def __str__(self):
        return self.title

    def add_tags(self, tags):
        for tag in tags:
            self.tags.add(Tag.objects.filter(unique_index=tag))

    def like(self, profile, is_pos):
        if Like.objects.filter(author=profile, content_object=self) == 0:
            Like.objects.add(author=profile, content_object=self,
                             is_positive=is_pos)
            if is_pos:
                self.rating += 1
            else:
                self.rating -= 1


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.question.title

    def like(self, profile, is_pos):
        if Like.objects.filter(author=profile, content_object=self) == 0:
            Like.objects.add(author=profile, content_object=self,
                             is_positive=is_pos)
            if is_pos:
                self.rating += 1
            else:
                self.rating -= 1


class Like(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_positive = models.BooleanField(default=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author)
