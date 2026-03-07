# Footyapp Backend - REST API

This is the Footyapp backend. This was rewritten from scratch to breakdown the original Footyapp monolith to benefit from the following 3 tier application princeiples.

# 3-Tier RESTful Application Principles:

## 1. Separation of Concerns:
- **Presentation Layer (Web)**: Handles the user interface and user experience. Responsible for displaying information to users and gathering user input. Built with Flask templates.
- **Application Layer (API)**: Business logic and operations. Offers an interface to the client via RESTful endpoints. Manages data transformation and processing. Implemented using Flask routes.
- **Data Layer (Database)**: Data persistence and storage. MongoDB serves as the NoSQL database to store, retrieve, and manage data.

## 2. Statelessness:
- Every HTTP request from the client to server should contain all the information needed to understand and process the request.

## 3. Modularity:
- Develop the application in distinct modules to promote reusability and ease of maintenance.

## 4. Scalability:
- Design the application to easily handle an increase in user load by potentially scaling horizontally (adding more servers).

## 5. Data Integrity:
- Ensure that the data stored in MongoDB is valid, consistent, and accurate.

## 6. Security:
- Implement authentication and authorisation mechanisms.
- Use HTTPS for secure communication.
- Sanitise user inputs to prevent SQL (or NoSQL) injection attacks.
- Handle and store passwords securely (hashing & salting).

## 7. Error Handling:
- Gracefully handle exceptions and errors at all layers. Provide meaningful error messages to clients.

## 8. Performance Optimisation:
- Efficiently use database indices in MongoDB to speed up queries.
- Minimise payload sizes, and consider caching frequently used data.
- Optimise Flask routes and operations for performance.

## 9. API Versioning:
- To maintain backward compatibility, versions of your API can be defined, allowing older apps to function without modifications.

## 10. Documentation:
- Maintain clear and comprehensive documentation for API endpoints, usage, and data models.

## 11. Testing:
- Implement unit, integration, and system tests to ensure application stability and correctness. Utilise tools like `pytest` for testing.

## 12. Continuous Integration & Continuous Deployment (CI/CD):
- Automate testing and deployment processes to ensure code quality and quick, reliable releases.


# Using the API

## Create tokens first

This API uses static tokens for each frontend. Generate a token and save in a .env file.
An example-env file is included to show the vars needed.

```
BOT_TOKEN=your-long-token
WEB_TOKEN=your-other-long-token
```

## Create the init-mongo.js and edit the docker-compose.yml

An example of the init-mongo.js is included.

```
version: '3.8'

services:
  footyapp-api:
    image: ghcr.io/bignellrp/footyapp-api:main
    container_name: footyapp-api-${BRANCH}
    networks:
      br0:
        ipv4_address: {your-web-ip}
    ports:
      - "8080:80"
    restart: always
    env_file:
      - /mnt/docker/footyapp-api/.env
    depends_on:
      - mongodb

  mongodb:
    image: mongo:7.0
    networks:
      br0:
        ipv4_address: {your-mongo-ip}
    ports:
      - "27017:27017"
    restart: always
    env_file:
      - {your-local-envfolder}.env
    volumes:
      - {your-local-mongofolder}/mongodb_data:/data/db
      - {your-local-mongofolder}/init-mongo.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
networks:
  br0:
    external: true
    name: br0
```

# API Documentation for Game Management

This API provides endpoints for managing and retrieving game statistics. It allows you to perform various operations such as getting game information, updating game scores, swapping players, and more. Below are the available routes and how to use them:

### Get All Games

**Endpoint:** `/games`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve a list of all games with their information.

**Request:**
```http
GET /games
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "date": "2023-08-30",
    "teamA": ["Player 1", "Player 2"],
    "teamB": ["Player 3", "Player 4"],
    "scoreTeamA": 3,
    "scoreTeamB": 2,
    "totalTeamA": 100,
    "totalTeamB": 80,
    "colourTeamA": "red",
    "colourTeamB": "blue"
  }
]
```

### Get Game Statistics

**Endpoint:** `/games/game_stats`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve game statistics, including dates and scores, sorted by date in descending order.

**Request:**
```http
GET /games/game_stats
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "date": "2023-08-30",
    "scoreTeamA": 3,
    "scoreTeamB": 2,
  },
  {
    "date": "2023-08-23",
    "scoreTeamA": 3,
    "scoreTeamB": 2,
  },
  {
    "date": "2023-08-16",
    "scoreTeamA": 3,
    "scoreTeamB": 2,
  }
]
```

### Get Player's Wins

