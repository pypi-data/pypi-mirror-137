import json
import urllib.parse
from urllib.parse import urlparse, parse_qs

from typing import List

from time import sleep

import requests

from requests import Response

from common.test_utils import TestUtils
from gateways.common.cs18_api_classes import Commit

from requests import Session
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import requests


class GithubGateway:
    def __init__(self, user: str = "QualiNext", repo: str = "cs18-space-testing"):
        token = TestUtils.get_test_github_access_token()
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "token " + token})
        self.session.headers.update({"Accept": "application/vnd.github.v3.raw"})
        self.base_api_url = "https://api.github.com/repos/{user}/{repo}".format(
            user=user, repo=repo
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def close(self):
        self.session.close()

    def get_file(self, file_path, branch=None, tag=None, commit_id=None) -> str:
        url = "{github_api_url}/contents/{file_path}?ref={v}".format(
            github_api_url=self.base_api_url,
            file_path=file_path,
            v=branch or tag or commit_id,
        )
        return self.http_get(url=url).text

    def get_commit_history(self, file_path, branch="master") -> List[Commit]:
        url = "{github_api_url}/commits?sha={branch}&path={path}".format(
            github_api_url=self.base_api_url,
            branch=branch,
            path=urllib.parse.quote(file_path, safe=""),
        )
        response = self.http_get(url=url)
        items = json.loads(response.text)
        commits = [Commit(x) for x in items]
        sorted(commits, key=lambda x: x.date)
        return commits

    def http_get(self, url: str) -> Response:
        response = None
        attempt = 0
        while attempt < 5:
            response = self.session.get(url=url)
            if response.ok:
                return response
            attempt += 1
            print("Response from '{0}' returned {1}".format(url, response.status_code))
            sleep(1)
        response.raise_for_status()


class GithubUiGateway:
    def get_oauth_app_temporary_code(self):
        server_consumer_auth_base_url = 'https://github.com/login/oauth/authorize'
        consumer_temp_code_url = \
            '{server_base_uri}?client_id={client_id}&scope={scope}&response_type=code&redirect_uri={redirect_uri}' \
                .format(server_base_uri=server_consumer_auth_base_url,
                        client_id='a39501dcd0f209a554c0',
                        scope='user',
                        redirect_uri="http://colony.localhost/api/OauthRedirect/")

        session = Session()
        # authorization = f'token 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'
        # headers = {
        #     'Accept': 'application/json',
        # }
        # session.headers = headers
        # session.auth = HTTPBasicAuth("gembom", "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")

        session = self.github_login("gembom", "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")

        response = session.get(consumer_temp_code_url, allow_redirects=False)
        session.close()

        redirect_url = ''
        if response.status_code == 200:
            results = BeautifulSoup(response.text, 'html.parser')
            redirect_url = results.find_all("body")[0]['data-redirect']
        elif response.status_code == 302:
            redirect_url = response.next.url

        code_array = parse_qs(urlparse(redirect_url).query).get('code')
        return code_array[0]

    def github_login(self, username: str, token: str):
        session = requests.Session()
        # headers = {
        #     "Host": "www.github.com",
        #     "Origin": "https://www.github.com",
        #     "X-Requested-With": "XMLHttpRequest",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        # }
        # session.headers = headers

        git = BeautifulSoup(session.get('https://github.com/login').text, 'html.parser')
        auth_token = git.find("input", {"name": "authenticity_token"}).attrs['value']
        commit = git.find("input", {"name": "commit"}).attrs['value']

        data = {
            'username': username,
            'password': token,
            'commit': commit,
            'authenticity_token': auth_token
        }

        login = session.post('https://github.com/session', data=data)
        print(login.status_code)
        print(login.text)

        return session
