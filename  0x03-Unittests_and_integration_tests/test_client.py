#!/usr/bin/env python3
"""
Unittests and Integration tests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


# Task 4: Parameterize + Patch (test_org)

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value"""
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    # Task 5: Mocking a property (_public_repos_url)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch("client.GithubOrgClient.org", new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, test_payload["repos_url"])


    # Task 6: More patching (public_repos)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit test for public_repos"""
        mock_json_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = mock_json_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=unittest.mock.PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://example.com/repos"

            client = GithubOrgClient("example")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://example.com/repos")


    # Task 7: Parameterize has_license()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Unit test for has_license"""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)



# Task 8–9: Integration Tests (fixtures + public_repos + license filter)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and mock .json() responses"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_resp = MagicMock()
            if "orgs" in url:
                mock_resp.json.return_value = cls.org_payload
            elif "repos" in url:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching"""
        cls.get_patcher.stop()


    # Task 9: Integration test for public_repos()

    def test_public_repos(self):
        """Test public_repos returns expected list"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license=apache-2.0"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
