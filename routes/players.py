from flask import Blueprint, jsonify, request
from db_connect import db_connect
#from flask_jwt_extended import jwt_required

# Create the blueprint
players_bp = Blueprint("players", __name__)

# Connect to the database
players_collection, games_collection, tenant_collection = db_connect()

# Routes for Players

## This gives an error the ObjectId is not serializable
# @players_bp.route('/players', methods=['GET'])
# def get_players():
#     players = players_collection.find()
#     player_list = [{"_id": str(player["_id"]), **player} for player in players]
#     print(player_list)
#     return jsonify(player_list)

@players_bp.route('/players', methods=['GET'])
#@jwt_required()
def get_players():
    players = players_collection.find()
    player_list =   [   {
                            "name": player["name"],
                            "total": player["total"],
                            "wins": player["wins"],
                            "draws": player["draws"],
                            "losses": player["losses"],
                            "score": player["score"],
                            "playing": player["playing"],
                            "played": player["played"],
                            "percent": player["percent"],
                            "winpercent": player["winpercent"]
                        } 
                    for player in players
                    ]
    return jsonify(player_list)

@players_bp.route('/players/player_names', methods=['GET'])
#@jwt_required()
def get_player_names():
    try:
        players = players_collection.find()

        #Example output:
        # {'name': 'Amy', 'playing': True}, 
        # {'name': 'Cal', 'playing': False}, 
        # {'name': 'Player 15', 'playing': True}, 
        # {'name': 'Rik', 'playing': True}

        # Sort players by name in alphabetical order
        sorted_players = sorted(players, key=lambda player: player["name"])

        # Create the player_names list with name and playing status
        player_names = [
            {"name": player["name"], "playing": player["playing"]} for player in sorted_players
        ]
        return jsonify(player_names)
    # except jwt.exceptions.InvalidTokenError:
    #     return jsonify({"msg": "Invalid token"}), 401
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"msg": "An error occurred"}), 500

@players_bp.route('/players/all_players', methods=['GET'])
#@jwt_required()
def get_all_players():
    players = players_collection.find()
    
    #Example output:
    # [{'name': 'Amy', 'total': 77}, 
    # {'name': 'Cal', 'total': 77}, 
    # {'name': 'Joe', 'total': 77}, 
    # {'name': 'Rik', 'total': 77}]

    # Sort players by name in alphabetical order
    sorted_players = sorted(players, key=lambda player: player["name"])

    # Create the player_totals list with name and total
    player_totals = [
        {"name" : player["name"], "total" : player["total"]} for player in sorted_players
    ]
    return jsonify(player_totals)

@players_bp.route('/players/player_stats', methods=['GET'])
#@jwt_required()
def get_player_stats():

    # Find all players from players collection
    players = players_collection.find()
    
    #Example output:
    #{'name': 'Amy', 'wins': 0, 'draws': 0, 'losses': 0, 'score': 0, 'winpercent': 0}, 
    #{'name': 'Cal', 'wins': 0, 'draws': 0, 'losses': 0, 'score': 0, 'winpercent': 0}, 
    #{'name': 'Joe', 'wins': 0, 'draws': 0, 'losses': 0, 'score': 0, 'winpercent': 0}, 
    #{'name': 'Rik', 'wins': 0, 'draws': 0, 'losses': 0, 'score': 0, 'winpercent': 0}

    # Sort players by name in alphabetical order
    sorted_players = sorted(players, key=lambda player: player["name"])

    # Create the player_stats list with name, wins, draws, losses, score and winpercent
    player_stats = [{
        "name" : player["name"], 
        "wins" : player["wins"],
        "draws" : player["draws"],
        "losses" : player["losses"],
        "score" : player["score"],
        "winpercent" : player["winpercent"]
        } for player in sorted_players
    ]
    return jsonify(player_stats)

@players_bp.route('/players/leaderboard', methods=['GET'])
#@jwt_required()
def get_leaderboard():

    # Find all players from players collection
    players = players_collection.find()
    
    #Example output:
    #{'name': 'Rik', 'score': 10}, 
    #{'name': 'Cal', 'score': 8}, 
    #{'name': 'Amy', 'score': 6}, 
    #{'name': 'Joe', 'score': 4}

    # Sort players by score in descending order
    sorted_players = sorted(players, key=lambda player: player["score"], reverse=True)
    
    # Select the top 10 players
    top_players = sorted_players[:10]

    # Create the leaderboard list with name and score
    leaderboard = [
        {"name" : player["name"],"score" : player["score"],"goals" : player["goals"]} for player in top_players
    ]
    return jsonify(leaderboard)

@players_bp.route('/players/winpercentage', methods=['GET'])
#@jwt_required()
def get_winpercentage():

    # Find all players from players collection
    players = players_collection.find()
    
    #Example output:
    #{'name': 'Rik', 'winpercent': 0}, 
    #{'name': 'Cal', 'winpercent': 0}, 
    #{'name': 'Amy', 'winpercent': 0}, 
    #{'name': 'Joe', 'winpercent': 0}

    # Sort players by name in alphabetical order
    sorted_players = sorted(players, key=lambda player: player["winpercent"])

    # Create the player_totals list with name and total
    player_winpercentages = [
        {"name" : player["name"], "winpercent" : player["winpercent"]} for player in sorted_players
    ]
    return jsonify(player_winpercentages)

@players_bp.route('/players/game_player_tally', methods=['GET'])
#@jwt_required()
def get_game_player_tally():

    # Find all players from players collection
    players = players_collection.find()
    
    #Example output:
    #[{'name': 'Rik'}, {'name': 'Amy'}, {'name': 'Joe'}]

    # Create the playing_players list with name
    playing_players = [
        {"name": player["name"], "total": player["total"]} for player in players if player.get("playing")
    ]
    return jsonify(playing_players)

