#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Tasks 4–7"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org, mock_get_json):
        test_payload = {"org": org}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")
        self.assertEqual(result, test_payload)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Task 5"""

        mock_org.return_value = {"repos_url": "http://example.com/repos"}

        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "http://example.com/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Task 6"""

        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_prop:
            mock_prop.return_value = "http://example.com/repos"

            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_prop.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Task 7"""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)