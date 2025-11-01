from django.shortcuts import render
from .forms import MovieRecommendationForm
from movie_recommender.ML_Files.movie_recommendation import recommend_movies


def homepage(request):
    recommendations = None
    error_message = None

    if request.method == 'POST':
        form = MovieRecommendationForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['movie_title']
            results = recommend_movies(movie_title)

            if results['success']:
                recommendations = results['recommendations']
            else:
                error_message = results['error']
            print(results)
    else:
        form = MovieRecommendationForm()

    context = {
        'form': form,
        'recommendations': recommendations,
        'error_message': error_message,
    }
    return render(request, 'movie_recommender/homepage.html', context)




