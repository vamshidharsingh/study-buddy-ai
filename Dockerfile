## Parent image
FROM python:3.10-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container # the name is app 
WORKDIR /app 

## Installing system dependancies which are required
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying ur all contents from local to app
COPY . .

## Run setup.py 3# previous catch is revmovd
RUN pip install --no-cache-dir -e .

# Used PORTS since steam let run on  8501 
EXPOSE 8501

# Run the app   # 0.0.0.0  our application can  be accessed by any addressed , server headless  there can be issues while opeining the steamlet 
CMD ["streamlit", "run", "application.py", "--server.port=8501", "--server.address=0.0.0.0","--server.headless=true"]