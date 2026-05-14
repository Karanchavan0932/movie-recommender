import pandas as pd
import numpy as np
import random

# Movie data with expanded metadata
movies_data = [
    {"title": "The Matrix", "genre": "Science Fiction Action", "year": 1999, "rating": 8.7, "director": "Lana Wachowski, Lilly Wachowski", "plot": "A computer hacker learns about the true nature of his reality and his role in the war against its controllers.", "runtime": 136, "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", "budget": 63000000, "revenue": 467222728},
    {"title": "Inception", "genre": "Science Fiction Thriller", "year": 2010, "rating": 8.8, "director": "Christopher Nolan", "plot": "A skilled thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.", "runtime": 148, "cast": "Leonardo DiCaprio, Marion Cotillard, Joseph Gordon-Levitt", "budget": 160000000, "revenue": 839292587},
    {"title": "Interstellar", "genre": "Science Fiction Drama", "year": 2014, "rating": 8.6, "director": "Christopher Nolan", "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "runtime": 169, "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "budget": 165000000, "revenue": 677463813},
    {"title": "Avatar", "genre": "Science Fiction Adventure", "year": 2009, "rating": 7.8, "director": "James Cameron", "plot": "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.", "runtime": 162, "cast": "Sam Worthington, Zoe Saldana, Stephen Lang", "budget": 237000000, "revenue": 2923706026},
    {"title": "The Dark Knight", "genre": "Action Crime", "year": 2008, "rating": 9.0, "director": "Christopher Nolan", "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.", "runtime": 152, "cast": "Christian Bale, Heath Ledger, Aaron Eckhart", "budget": 185000000, "revenue": 1005045668},
    {"title": "The Avengers", "genre": "Action Adventure Superhero", "year": 2012, "rating": 8.0, "director": "Joss Whedon", "plot": "Earth's mightiest heroes must come together and learn to fight as a team to save the planet from an alien invasion.", "runtime": 143, "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo", "budget": 220000000, "revenue": 1519557910},
    {"title": "Pulp Fiction", "genre": "Crime Drama", "year": 1994, "rating": 8.9, "director": "Quentin Tarantino", "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.", "runtime": 154, "cast": "John Travolta, Samuel L. Jackson, Uma Thurman", "budget": 8000000, "revenue": 213959223},
    {"title": "Forrest Gump", "genre": "Drama Romance", "year": 1994, "rating": 8.8, "director": "Robert Zemeckis", "plot": "The presidencies of Kennedy and Johnson, the Vietnam War, and the Watergate scandal unfold from the perspective of an Alabama man with an IQ of 75.", "runtime": 142, "cast": "Tom Hanks, Sally Field, Gary Sinise", "budget": 55000000, "revenue": 678226993},
    {"title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "rating": 9.3, "director": "Frank Darabont", "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "runtime": 142, "cast": "Tim Robbins, Morgan Freeman, Bob Gunton", "budget": 25000000, "revenue": 58300000},
    {"title": "Titanic", "genre": "Romance Drama", "year": 1997, "rating": 7.8, "director": "James Cameron", "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.", "runtime": 194, "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane", "budget": 200000000, "revenue": 2257844680},
    {"title": "The Notebook", "genre": "Romance Drama", "year": 2004, "rating": 7.8, "director": "Nick Cassavetes", "plot": "A poor yet passionate young man falls in love with a rich young woman, giving her a sense of freedom, but they are soon separated because of their social differences.", "runtime": 123, "cast": "Ryan Gosling, Rachel McAdams, James Garner", "budget": 29000000, "revenue": 115725326},
    {"title": "The Fault in Our Stars", "genre": "Romance Drama", "year": 2014, "rating": 7.7, "director": "Josh Boone", "plot": "Two teenagers with terminal illnesses embark on a cross-country road trip to find meaning in their lives.", "runtime": 125, "cast": "Ansel Elgort, Shailene Woodley, Nat Wolff", "budget": 12000000, "revenue": 307950854},
    {"title": "Jurassic Park", "genre": "Science Fiction Adventure", "year": 1993, "rating": 8.2, "director": "Steven Spielberg", "plot": "A pragmatic paleontologist touring an almost complete theme park is tasked with protecting a couple of kids.", "runtime": 127, "cast": "Sam Neill, Laura Dern, Jeff Goldblum", "budget": 63000000, "revenue": 914691118},
    {"title": "The Terminator", "genre": "Science Fiction Action", "year": 1984, "rating": 8.1, "director": "James Cameron", "plot": "A cyborg assassin is sent back in time to kill the mother of the leader of the human resistance against the machines.", "runtime": 107, "cast": "Arnold Schwarzenegger, Linda Hamilton, Michael Biehn", "budget": 6400000, "revenue": 78371200},
    {"title": "Back to the Future", "genre": "Science Fiction Comedy", "year": 1985, "rating": 8.5, "director": "Robert Zemeckis", "plot": "A teenager is accidentally sent 30 years into the past in a time-traveling DeLorean invented by his friend.", "runtime": 116, "cast": "Michael J. Fox, Christopher Lloyd, Lea Thompson", "budget": 19000000, "revenue": 388328455},
    {"title": "The Ring", "genre": "Horror Thriller", "year": 2002, "rating": 7.3, "director": "Gore Verbinski", "plot": "A journalist must investigate a mysterious videotape which seems to cause the death of anyone in a week of viewing it.", "runtime": 115, "cast": "Naomi Watts, Martin Henderson, David Dorfman", "budget": 48000000, "revenue": 249346213},
    {"title": "A Quiet Place", "genre": "Horror Thriller", "year": 2018, "rating": 7.5, "director": "John Krasinski", "plot": "In a world filled with sound-hunting monsters, the only way to survive is to stay quiet.", "runtime": 90, "cast": "Emily Blunt, John Krasinski, Millicent Simmonds", "budget": 17000000, "revenue": 374505500},
    {"title": "The Conjuring", "genre": "Horror Thriller", "year": 2013, "rating": 7.5, "director": "James Wan", "plot": "Paranormal investigators work to help a family terrorized by a dark presence in their farmhouse.", "runtime": 112, "cast": "Vera Farmiga, Patrick Wilson, Ron Livingston", "budget": 20000000, "revenue": 319475522},
    {"title": "Toy Story", "genre": "Animation Comedy", "year": 1995, "rating": 8.3, "director": "John Lasseter", "plot": "A cowboy doll is profoundly threatened when a new spaceman figure supplants him as top toy in a boy's bedroom.", "runtime": 81, "cast": "Tom Hanks, Tim Allen, Don Rickles", "budget": 30000000, "revenue": 365019265},
]

