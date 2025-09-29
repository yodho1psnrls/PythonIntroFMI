from typing import Callable, Any


class DatabaseHandler:
    def __init__(self):
        # The Action Key Router: maps string keys to DB methods
        self.router: dict[str, Callable] = {
            "POST:LOG_IN": self._authenticate,
            "POST:NEW_ACCOUNT": self._create_account,
            "POST:NEW_POST": self._insert_post,
            "GET:PUBLICATIONS": self._fetch_publications
        }
        self.users = {}
        self.posts = []

    def _authenticate(self, username, password):
        if self.users.get(username) == password:
            return {"status": "success", "user": username}
        return {"status": "error", "message": "Invalid credentials."}

    def _create_account(self, username, password):
        if username in self.users:
            return {"status": "error", "message": "Account already exists."}
        self.users[username] = password
        return {"status": "success", "user": username}

    def _insert_post(self, user, text):
        post = {"id": len(self.posts) + 1, "author": user, "text": text}
        self.posts.append(post)
        return {"status": "success", "post_id": post['id']}

    def _fetch_publications(self):
        return self.posts

    def execute_action(self, action_string: str, **kwargs) -> Any:
        # Simplified execution for the terminal emulator
        target_function = self.router.get(action_string)
        if not target_function:
            return {"status": "error", "message": f"Action key '{action_string}' not found."}

        print(f"\n[Executing DB Action: {action_string}]")
        return target_function(**kwargs)
