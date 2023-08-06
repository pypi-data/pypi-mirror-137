class YamlExample:
    @staticmethod
    def print():
        print(
            f"""
development:
  mongodbs:
    mongodb_1:
      "host": ""
      "user_name": ""
      "password": ""
      "auth": ""
    mongodb_2:
      "uri": ""

  external_api:
    api_1:
      "url": ""

    api_2:
      "url": ""


prod:
  mongodbs:
    mongodb_1:
      "host": ""
      "user_name": ""
      "password": ""
      "auth": ""
    mongodb_2:
      "uri": ""

  external_api:
    api_1:
      "url": ""

    api_2:
      "url": ""

common:
  SENTRY_DSN:

  SMTP_SERVER:
        """
        )


if __name__ == "__main__":
    YamlExample.print()