# Generate additional movies
genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Science Fiction", "Thriller", "Adventure", "Fantasy", "Animation"]
genre_combinations = [
    "Action Adventure", "Science Fiction Action", "Comedy Drama", "Horror Thriller",
    "Romance Comedy", "Action Thriller", "Drama Crime", "Adventure Fantasy",
    "Science Fiction Drama", "Action Crime", "Comedy Animation", "Family Adventure",
    "Mystery Thriller", "Historical Drama", "Romance Drama", "Biography"
]

directors = [
    "Steven Spielberg", "Martin Scorsese", "David Fincher", "Christopher Nolan",
    "Quentin Tarantino", "Denis Villeneuve", "Cary Joji Fukunaga", "Damien Chazelle",
    "Brad Bird", "Peter Jackson", "James Cameron", "Greta Gerwig",
    "Barry Jenkins", "Wong Kar-wai", "Bong Joon-ho", "Alejandro González Iñárritu",
    "Alfonso Cuarón", "Spike Lee", "Hayao Miyazaki", "Park Chan-wook"
]

titles_additional = [
    "The Godfather", "The Godfather Part II", "The Dark Knight Rises", "Gladiator",
    "The Silence of the Lambs", "Parasite", "Everything Everywhere All at Once", "Oppenheimer",
    "Dune", "Dune: Part Two", "The Wolf of Wall Street", "American Beauty",
    "Se7en", "Fight Club", "The Social Network", "The Revenant",
    "Braveheart", "Saving Private Ryan", "The Green Mile", "Schindler's List",
    "The Sixth Sense", "Unbreakable", "Split", "Glass",
    "The Usual Suspects", "Heat", "L.A. Confidential", "The Departed",
    "Mystic River", "Prisoners", "Sicario", "Wind River",
    "True Grit", "No Country for Old Men", "There Will Be Blood", "Phantom Thread",
    "The Master", "Whiplash", "La La Land", "Moonlight",
    "Black Panther", "Captain America: The Winter Soldier", "Iron Man", "Doctor Strange",
    "Thor: Ragnarok", "Avengers: Infinity War", "Avengers: Endgame", "Spider-Man: Into the Spider-Verse",
    "The Lego Movie", "Coco", "Inside Out", "Frozen",
    "Spirited Away", "Your Name", "A Silent Voice", "Makoto Shinkai Films",
    "The Hunger Games", "The Maze Runner", "Ready Player One", "Aquaman",
    "Wonder Woman", "Joker", "The Dark Knight", "Superman",
    "X-Men: Days of Future Past", "Deadpool", "Logan", "Eternals",
    "Black Widow", "Shang-Chi", "The Matrix Resurrections", "Twisters",
    "Asteroid City", "Poor Things", "Killers of the Flower Moon", "Barbie",
    "Oppenheimer", "The Brutalist", "Past Lives", "Anatomy of a Fall",
    "The Zone of Interest", "Sanctuary", "All of Us Strangers", "Saltburn",
    "Guardians of the Galaxy Vol. 3", "The Marvels", "Ant-Man: Quantumania", "Blue Beetle",
    "Dungeons & Dragons: Honor Among Thieves", "Five Nights at Freddy's", "Insidious", "Insidious: Chapter 2",
    "Conjuring 2", "Annabelle", "The Ring Two", "Sinister",
    "Hereditary", "Midsommar", "Candyman", "Get Out",
    "Us", "Nope", "A Clockwork Orange", "2001: A Space Odyssey",
    "Blade Runner", "Blade Runner 2049", "Alien", "Aliens",
    "The Thing", "The Fly", "The Elephant Man", "Videodrome",
    "Eraserhead", "Mulholland Drive", "Inland Empire", "The Straight Story",
    "Blue Velvet", "Twin Peaks: Fire Walk with Me", "Wild at Heart", "The Elephant Man",
    "Stalker", "Solaris", "Andrei Rublev", "Mirror",
    "Seven Samurai", "Rashomon", "Ikiru", "Sanjuro",
    "Pan's Labyrinth", "The Devil's Backbone", "Crimson Peak", "Nightmare Alley",
    "The Shape of Water", "Guillermo del Toro's Pinocchio", "Swamp Thing", "Creature from the Black Lagoon",
    "Frankenstein", "The Mummy", "Dracula", "The Invisible Man",
    "The Wolf Man", "The Phantom of the Opera", "Nosferatu", "The Cabinet of Dr. Caligari",
    "Metropolis", "The Golem", "The Student of Prague", "The Waxworks",
    "M", "The Hands of Orlac", "The Last Laugh", "Sunrise",
    "The Passion of Joan of Arc", "L'Atalante", "Un Chien Andalou", "L'Age d'Or",
    "L'avventura", "La Dolce Vita", "8½", "Amarcord",
    "The Night of the Hunter", "Kiss Me Deadly", "Out of the Past", "The Big Sleep",
    "Double Indemnity", "The Killers", "Gun Crazy", "In a Lonely Place",
]