**Endpoint:** `/games/wins/<player>`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Get the number of games won by a specific player. Updates the player's win count.

**Request:**
```http
GET /games/wins/Player1
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
{
  "wins": 10
}
```

### Update Game Score

**Endpoint:** `/games/updatescore/<date>`  
**Method:** `PUT`  
**Protected:** Yes (TOKEN Required)  
**Description:** Update the scores of a game and calculate statistics for the players involved.

**Request:**
```http
PUT /games/updatescore/2023-08-30
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "scoreTeamA": 4,
  "scoreTeamB": 4
}
```

**Response:**
```json
{
  "message": "Game updated successfully"
}
```

### Get Most Recent Game

**Endpoint:** `/games/most_recent_game`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve information about the most recent game played.

**Request:**
```http
GET /games/most_recent_game
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "date": "2023-08-30",
    "teamA": ["Player 1", "Player 2"],
    "teamB": ["Player 3", "Player 4"],
    "scoreTeamA": 3,
    "scoreTeamB": 2,
    "totalTeamA": 100,
    "totalTeamB": 80,
    "colourTeamA": "red",
    "colourTeamB": "blue"
  }
]
```

### Swap Players in a Game

**Endpoint:** `/games/swap_player`  
**Method:** `PUT`  
**Protected:** Yes (TOKEN Required)  
**Description:** Swap a player's position with a new player in the most recent game. Update team composition and game totals accordingly.

**Request:**
```http
PUT /games/swap_player
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "current_player": "CurrPlayer",
  "new_player": "NewPlayer"
}
```

**Response:**
```json
{
  "message": "Player swapped and totals updated successfully"
}
```

### Update Score

**Endpoint:** `/games/updatescore/<date>`  
**Method:** `PUT`  
**Protected:** Yes (TOKEN Required)  
**Description:** Update an existing game's score using the specified date. Once scores saved this function also runs the wins/draws/losses formulas for each player. 3 points for a win, 1 for a draw, 0 for a loss, games played +1, winpercentage.

**Request:**
```http
PUT /games/updatescore2023-09-01
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "scoreTeamA": 3,
  "scoreTeamB": 3
}
```

**Response:**
```json
{
  "message": "Game updated successfully"
}
```

### Add New Game

**Endpoint:** `/games`  
**Method:** `POST`  
**Protected:** Yes (TOKEN Required)  
**Description:** Add a new game record to the database.

**Request:**
```http
POST /games
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "date": "2023-09-01",
  "teamA": ["Player 5", "Player 6"],
  "teamB": ["Player 7", "Player 8"],
  "scoreTeamA": 2,
  "scoreTeamB": 3,
  "totalTeamA": 90,
  "totalTeamB": 95,
  "colourTeamA": "green",
  "colourTeamB": "yellow"
}
```

**Response:**
```json
{
  "_id": "YOUR_GENERATED_ID",
  "message": "Game added successfully"
}
```

### Update Game

**Endpoint:** `/games/<date>`  
**Method:** `PUT`  
**Protected:** Yes (TOKEN Required)  
**Description:** Update an existing game's information using the specified date.

**Request:**
```http
PUT /games/2023-09-01
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "scoreTeamA": 3,
  "scoreTeamB": 3
}
```

**Response:**
```json
{
  "message": "Game updated successfully"
}
```

### Delete Game

**Endpoint:** `/games/<date>`  
**Method:** `DELETE`  
**Protected:** Yes (TOKEN Required)  
**Description:** Delete a game record from the database using the specified date.

**Request:**
```http
DELETE /games/2023-09-01
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
{
  "message": "Game deleted successfully"
}
```

# API Documentation for Player Management

This API provides endpoints for managing and retrieving player statistics. It enables various operations such as getting player information, updating player data, deleting players, and more. Below are the available routes and how to use them:

### Get All Players

**Endpoint:** `/players`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve a list of all players with their statistics.

**Request:**
```http
GET /players
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1",
    "total": 77,
    "wins": 5,
    "draws": 3,
    "losses": 2,
    "score": 16,
    "playing": true,
    "played": 10,
    "percent": 50,
    "winpercent": 50
  },
]
```

### Get Player Names

**Endpoint:** `/players/player_names`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve a list of player names and their playing status.

**Request:**
```http
GET /players/player_names
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1",
    "playing": true
  },
]
```

### Get All Player Totals

**Endpoint:** `/players/all_players`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve a list of all player names and their total scores.

**Request:**
```http
GET /players/all_players
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1",
    "total": 77
  },
]
```

### Get Player Stats

