from flask import Blueprint, jsonify, request
from db_connect import db_connect
from datetime import datetime
#from flask_jwt_extended import jwt_required


games_bp = Blueprint("games", __name__)
players_collection, games_collection, tenant_collection = db_connect()

# Routes for Games
@games_bp.route('/games', methods=['GET'])
#@jwt_required()
def get_games():
    games = games_collection.find()
    # for game in games:
    #         game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')
    game_list =   [   {
                            "date": game["date"],
                            "teamA": [game["teamA"]],
                            "teamB": [game["teamB"]],
                            "scoreTeamA": game["scoreTeamA"],
                            "scoreTeamB": game["scoreTeamB"],
                            "totalTeamA": game["totalTeamA"],
                            "totalTeamB": game["totalTeamB"],
                            "colourTeamA": game["colourTeamA"],
                            "colourTeamB": game["colourTeamB"]
                        } 
                    for game in games
                    ]
    return jsonify(game_list)

@games_bp.route('/games/game_stats', methods=['GET'])
#@jwt_required()
def get_game_stats():
    games = list(games_collection.find())  # Convert cursor to a list
    for game in games:
        game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')

    # Sort players by name in alphabetical order
    # This might not work until date is converted in the api
    sorted_games = sorted(games, key=lambda game: game["date"], reverse=True)
    game_list =   [   {
                            "date": game["date"].strftime('%Y-%m-%d'),
                            "scoreTeamA": game["scoreTeamA"],
                            "scoreTeamB": game["scoreTeamB"]
                        } 
                    for game in sorted_games
                    ]
    return jsonify(game_list)

@games_bp.route('/games/wins/<player>', methods=['GET'])
#@jwt_required()
def get_game_wins(player):
    # Count games that match the criteria
    count = games_collection.count_documents({
        "scoreTeamA": {"$gt": "scoreTeamB"},
        "teamA": {"$elemMatch": {"$in": [player]}}
    })
    
    # Update the number of wins for the player
    players_collection.update_one({"name": player},{"$inc": {"wins": 1}})
    
    return jsonify({"wins": count})

