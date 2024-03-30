import pickle
import streamlit as st
import requests

def recommend(movie):
    index = movies[movies['Name'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    year=[]
    rating=[]
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(movies.iloc[i[0]].img)
        recommended_movie_names.append(movies.iloc[i[0]].Name)
        year.append(movies.iloc[i[0]].Year)
        rating.append(movies.iloc[i[0]].Rating)

    return recommended_movie_names,recommended_movie_posters,year,rating
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://media.istockphoto.com/id/165596429/vector/35mm-motion-picture-film.jpg?s=612x612&w=0&k=20&c=HUQFwuJH22OZyOnMfCejb6qH5lwIjlOn4fSxY6sMFK8=");
background-size: 120%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.header("**:white[CONTENT BASED MOVIE RECOMMENDATION]**")
movies = pickle.load(open('Desktop/pkl/movie_list.pkl','rb'))
similarity = pickle.load(open('Desktop/pkl/similarity.pkl','rb'))

movie_list = movies['Name'].values
selected_movie = st.selectbox(
    " Select the movie you have watched recently ",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters,year,rating = recommend(selected_movie)
    st.markdown("<h4 style='text-align: left; color: black;'> Have a look on these movies too, </h4>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.text("Year:"+ year[0])
        st.text("Rating:"+rating[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.text("Year:"+ year[1])
        st.text("Rating:"+rating[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.text("Year:"+ year[2])
        st.text("Rating:"+rating[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.text("Year:"+ year[3])
        st.text("Rating:"+rating[3])        
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.text("Year:"+ year[4])
        st.text("Rating:"+rating[4])

