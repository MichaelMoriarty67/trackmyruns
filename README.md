# TrackMyRuns
🏃‍♀️ **WHAT?** TrackMyRuns is a full stack app for tracking exercise routes that I built to learn more about RESTful API design. 
The app allow users to stream geolocation time-series data from client to server while moving to build a 'RunMap'.
RunMaps get plotted against a map by the client to visualize exercise routes.
Additional features includes the ability to authenticate as user, see your aggregated exercise data, and see details analytics on specific runs.  

📖 **WHAT I LEARNED?** I purposfully did not use Django REST Framework to learn more about _request parsing_, _data serialization_, and _response formatting_.

*p.s. yes... I'm a Strava fanboy if you're wondering.*

**Frontend**: React  
**Backend**: Django  
**Database**: PostgreSQL  

## Milestones
- [x] Django, PostgreSQL, & SQL basics
- [x] Database tables designed & Django Models created
- [x] API Spec designed, built with Django Views, and tested via Postman
- [ ] Add Authentication
- [ ] Design & build basic frontend to consume API (Mobile first design)


## Backend API Spec
| HTTP Method | Endpoint                   | Description                            |
|-------------|----------------------------|----------------------------------------|
| POST        | api/runs                   | Creates a new run                      |
| GET         | api/runs                   | Gets a list of all runs               |
| GET         | api/runs/{run_id}          | Gets a specific run                    |
| PUT         | api/runs/{run_id}          | Updates a run (adds to its RunMap)     |
| DELETE      | api/runs/{run_id}          | Deletes a specific run                 |
| GET         | api/runs/{runs_id}/map     | Gets a run's RunMap(s)                |
| POST        | api/runs/{runs_id}/map     | Adds n rows to a RunMap                |
| GET         | api/user/{user_id}         | Gets all information about a user      |
| GET         | api/user/{user_id}/runs    | Gets all runs from a specific user     |
| POST        | api/user                   | Creates a new user                     |
| PATCH       | api/user/{user_id}         | Updates information about a user       |



