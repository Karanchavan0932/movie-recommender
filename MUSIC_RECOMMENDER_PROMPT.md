# 🎵 Music Recommender System - Complete Project Specification

## PROJECT OVERVIEW
Create a **Music Recommendation System** - an intelligent web application that suggests songs based on user preferences. This project replicates the exact structure, concepts, and technologies of the Movie Recommender System but adapted for music.

---

## 📋 PROJECT STRUCTURE

```
music-recommender/
├── app.py                   # Main Streamlit application
├── generate_document.py     # Document generator for project documentation
├── music.csv                # Sample music dataset (CSV format)
├── requirements.txt         # Python dependencies
├── setup.bat               # Batch script for Windows setup
├── setup.sh                # Shell script for Mac/Linux setup
└── README.md               # Project documentation
```

---

## 📊 DATASET STRUCTURE (music.csv)

Create a CSV file with the following columns:
- **song_name** (string): Name of the song
- **artist** (string): Artist/Band name
- **genre** (string): Music genre(s) - multiple genres separated by spaces (e.g., "Pop Rock Electronic")

### Sample Data (20-100 songs minimum):
```csv
song_name,artist,genre
Blinding Lights,The Weeknd,Synthwave Pop Electronic
Levitating,Dua Lipa,Disco Pop
Heat Waves,Glass Animals,Indie Pop Psychedelic
As It Was,Harry Styles,Pop
Anti-Hero,Taylor Swift,Pop
Cruel Summer,Taylor Swift,Pop Synth
Unholy,Sam Smith Kim Petras,Dark Pop Electronic
Kill Bill,SZA,R&B Hip-Hop
Flowers,Miley Cyrus,Pop Disco
Vampire,Olivia Rodrigo,Pop Rock
Blank Space,Taylor Swift,Pop
Shape of You,Ed Sheeran,Pop Dance
Shut Up and Dance,Walk the Moon,Indie Pop
Take Me Out,Franz Ferdinand,Indie Rock
Mr. Brightside,The Killers,New Wave Synthpop
Come Together,The Beatles,Rock Psychedelic
Bohemian Rhapsody,Queen,Rock Theatrical
Imagine,John Lennon,Rock Pop
Hotel California,Eagles,Rock
Stairway to Heaven,Led Zeppelin,Rock
```

---

## 🛠️ TECHNOLOGIES & DEPENDENCIES

### Core Libraries:
1. **streamlit** (≥1.28.0) - Web UI framework
2. **pandas** (≥2.0.0) - Data manipulation
3. **scikit-learn** (≥1.3.0) - Machine learning (CountVectorizer, cosine_similarity)
4. **numpy** (≥1.24.0) - Numerical operations
5. **python-docx** - Document generation (for generate_document.py)

### Installation Command:
```bash
pip install streamlit>=1.28.0 pandas>=2.0.0 scikit-learn>=1.3.0 numpy>=1.24.0 python-docx
```

---

## 💻 CORE FEATURES & CONCEPTS

### 1. **Smart Recommendations**
- Uses **cosine similarity** algorithm to find songs similar to input
- Analyzes genre-based features
- Returns top 5 most similar songs

### 2. **Error Handling**
- Input validation (empty input check)
- File not found handling
- Song not found in database
- Graceful error messages with emoji indicators

### 3. **Caching & Performance**
- `@st.cache_data` decorator to cache loaded data
- Pre-computed similarity matrix
- Fast recommendation generation

### 4. **Clean User Interface**
- Centered layout
- Emoji indicators for status (✅, ❌, ⚠️, 💡)
- Sidebar with database information
- Sample songs suggestion
- Formatted output

### 5. **Scalability**
- Ready for Streamlit Cloud deployment
- GitHub repository compatible
- CSV-based data (easily expandable)

---

## 📝 COMPLETE app.py CODE STRUCTURE

