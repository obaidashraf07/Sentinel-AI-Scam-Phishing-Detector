# Sentinel AI - Scam & Phishing Detector

A multilingual scam and phishing message detection system combining Data Science, Machine Learning, and Explainable AI (XAI).

## Project Overview

Sentinel AI is a machine learning-based application designed to analyze text messages and identify potential scam messages. It supports English and Roman Urdu and provides an interactive web interface for message analysis.

The project combines three major areas: Data Science, Machine Learning, and Explainable AI.

## Key Features

* English and Roman Urdu message analysis
* Text preprocessing and normalization
* Word-level and character-level TF-IDF feature extraction
* LinearSVC classification model
* Explainable AI with important word contributions
* Interactive Streamlit web application
* Scam indicators and safety recommendations
* Model evaluation and robustness testing
* Model performance visualizations

## Technologies Used

* Python
* Data Science
* Machine Learning
* Natural Language Processing (NLP)
* Pandas
* NumPy
* Scikit-learn
* TF-IDF
* LinearSVC
* Explainable AI (XAI)
* Streamlit
* Matplotlib
* Seaborn
* Joblib

## Project Structure

```text
Scam_Phishing_Detector/
│
├── app.py
├── train_model.py
├── text_preprocessing.py
├── explain_model.py
├── attack_testing.py
├── requirements.txt
│
├── dataset/
│   ├── SMSSpamCollection
│   └── roman_urdu_messages.csv
│
├── models/
│   └── multilingual_scam_detector.pkl
│
└── results/
    ├── confusion_matrix.png
    ├── model_performance.png
    └── other evaluation results
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/obaidashraf07/Sentinel-AI-Scam-Phishing-Detector.git
```

### 2. Open the Project Directory

```bash
cd Sentinel-AI-Scam-Phishing-Detector
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your web browser.

**Note:** The trained model file must be available in the expected location for the application to run. If it is not included in the repository, train the model using the provided training script.

## How the System Works

1. The user enters a text message.
2. The system preprocesses and normalizes the text.
3. TF-IDF extracts word-level and character-level features.
4. The trained LinearSVC model classifies the message.
5. The application displays the prediction and safety recommendations.
6. The explanation panel displays important word-level feature contributions to help interpret the prediction.

## Three Main Project Areas

### 1. Data Science

* Dataset preparation and cleaning
* Text preprocessing
* Exploratory data analysis
* Model evaluation
* Performance visualization

### 2. Machine Learning

* TF-IDF feature extraction
* Word and character n-grams
* LinearSVC classification
* Model testing and comparison
* Robustness evaluation

### 3. Explainable AI

* Word-level feature contributions
* Interpretation of model predictions
* Identification of influential message terms

## Limitations

* Predictions may be incorrect.
* A message classified as normal is not guaranteed to be safe.
* Performance may vary on unfamiliar messages and new scam patterns.
* The system should be used as an assistance tool rather than a replacement for official security verification.

## Disclaimer

Sentinel AI is an educational project intended to support scam awareness. Always verify suspicious messages through official channels. Never share passwords, PINs, or OTPs in response to suspicious messages.

## Author

Obaid Ashraf
