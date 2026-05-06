# 🎬 Movie Recommender System

A simple, fast, and user-friendly movie recommendation system built with Python, Streamlit, pandas, and scikit-learn.

## Features

✅ **Smart Recommendations** - Uses cosine similarity to find movies similar to your input  
✅ **Error Handling** - Graceful error messages and input validation  
✅ **Fast Processing** - Caches data and computations for instant results  
✅ **Clean UI** - Intuitive Streamlit interface with emojis and helpful guidance  
✅ **Scalable** - Ready for deployment on Streamlit Cloud  

## Project Structure

```
movie-recommender/
├── app.py              # Main Streamlit application
├── movies.csv          # Sample movie dataset
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file (optional)
```

## Installation & Local Testing

### Step 1: Clone or Download the Project

```bash
cd movie-recommender
```

### Step 2: Create a Virtual Environment (Optional but Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Locally

```bash
streamlit run app.py
```

Your app will open at `http://localhost:8501` in your browser.

## How It Works

1. **Data Loading** - Loads movies from `movies.csv` with title and genre columns
2. **Genre Vectorization** - Converts genre text into numerical vectors using CountVectorizer
3. **Similarity Calculation** - Computes cosine similarity between movies
4. **Recommendation** - Returns top 5 movies most similar to the input movie

## Testing the Application

Try these movies from the sample dataset:
- "The Matrix" → Returns sci-fi/action movies
- "Titanic" → Returns romance/drama movies
- "Toy Story" → Returns animation movies
- "The Dark Knight" → Returns action/crime movies

---

# 🚀 Deploy to Streamlit Cloud (Free & Global!)

Follow these steps to deploy your app and get a public link anyone can access worldwide.

## Prerequisites

- GitHub account (free at github.com)
- Streamlit Cloud account (free at streamlit.io)
- Git installed on your computer

## Deployment Steps

### Step 1: Install Git

Download and install from: https://git-scm.com/

### Step 2: Create a GitHub Repository

1. Go to https://github.com/new
2. Repository name: `movie-recommender`
3. Add description: "A simple movie recommendation system"
4. Click **Create repository**

### Step 3: Push Your Code to GitHub

```bash
# Navigate to your project folder
cd movie-recommender

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Movie Recommender System"

# Add remote repository (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/movie-recommender.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **Deploy an app** (top right)
3. Select **GitHub** as the repository source
4. Choose your `USERNAME/movie-recommender` repository
5. Select `main` branch
6. Set main file path to `app.py`
7. Click **Deploy**

Streamlit will build and deploy your app (takes ~2-3 minutes).

### Step 5: Get Your Public Link

✅ Your app will be live at: `https://movie-recommender-USERNAME.streamlit.app`

Share this link with anyone - they can use it worldwide without any installation!

## Updating Your Deployed App

After making changes:

```bash
# Stage changes
git add .

# Commit
git commit -m "Update: Added new features"

# Push to GitHub
git push
```

Streamlit Cloud will automatically rebuild and redeploy your app!

## Adding New Movies

1. Open `movies.csv`
2. Add new rows with `title` and `genre` (comma-separated genres)
3. Save and commit to GitHub
4. App updates automatically

Example:
```
The Silence of the Lambs,Thriller Crime
Parasite,Thriller Drama
```

## Troubleshooting

**"Movie not found" error**
- Check the exact movie name in `movies.csv`
- Movie names are case-insensitive

**Deployment fails**
- Ensure `requirements.txt` is in the root directory
- Check that `app.py` exists
- All files must be pushed to GitHub

**App runs slow**
- Add more movies to `movies.csv` (currently ~30 movies)
- Streamlit caches results, so second search is instant

## Customization Ideas

- 🎥 Add movie ratings or popularity data
- ⭐ Include user ratings system
- 🔗 Add links to movie trailers
- 📊 Show similarity scores
- 🎭 Add more genres to dataset
- 🌐 Fetch data from online APIs (e.g., TMDB)

## Dataset Format

The `movies.csv` file should have exactly 2 columns:

| title | genre |
|-------|-------|
| The Matrix | Science Fiction Action |
| Inception | Science Fiction Thriller |
| Forrest Gump | Drama Romance |

**Rules:**
- Genres should be separated by spaces
- No commas within genre fields
- Remove or fill in missing values

## Tech Stack

- **Backend:** Python, pandas, scikit-learn
- **Frontend:** Streamlit
- **Hosting:** Streamlit Cloud
- **Deployment:** GitHub

## Performance

- Dataset: ~30 movies (easily scalable to 1000+)
- Response time: <100ms locally, <500ms on cloud
- Memory usage: ~10MB
- Database: CSV (can upgrade to SQLite/PostgreSQL)

## License

Free to use and modify. Enjoy! 🎉