```python
# IMPORTS
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# PAGE CONFIGURATION
# - Set page title: "Music Recommender System"
# - Set icon: "🎵"
# - Layout: "centered"

# FUNCTION 1: load_data()
# - Decorator: @st.cache_data
# - Functionality:
#   * Read music.csv
#   * Handle missing values in song_name, artist, genre columns
#   * Return dataframe
# - Error handling:
#   * FileNotFoundError: Display error if CSV not found
#   * Generic Exception: Display error message

# FUNCTION 2: create_similarity_matrix(df)
# - Decorator: @st.cache_data
# - Functionality:
#   * Create CountVectorizer from genre column
#   * Transform genre data into vectors
#   * Compute cosine_similarity matrix
#   * Return similarity matrix
# - Error handling: Wrap in try-except

# FUNCTION 3: recommend_songs(song_name, df, similarity_matrix, num_recommendations=5)
# - Functionality:
#   * Case-insensitive search for song
#   * Validate if song exists in database
#   * Get index of the song
#   * Extract similarity scores
#   * Sort by similarity (descending)
#   * Exclude the input song itself
#   * Return top N song names
# - Error handling: Try-except block

# MAIN UI SECTION
# 1. Display title: "🎵 Music Recommender System"
# 2. Display subtitle: "Find songs similar to your favorite music!"
# 3. Load data using load_data()
# 4. Create similarity matrix using create_similarity_matrix()
# 5. INPUT SECTION:
#    - Use st.columns for layout (3:1 ratio)
#    - Text input for song name (placeholder: "e.g., Blinding Lights")
#    - Button: "🔍 Recommend"
# 6. RECOMMENDATION SECTION:
#    - Validate empty input
#    - Call recommend_songs()
#    - Display recommendations in numbered list format
#    - Show success message with count
#    - Show error if song not found
#    - Display sample songs if not found
# 7. SIDEBAR:
#    - Header: "📊 Database Info"
#    - Total songs count
#    - Total unique artists
#    - Total unique genres
#    - Sample songs list
```

---

## 🎨 UI/UX DESIGN PATTERNS

### Color Scheme:
- Primary Headings: RGB(0, 102, 204) - Blue
- Success Messages: Green with ✅
- Error Messages: Red with ❌
- Warning Messages: Orange with ⚠️
- Info Messages: Blue with 💡

### Layout Structure:
```
┌─────────────────────────────────────┐
│    🎵 Music Recommender System      │
│   Find songs similar to favorites!  │
├─────────────────────────────────────┤
│  Song Input [____________________]  │
│             [🔍 Recommend]          │
├─────────────────────────────────────┤
│  Recommendations:                   │
│  1. Song Name - Artist              │
│  2. Song Name - Artist              │
│  3. Song Name - Artist              │
│  4. Song Name - Artist              │
│  5. Song Name - Artist              │
└─────────────────────────────────────┘
      SIDEBAR: Database Stats
      Total Songs: X
      Artists: Y
      Genres: Z
      Sample Songs: ...
```

---

## 🧠 ALGORITHM EXPLANATION

### CountVectorizer:
- Converts text (genres) into a matrix of token counts
- Each genre becomes a feature vector
- Example: "Pop Rock" → [1, 1, 0, 0, ...] for each genre word

### Cosine Similarity:
- Measures angle between genre vectors
- Returns values between 0 (no similarity) and 1 (identical)
- Formula: cos(θ) = (A·B) / (|A| × |B|)
- Perfect for genre-based music recommendation

### Recommendation Pipeline:
1. User enters song name → "Blinding Lights"
2. Find index of "Blinding Lights" in database
3. Get its genre vector (Synthwave Pop Electronic)
4. Compare with all other songs' genre vectors
5. Sort by similarity score (highest first)
6. Return top 5 songs (excluding input song)

---

## 📄 DOCUMENT GENERATION (generate_document.py)

Create a Word document (.docx) with project documentation including:
- Title and styling
- Project introduction
- System architecture explanation
- Technologies used
- Installation instructions
- Deployment guide
- Sample testing scenarios
- Feature descriptions

### Key Functions:
- `add_heading_with_color()` - Add colored headings
- `add_colored_paragraph()` - Add formatted paragraphs
- `shade_paragraph()` - Add background colors
- Generate professional documentation automatically

---

## 📥 REQUIREMENTS.txt

```
streamlit>=1.28.0
pandas>=2.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
python-docx>=0.8.11
```

---

## 🚀 INSTALLATION & SETUP

### Windows Setup (setup.bat):
```batch
@echo off
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Setup complete! Run: streamlit run app.py
pause
```

