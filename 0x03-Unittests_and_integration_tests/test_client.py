#!/usr/bin/env python3
"""
1. Parameterize and patch as decorators
"""
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch
import unittest
from parameterized import parameterized, parameterized_class
import requests
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test for GithubOrgClient."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org_name, mock_get):
        """Test that GithubOrgClient.org returns the correct value."""
        test_client = GithubOrgClient(org_name)
        response = test_client.org
        self.assertEqual(response, {"payload": True})
        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that GithubOrgClient._public_repos_url
        returns the correct value.
        """
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = payload

        test_client = GithubOrgClient('google')
        self.assertEqual(test_client._public_repos_url, payload["repos_url"])

    @patch('client.get_json', return_value=[
        {
            "id": 7697149,
            "name": "episodes.dart",
            "private": False,
            "owner": {
                "login": "google",
                "id": 1342004,
            },
            "fork": False,
            "created_at": "2013-01-19T00:31:37Z",
            "updated_at": "2019-09-23T11:53:58Z",
            "forks": 26,
            "archived": True,
            "has_issues": True,
            "url": "https://api.github.com/repos/google/episodes.dart",
        },
        {
            "id": 8566972,
            "name": "kratu",
            "private": False,
            "owner": {
                "login": "google",
                "id": 1342004,
            },
            "fork": False,
            "created_at": "2013-03-04T22:52:33Z",
            "updated_at": "2024-04-02T17:41:15Z",
            "forks": 40,
            "archived": True,
            "has_issues": True,
            "url": "https://api.github.com/repos/google/kratu",
        },
    ])
    def test_public_repos(self, mock_get):
        """Test that GithubOrgClient.public_repos returns
        the correct value.
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
        }
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload['repos_url']
            test_client = GithubOrgClient('google')
            response = test_client.public_repos()
            self.assertEqual(response, ["episodes.dart", "kratu"])
            mock_get.assert_called_once_with(
                mock_public_repos_url.return_value)
            mock_public_repos_url.assert_called_once()


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(TestCase):
    """Integration test for GithubOrgClient."""
    @classmethod
    def setUpClass(cls):
        """Set up the class with the patcher."""
        cls.get_patcher = patch('requests.get')

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

        # Set the side effect of the mock to return the correct fixtures
        routes = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def payload(url):
            if url in routes:
                return MagicMock(json=lambda: routes[url])
            return requests.get(url)

        cls.get_patcher = patch('requests.get', payload)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that the public_repos method returns the correct value."""
        test_client = GithubOrgClient('google')
        response = test_client.public_repos()
        self.assertEqual(response, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that the public_repos method returns the correct value."""
        test_client = GithubOrgClient('google')
        response = test_client.public_repos("apache-2.0")
        self.assertEqual(response, self.apache2_repos)
