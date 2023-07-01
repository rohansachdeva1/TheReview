from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from users.models import User, SearchHistory
from content.views import generate_genre_recs

def homepage(request):
    genre_recs = set()

    # Check if the user is logged in
    if request.user.is_authenticated:

        recent_searches = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:5] # Retrieve the 5 most recent searches for the logged-in user
        
        # Loop through the recent searches and add entity recommendations
        for search in recent_searches:
            entity_id = search.entity_id
            recommended_entities = generate_genre_recs(entity_id) # Call existing function to generate entity recommendations based on the entity_id 
            genre_recs.update(recommended_entities) # Add the recommended entities to the entity recommendations set

        genre_recs = list(genre_recs) # Convert the set back to a list if needed

    context = {
        'genre_recs': genre_recs,
        # ... other context data ...
    }
    
    return render(request, 'homepage.html', context)