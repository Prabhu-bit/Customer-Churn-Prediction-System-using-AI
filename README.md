# Customer-Churn-Prediction-System-using-AI

A production-style machine learning project that predicts customer churn and generates personalized AI retention emails for at-risk customers.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Status](https://img.shields.io/badge/Status-Ready-success)

## Overview

Customer churn is a major business problem in telecom and subscription-based services. Losing existing customers is often more expensive than acquiring new ones, so early churn detection is critical.

This project solves that problem by combining:
- A trained churn prediction model
- A Streamlit dashboard for interactive prediction
- A FastAPI backend for API access
- An LLM-powered retention email generator for medium and high-risk customers

## Problem Statement

The goal is not only to predict whether a customer may churn, but also to turn that prediction into an actionable business response.

This project helps businesses:
- Detect churn risk early
- Classify customers into low, medium, and high risk
- Generate a human-style retention email for at-risk customers
- Use AI in a practical, enterprise-style workflow instead of a chatbot

## How It Works

1. The user enters customer account details in the dashboard.
2. The model processes the input and predicts churn probability.
3. The app assigns a risk category based on the probability.
4. If the customer is medium or high risk, the app generates a personalized retention email.
5. The email appears directly below the prediction results in the Make Prediction tab.

## Technical Stack

- Python
- Streamlit
- FastAPI
- scikit-learn
- pandas
- numpy
- joblib
- requests
- OpenAI API for LLM-based retention suggestions

## Model Background

The active inference model used by the main Streamlit app is:

- `final_optimized_churn_model_reduced.pkl`

This project uses a reduced-feature scikit-learn MLP-based classifier for churn prediction.

### Inference Flow
- User input
- Feature preparation
- Preprocessing
- Model prediction
- Probability scoring
- Risk thresholding
- LLM retention suggestion for higher-risk customers

## Risk Thresholds

The current prediction thresholds are:

- Low Risk: churn probability below `0.35`
- Medium Risk: churn probability from `0.35` up to below `0.70`
- High Risk: churn probability `0.70` and above

These thresholds drive both the UI label and the LLM retention behavior.

## LLM Retention Suggestions

The LLM feature is designed as an enterprise automation workflow, not a chatbot.

It generates:
- A human-style retention email draft
- A different tone for medium-risk and high-risk customers
- A ready-to-copy message shown below the prediction result

If `OPENAI_API_KEY` is not set, the app still runs and uses a local fallback message.

## Project Structure

- `run_app.py` - Universal launcher for the Streamlit app
- `08_Applications_UI_API/streamlit_app.py` - Main Streamlit dashboard
- `08_Applications_UI_API/fastapi_server.py` - FastAPI backend
- `reduced_model_utils.py` - Input preparation for the reduced model
- `evaluation_utils.py` - Model evaluation helpers
- `07_Models_Trained/final_optimized_churn_model_reduced.pkl` - Active inference model
- `07_Models_Trained/model_metadata.json` - Feature metadata
- `05_Data_Splits/` - Train/test split files
- `03_Visualizations_Charts/` - Evaluation charts and visuals
- `01_Documentation/` - Reports, guides, and summaries
- `requirements.txt` - Python dependencies

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPO_URL>
cd Internship_Project
