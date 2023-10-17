# TrackMyRuns
![tmr-wireframe-ui-2](https://github.com/MichaelMoriarty67/trackmyruns/assets/86428098/d6fd7b9d-9060-41c9-975a-344a1cf5d4af)
*Wireframe of what TMR web app (mobile) will look like... *if I get around to it**

### Table of Contents
1. [Project Summary](#project-summary)
2. [Milestones](#milestones)
3. [Backend API Spec](#backend-api-spec)
4. [Setup](#setup)

## Project Summary
🏃‍♀️ **WHAT?** TrackMyRuns is a full stack app for tracking exercise routes that I built to learn more about RESTful API design. The app allow users to stream geolocation time-series data from client to server while moving to build a 'RunMap'. RunMaps get plotted against a map by the client to visualize exercise routes (not done yet).  

Additional features includes:
- User authentication via **Firebase**
- Custom Authorization logic for each endpoint
- Resuable RESTful endpoints class (replacement for Django REST Framework)  

📖 **WHAT I LEARNED?** I purposfully did not use Django REST Framework to learn more about _request parsing_, _data serialization_, and _response formatting_.  

🏗️ **APP STACK**  
Frontend: React  
Backend: Django  
Database: PostgreSQL  

## Milestones
- [x] Django, PostgreSQL, & SQL basics
- [x] Database tables designed & Django Models created
- [x] API Spec designed, built with Django Views, and tested via Postman
- [x] Add Authentication & Authorization
- [ ] Design & build basic frontend to consume API (Mobile first design)


## Backend API Spec
| HTTP Method | Endpoint                   | Description                                   |
|-------------|----------------------------|-----------------------------------------------|
| POST        | api/runs                   | Creates a new run for an authenticated user   |
| GET         | api/runs                   | Gets a list of all runs for an authenticated user |
| GET         | api/runs/{run_id}          | Gets a specific run for an authenticated user |
| DELETE      | api/runs/{run_id}          | Deletes a specific run for an authenticated user |
| GET         | api/runs/{run_id}/map     | Gets a run's RunMap(s) for an authenticated user |
| POST        | api/runs/{run_id}/map     | Adds n rows to a RunMap for an authenticated user |
| POST        | api/register               | Calls Firebase to create a new user and creates a new Runner |
| GET         | api/user                   | Gets information about the authenticated user |
| PATCH       | api/user                   | Updates information about the authenticated user |

## SETUP
 1. Make sure you have both Python and Node installed
 2. (Optionally) Start a python virtual environment in the top level dir
 3. Install the server dependencies by running `pip install -r requirements.txt`
 4. Install the client dependencies by running `cd client && npm install`
 5. Migrate back to the top level dir and start the backend dev server with `python manage.py runserver`
 6. In a seperate shell process, migrate to the `client` dir and start the client dev server with `npm start`
 7. Your client is now avial on `localhost:3000` and server is running on `localhost:8000`! 🥳



