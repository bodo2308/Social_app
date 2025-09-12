# Social Network App 


### Step 1: Clone the Repository

```bash
# Copy the repository URL from GitHub
git clone https://github.com/YOUR_USERNAME/social_app.git

# Navigate to the project directory
cd social_app
```

### Step 2: Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate


### Step 3: Install Dependencies

```bash
# Install required packages
# Navigate to the project directory
cd social_app
pip install -r requirements.txt
```

### Step 4: Set Up Database

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate

# Create a superuser account (optional)
python manage.py createsuperuser
```

### Step 5: Run the Development Server

```bash
# Start the development server
python manage.py runserver
```

### Step 6: Access the Application

Open your web browser and go to: `http://127.0.0.1:8000/`


## 🔧 Development Commands

```bash
# Run the development server
python manage.py runserver

# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create a superuser
python manage.py createsuperuser




1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request


