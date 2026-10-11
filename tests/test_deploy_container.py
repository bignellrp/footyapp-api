"""No Docker, network or database access: production deployment API is mocked."""
import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('deploy_api', Path(__file__).resolve().parents[1] / 'scripts/deploy_api_container.py')
deploy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deploy)

class DeploymentTests(unittest.TestCase):
    def test_replaces_only_api_preserving_configuration(self):
        old = {'Id': 'old-api-id', 'State': {'Running': True},
               'Config': {'Image': 'old-image', 'Env': ['WEB_TOKEN=fake', 'MONGO_HOST=fake'],
                          'Labels': {'com.docker.compose.service': 'footyapp-api'}},
               'HostConfig': {'NetworkMode': 'br1', 'PortBindings': {'80/tcp': [{'HostPort': '2232'}]}},
               'NetworkSettings': {'Networks': {'br1': {'Aliases': ['footyapp-api-main', 'footyapp-api']}}}}
        database = {'Id': 'unchanged-db', 'State': {'Running': True, 'StartedAt': 'unchanged'}}
        calls = []
        def response(request, timeout=None):
            path = request.full_url.split('/docker/')[1]
            method = request.get_method()
            calls.append((method, path))
            result = None
            if path == 'containers/footyapp-api-main/json': result = old
            elif path == 'containers/footyapp-db-main/json': result = database
            elif path.startswith('images/'): result = {'Id': 'new-image'}
            elif path.startswith('containers/create'):
                config = json.loads(request.data)
                self.assertEqual(config['Image'], 'ghcr.io/bignellrp/footyapp-api:test-sha')
                self.assertEqual(config['Env'], old['Config']['Env'])
                self.assertEqual(config['HostConfig'], old['HostConfig'])
                self.assertEqual(config['NetworkingConfig']['EndpointsConfig']['br1']['Aliases'], ['footyapp-api-main', 'footyapp-api'])
                result = {'Id': 'new-api'}
            elif path.endswith('/exec'):
                command = json.loads(request.data)['Cmd'][-1]
                self.assertIn('urllib.request.urlopen', command)
                self.assertNotIn('requests.put', command)
                result = {'Id': 'health'}
            elif path == 'exec/health/json': result = {'ExitCode': 0}
            return io.BytesIO(json.dumps(result).encode() if result is not None else b'')
        with patch.dict(os.environ, {'PORTAINER_URL': 'https://fake.invalid', 'PORTAINER_TOKEN': 'fake', 'GITHUB_SHA': 'test-sha'}), patch.object(deploy.urllib.request, 'urlopen', side_effect=response):
            deploy.main()
        database_calls = [(m,p) for m,p in calls if 'db-main' in p]
        self.assertEqual(database_calls, [('GET','containers/footyapp-db-main/json')]*2)
        self.assertFalse(any('stacks' in path for _,path in calls))
        self.assertFalse(any(method == 'DELETE' for method,_ in calls))

if __name__ == '__main__':
    unittest.main()
