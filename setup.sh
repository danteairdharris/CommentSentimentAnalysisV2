mkdir -p ~/.streamlit/

echo "[theme]
base='dark'
primaryColor='#4833f6'
backgroundColor='#000000'
[server]
port = $PORT
enableCORS = false
headless = true

" > ~/.streamlit/config.toml
