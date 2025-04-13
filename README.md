# Comment System with Toxicity Detection

A web application that allows users to post comments with automatic toxicity detection using a pre-trained LSTM model.

## Features

- Modern UI inspired by YouTube and Twitter
- Real-time comment posting
- Automatic toxicity detection
- Toxic comments are automatically filtered
- User authentication
- Responsive design

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SQLite (included with Python)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the Django development server:
```bash
python manage.py runserver
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8000
```

3. To access the admin interface, go to:
```
http://127.0.0.1:8000/admin
```

## Project Structure

- `comments/` - Main application directory
  - `models.py` - Database models
  - `views.py` - API endpoints and toxicity detection
  - `urls.py` - URL routing
- `templates/` - HTML templates
  - `index.html` - Main page template
- `comment_system/` - Project configuration
  - `settings.py` - Django settings
  - `urls.py` - Main URL configuration

## How It Works

1. Users can post comments through the web interface
2. Each comment is automatically checked for toxicity using the LSTM model
3. Toxic comments are marked and filtered out
4. Non-toxic comments are displayed in the comment feed

## Contributing

## Find Toxic Comments 

Insult + Toxic:
"You're such a stupid idiot who doesn't know anything about this topic. Your opinion is completely worthless."
Threat + Severe Toxic:
"I'm going to find you and make you pay for what you've done. You better watch your back."
Obscene + Identity Hate:
"You're a disgusting piece of trash who shouldn't even be allowed to speak. People like you are the problem."
Multiple Categories:
"This is the most idiotic and worthless content I've ever seen. The creator is a complete moron who should be ashamed."
Severe Toxic + Threat:
"You're a complete waste of space and I hope something terrible happens to you. You deserve to suffer."
Identity Hate + Insult:
"People like you are the reason this world is going to hell. You're a disgrace to humanity."
Obscene + Toxic:
"This is absolute garbage and the person who made it is a complete idiot. What a waste of time."
Threat + Identity Hate:
"I'll make sure you never show your face here again. People like you don't belong in this community."
Severe Toxic + Obscene:
"This is the most disgusting and terrible thing I've ever seen. The creator should be ashamed of themselves."
Multiple Categories (High Toxicity):
"You're a complete waste of oxygen and I hope you suffer for what you've done. People like you are the reason this world is going to hell."

Feel free to submit issues and enhancement requests! 