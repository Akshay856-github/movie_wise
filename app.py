import streamlit as st
import pickle
import pandas as pd
import requests

# Load the pre-processed movie dictionary and convert it into a DataFrame
movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

# Load the similarity matrix
similarity=pickle.load(open('similarity.pkl','rb'))

# Hardcoded user credentials (for login/signup)
USER_CREDENTIALS = {
    "Akshay": "akshay@1234",
    "Aryan": "aryan@5678"
}
# Function to fetch the poster image from the TMDB API
def fetch_poster(movie_id):
    url= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a4f1238cfbf5ae44582df1d5f95ddb83&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Function to recommend movies based on the selected movie
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]]['id']
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_posters

# Main App UI after login
def main_app():
    # Add custom CSS for the logout button
    st.markdown("""
            <style>
            .logout-button {
                position: absolute;
                top: 20px;
                left: 20px;
                background-color: #ff4b4b;
                color: white;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                font-weight: bold;
                border-radius: 5px;
            }
            .logout-button:hover {
                background-color: #ff0000;
            }
            </style>
        """, unsafe_allow_html=True)

    # Display logout button
    col1, col2 = st.columns([8, 2])
    with col2:
     if st.button("Logout", key="logout", use_container_width=False):
        st.session_state.logged_in = False
        st.experimental_rerun()

    # App header and welcome message
    st.image("WatchWise Logo Design.png",width=120)
    st.title(f"Welcome, {st.session_state.username}!")
    st.subheader('Movie Recommendation System')

    # Dropdown to select a movie
    select_movie_name = st.selectbox(
    'Enter the Name of Movie',
    movies['title'].values
    )
    # Show recommendations when button is clicked
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(select_movie_name)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])




# Login Page UI
def login_page():
    # Center align the login box
    col1, col2, col3 = st.columns([1.5,1.2, 1])
    with col2:
     st.image("WatchWise Logo Design.png", width=120)


    st.title("Sign In")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Sign In and Sign Up buttons
    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col2:
     if st.button("Sign In"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

     if st.button("Sign Up"):
         st.session_state.page = 'signup'
         st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Signup Page UI
def signup_page():
    # Center align the signup box
    col1, col2, col3 = st.columns([1.5, 1.2, 1])
    with col2:
     st.image("WatchWise Logo Design.png", width=120)

    st.title("Sign Up")

    # Input fields for new username and password
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")

    # Create Account and Back to Sign In buttons
    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col2:
     if st.button("Create Account"):
        if new_username in USER_CREDENTIALS:
            st.error("Username already exists!")
        else:
            USER_CREDENTIALS[new_username] = new_password
            st.success("Account created successfully! Please sign in now.")
            st.session_state.page = 'login'
            st.experimental_rerun()

     if st.button("Back to Sign In"):
        st.session_state.page = 'login'
        st.experimental_rerun()

# --------- App Routing Section ---------

# Initialize session states if not already initialized
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'


# Based on login status, show appropriate page
if st.session_state.logged_in:
    main_app()
else:
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'signup':
        signup_page()
