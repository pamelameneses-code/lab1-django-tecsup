from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class AuthorProfile(models.Model):
    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.author.name}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    cover = models.ImageField(upload_to='books/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='books')
    publishers = models.ManyToManyField(
        Publisher,
        through='Publication',
        related_name='books'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Publication(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    edition = models.PositiveIntegerField(default=1)
    publication_date = models.DateField()

    class Meta:
        unique_together = ('book', 'publisher', 'edition')

    def __str__(self):
        return f"{self.book.title} - {self.publisher.name} (ed. {self.edition})"