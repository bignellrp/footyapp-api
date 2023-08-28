# Footyapp Backend - REST API

# API Documentation for Game Management

This API provides endpoints for managing and retrieving game statistics. It allows you to perform various operations such as getting game information, updating game scores, swapping players, and more. Below are the available routes and how to use them:

### Get All Games

**Endpoint:** `/games`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve a list of all games with their information.

### Get Game Statistics

**Endpoint:** `/games/game_stats`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve game statistics, including dates and scores, sorted by date in descending order.

### Get Player's Wins

**Endpoint:** `/games/wins/<player>`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Get the number of games won by a specific player. Updates the player's win count.

### Update Game Score

**Endpoint:** `/games/updatescore/<date>`  
**Method:** `PUT`  
**Protected:** Yes (JWT Required)  
**Description:** Update the scores of a game and calculate statistics for the players involved.

### Get Most Recent Game

**Endpoint:** `/games/most_recent_game`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve information about the most recent game played.

### Swap Players in a Game

**Endpoint:** `/games/swap_player`  
**Method:** `PUT`  
**Protected:** Yes (JWT Required)  
**Description:** Swap a player's position with a new player in the most recent game. Update team composition and game totals accordingly.

### Add New Game

**Endpoint:** `/games`  
**Method:** `POST`  
**Protected:** Yes (JWT Required)  
**Description:** Add a new game record to the database.

### Update Game

**Endpoint:** `/games/<date>`  
**Method:** `PUT`  
**Protected:** Yes (JWT Required)  
**Description:** Update an existing game's information using the specified date.

### Delete Game

**Endpoint:** `/games/<date>`  
**Method:** `DELETE`  
**Protected:** Yes (JWT Required)  
**Description:** Delete a game record from the database using the specified date.

## Example Usage

### Get All Games

**Request:**
```http
GET /games
Authorization: Bearer YOUR_JWT_TOKEN
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
  },
  // Other game records...
]
```

### Get Player's Wins

**Request:**
```http
GET /games/wins/Player1
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:**
```json
{
  "wins": 10
}
```

### Update Game Score

**Request:**
```http
PUT /games/updatescore/2023-08-30
Authorization: Bearer YOUR_JWT_TOKEN
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

### Swap Players in a Game

**Request:**
```http
PUT /games/swap_player
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "current_player": "Player1",
  "new_player": "NewPlayer"
}
```

**Response:**
```json
{
  "message": "Player swapped and totals updated successfully"
}
```

### Add New Game

**Request:**
```http
POST /games
Authorization: Bearer YOUR_JWT_TOKEN
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

**Request:**
```http
PUT /games/2023-09-01
Authorization: Bearer YOUR_JWT_TOKEN
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

**Request:**
```http
DELETE /games/2023-09-01
Authorization: Bearer YOUR_JWT_TOKEN
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
**Protected:** Yes (JWT Required)  
**Description:** Retrieve a list of all players with their statistics.

### Get Player Names

**Endpoint:** `/players/player_names`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve a list of player names and their playing status.

### Get All Player Totals

**Endpoint:** `/players/all_players`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve a list of all player names and their total scores.

### Get Player Stats

**Endpoint:** `/players/player_stats`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve detailed statistics for each player, including wins, draws, losses, and more.

### Get Leaderboard

**Endpoint:** `/players/leaderboard`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve a leaderboard of the top players based on their scores.

### Get Win Percentages

**Endpoint:** `/players/winpercentage`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve win percentages for each player.

### Get Game Player Tally

**Endpoint:** `/players/game_player_tally`  
**Method:** `GET`  
**Protected:** Yes (JWT Required)  
**Description:** Retrieve a list of players currently playing in games.

### Add New Player

**Endpoint:** `/players`  
**Method:** `POST`  
**Description:** Add a new player with specified attributes.

### Update All Players

**Endpoint:** `/players`  
**Method:** `PUT`  
**Protected:** Yes (JWT Required)  
**Description:** Update attributes for all players.

### Update Player

**Endpoint:** `/players/<player_name>`  
**Method:** `PUT`  
**Description:** Update attributes for a specific player.

### Delete Player

**Endpoint:** `/players/<player_name>`  
**Method:** `DELETE`  
**Description:** Delete a specific player from the database.

### Update Playing Players

**Endpoint:** `/players/update_playing`  
**Method:** `PUT`  
**Description:** Update the "playing" status to True for specified players.

### Update Not Playing Players

**Endpoint:** `/players/update_notplaying`  
**Method:** `PUT`  
**Description:** Update the "playing" status to False for specified players.

## Example Usage

### Get All Players

**Request:**
```http
GET /players
Authorization: Bearer YOUR_JWT_TOKEN
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
  // Other player records...
]
```

### Get Player Names

**Request:**
```http
GET /players/player_names
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:**
```json
[
  {
    "name": "Player 1",
    "playing": true
  },
  // Other player names...
]
```

### Add New Player

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

### Update Player

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

Feel free to adapt and expand upon this README template to suit your project's requirements and formatting preferences.