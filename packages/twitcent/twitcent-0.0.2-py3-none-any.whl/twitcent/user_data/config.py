import os


def main():
    user_params = {
        "consumerKey": os.environ.get("consumerKey"),
        "consumerSecret": os.environ.get("consumerSecret"),
        "accessToken": os.environ.get("accessToken"),
        "accessTokenSecret": os.environ.get("accessTokenSecret"),
    }

    return user_params

if __name__ == '__main__':
    main()