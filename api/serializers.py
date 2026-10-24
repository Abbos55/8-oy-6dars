from rest_framework import serializers
from .models import Genre, Book, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'text']
        read_only_fields = ['id', 'user']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookInGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'price']

class GenreListSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True, read_only=True)
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'books_count', 'books']

    def get_books_count(self, obj):
        return obj.books.count()

class GenreDetailSerializer(serializers.ModelSerializer):
    books = BookInGenreSerializer(many=True, read_only=True)
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'books_count', 'books']

    def get_books_count(self, obj):
        return obj.books.count()

class BookListSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'price', 'genre']

class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    course = GenreSerializer(source='genre', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'price', 'genre', 'course', 'comments']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'price', 'genre']
