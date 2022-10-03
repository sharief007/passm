import sqlite3
import datetime

import click

import config
import query_manager


class Repository:

    def __init__(self):
        db_url = config.get_db_path().absolute()
        self.query_manager = query_manager.QueryFormatter()
        try:
            self.conn = sqlite3.connect(db_url)
        except Exception as ex:
            click.echo(f"Error creating a database connection: {ex}")

    def quick_save(self, credentials):
        try:
            (app, username, password) = credentials
            query = self.query_manager.get_save_credential(app, username, password)
            with self.conn as connection:
                cursor = connection.cursor()
                result = cursor.execute(query)
                connection.commit()
                print(result.lastrowid)
                click.echo(f"Successfully saved {result.rowcount} record(s)")
                cursor.close()
        except Exception as ex:
            click.echo(f"Error saving credentials to the database: {ex}")
        finally:
            if self.conn:
                self.conn.close()

    def setup(self):
        try:
            with self.conn as connection:
                with open("schema.sql", "r") as script:
                    sql = script.read()
                cursor = connection.cursor()
                cursor.executescript(sql)
                connection.commit()
                click.echo("SetUp Successful")
                cursor.close()
        except Exception as ex:
            click.echo(f"Error Initializing schema for database: {ex}")
        finally:
            if self.conn:
                self.conn.close()

    def save(self, credential):
        transaction = False

        try:
            query = self.query_manager.get_save_credential(credential["App"], credential["Username"],
                                                           credential["Password"])
            cursor = self.conn.cursor()
            print(query)
            result = cursor.execute(query)

            cred_id, hosts = result.lastrowid, credential["Hosts"]
            if len(hosts) > 0:
                query = self.query_manager.get_insert_hosts(cred_id, hosts)
                print(query)
                cursor.executescript(query)

            emails = credential["Emails"]
            if len(emails) > 0:
                query = self.query_manager.get_insert_emails(cred_id, emails)
                print(query)
                cursor.executescript(query)

            questions = credential["Questions"]
            if len(questions):
                query = self.query_manager.get_insert_questions(cred_id, questions)
                print(query)
                cursor.executescript(query)

            info = credential["Other_info"]
            if len(info) > 0:
                query = self.query_manager.get_insert_info(cred_id, info)
                print(query)
                cursor.executescript(query)

            cursor.close()
            transaction = True
        except Exception as ex:
            click.echo(f"Error saving credentials to database: {ex}")
        finally:
            if transaction:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    def get_all_apps(self):
        apps = tuple()
        try:
            query = self.query_manager.get_all_apps()
            with self.conn as connection:
                cursor = connection.cursor()
                result = cursor.execute(query)
                apps = result.fetchall()
                cursor.close()
        except Exception as ex:
            click.echo(f"Error saving credentials to the database: {ex}")
        finally:
            if self.conn:
                self.conn.close()
            return apps

    def get_details_by_app(self, app):
        data = dict()
        try:
            query = self.query_manager.get_details_by_app(app)
            with self.conn as connection:
                cursor = connection.cursor()
                result = cursor.execute(query)
                result = result.fetchone()
                if result is None or len(result) < 1:
                    click.echo(f"No Apps found with name {app}", err=True)
                else:
                    creation_date = datetime.datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S.%f')
                    duration = datetime.datetime.now() - creation_date
                    duration, units = get_duration(duration.total_seconds())

                    data["Application Name"], data["username"], data["password"] = result[0], result[1], result[2]
                    data["created"] = f"{duration} {units} ago"

                    query = self.query_manager.get_hosts_by_app(result[0])
                    result = cursor.execute(query).fetchall()
                    data["Hosts"] = list(result)

                    query = self.query_manager.get_emails_by_app(result[0])
                    result = cursor.execute(query).fetchall()
                    data["emails"] = list(result)

                    query = self.query_manager.get_questions_by_app(result[0])
                    result = cursor.execute(query).fetchall()
                    security_questions = list()
                    for item in result:
                        security_questions.append({
                            "Question": item[0],
                            "Answer": item[1]
                        })

                    query = self.query_manager.get_info_by_app(result[0])
                    result = cursor.execute(query).fetchall()
                    info = list()
                    for item in result:
                        info.append({
                            "Key": item[0],
                            "Value": item[1]
                        })

                    data["Security Questions"], data["Other Info"] = security_questions, info
                cursor.close()
        except Exception as ex:
            click.echo(f"Error retrieving details from database: {ex}", err=True)
        finally:
            if self.conn:
                self.conn.close()
            return data

    def get_password_by_app(self, app):
        password = str()
        try:
            query = self.query_manager.get_password(app)
            with self.conn as connection:
                cursor = connection.cursor()
                result = cursor.execute(query).fetchone()
                if result is None:
                    click.echo(f"No Apps found with name {app}", err=True)
                else:
                    password = result[0]
                cursor.close()
        except Exception as ex:
            click.echo(f"Error retrieving password from database: {ex}", err=True)
        finally:
            if self.conn:
                self.conn.close()
            return password

    def get_all_data(self):
        data = dict()
        try:
            with self.conn as connection:
                query = self.query_manager.get_all_credentials()
                cursor = connection.cursor()
                credentials = cursor.execute(query).fetchall()
                query = self.query_manager.get_all_hosts()
                hosts = cursor.execute(query).fetchall()
                query = self.query_manager.get_all_emails()
                emails = cursor.execute(query).fetchall()
                query = self.query_manager.get_all_questions()
                questions = cursor.execute(query).fetchall()
                query = self.query_manager.get_all_info()
                info = cursor.execute(query).fetchall()

                for item in credentials:
                    data[item[0]] = {
                        "app": item[1],
                        "username": item[2],
                        "password": item[3],
                        "hosts": set(),
                        "emails": set(),
                        "questions": list(),
                        "info": list()
                    }

                for item in hosts:
                    cred_id, val = item[0], item[1]
                    data[cred_id]["hosts"].add(val)

                for item in emails:
                    cred_id, val = item[0], item[1]
                    data[cred_id]["emails"].add(val)

                for item in questions:
                    data[item[0]]["questions"].append({
                        "question": item[1],
                        "answer": item[2]
                    })

                for item in info:
                    data[item[0]]["info"].append({
                        "key": item[1],
                        "value": item[2]
                    })
                cursor.close()
        except Exception as ex:
            click.echo(f"Error retrieving details from database: {ex}", err=True)
        finally:
            if self.conn:
                self.conn.close()
            return data


def get_duration(seconds):
    duration, units = seconds, "sec"
    if duration > 60:
        duration, units = divmod(seconds, 60)[0], "mins"  # duration in minutes
    if duration > 60:
        duration, units = divmod(seconds, 3600)[0], "hrs"  # duration in hours
    if duration > 24:
        duration, units = divmod(seconds, 86400)[0], "days"  # duration in days
    if duration > 7:
        duration, units = divmod(seconds, 31536000)[0], "weeks"  # duration in years
    return duration, units
