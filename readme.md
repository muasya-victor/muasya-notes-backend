# Muasya Notes


## Prerequisites

- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Google Developer Console API credentials (Client ID and Secret)
  
## Setup Instructions

### 1. Set Up API
1. Create Virtual environment
    #### windows 
    ```` bash 
        python -m venv env
2. Activate it 
    ### windows
   ````bash
    env/scripts/activate
3. Install requirements
    ````bash 
   pip install -r requirements.txt


### SET UP DB
1. ``` bash
   flask db init
2. ```` bash
   flask db migrate -m "Initial migration"
3. ```` bash
   flask db upgrade
   
### Updating db 
1. ```` bash
    flask db migrate -m "Description of the changes"
2. ```` bash 
   flask db upgrade

### downgrading db
1. ```` bash 
        flask db downgrade

### Run Server
 ```` bash 
    flask run

#   m u a s y a - n o t e s - b a c k e n d  
 