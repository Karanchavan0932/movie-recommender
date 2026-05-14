import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="CineMatch - Professional Movie Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS & STYLING
# ============================================================================
st.markdown("""
    <style>
    /* Main theme */
    :root {
        --primary: #FF6B35;
        --secondary: #004E89;
        --background: #F7F7F7;
    }
    
    .main {
        padding: 0px;
    }
    
    /* Movie card styling */
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
    }
    
    .movie-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .movie-rating {
        display: inline-block;
        background: #FF6B35;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        margin: 5px 0;
    }
    
    /* Stats box */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .header h1 {
        font-size: 3em;
        margin: 0;
    }
    
    .header p {
        font-size: 1.2em;
        margin: 10px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('movies.csv')
        df['title'] = df['title'].fillna('Unknown')
        df['genre'] = df['genre'].fillna('Unknown')
        df['director'] = df['director'].fillna('Unknown')
        df['plot'] = df['plot'].fillna('Unknown')
        df['runtime'] = pd.to_numeric(df['runtime'], errors='coerce').fillna(120).astype(int)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(7.0)
        df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(2000).astype(int)
        df['cast'] = df['cast'].fillna('Unknown')
        df['budget'] = pd.to_numeric(df['budget'], errors='coerce').fillna(0)
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        st.error("❌ movies.csv file not found.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

@st.cache_data
def create_similarity_matrix(df):
    try:
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
        title_vectors = vectorizer.fit_transform(df['title'].str.lower())
        genre_vectors = CountVectorizer().fit_transform(df['genre'])
        combined_vectors = (title_vectors * 0.3 + genre_vectors * 0.7)
        similarity_matrix = cosine_similarity(combined_vectors)
        return similarity_matrix
    except Exception as e:
        st.error(f"❌ Error creating similarity matrix: {str(e)}")
        return None

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def recommend_movies(movie_name, df, similarity_matrix, num_recommendations=5):
    try:
        movie_list = df['title'].str.lower().tolist()
        if movie_name.lower() not in movie_list:
            return None
        
        movie_idx = movie_list.index(movie_name.lower())
        sim_scores = list(enumerate(similarity_matrix[movie_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]
        movie_indices = [i[0] for i in sim_scores]
        return df.iloc[movie_indices]
    except Exception as e:
        return None

def format_currency(value):
    if value >= 1000000000:
        return f"${value/1000000000:.2f}B"
    elif value >= 1000000:
        return f"${value/1000000:.2f}M"
    return f"${value:,.0f}"

def get_star_rating(rating):
    stars = "⭐" * int(rating)
    if rating % 1 >= 0.5:
        stars += "✨"
    return stars

def display_movie_card(movie, col):
    with col:
        with st.container():
            # Title
            st.markdown(f"### 🎬 {movie['title']}")
            
            # Rating and Year
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**⭐ Rating:** {movie['rating']}/10 {get_star_rating(movie['rating'])}")
            with col2:
                st.markdown(f"**📅 Year:** {movie['year']}")
            with col3:
                st.markdown(f"**⏱️ {movie['runtime']}m**")
            
            # Genre and Director
            st.markdown(f"**🎭 Genre:** {movie['genre']}")
            st.markdown(f"**🎥 Director:** {movie['director']}")
            
            # Plot
            st.markdown(f"**📖 Plot:** {movie['plot'][:150]}...")
            
            # Cast
            st.markdown(f"**👥 Cast:** {movie['cast'][:60]}...")
            
            # Budget and Revenue
            budget_revenue = st.columns(2)
            with budget_revenue[0]:
                st.markdown(f"**💰 Budget:** {format_currency(movie['budget'])}")
            with budget_revenue[1]:
                st.markdown(f"**💵 Revenue:** {format_currency(movie['revenue'])}")
            
            # Action buttons
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button(f"➕ Add to Watchlist", key=f"add_{movie['title']}"):
                    if movie['title'] not in st.session_state.watchlist:
                        st.session_state.watchlist.append(movie['title'])
                        st.success(f"Added to watchlist!")
            
            with btn_col2:
                if st.button(f"❤️ View Details", key=f"details_{movie['title']}"):
                    st.session_state.selected_movie = movie['title']

# ============================================================================
# MAIN APPLICATION
# ============================================================================

# Load data
df = load_data()

if df is not None and len(df) > 0:
    
    # ========================================================================
    # HEADER SECTION
    # ========================================================================
    st.markdown("""
        <div class="header">
            <h1>🎬 CineMatch</h1>
            <p>Your Professional Movie Discovery & Recommendation Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # TOP STATISTICS
    # ========================================================================
    st.subheader("📊 Platform Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        with st.container():
            st.markdown("<div class='stat-box' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'><h3>🎬</h3><h2>" + str(len(df)) + "</h2><p>Total Movies</p></div>", unsafe_allow_html=True)
    
    with col2:
        genres_count = df['genre'].nunique()
        with st.container():
            st.markdown(f"<div class='stat-box' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'><h3>🎭</h3><h2>{genres_count}</h2><p>Genres</p></div>", unsafe_allow_html=True)
    
    with col3:
        avg_rating = df['rating'].mean()
        with st.container():
            st.markdown(f"<div class='stat-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'><h3>⭐</h3><h2>{avg_rating:.1f}</h2><p>Avg Rating</p></div>", unsafe_allow_html=True)
    
    with col4:
        decades = len(df['year'].unique())
        with st.container():
            st.markdown(f"<div class='stat-box' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'><h3>📅</h3><h2>{df['year'].min()}-{df['year'].max()}</h2><p>Year Range</p></div>", unsafe_allow_html=True)
    
    with col5:
        watchlist_count = len(st.session_state.watchlist)
        with st.container():
            st.markdown(f"<div class='stat-box' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'><h3>❤️</h3><h2>{watchlist_count}</h2><p>Watchlist</p></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    with st.sidebar:
        st.header("🔍 Advanced Filters")
        
        # Genre filter
        genres_list = sorted(df['genre'].str.split().explode().unique().tolist())
        selected_genres = st.multiselect(
            "Filter by Genre:",
            genres_list,
            help="Select one or more genres"
        )
        
        # Year range filter
        year_range = st.slider(
            "Year Range:",
            int(df['year'].min()),
            int(df['year'].max()),
            (int(df['year'].min()), int(df['year'].max()))
        )
        
        # Rating filter
        rating_range = st.slider(
            "Rating Range:",
            5.0, 10.0,
            (5.0, 10.0),
            0.1
        )
        
        # Runtime filter
        runtime_range = st.slider(
            "Runtime (minutes):",
            int(df['runtime'].min()),
            int(df['runtime'].max()),
            (int(df['runtime'].min()), int(df['runtime'].max()))
        )
        
        # Sort options
        sort_by = st.selectbox(
            "Sort By:",
            ["Rating (High to Low)", "Rating (Low to High)", "Year (Newest)", 
             "Year (Oldest)", "Runtime (Longest)", "Runtime (Shortest)", 
             "Revenue (Highest)", "Title (A-Z)"]
        )
        
        st.divider()
        
        # Watchlist section
        st.subheader("❤️ My Watchlist")
        if st.session_state.watchlist:
            for movie_title in st.session_state.watchlist:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"🎬 {movie_title}")
                with col2:
                    if st.button("✕", key=f"remove_{movie_title}"):
                        st.session_state.watchlist.remove(movie_title)
                        st.rerun()
        else:
            st.info("Your watchlist is empty. Add movies to get started!")
    
    # ========================================================================
    # APPLY FILTERS
    # ========================================================================
    filtered_df = df.copy()
    
    # Genre filter
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genre'].str.contains(
            '|'.join(selected_genres), case=False, na=False
        )]
    
    # Year filter
    filtered_df = filtered_df[
        (filtered_df['year'] >= year_range[0]) & 
        (filtered_df['year'] <= year_range[1])
    ]
    
    # Rating filter
    filtered_df = filtered_df[
        (filtered_df['rating'] >= rating_range[0]) & 
        (filtered_df['rating'] <= rating_range[1])
    ]
    
    # Runtime filter
    filtered_df = filtered_df[
        (filtered_df['runtime'] >= runtime_range[0]) & 
        (filtered_df['runtime'] <= runtime_range[1])
    ]
    
    # Apply sorting
    if sort_by == "Rating (High to Low)":
        filtered_df = filtered_df.sort_values('rating', ascending=False)
    elif sort_by == "Rating (Low to High)":
        filtered_df = filtered_df.sort_values('rating', ascending=True)
    elif sort_by == "Year (Newest)":
        filtered_df = filtered_df.sort_values('year', ascending=False)
    elif sort_by == "Year (Oldest)":
        filtered_df = filtered_df.sort_values('year', ascending=True)
    elif sort_by == "Runtime (Longest)":
        filtered_df = filtered_df.sort_values('runtime', ascending=False)
    elif sort_by == "Runtime (Shortest)":
        filtered_df = filtered_df.sort_values('runtime', ascending=True)
    elif sort_by == "Revenue (Highest)":
        filtered_df = filtered_df.sort_values('revenue', ascending=False)
    elif sort_by == "Title (A-Z)":
        filtered_df = filtered_df.sort_values('title', ascending=True)
    
    # ========================================================================
    # MAIN CONTENT TABS
    # ========================================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 Top Rated",
        "🔎 Search & Browse",
        "🎯 Recommendations",
        "📈 Analytics",
        "❤️ Watchlist"
    ])
    
    # TAB 1: TOP RATED
    with tab1:
        st.subheader("🏆 Top Rated Movies")
        top_movies = filtered_df.nlargest(12, 'rating')
        
        if len(top_movies) > 0:
            cols = st.columns(3)
            for idx, movie in top_movies.iterrows():
                col_idx = (top_movies.index.get_loc(idx)) % 3
                display_movie_card(movie, cols[col_idx])
        else:
            st.warning("No movies match your filters.")
    
    # TAB 2: SEARCH & BROWSE
    with tab2:
        st.subheader("🔎 Search & Browse Movies")
        
        search_col1, search_col2 = st.columns([4, 1])
        with search_col1:
            search_query = st.text_input(
                "Search movies by title or director:",
                placeholder="Enter movie name..."
            )
        
        with search_col2:
            results_count = st.number_input("Results per page:", 1, 50, 9)
        
        # Filter based on search
        if search_query:
            search_df = filtered_df[
                (filtered_df['title'].str.contains(search_query, case=False, na=False)) |
                (filtered_df['director'].str.contains(search_query, case=False, na=False))
            ]
        else:
            search_df = filtered_df
        
        st.write(f"**Found {len(search_df)} movies**")
        
        if len(search_df) > 0:
            # Pagination
            total_pages = (len(search_df) + results_count - 1) // results_count
            page = st.slider("Page:", 1, max(1, total_pages), 1)
            
            start_idx = (page - 1) * results_count
            end_idx = start_idx + results_count
            page_movies = search_df.iloc[start_idx:end_idx]
            
            cols = st.columns(3)
            for idx, (_, movie) in enumerate(page_movies.iterrows()):
                col_idx = idx % 3
                display_movie_card(movie, cols[col_idx])
        else:
            st.info("No movies found. Try different search terms or filters.")
    
    # TAB 3: RECOMMENDATIONS
    with tab3:
        st.subheader("🎯 Get Movie Recommendations")
        
        rec_col1, rec_col2 = st.columns([3, 1])
        with rec_col1:
            selected_movie = st.selectbox(
                "Select a movie to find similar recommendations:",
                df['title'].sort_values().tolist()
            )
        
        with rec_col2:
            num_rec = st.number_input("Number of recommendations:", 3, 20, 5)
        
        if st.button("🔍 Get Recommendations", use_container_width=True):
            similarity_matrix = create_similarity_matrix(df)
            if similarity_matrix is not None:
                recommendations = recommend_movies(
                    selected_movie, df, similarity_matrix, num_rec
                )
                
                if recommendations is not None and len(recommendations) > 0:
                    st.success(f"Found {len(recommendations)} similar movies!")
                    
                    cols = st.columns(3)
                    for idx, (_, movie) in enumerate(recommendations.iterrows()):
                        col_idx = idx % 3
                        display_movie_card(movie, cols[col_idx])
                else:
                    st.warning("Could not generate recommendations.")
    
    # TAB 4: ANALYTICS
    with tab4:
        st.subheader("📈 Movie Analytics Dashboard")
        
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            # Rating distribution
            fig_rating = px.histogram(
                filtered_df,
                x='rating',
                nbins=20,
                title='Rating Distribution',
                labels={'rating': 'Rating', 'count': 'Number of Movies'},
                color_discrete_sequence=['#667eea']
            )
            st.plotly_chart(fig_rating, use_container_width=True)
        
        with analytics_col2:
            # Movies by genre
            genre_data = filtered_df['genre'].str.split(expand=True).stack().value_counts().head(10)
            fig_genre = px.bar(
                x=genre_data.values,
                y=genre_data.index,
                orientation='h',
                title='Top 10 Genres',
                labels={'x': 'Count', 'y': 'Genre'},
                color_discrete_sequence=['#764ba2']
            )
            st.plotly_chart(fig_genre, use_container_width=True)
        
        # Movies over time
        fig_timeline = px.line(
            filtered_df.groupby('year').size().reset_index(name='count'),
            x='year',
            y='count',
            title='Movies Released Over Time',
            markers=True,
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Revenue vs Budget scatter
        fig_scatter = px.scatter(
            filtered_df[filtered_df['budget'] > 0],
            x='budget',
            y='revenue',
            size='rating',
            hover_name='title',
            title='Budget vs Revenue',
            color_discrete_sequence=['#f093fb'],
            labels={'budget': 'Budget ($)', 'revenue': 'Revenue ($)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # TAB 5: WATCHLIST
    with tab5:
        st.subheader("❤️ My Watchlist")
        
        if st.session_state.watchlist:
            watchlist_movies = df[df['title'].isin(st.session_state.watchlist)]
            
            st.write(f"**Total movies in watchlist: {len(watchlist_movies)}**")
            
            watchlist_stats_col1, watchlist_stats_col2, watchlist_stats_col3 = st.columns(3)
            
            with watchlist_stats_col1:
                avg_rating_watchlist = watchlist_movies['rating'].mean()
                st.metric("Average Rating", f"{avg_rating_watchlist:.1f}/10")
            
            with watchlist_stats_col2:
                total_runtime = watchlist_movies['runtime'].sum()
                hours = total_runtime // 60
                minutes = total_runtime % 60
                st.metric("Total Runtime", f"{hours}h {minutes}m")
            
            with watchlist_stats_col3:
                total_revenue = watchlist_movies['revenue'].sum()
                st.metric("Total Revenue", format_currency(total_revenue))
            
            st.divider()
            
            cols = st.columns(3)
            for idx, (_, movie) in enumerate(watchlist_movies.iterrows()):
                col_idx = idx % 3
                display_movie_card(movie, cols[col_idx])
        
        else:
            st.info("Your watchlist is empty! Add movies from other tabs to get started.")
    
    st.divider()
    st.markdown("---")
    st.markdown("### 📝 About CineMatch")
    st.markdown("""
    **CineMatch** is a professional movie discovery and recommendation platform featuring:
    - 500+ carefully curated movies
    - Advanced filtering and sorting options
    - Personalized movie recommendations
    - Comprehensive analytics dashboard
    - Personal watchlist management
    - Detailed movie information including cast, directors, budget, and revenue
    
    **Created with Streamlit | Powered by Machine Learning Recommendations**
    """)

else:
    st.error("❌ Unable to load movie database. Please ensure movies.csv exists.")
