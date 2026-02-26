# RAG for Job Retrieval using LangChain + Ollama

## Overview

This project aims to present a useful tool for IT professionals (software engineers, data scientist, and so on...) to search job offers and find out which technical skills are most in demand in the market.

This application get jobs dynamically on the main databases (Indeed, Linkedin, Google...), build a vector database using jobs descriptions, then use a local Ollama open-source model to run a Q&A bot allowing the user to chat with this roles - which can be useful for guiding professional development based on current market demands.

The interface was built in Streamlit, with features like job search, job skills analysis and the chatbot mentioned.

## How to Use

If you are using this on WSL and Ollama server is on Windows Host, running the following on Powershell (as Admin):
```
netsh interface portproxy add v4tov4 `
    listenaddress=0.0.0.0 `
    listenport=11434 `
    connectaddress=127.0.0.1 `
    connectport=11434
```

To run the app.py...

1. Install the dependencies on `requirements.txt` (make sure to use Python 3.8+)
2. Set up and start Ollama server on the host
3. Run `streamlit run app.py`
4. On *Overview* page, analyze job skills and ask to the chatbot for more details about these roles
5. On *Search* page, enter a job keyword and location in the input fields
6. Click the **Scrape Jobs** button to start the job search
7. Select a job offer so you can see it more details
