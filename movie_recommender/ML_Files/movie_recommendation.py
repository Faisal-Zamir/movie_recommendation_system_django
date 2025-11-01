import joblib
import os

# ------------------------------------
# Load Pre-Trained Model Components
# ------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cv = joblib.load(os.path.join(BASE_DIR, "count_vectorizer.pkl"))
similarity = joblib.load(os.path.join(BASE_DIR, "similarity_matrix.pkl"))
final_df = joblib.load(os.path.join(BASE_DIR, "movie_data.pkl"))


def recommend_movies(movie_title: str):
    """
    Recommend top 5 similar movies based on a given title.
    Returns:
        dict: {success: bool, recommendations: list or error message}
    """

    movie_title = movie_title.strip()
    if not movie_title:
        return {'success': False, 'error': "No movie title provided."}

    # Case-insensitive matching
    matched_indices = final_df[final_df['title'].str.lower() == movie_title.lower()].index.tolist()
    if not matched_indices:
        return {'success': False, 'error': f"Movie '{movie_title}' not found in database."}

    movie_index = matched_indices[0]

    try:
        # Get similarity scores for this movie
        sim_scores = list(enumerate(similarity[movie_index]))

        # Sort by similarity (descending), skip the movie itself
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

        recommendations = []
        for rank, (idx, score) in enumerate(sorted_scores, start=1):
            movie_data = final_df.iloc[idx]
            recommendations.append({
                'rank': rank,
                'title': movie_data['title'],
                'genres': movie_data.get('genres', 'N/A'),
                'overview': (movie_data.get('overview', '')[:250] + '...') if 'overview' in movie_data else '',
                'similarity_percent': round(float(score) * 100, 2)
            })

        return {
            'success': True,
            'input_movie': movie_title,
            'recommendations': recommendations
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}


# ------------------------------------
# Example Test (for standalone run)
# ------------------------------------
if __name__ == "__main__":
    movie_name = "Avatar"
    results = recommend_movies(movie_name)

    if results['success']:
        print(f"\n🎬 Top 5 movies similar to '{results['input_movie']}':\n")
        for rec in results['recommendations']:
            print(f"{rec['rank']}. {rec['title']} — {rec['genres']}")
            print(f"   Similarity: {rec['similarity_percent']}%")
            print(f"   Overview: {rec['overview']}\n")
    else:
        print("❌ Error:", results['error'])