**Endpoint:** `/players/player_stats`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve detailed statistics for each player, including wins, draws, losses, score and winpercentage.

**Request:**
```http
GET /players/player_stats
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1",
    "wins": 5,
    "draws": 3,
    "losses": 2,
    "score": 16,
    "winpercent": 50
  },
]
```

### Get Leaderboard

**Endpoint:** `/players/leaderboard`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve a leaderboard of the top 10 players based on their scores.

**Request:**
```http
GET /players/leaderboard
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1",
    "score": 99
  },
  {
    "name": "Player 2",
    "score": 88
  },
  {
    "name": "Player 3",
    "score": 77
  },
  {
    "name": "Player 4",
    "score": 66
  },
]
```

### Get Win Percentages

**Endpoint:** `/players/winpercentage`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve win percentages for each player.

**Request:**
```http
GET /players/winpercentage
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1",
    "winpercent": 99
  },
  {
    "name": "Player 2",
    "winpercent": 88
  },
  {
    "name": "Player 3",
    "winpercent": 77
  },
  {
    "name": "Player 4",
    "winpercent": 66
  },
]
```

### Get Game Player Tally

**Endpoint:** `/players/game_player_tally`  
**Method:** `GET`  
**Protected:** Yes (TOKEN Required)  
**Description:** Retrieve a list of players currently playing in games. e.g if playing is true

**Request:**
```http
GET /players/game_player_tally
Authorization: Bearer YOUR_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1"
  },
  {
    "name": "Player 2"
  },
  {
    "name": "Player 3"
  },
  {
    "name": "Player 4"
  },
]
```

### Add New Player

**Endpoint:** `/players`  
**Method:** `POST`  
**Description:** Add a new player with specified attributes.

**Request:**
```http
POST /players
Content-Type: application/json

{
  "name": "New Player",
  "total": 0,
  "wins": 0,
  "draws": 0,
  "losses": 0,
  "score": 0,
  "playing": true,
  "played": 0,
  "percent": 0,
  "winpercent": 0
}
```

**Response:**
```json
{
  "_id": "YOUR_GENERATED_ID",
  "message": "Player added successfully"
}
```

### Update All Players

**Endpoint:** `/players`  
**Method:** `PUT`  
**Protected:** Yes (TOKEN Required)  
**Description:** Update attributes for all players.

**Request:**
```http
PUT /players
Content-Type: application/json

{
  "name": "New Player",
  "total": 0,
  "wins": 0,
  "draws": 0,
  "losses": 0,
  "score": 0,
  "playing": true,
  "played": 0,
  "percent": 0,
  "winpercent": 0
},
{
  "name": "New Player",
  "total": 0,
  "wins": 0,
  "draws": 0,
  "losses": 0,
  "score": 0,
  "playing": true,
  "played": 0,
  "percent": 0,
  "winpercent": 0
},
{
  "name": "New Player",
  "total": 0,
  "wins": 0,
  "draws": 0,
  "losses": 0,
  "score": 0,
  "playing": true,
  "played": 0,
  "percent": 0,
  "winpercent": 0
}
```

**Response:**
```json
{
  "_id": "YOUR_GENERATED_ID",
  "message": "Players added successfully"
}
```

### Update Player

**Endpoint:** `/players/<player_name>`  
**Method:** `PUT`  
**Description:** Update attributes for a specific player.

**Request:**
```http
PUT /players/Player%201
Content-Type: application/json

{
  "total": 100,
  "playing": false
}
```

**Response:**
```json
{
  "message": "Player updated successfully"
}
```

### Delete Player

**Endpoint:** `/players/<player_name>`  
**Method:** `DELETE`  
**Description:** Delete a specific player from the database.

**Request:**
```http
DELETE /players/Player%201
```

**Response:**
```json
{
  "message": "Player 'Player 1' deleted successfully"
}
```

### Update Playing Players

**Endpoint:** `/players/update_playing`  
**Method:** `PUT`  
**Description:** Update the "playing" status to True for specified players.

**Request:**
```http
PUT /players/update_playing
Content-Type: application/json

["Player 1", "Player 2"]
```

**Response:**
```json
{
  "message": "Players updated successfully"
}
```

### Update Not Playing Players

**Endpoint:** `/players/update_notplaying`  
**Method:** `PUT`  
**Description:** Update the "playing" status to False for specified players.

**Request:**
```http
PUT /players/update_notplaying
Content-Type: application/json

["Player 1", "Player 2"]
```

**Response:**
```json
{
  "message": "Players updated successfully"
}
```
