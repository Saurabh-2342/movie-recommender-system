# Movie Recommender System

A movie recommendation app built with Streamlit that suggests similar movies based on user input. It displays movie posters, IMDb links, genres, and trailers using The Movie Database (TMDb) API.

## Features
- Recommend similar movies based on user-selected input.
- Display movie posters with clickable links to IMDb.
- Show genres for each recommended movie.
- Provide links to trailers on YouTube.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

   git clone https://github.com/yourusername/movie-recommender-system.git
   cd movie-recommender-system


2. Install the required packages:

   pip install -r requirements.txt


3. Make sure you have a valid TMDb API key. Update the API key in the code where necessary.

## Usage

To run the app, use the following command:


streamlit run app.py


After running the command, open your web browser and go to `http://localhost:8501` to view the application.

## Technologies Used
- Python
- Streamlit
- Requests
- TMDb API

## API Information
This project uses the [TMDb API](https://www.themoviedb.org/documentation/api) for fetching movie data. You will need to obtain an API key and update the code with your key for it to function correctly.

## Contributing
Contributions are welcome! If you have suggestions for improvements or want to add features, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
