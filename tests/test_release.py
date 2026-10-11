import sys,types,unittest,importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from unittest.mock import Mock,patch,call
sys.path.insert(0,str(ROOT))
mongo=types.ModuleType('pymongo');mongo.MongoClient=Mock();sys.modules['pymongo']=mongo
import db_connect
from flask import Flask

class APIReleaseTests(unittest.TestCase):
 def test_startup_has_no_database_mutations(self):
  client=Mock();db=Mock();collections={n:Mock() for n in ('players','games','tenant')}
  client.__getitem__=Mock(return_value=db);db.__getitem__=Mock(side_effect=collections.__getitem__)
  with patch.object(db_connect,'MongoClient',return_value=client):
   self.assertEqual(db_connect.db_connect(),tuple(collections.values()))
  for c in collections.values():self.assertEqual(c.mock_calls,[])
  self.assertEqual(db.mock_calls,[call.__getitem__('players'),call.__getitem__('games'),call.__getitem__('tenant')])
 def test_routes_goals_projection_and_invalid_updates(self):
  players=Mock();player=dict(name='Alice',total=80,wins=1,draws=0,losses=0,score=3,playing=True,played=1,percent=100,winpercent=100,goals=7)
  players.find.side_effect=lambda:[dict(player)]
  with patch.object(db_connect,'db_connect',return_value=(players,Mock(),Mock())):
   spec=importlib.util.spec_from_file_location('offline_players',str(ROOT/'routes/players.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  app=Flask(__name__);app.register_blueprint(mod.players_bp);c=app.test_client()
  for path in ('/players','/players/player_stats','/players/leaderboard'):
   self.assertEqual(c.get(path).json[0]['goals'],7)
  for bad in (-1,True,2.5,'2',None):self.assertEqual(c.put('/players/goals/Alice',json={'goals':bad}).status_code,400)
  players.update_one.assert_not_called()
  players.update_one.return_value=Mock(matched_count=1)
  self.assertEqual(c.put('/players/goals/Alice',json={'goals':2}).status_code,200)
  players.update_one.assert_called_once_with({'name':'Alice'},{'$inc':{'goals':2}})
  player.pop('goals');self.assertEqual(c.get('/players/player_stats').json[0]['goals'],0)

if __name__ == '__main__':
 unittest.main()
