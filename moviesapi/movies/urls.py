from rest_framework import routers
from movies.views import Movies, Comments, TopMovies

router = routers.DefaultRouter()
router.register(r'movies', Movies, 'movies')
router.register(r'comments', Comments, 'comments')
router.register(r'top', TopMovies, 'top-movies')
urlpatterns = router.urls