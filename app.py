import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="centered"
)

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('movies.csv')
        # Handle missing values
        df['title'] = df['title'].fillna('Unknown')
        df['genre'] = df['genre'].fillna('Unknown')
        return df
    except FileNotFoundError:
        st.error("❌ movies.csv file not found. Please ensure it exists in the project directory.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# Create similarity matrix
@st.cache_data
def create_similarity_matrix(df):
    try:
        # Vectorize genres
        vectorizer = CountVectorizer()
        genre_vectors = vectorizer.fit_transform(df['genre'])
        # Compute cosine similarity
        similarity_matrix = cosine_similarity(genre_vectors)
        return similarity_matrix
    except Exception as e:
        st.error(f"❌ Error creating similarity matrix: {str(e)}")
        return None

# Recommendation function
def recommend_movies(movie_name, df, similarity_matrix, num_recommendations=5):
    try:
        # Case-insensitive search
        movie_list = df['title'].str.lower().tolist()
        
        if movie_name.lower() not in movie_list:
            return None
        
        # Get index of the movie
        movie_idx = movie_list.index(movie_name.lower())
        
        # Get similarity scores
        sim_scores = list(enumerate(similarity_matrix[movie_idx]))
        
        # Sort by similarity (descending) and exclude the movie itself
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return recommended movies
        recommended_titles = df['title'].iloc[movie_indices].tolist()
        return recommended_titles
    
    except Exception as e:
        st.error(f"❌ Error during recommendation: {str(e)}")
        return None

# Main UI
st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite film!")

# Load data
df = load_data()

if df is not None and len(df) > 0:
    # Create similarity matrix
    similarity_matrix = create_similarity_matrix(df)
    
    if similarity_matrix is not None:
        # Input section
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            movie_input = st.text_input(
                "Enter a movie name:",
                placeholder="e.g., The Matrix"
            )
        
        with col2:
            search_button = st.button("🔍 Recommend", use_container_width=True)
        
        st.markdown("---")
        
        # Recommendation section
        if search_button:
            if movie_input.strip() == "":
                st.warning("⚠️ Please enter a movie name.")
            else:
                recommendations = recommend_movies(movie_input, df, similarity_matrix)
                
                if recommendations is None:
                    st.error(f"❌ Movie '{movie_input}' not found in database.")
                    st.info("💡 Try one of these movies instead:")
                    # Show first 10 available movies
                    st.write(", ".join(df['title'].head(10).tolist()))
                else:
                    st.success(f"✅ Found {len(recommendations)} similar movies!")
                    st.subheader("Recommended Movies:")
                    for i, movie in enumerate(recommendations, 1):
                        st.write(f"{i}. **{movie}**")
        
        # Sidebar with additional info
        with st.sidebar:
            st.header("📊 Database Info")
            st.write(f"**Total Movies:** {len(df)}")
            st.write(f"**Genres Available:** {df['genre'].nunique()}")
            
            st.subheader("📚 Sample Movies")
            st.write(", ".join(df['title'].head(5).tolist()))
else:
    st.error("❌ Unable to load movie database.")
