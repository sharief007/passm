import datetime


class QueryFormatter:

    def __init__(self):
        self.queries = {
            "insert_credential": "INSERT INTO CREDENTIALS(APPLICATION_NAME, USERNAME, PASSWORD, CREATION_TIME) VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\")",
            "insert_hosts": "INSERT INTO HOSTS(CREDENTIALS_ID, APPLICATION_HOST) VALUES (\"{0}\", \"{1}\")",
            "insert_emails": "INSERT INTO EMAILS(CREDENTIALS_ID, EMAIL_ADDRESS) VALUES (\"{0}\",\"{1}\")",
            "insert_questions": "INSERT INTO QUESTIONS(CREDENTIALS_ID, QUESTION, ANSWER) VALUES (\"{0}\",\"{1}\",\"{2}\")",
            "insert_info": "INSERT INTO INFO(CREDENTIALS_ID, INFO_KEY, INFO_VALUE) VALUES (\"{0}\",\"{1}\",\"{2}\")",

            "get_all_apps": "SELECT APPLICATION_NAME FROM CREDENTIALS",
            "get_details_by_app": "SELECT * FROM CREDENTIALS WHERE LOWER(APPLICATION_NAME) = LOWER(\"{}\")",
            "get_hosts_by_app": "SELECT APPLICATION_HOST FROM HOSTS WHERE CREDENTIALS_ID = {0}",
            "get_emails_by_app": "SELECT EMAIL_ADDRESS FROM EMAILS WHERE CREDENTIALS_ID = {0}",
            "get_questions_by_app": "SELECT QUESTION, ANSWER FROM QUESTIONS WHERE CREDENTIALS_ID = {0}",
            "get_info_by_app": "SELECT INFO_KEY, INFO_VALUE FROM INFO WHERE CREDENTIALS_ID = {0}",
            "get_password": "SELECT PASSWORD FROM CREDENTIALS WHERE LOWER(APPLICATION_NAME) = LOWER(\"{0}\")",
            "get_all_credentials": "SELECT ID, APPLICATION_NAME, USERNAME, PASSWORD FROM CREDENTIALS",
            "get_all_hosts": "SELECT CREDENTIALS_ID, APPLICATION_HOST FROM HOSTS",
            "get_all_emails": "SELECT CREDENTIALS_ID, EMAIL_ADDRESS FROM EMAILS",
            "get_all_questions": "SELECT CREDENTIALS_ID, QUESTION, ANSWER FROM QUESTIONS",
            "get_all_info": "SELECT CREDENTIALS_ID, INFO_KEY, INFO_VALUE FROM INFO"
        }

    def get_queries(self):
        return self.queries

    def get_insert_hosts(self, cred_id, hosts):
        statements = list()
        for host in hosts:
            statements.append(
                self.queries.get("insert_hosts").format(cred_id, host)
            )
        return ";".join(statements)

    def get_save_credential(self, app=None, username=None, password=None):
        return self.queries.get("insert_credential").format(app, username, password, datetime.datetime.now())

    def get_insert_emails(self, cred_id, emails):
        statements = list()
        for email in emails:
            statements.append(
                self.queries.get("insert_emails").format(cred_id, email)
            )
        return ";".join(statements)

    def get_insert_questions(self, cred_id, questions):
        statements = list()
        for item in questions:
            statements.append(
                self.queries.get("insert_questions").format(cred_id, item["question"], item["answer"])
            )
        return ";".join(statements)

    def get_insert_info(self, cred_id, info):
        statements = list()
        for item in info:
            statements.append(
                self.queries.get("insert_info").format(cred_id, item["key"], item["value"])
            )
        return ";".join(statements)

    def get_all_apps(self):
        return self.queries.get("get_all_apps")

    def get_details_by_app(self, app: str):
        return self.queries.get("get_details_by_app").format(app)

    def get_hosts_by_app(self, app: str):
        return self.queries.get("get_hosts_by_app").format(app)

    def get_emails_by_app(self, app: str):
        return self.queries.get("get_emails_by_app").format(app)

    def get_questions_by_app(self, app: str):
        return self.queries.get("get_questions_by_app").format(app)

    def get_info_by_app(self, app: str):
        return self.queries.get("get_info_by_app").format(app)

    def get_password(self, app):
        return self.queries.get("get_password").format(app)

    def get_all_credentials(self):
        return self.queries.get("get_all_credentials")

    def get_all_hosts(self):
        return self.queries.get("get_all_hosts")

    def get_all_emails(self):
        return self.queries.get("get_all_emails")

    def get_all_questions(self):
        return self.queries.get("get_all_questions")

    def get_all_info(self):
        return self.queries.get("get_all_info")