# Generate 500+ movies
np.random.seed(42)
random.seed(42)

all_movies = movies_data.copy()

for i in range(len(movies_data), 520):
    title = titles_additional[i % len(titles_additional)]
    if i >= len(titles_additional):
        title = f"{titles_additional[i % len(titles_additional)]} {i // len(titles_additional)}"
    
    movie = {
        "title": title,
        "genre": random.choice(genre_combinations),
        "year": random.randint(1970, 2024),
        "rating": round(random.uniform(5.5, 9.9), 1),
        "director": ", ".join(random.sample(directors, random.randint(1, 2))),
        "plot": f"An engaging story about {['adventure', 'mystery', 'romance', 'survival', 'discovery', 'transformation'][random.randint(0, 5)]} that captivates audiences with compelling characters and unexpected twists.",
        "runtime": random.randint(80, 180),
        "cast": ", ".join([f"Actor {j}" for j in range(random.randint(3, 5))]),
        "budget": random.randint(10000000, 300000000),
        "revenue": random.randint(50000000, 3000000000),
    }
    all_movies.append(movie)

# Remove duplicates based on title
df = pd.DataFrame(all_movies)
df = df.drop_duplicates(subset=['title'], keep='first')

# Save to CSV
df.to_csv('movies.csv', index=False)

print(f"✅ Generated {len(df)} movies successfully!")
print(f"Dataset saved to movies.csv")
print("\nDataset Preview:")
print(df.head())
print(f"\nDataset shape: {df.shape}")
