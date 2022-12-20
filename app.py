import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title='Sentiment Analysis Demo')

from selenium import webdriver
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pickle
from selenium.webdriver.chrome.options import Options
import os, sys
from webdriver_manager.chrome import ChromeDriverManager


def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_sent(pred):
    if np.argmax(pred) == 0:
        return 'negative'
    else: 
        return 'positive'
    
def scrapecomments(title, param):
    global log_container
    global thumbnail_container
    global score_container
    wait = WebDriverWait(driver,15)
    start = time.perf_counter()
    
    log_container.write('Searching...')
    driver.get('https://www.youtube.com/results?search_query={}'.format(str(title+" Official Trailer")))
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="thumbnail"]/yt-image/img')))
    images = driver.find_elements(By.XPATH, '//*[@id="thumbnail"]/yt-image/img')
    thumbnail_container.image(images[1].get_attribute('src'))
    videos = driver.find_elements(By.ID,'video-title')
    video = videos[1].get_attribute('href')
    
    driver.get(video)  
    time.sleep(2)
    log_container.write('Scraping...')
    comments=[]

    for item in range(param): 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME,                "body"))).send_keys(Keys.END)

    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))):
          comments.append(comment.text)                                                                                                          
    comments = comments[:param]
    df_comments = pd.DataFrame(comments,columns=['comment'])
    dataframe_container.dataframe(data=df_comments, use_container_width=True, height=300)
    
    log_container.write('Sentiment Analysis...')
    sent = sk_test(comments)
    count = 0
    for s in sent:
        if s == 'positive':
            count += 1
    score = '{sentiment:0.2f}'.format(sentiment=(count/len(comments)))
    score_container.metric(label="Sentiment Score", value=score)
    
    data = []
    for i, j in zip(comments, sent):
        data.append([i, j])
        
    dataframe_container.dataframe(data=data, use_container_width=True, height=300)
        
    end = time.perf_counter()
    txt = "Finished in {time:0.2f} seconds.".format(length = len(comments), time = (end-start))
    log_container.write(txt)



def sk_test(corpus):
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(fit_vec)
    test_vec = vectorizer.transform(corpus)
    pred = model.predict(test_vec)
    return pred

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


model = load_data('./logreg_model.pickle')
fit_vec = load_data('./fit_vector.pickle')

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: black;'>About</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Type in a movie title into the search bar and press 'Search'.</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>The comments from the YouTube trailer regarding the title you searched will be scraped and evaluated for sentiment. A number between 0 and 1 will show up on the right side of the screen which represents the overall sentiment score (closer to 1 is positive).</h2>", unsafe_allow_html=True)
    
top_container = st.empty()
bot_container = st.empty()
col1, col2, col3 = top_container.columns([2, 1, 1])


with bot_container:
    st.header('Comments')
    dataframe_container = st.empty()
    
with top_container:
    with col3:
        score_container = st.empty()
    with col2:
        thumbnail_container = st.empty()
        log_container = st.empty()

    with col1:
        with st.form('YouTube Comment Scraper'):
            title = st.text_input(label='Movie Title', max_chars=70)
            param = st.slider(label='Select amount of comments', min_value=0, max_value=100, value=20, key=4)
            search = st.form_submit_button('Search')


        if search and len(title) > 0:

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(
                options=chrome_options,
                service=service,
            )
            scrapecomments(title, param)
            driver.quit()
            
            
    
  

    
        
    