FROM python:3.11  
  
WORKDIR /app  
  
# Install dependencies  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  
  
# Copy the rest of the code  
COPY . .  
  
# Create necessary directories  
RUN mkdir -p /app/models /app/data  
  
EXPOSE 8000  
  
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]