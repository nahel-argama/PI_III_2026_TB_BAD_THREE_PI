import os
import uvicorn

def main():
    # Valores padrão
    port = 8002
    host = "127.0.0.1"
    
    # Lendo o arquivo .env manualmente para evitar a necessidade do pacote python-dotenv
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                # Ignora linhas vazias e comentários
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key, val = key.strip(), val.strip()
                    
                    if key == "PORT":
                        port = int(val)
                    elif key == "HOST":
                        host = val
                        
    print(f"🚀 Iniciando servidor em http://{host}:{port} (com reload ativado)...")
    
    # O equivalente a rodar: uvicorn src.main:app --reload --host <host> --port <port>
    uvicorn.run("src.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
