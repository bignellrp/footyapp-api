"""Replace only the production API container; never redeploy the MongoDB stack."""
import json
import os
import urllib.request
import urllib.error


def main():
    base = os.environ['PORTAINER_URL'].rstrip('/') + '/api/endpoints/2/docker/'
    image = 'ghcr.io/bignellrp/footyapp-api:' + os.environ['GITHUB_SHA']
    headers = {'X-API-Key': os.environ['PORTAINER_TOKEN'], 'Content-Type': 'application/json'}

    def call(method, path, body=None, raw=False):
        request = urllib.request.Request(base + path, headers=headers, method=method,
                                         data=None if body is None else json.dumps(body).encode())
        with urllib.request.urlopen(request, timeout=90) as response:
            content = response.read()
        if raw:
            return content
        return json.loads(content) if content else None

    old = call('GET', 'containers/footyapp-api-main/json')
    database = call('GET', 'containers/footyapp-db-main/json')
    call('GET', 'images/' + image + '/json')  # Require the image to be pulled first.
    if old['Config']['Labels'].get('com.docker.compose.service') != 'footyapp-api':
        raise RuntimeError('Unexpected production container; deployment stopped.')
    if not database['State']['Running'] or not old['State']['Running']:
        raise RuntimeError('Production services are not running; deployment stopped.')
    environment = dict(item.split('=', 1) for item in old['Config']['Env'])
    if not all(environment.get(k) for k in ('WEB_TOKEN', 'MONGO_HOST')):
        raise RuntimeError('Missing production API settings; deployment stopped.')
    config = dict(old['Config'])
    config['Image'] = image
    config['Hostname'] = ''
    config['HostConfig'] = old['HostConfig']
    endpoints = {}
    for name, network in old['NetworkSettings']['Networks'].items():
        aliases = [a for a in (network.get('Aliases') or []) if a not in (old['Id'], old['Id'][:12])]
        endpoints[name] = {'Aliases': aliases}
    config['NetworkingConfig'] = {'EndpointsConfig': endpoints}
    backup = 'footyapp-api-main-rollback-' + old['Id'][:12]
    replacement = None
    renamed = False
    stopped = False
    try:
        call('POST', 'containers/' + old['Id'] + '/stop?t=30')
        stopped = True
        call('POST', 'containers/' + old['Id'] + '/rename?name=' + backup)
        renamed = True
        replacement = call('POST', 'containers/create?name=footyapp-api-main', config)['Id']
        call('POST', 'containers/' + replacement + '/start')
        # Only HTTP GETs inside the API. Never import routes or connect to Mongo directly.
        check = "import os,urllib.request,json,time; time.sleep(3); r=urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:80/players/player_stats',headers={'Authorization':'Bearer '+os.environ['WEB_TOKEN']}),timeout=15); rows=json.load(r); assert rows and all('goals' in p for p in rows); print('API read-only health check passed')"
        execution = call('POST', 'containers/' + replacement + '/exec', {
            'AttachStdout': True, 'AttachStderr': True, 'Cmd': ['python', '-c', check]})['Id']
        call('POST', 'exec/' + execution + '/start', {'Detach': False, 'Tty': True}, raw=True)
        if call('GET', 'exec/' + execution + '/json')['ExitCode'] != 0:
            raise RuntimeError('Production API read-only health check failed.')
        current_database = call('GET', 'containers/footyapp-db-main/json')
        if current_database['Id'] != database['Id'] or current_database['State']['StartedAt'] != database['State']['StartedAt']:
            raise RuntimeError('Database container identity changed unexpectedly.')
        print('Production API updated to ' + image)
        print('MongoDB container was not restarted or recreated.')
        print('Previous API container retained stopped as ' + backup)
    except Exception:
        if replacement:
            call('DELETE', 'containers/' + replacement + '?force=true')
        if renamed:
            call('POST', 'containers/' + old['Id'] + '/rename?name=footyapp-api-main')
        if stopped:
            call('POST', 'containers/' + old['Id'] + '/start')
        raise


if __name__ == '__main__':
    main()
