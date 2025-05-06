from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.

class Category_Tasks(models.Model):
    points = models.CharField(blank=False,max_length=10,verbose_name="Максимальные баллы")
    difficult = models.CharField(blank=False,max_length=20,verbose_name="Сложность")

    def __str__(self):
        return f'Задание {self.id}'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.id})

    class Meta:
        verbose_name = 'Категории для заданий ЕГЭ'
        verbose_name_plural = 'Категории для заданий ЕГЭ'

class Category_Tasks_Filter(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Название фильтра")
    slug = models.SlugField(max_length=255, blank=False, db_index=True, verbose_name="URL-slug")
    cat = models.ForeignKey('Category_Tasks', on_delete=models.PROTECT, null=True, verbose_name="Ключ к категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фильтры для заданий ЕГЭ'
        verbose_name_plural = 'Фильтры для заданий ЕГЭ'

    def get_absolute_url(self):
        return reverse('filter_category', kwargs={'filter_slug': self.slug})






class Task(models.Model):
    condition = models.TextField(blank=False,verbose_name="Условие")
    solution = models.TextField(blank=False,verbose_name="Решение")
    answer = models.TextField(blank=False,verbose_name="Ответ")
    time_create = models.DateTimeField(auto_now_add=True,verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True,verbose_name="Время обновления")
    photo_condition = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True,verbose_name="Фото в условии")
    photo_before = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True,verbose_name="Фото перед решением")
    photo_after = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True,verbose_name="Фото после решения")
    is_published = models.BooleanField(default=True,blank=False,verbose_name="<= будет опубликовано?")
    ytb = models.CharField(max_length=255,blank=True,default='',verbose_name="YouTube")
    cat = models.ForeignKey('Category_Tasks', on_delete=models.PROTECT, null=True,blank=False,verbose_name="Ключ к категории заданий")
    filter = models.ForeignKey('Category_Tasks_Filter', on_delete=models.PROTECT, null=True,blank=True,verbose_name="Ключ к категории фильтров для заданий")

    def __str__(self):
        return self.condition.replace("<span>","").replace("</span>","")

    class Meta:
        verbose_name = 'Задания ЕГЭ'
        verbose_name_plural = 'Задания ЕГЭ'
        ordering = ['time_update']

    def get_absolute_url(self):
        return reverse('task_object', kwargs={'task_id': self.id})

class Category_Options(models.Model):
    description = models.CharField(max_length=255,verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True,verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True,verbose_name="Время обновления")
    difficult = models.CharField(max_length=20,blank=False,verbose_name="Сложность")
    ytb = models.CharField(max_length=255,blank=True,default='',verbose_name="YouTube")
    is_published = models.BooleanField(default=True,blank=False,verbose_name="<= будет опубликовано?")

    id_number_1 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {1}")
    id_number_2 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {2}")
    id_number_3 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {3}")
    id_number_4 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {4}")
    id_number_5 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {5}")
    id_number_6 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {6}")
    id_number_7 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {7}")
    id_number_8 = models.CharField(max_length=255, blank=False, unique=True, db_index=True,verbose_name=f"id для задания {8}")
    id_number_9 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {9}")
    id_number_10 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {10}")
    id_number_11 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {11}")
    id_number_12 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {12}")
    id_number_13 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {13}")
    id_number_14 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {14}")
    id_number_15 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {15}")
    id_number_16 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {16}")
    id_number_17 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {17}")
    id_number_18 = models.CharField(max_length=255,blank=False,unique=True, db_index=True, verbose_name=f"id для задания {18}")

    def __str__(self):
        return f'Вариант {self.id}'

    def get_absolute_url(self):
        return reverse('option', kwargs={'opt_id': self.id})

    class Meta:
        verbose_name = 'Варианты ЕГЭ'
        verbose_name_plural = 'Варианты ЕГЭ'


class Theory_category(models.Model):
    category = models.CharField(max_length=100,blank=False,verbose_name="Тема")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Раздел математики (Теория)'
        verbose_name_plural = 'Раздел математики (Теория)'

class Theory_item(models.Model):
    title = models.CharField(max_length=100,blank=False,verbose_name="Заголовок")
    ytb = models.CharField(max_length=255,blank=True,default='',verbose_name="YouTube")
    time_create = models.DateTimeField(auto_now_add=True,verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True,verbose_name="Время обновления")
    is_published = models.BooleanField(default=True,blank=False,verbose_name="<= будет опубликовано?")
    cat = models.ForeignKey('Theory_category', on_delete=models.PROTECT, null=True,verbose_name="Ключ к категории")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема (Теория)'
        verbose_name_plural = 'Тема (Теория)'
        ordering = ['time_update']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,null=False, blank=False,  verbose_name="Пользователь")
    post = models.ForeignKey('Task', on_delete=models.PROTECT,null=False, blank=False,  verbose_name="Задача")
    text = models.TextField(null=False, blank=False, verbose_name="Текст комментария")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Время написания", blank=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Время обновления", blank=False)
    is_published = models.BooleanField(default=True,blank=False,verbose_name="<= будет опубликован?")

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Комментарий {self.user} к задаче №{self.post.id} от {str(self.created).split()[0]} : {self.text}"