@players_bp.route('/players', methods=['POST'])
def add_player():
    new_player = request.json
    player_id = players_collection.insert_one(new_player).inserted_id
    return jsonify({"_id": str(player_id), "message": "Player added successfully"})

@players_bp.route('/players', methods=['PUT'])
#@jwt_required()
def update_players():
    updated_data = request.json  # New values to update for all players

    # Update all records in the players collection with the provided data
    result = players_collection.update_many({}, {"$set": updated_data})

    if result.modified_count > 0:
        return jsonify({"message": "Players updated successfully"})
    else:
        return jsonify({"message": "No players were updated"})

@players_bp.route('/players/<player_name>', methods=['PUT'])
#@jwt_required()
def update_player(player_name):
    updated_data = request.json  # New values to update for the specific player

    # Update the specific player by matching the unique identifier
    result = players_collection.update_one({"name": player_name}, {"$set": updated_data})

    if result.modified_count > 0:
        return jsonify({"message": "Player updated successfully"})
    else:
        return jsonify({"message": "Player not found or no changes applied"})

@players_bp.route('/players/goals/<player_name>', methods=['PUT'])
#@jwt_required()
def update_player_goals(player_name):
    updated_data = request.json  # New values to update for the specific player

    # Use the "$inc" operator to add incoming goals to the existing ones
    update_goal = {"$inc": {"goals": updated_data["goals"]}}

    # Update the specific player by matching the unique identifier
    result = players_collection.update_one({"name": player_name}, update_goal)

    if result.modified_count > 0:
        return jsonify({"message": "Player's goal count updated successfully"})
    else:
        return jsonify({"message": "Player not found or no changes applied"})


@players_bp.route('/players/<player_name>', methods=['DELETE'])
#@jwt_required()
def delete_player(player_name):
    # Delete the specific player by matching the player's name
    result = players_collection.delete_one({"name": player_name})

    if result.deleted_count > 0:
        return jsonify({"message": f"Player '{player_name}' deleted successfully"})
    else:
        return jsonify({"message": f"Player '{player_name}' not found"})

@players_bp.route('/players/update_playing', methods=['PUT'])
#@jwt_required()
def update_playing_players():
    data = request.json  # List of player names to update

    # Update the 'playing' field to True for the specified players
    result = players_collection.update_many({"name": {"$in": data}}, {"$set": {"playing": True}})

    if result.modified_count > 0:
        return jsonify({"message": "Players updated successfully"})
    else:
        return jsonify({"message": "No players were updated"})

@players_bp.route('/players/update_notplaying', methods=['PUT'])
#@jwt_required()
def update_not_playing_players():
    data = request.json  # List of player names to update

    # Update the 'playing' field to False for the specified players
    result = players_collection.update_many({"name": {"$in": data}}, {"$set": {"playing": False}})

    if result.modified_count > 0:
        return jsonify({"message": "Players updated successfully"})
    else:
        return jsonify({"message": "No players were updated"})

@players_bp.route('/players/all_players_by_channel/<channel>', methods=['GET'])
#@jwt_required()
def get_all_players_by_channel(channel):

    # Find all players from players collection
    players = players_collection.find()
    
    #Example output:
    # [{'name': 'Amy', 'total': 77}, 
    # {'name': 'Cal', 'total': 77}, 
    # {'name': 'Joe', 'total': 77}, 
    # {'name': 'Rik', 'total': 77}]

    # Sort players by name in alphabetical order
    sorted_players = sorted(players, key=lambda player: player["name"])

    # Create the playing_players list with name
    playing_players = [
        {"name": player["name"], "total": player["total"]} for player in sorted_players if player.get("channelid") == channel
    ]
    return jsonify(playing_players)

@players_bp.route('/players/player_names_by_channel/<channel>', methods=['GET'])
#@jwt_required()
def get_player_names_by_channel(channel):
    try:
        players = players_collection.find()

        #Example output:
        # {'name': 'Amy', 'playing': True}, 
        # {'name': 'Cal', 'playing': False}, 
        # {'name': 'Player 15', 'playing': True}, 
        # {'name': 'Rik', 'playing': True}

        # Sort players by name in alphabetical order
        sorted_players = sorted(players, key=lambda player: player["name"])

        # Create the player_names list with name and playing status
        player_names = [
            {"name": player["name"], "playing": player["playing"]} for player in sorted_players if player.get("channelid") == channel
        ]
        return jsonify(player_names)
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"msg": "An error occurred"}), 500

@players_bp.route('/players/reset_season', methods=['PUT'])
#@jwt_required()
def reset_season_players():
    """
    Reset all player stats for a new season.
    Preserves: name, total
    Resets: wins, draws, losses, score, playing, played, percent, winpercent, goals
    """
    try:
        reset_data = request.json
        if not reset_data:
            return jsonify({"error": "Request body is required"}), 400
        allowed_fields = ['wins', 'draws', 'losses', 'score', 'playing', 'played', 'percent', 'winpercent', 'goals']
        filtered_data = {k: v for k, v in reset_data.items() if k in allowed_fields}
        if not filtered_data:
            return jsonify({
                "error": "No valid fields to reset",
                "allowed_fields": allowed_fields
            }), 400
        result = players_collection.update_many({}, {"$set": filtered_data})
        if result.modified_count > 0:
            return jsonify({"message": f"Season reset successfully. {result.modified_count} players updated."}), 200
        else:
            return jsonify({"message": "No players were updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500