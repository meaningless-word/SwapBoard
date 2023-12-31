from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Sum
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой публикации автора
        post_rating = 0
        if self.post_set.exists():
            post_rating_sum = self.post_set.aggregate(pr=Sum('rating'))
        post_rating += post_rating_sum.get('pr')

    def __str__(self):
        return f'{self.user.username} [{self.rating}]'


class Post(models.Model):
    linkedAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)

    TANKS = "T"
    HEALERS = "H"
    DD = "D"
    SELLERS = "S"
    GUILD_MASTERS = "G"
    QUEST_GIVERS = "Q"
    BLACKSMITHS = "B"
    TANNERS = "T"
    POTION_MASTERS = "P"
    CAST_SPELLERS = "C"
    NO_ONE = "N"
    CATEGORY_CHOICES = (
        (TANKS, 'Танки'),
        (HEALERS, 'Хилы'),
        (DD, 'ДД'),
        (SELLERS, 'Торговцы'),
        (GUILD_MASTERS, 'Гилдмастеры'),
        (QUEST_GIVERS, 'Квестгиверы'),
        (BLACKSMITHS, 'Кузнецы'),
        (TANNERS, 'Кожевники'),
        (POTION_MASTERS, 'Зельевары'),
        (CAST_SPELLERS, 'Мастера заклинаний'),
        (NO_ONE, 'Никто')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NO_ONE)
    title = models.CharField(max_length=50, unique=True, verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Сообщение")
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[0:40]} ... [{str(self.rating)}]'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class Comment(models.Model):
    linkedPost = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='linkedComments')
    linkedUser = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name="commented")
    acceptedBy = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="accepted")

    commentText = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    familyTree = models.CharField(max_length=500, blank=True, null=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.commentText[:40]}'

    def get_offset(self):
        x = len(str(self.familyTree).split("-")) - 2
        return 5 if x > 5 else x

    def get_col(self):
        return 12 - self.get_offset()

