import os
import logging
import requests
from groq import Groq, GroqError
from functools import lru_cache
import streamlit as st


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GroqLLM:
    def __init__(self, model: str = "llama3-8b-8192"):
        api_key = st.secrets["GROQ_API_KEY"]
        if not api_key:
            logging.error("GROQ_API_KEY environment variable not found.")
            raise ValueError("API key for Groq is not set. Please set the GROQ_API_KEY environment variable.")
        
        try:
            self.client = Groq(api_key=api_key)
            self.model = model
            logging.info(f"GroqLLM initialized with model: {self.model}")
        except GroqError as e:
            logging.error(f"Failed to initialize Groq client: {e}")
            raise

    def generate(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        logging.info(f"Generating response for model {self.model}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except GroqError as e:
            logging.error(f"API error during GroqLLM.generate: {e}")
            return "Error: Could not generate a response due to an API issue."
        except Exception as e:
            logging.error(f"An unexpected error occurred in GroqLLM.generate: {e}")
            return "Error: An unexpected error occurred while generating a response."

@lru_cache(maxsize=1)
def list_groq_models() -> list[str]:
    api_key = st.secrets["GROQ_API_KEY"]
    if not api_key:
        logging.warning("GROQ_API_KEY not found, cannot fetch models from API.")
        return ["llama3-8b-8192"]

    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        
        exclude_keywords = ['whisper', 'tts', 'guard']
        valid_models = [
            model["id"] for model in data
            if not any(keyword in model["id"].lower() for keyword in exclude_keywords)
        ]

        if not valid_models:
            logging.warning("No valid chat models found after filtering, returning a hardcoded default list.")
            return ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it", "mixtral-8x7b-32768"]

        logging.info(f"Successfully fetched and filtered Groq models: {valid_models}")
        return valid_models

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error fetching Groq models: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching Groq models: {e}")

    return ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it", "mixtral-8x7b-32768"]