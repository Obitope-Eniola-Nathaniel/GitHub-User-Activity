import requests
import sys

def get_posts(name):
    # Define the API endpoint URL
    url = f'https://api.github.com/users/{name}/events'

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
    # Handle any network-related errors or exceptions
        print('Error:', e)
        return None

def display_git_post(posts):
    if posts:
        for post in posts[:10]:
            event_type = post['type']
            repo_name = post['repo']['name']

            if event_type == 'PushEvent':
                commit_count = len(post['payload']['commits'])
                print(f"Pushed {commit_count} commits to {repo_name}")
            elif event_type == "IssuesEvent":
                action = post["payload"]["action"]
                print(f"- {action.capitalize()} an issue in {repo_name}")
            elif event_type == "WatchEvent":
                print(f"- Starred {repo_name}")
            elif event_type == "ForkEvent":
                print(f"- Forked {repo_name}")
            elif event_type == "PullRequestEvent":
                action = post["payload"]["action"]
                print(f"- {action.capitalize()} a pull request in {repo_name}")
            else:
                print(f"- {event_type} in {repo_name}")
    else:
        print('Failed to fetch posts from API.')

def main():
    # Check if the username is provided as an argument
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Usage: python git-hub.py <username>")
        sys.exit(1)

    # Get the username from the command-line
    username = sys.argv[1]
    print(f"Recent activity for {username}:")
    # Get the posts from the GitHub API
    posts = get_posts(username)
    # Display the posts
    display_git_post(posts)

if __name__ == "__main__":
    main()
