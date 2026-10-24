from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Genre, Book, Comment
from .serializers import (
    GenreSerializer,
    GenreListSerializer,
    GenreDetailSerializer,
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    CommentSerializer,
)
from .permissions import IsAuthorOrReadOnly

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GenreDetailSerializer
        if self.action == 'list':
            return GenreListSerializer
        return GenreSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('genre').prefetch_related('comments__user').order_by('id')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user', 'book').order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
