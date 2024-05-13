#!/usr/bin/env python3
"""
1. Parameterize and patch as decorators
"""
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
import unittest


class TestGithubOrgClient(unittest.TestCase):
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

    @patch('client.get_json',
           return_value=[{"name": "repo1"},
                         {"name": "repo2"}])
    def test_public_repos(self, mock_get):
        """Test that GithubOrgClient.public_repos
        returns the correct value.
        """
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://\
            api.github.com/orgs/google/repos"

            test_client = GithubOrgClient('google')
            response = test_client.public_repos

            self.assertEqual(response, ["repo1", "repo2"])
            mock_get.assert_called_once_with(
                mock_public_repos_url.return_value)
            mock_public_repos_url.assert_called_once()
