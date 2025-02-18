import os
import requests
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_merged_pr_count(username):
    """
    Get the count of merged pull requests using GitHub's GraphQL API.
    """
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    query = """
    query($login: String!) {
      user(login: $login) {
        pullRequests(states: MERGED) {
          totalCount
        }
      }
    }
    """
    variables = {"login": username}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )

    if response.status_code == 200:
        json_data = response.json()
        return json_data.get("data", {}).get("user", {}).get("pullRequests", {}).get("totalCount", 0)
    else:
        logger.error(f"GraphQL API error: {response.status_code} {response.text}")
        return 0

@api_view(['GET'])
def github_user_data(request, username):
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    # Fetch repositories
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_resp = requests.get(repos_url, headers=headers)

    if repos_resp.status_code != 200:
        logger.error(f"Error fetching repos: {repos_resp.status_code} {repos_resp.text}")
        return Response({"error": "User not found or error fetching repos"}, status=repos_resp.status_code)

    repos_data = repos_resp.json()

    # Fetch total commits from user events
    events_url = f"https://api.github.com/users/{username}/events/public"
    events_resp = requests.get(events_url, headers=headers)
    
    commit_count = 0
    if events_resp.status_code == 200:
        events_data = events_resp.json()
        for event in events_data:
            if event.get("type") == "PushEvent":
                commit_count += len(event.get("payload", {}).get("commits", []))
    else:
        logger.error(f"Error fetching events: {events_resp.status_code} {events_resp.text}")

    # Fetch total PR count using search API
    pr_search_url = f"https://api.github.com/search/issues?q=author:{username}+type:pr"
    pr_resp = requests.get(pr_search_url, headers=headers)
    pr_count = 0
    if pr_resp.status_code == 200:
        pr_data = pr_resp.json()
        pr_count = pr_data.get("total_count", 0)
    else:
        logger.error(f"Error fetching PRs: {pr_resp.status_code} {pr_resp.text}")

    # Fetch merged PR count using GraphQL
    merged_pr_count = get_merged_pr_count(username)

    # Final response
    return Response({
        "username": username,
        "total_commits": commit_count,
        "total_pull_requests": pr_count,
        "total_merged_pull_requests": merged_pr_count,
        "repositories": repos_data
    })
 