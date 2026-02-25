import requests
import subprocess

def get_windows_ip():
    cmd = "ip route show | grep default | awk '{print $3}'"
    return subprocess.check_output(cmd, shell=True).decode().strip()


def process_text_with_ollama(text, prompt="Summarize:", model="qwen3:8b"):

    win_ip = get_windows_ip()
    print(win_ip)
    url = f"http://{win_ip}:11434/"

    response = requests.get(url, timeout=3)
    print(response)

    url = f"http://{win_ip}:11434/api/generate"
    
    print(f"Tentando conectar ao Windows em: {url}")
    payload = {
        "model": model,
        "prompt": f"{prompt}\n\n{text}",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        print(f"Erro: {e}")
        return None