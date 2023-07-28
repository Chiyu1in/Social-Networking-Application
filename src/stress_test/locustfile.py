from locust import HttpUser, between, task, tag
from urllib import parse

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    Authorization = None
    boards = [
        "Baseball",
        "Beauty",
        "C_Chat",
        "car",
        "creditcard",
        "Gossiping",
        "HatePolitics",
        "KoreaStar",
        "Lifeismoney",
        "LoL",
        "MobileComm",
        "movie",
        "NBA",
        "Stock",
        "Tech_Job",
    ]

    def on_start(self):

        FormData = {
            "grant_type": "",
            "username": "aics_admin1",
            "password": "aics_admin1",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        payload = parse.urlencode(FormData)

        response = self.client.post(
            "/login",
            data=payload,
            headers={
                "accept": "application-json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        if response.status_code == 200:
            json_data = response.json()
            self.Authorization = (
                json_data["token_type"] + " " + json_data["access_token"]
            )
        

    @tag("has_user")
    @task(1)
    def has_user(self):
        users = ["aics_admin1", "aics_admin2", "not_authorized_user"]

        for user in users:

            # payload = '{"user": "aics_admin1"}'
            payload = f'{{"username": "{user}"}}'

            self.client.post(
                "/has_user/",
                data=payload,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": self.Authorization,
                },
            )

    @tag("is_latest_unread")
    @task(3)
    def is_latest_unread(self):

        for board in self.boards:

            # payload = '{"user": "aics_admin1", "board": "Baseball"}'
            payload = f'{{"user": "aics_admin1", "board": "{board}"}}'

            self.client.post(
                "/is_latest_unread/",
                data=payload,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": self.Authorization,
                },
            )

    # @tag("write_post")
    # @task(2)
    # def write_post(self):

    #     user = "aics_admin1"
    #     board = "Baseball"

    #     for i in range(10):

    #         # payload = '{
    #         #   "user": "aics_admin1",
    #         #   "board": "Baseball",
    #         #   "title": "stress_test_1",
    #         #   "article": "stress_test_1"
    #         # }'
    #         payload = f' \
    #             {{ \
    #                 "user": "{user}", \
    #                 "board": "{board}", \
    #                 "title": "stress_test_{i}", \
    #                 "article": "stress_test_{i}" \
    #             }}'

    #         self.client.post(
    #             "/write_post/",
    #             data=payload,
    #             headers={
    #                 "accept": "application/json",
    #                 "Content-Type": "application/json",
    #                 "Authorization": self.Authorization,
    #             },
    #         )

    @tag("read_latest_post")
    @task(3)
    def read_latest_post(self):

        for board in self.boards:

            # payload = '{"board": "Baseball"}'
            payload = f'{{"board": "{board}"}}'

            self.client.post(
                "/read_latest_post/",
                data=payload,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": self.Authorization,
                },
            )

    @tag("count_likes")
    @task(2)
    def count_likes(self):

        for board in self.boards:

            # payload = '{"board": "Baseball"}'
            payload = f'{{"board": "{board}"}}'

            self.client.post(
                "/count_likes/",
                data=payload,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": self.Authorization,
                },
            )