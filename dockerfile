FROM python:3.11

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

EXPOSE 8000

# This must be on one line to avoid "Unknown instruction" errors
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]