@games_bp.route('/games/updatescore/<date>', methods=['PUT'])
#@jwt_required()
def update_score(date):
    try:
        game = games_collection.find_one({"date": date})
        if not game:
            # If the game with the given date is not found, return a response indicating it wasn't found.
            return jsonify({"message": "Game not found"}), 404
        game = games_collection.find_one({"date": date})
        if game:
            game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')
            game_record = {
                "date": game["date"].strftime('%Y-%m-%d'),
                "teamA": game["teamA"],
                "teamB": game["teamB"],
                "scoreTeamA": game["scoreTeamA"],
                "scoreTeamB": game["scoreTeamB"],
                "totalTeamA": game["totalTeamA"],
                "totalTeamB": game["totalTeamB"],
                "colourTeamA": game["colourTeamA"],
                "colourTeamB": game["colourTeamB"]
            }
        score = request.json
        games_collection.update_one({"date": date}, {"$set": score})
        updated_teama_score = score["scoreTeamA"]
        updated_teamb_score = score["scoreTeamB"]
        updated_teama_score = int(updated_teama_score)
        updated_teamb_score = int(updated_teamb_score)
        if updated_teama_score > updated_teamb_score:
            print(f"TeamA:{updated_teama_score} is greater than TeamB:{updated_teamb_score} so Team A Won! Updating stats.")
            for player in game_record["teamA"]:
                players_collection.update_one({"name": player},{"$inc": {"wins": 1}})
                players_collection.update_one({"name": player},{"$inc": {"played": 1}})
                players_collection.update_one({"name": player},{"$inc": {"score": 3}})
            for player in game_record["teamB"]:
                players_collection.update_one({"name": player},{"$inc": {"losses": 1}})
                players_collection.update_one({"name": player},{"$inc": {"played": 1}})
        elif updated_teama_score < updated_teamb_score:
            print(f"TeamA:{updated_teama_score} is less than TeamB:{updated_teamb_score} so Team B Won! Updating stats.")
            for player in game_record["teamB"]:
                players_collection.update_one({"name": player},{"$inc": {"wins": 1}})
                players_collection.update_one({"name": player},{"$inc": {"played": 1}})
                players_collection.update_one({"name": player},{"$inc": {"score": 3}})
            for player in game_record["teamA"]:
                players_collection.update_one({"name": player},{"$inc": {"losses": 1}})
                players_collection.update_one({"name": player},{"$inc": {"played": 1}})
        elif updated_teama_score == updated_teamb_score:
            print(f"TeamA:{updated_teama_score} is the same as TeamB:{updated_teamb_score} so Draw! Updating stats.")
            for player in game_record["teamB"]:
                players_collection.update_one({"name": player},{"$inc": {"draws": 1}})
                players_collection.update_one({"name": player},{"$inc": {"played": 1}})
                players_collection.update_one({"name": player},{"$inc": {"score": 1}})
            for player in game_record["teamA"]:
                players_collection.update_one({"name": player},{"$inc": {"draws": 1}})
                players_collection.update_one({"name": player},{"$inc": {"played": 1}})
                players_collection.update_one({"name": player},{"$inc": {"score": 1}})
        #Need to make sure the player_collection is updated by the above first
        for player in game_record["teamA"] or game_record["teamB"]:
            findplayer = players_collection.find_one({"name": player})
            if findplayer:
                player_record = {
                    "name": findplayer["name"],
                    "total": findplayer["total"],
                    "wins": findplayer["wins"],
                    "draws": findplayer["draws"],
                    "losses": findplayer["losses"],
                    "score": findplayer["score"],
                    "playing": findplayer["playing"],
                    "played": findplayer["played"],
                    "percent": findplayer["percent"],
                    "winpercent": findplayer["winpercent"]
                }
            percentage = player_record["wins"] / player_record["played"] * 100
            percentage = int(round(percentage))
            if player_record["wins"] < 5:
                winpercentage = 0
            else:
                winpercentage = percentage
            players_collection.update_one({"name": player},{"$set": {"percent": percentage}})
            players_collection.update_one({"name": player},{"$set": {"winpercent": winpercentage}})
        return jsonify({"message": "Game updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@games_bp.route('/games/most_recent_game', methods=['GET'])
#@jwt_required()
def get_most_recent_game():
    games = list(games_collection.find())  # Convert cursor to a list
    for game in games:
        game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')

    # Sort players by name in alphabetical order
    # This might not work until date is converted in the api
    sorted_games = sorted(games, key=lambda game: game["date"], reverse=True)
    game_list =   [   {
                            "date": game["date"].strftime('%Y-%m-%d'),
                            "teamA": game["teamA"],
                            "teamB": game["teamB"],
                            "scoreTeamA": game["scoreTeamA"],
                            "scoreTeamB": game["scoreTeamB"],
                            "totalTeamA": game["totalTeamA"],
                            "totalTeamB": game["totalTeamB"],
                            "colourTeamA": game["colourTeamA"],
                            "colourTeamB": game["colourTeamB"]
                        } 
                    for game in sorted_games
                    ]
    return jsonify(game_list)

@games_bp.route('/games/teama', methods=['GET'])
#@jwt_required()
def get_teama():
    games = list(games_collection.find())  # Convert cursor to a list
    if not games:  # We return an empty array if no games found
        return jsonify([])

    for game in games:
        game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')

    # Sort games by date in descending order
    sorted_games = sorted(games, key=lambda game: game["date"], reverse=True)
    
    # Get 'teamA' of the most recent game
    most_recent_team_a = sorted_games[0]["teamA"]
    most_recent_date = sorted_games[0]["date"].strftime('%Y-%m-%d')
    most_recent_colour_a = sorted_games[0]["colourTeamA"]
    
    # Create an array containing 'teamA' field from the most recent game.
    team_a_list = [most_recent_team_a]
    return jsonify({"teamA": team_a_list, "date": most_recent_date, "colourA": most_recent_colour_a})

@games_bp.route('/games/teamb', methods=['GET'])
#@jwt_required()
def get_teamb():
    games = list(games_collection.find())  # Convert cursor to a list
    if not games:  # We return an empty array if no games found
        return jsonify([])

    for game in games:
        game["date"] = datetime.strptime(game["date"], '%Y-%m-%d')

    # Sort games by date in descending order
    sorted_games = sorted(games, key=lambda game: game["date"], reverse=True)
    
    # Get 'teamA' of the most recent game
    most_recent_team_b = sorted_games[0]["teamB"]
    most_recent_date = sorted_games[0]["date"].strftime('%Y-%m-%d')
    most_recent_colour_b = sorted_games[0]["colourTeamB"]
    
    # Create an array containing 'teamA' field from the most recent game.
    team_b_list = [most_recent_team_b]
    return jsonify({"teamB": team_b_list, "date": most_recent_date, "colourB": most_recent_colour_b})

@games_bp.route('/games/swap_player', methods=['PUT'])
#@jwt_required()
def swap_player():
    try:
        # Get input data
        current_player = request.json.get("current_player")
        new_player = request.json.get("new_player")
        
        # Find the most recent game
        most_recent_game = games_collection.find_one({}, sort=[("date", -1)])
        
        if most_recent_game:
            teamA = most_recent_game.get("teamA", [])
            teamB = most_recent_game.get("teamB", [])
            
            # Calculate player total differences
            current_player_total_diff = 0
            new_player_total_diff = 0
            
            # Calculate current player total difference
            current_player_info = players_collection.find_one({"name": current_player})
            if current_player_info:
                current_player_total_diff = current_player_info["total"]
            
            # Calculate new player total difference
            new_player_info = players_collection.find_one({"name": new_player})
            if new_player_info:
                new_player_total_diff = new_player_info["total"]
            
            # Replace current_player with new_player in teamA
            if current_player in teamA:
                teamA = [new_player if player == current_player else player for player in teamA]
                # Update the total for Team A
                games_collection.update_one(
                    {"date": most_recent_game["date"]},
                    {"$inc": {"totalTeamA": new_player_total_diff - current_player_total_diff}}
                )
            # Replace current_player with new_player in teamB
            if current_player in teamB:
                teamB = [new_player if player == current_player else player for player in teamB]
                # Update the total for Team B
                games_collection.update_one(
                    {"date": most_recent_game["date"]},
                    {"$inc": {"totalTeamB": new_player_total_diff - current_player_total_diff}}
                )
            # Update the game with the modified teams
            games_collection.update_one(
                {"date": most_recent_game["date"]},
                {"$set": {"teamA": teamA, "teamB": teamB}}
            )
            
            return jsonify({"message": "Player swapped and totals updated successfully"})
        else:
            return jsonify({"message": "No games found"})
    except Exception as e:
        return jsonify({"message": str(e)})

@games_bp.route('/games', methods=['POST'])
#@jwt_required()
def add_game():
    new_game = request.json
    game_id = games_collection.insert_one(new_game).inserted_id
    return jsonify({"_id": str(game_id), "message": "Game added successfully"})

@games_bp.route('/games/<date>', methods=['PUT'])
#@jwt_required()
def update_game(date):
    game_updates = request.json
    games_collection.update_one({"date": date}, {"$set": game_updates})
    return jsonify({"message": "Game updated successfully"})

@games_bp.route('/games/<date>', methods=['DELETE'])
#@jwt_required()
def delete_game(date):
    games_collection.delete_one({"date": date})
    return jsonify({"message": "Game deleted successfully"})

@games_bp.route('/games', methods=['DELETE'])
#@jwt_required()
def delete_all_games():
    """Delete all games from the database"""
    try:
        result = games_collection.delete_many({})
        return jsonify({
            "message": f"All games deleted successfully. {result.deleted_count} games removed."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500