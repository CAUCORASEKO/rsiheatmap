# Crypto RSI Heatmap

This project displays a heatmap of the Relative Strength Index (RSI) for cryptocurrencies. It uses volume and RSI data to generate visualizations that help identify market trends.

## Credits

The original code for this project was created by [Stephan Akkerman](https://github.com/StephanAkkerman) and can be found in his original repository: [crypto-rsi-heatmap](https://github.com/StephanAkkerman/crypto-rsi-heatmap).

All credit for the original development of this code belongs to him.

## Modifications

To integrate this RSI heatmap into our Svelte project, we made the following modifications:

1. **CORS Configuration**: 
   - We enabled Cross-Origin Resource Sharing (CORS) in the `main.py` file to allow requests from our Svelte frontend hosted on a different domain. This was essential to avoid CORS errors when fetching the heatmap image.
   - We used the `flask-cors` package to handle CORS in Flask.

2. **Image Saving Path**:
   - We modified the path where the heatmap image is saved in `main.py` to ensure it is correctly referenced when the Flask server serves it.

3. **Frontend Integration**:
   - In our Svelte project, we created a new component that fetches the heatmap image from the deployed Flask server and displays it. The component uses `fetch` to request the image and handles the image rendering using Svelte's reactive features.

4. **Deployment on Railway**:
   - Both the Flask backend (for generating the RSI heatmap) and the Svelte frontend are deployed on [Railway](https://railway.app). The backend serves the heatmap image, which is fetched by the frontend.

## Usage

To run the RSI heatmap locally, follow these steps:

1. **Clone the Repository**:
  
   git clone https://github.com/your-username/crypto-rsi-heatmap.git
   cd crypto-rsi-heatmap

    Create and Activate a Virtual Environment:

  

python3 -m venv venv
source venv/bin/activate

Install Dependencies:



pip install -r requirements.txt

Run the Flask Server:



python src/main.py

Access the Heatmap:

    Open your browser and go to http://localhost:8080/ to see the heatmap.