### Mac/Linux Setup (setup.sh):
```bash
#!/bin/bash
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Setup complete! Run: streamlit run app.py"
```

### Manual Setup:
```bash
# Step 1: Create virtual environment
python -m venv venv

# Step 2: Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run application
streamlit run app.py
```

---

## 🧪 TESTING SCENARIOS

Test with these songs from sample data:
- "Blinding Lights" → Returns Synthwave/Pop/Electronic songs
- "Bohemian Rhapsody" → Returns Rock/Theatrical songs
- "Heat Waves" → Returns Indie Pop/Psychedelic songs
- "Come Together" → Returns Rock songs
- "Hotel California" → Returns Classic Rock songs

---

## 📊 KEY METRICS

- **Total Songs**: 20-100 (expandable)
- **Total Artists**: Varies
- **Total Genres**: 15-20 unique genres
- **Recommendation Count**: Top 5 per request
- **Performance**: ~10-100ms per recommendation
- **Caching**: Automatic with Streamlit

---

## 🌐 DEPLOYMENT (STREAMLIT CLOUD)

### Prerequisites:
- GitHub account
- Git installed
- Streamlit account (free)

### Deployment Steps:
1. Create GitHub repository: `music-recommender`
2. Push code to GitHub
3. Go to streamlit.io/cloud
4. Click "New app"
5. Select repository, branch, main file (app.py)
6. Deploy!

---

## 📋 ERROR HANDLING CHECKLIST

- ✅ File not found error
- ✅ Missing column error
- ✅ Empty input validation
- ✅ Song not found in database
- ✅ Data type errors
- ✅ Similarity matrix computation errors
- ✅ User-friendly error messages

---

## 🔄 DATA FLOW DIAGRAM

```
START
  ↓
User Opens App (app.py)
  ↓
Load music.csv → @st.cache_data
  ↓
Preprocess Data (fill NaN values)
  ↓
Create Similarity Matrix → @st.cache_data
  ↓
User Enters Song Name + Clicks Recommend
  ↓
Validate Input (not empty)
  ↓
Search Song in Database (case-insensitive)
  ↓
Found? → No → Show Error Message
   ↓ Yes
Compute Similarity Scores
  ↓
Sort by Score (descending)
  ↓
Get Top 5 Songs (exclude input)
  ↓
Display Results
  ↓
END
```

---

## 📚 FILE DESCRIPTIONS

| File | Purpose | Key Concepts |
|------|---------|--------------|
| app.py | Main application | Streamlit UI, caching, ML pipeline |
| music.csv | Data source | Structured data, genres |
| requirements.txt | Dependencies | Version management |
| generate_document.py | Documentation | Word generation, styling |
| setup.bat | Windows setup | Environment setup automation |
| setup.sh | Unix setup | Environment setup automation |
| README.md | User guide | Installation, deployment, usage |

---

## 💡 EXTENSION IDEAS

1. **Add ratings/popularity**: Include song popularity and factor into recommendations
2. **User preferences**: Save favorite songs and build personalized profiles
3. **Multi-feature similarity**: Use artist, release date, popularity alongside genres
4. **Search filters**: Filter by artist, genre, release date
5. **Similar artists**: Find artists similar to selected artist
6. **Playlist generator**: Auto-generate playlists from recommendations
7. **Export recommendations**: Download recommendations as CSV/text
8. **Dark mode**: Add theme toggle
9. **Recommendation confidence**: Show similarity percentage
10. **Advanced ML**: Use embedding models (Word2Vec, BERT) for better recommendations

---

## 🎯 SUCCESS CRITERIA

✅ Application loads without errors
✅ Recommendations are generated instantly
✅ UI is clean and intuitive
✅ Error messages are helpful
✅ Can deploy to Streamlit Cloud
✅ Data can be easily updated
✅ Code is well-commented
✅ Performance is smooth (<1s per request)

---

## 📞 SUMMARY

This is a **complete, production-ready music recommendation system** that follows the exact architecture of the movie recommender but tailored for music. All concepts from the original project (caching, similarity algorithms, error handling, UI design, deployment) are replicated and adapted for music data.

**Use this specification to create your music recommendation system from scratch, ensuring all features and best practices are included.**
