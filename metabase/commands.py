import json
import os
from pprint import pprint

import requests

from tests.data_creators import clean_database, clean_views
from db import DATABASE_URL, LOCAL_DATABASE_URL
from utils.logger import logger

METABASE_URL = os.environ.get('METABASE_URL', 'http://localhost:3002')


def configure_new_metabase_session(user_name: str, password: str):
    response = requests.post(f'{METABASE_URL}/api/session/',
                             json={"username": user_name, "password": password})
    session = response.json()
    return session['id']


def get_connected_database_id(database_name: str, session_id: str):
    response = requests.get(f'{METABASE_URL}/api/database/',
                            headers={'cookie': f'metabase.SESSION={session_id}'})
    table_infos = [table for table in response.json() if table['name'] == database_name]
    return table_infos[0]['id']


def switch_metabase_database_connection(database_name: str, user_name: str, password: str):
    session_id = configure_new_metabase_session(user_name, password)
    database_id = get_connected_database_id(database_name, session_id)
    app_name = get_app_name_for_restore()
    db_details = get_db_details_by_app_name(app_name)
    db_details['ssl'] = False if LOCAL_DATABASE_URL == DATABASE_URL else True
    db_settings = {'details': db_details,
                 'name': database_name,
                 'engine': "postgres"}
    requests.put(f'{METABASE_URL}/api/database/{database_id}',
                 headers={'cookie': f'metabase.SESSION={session_id}'},

                 json=db_settings)


def get_connected_database_host_name(database_name: str, session_id: str):
    database_id = get_connected_database_id(database_name, session_id)
    response = requests.get(f'{METABASE_URL}/api/database/{database_id}',
                            headers={'cookie': f'metabase.SESSION={session_id}'})
    jsonified_response = response.json()
    return jsonified_response['details']['host']


def get_app_name_for_restore():
    session_id = configure_new_metabase_session(os.environ.get('METABASE_USER_NAME'), os.environ.get('METABASE_PASSWORD'))
    host = get_connected_database_host_name(os.environ.get('METABASE_DBNAME'), session_id)
    db_blue = json.loads(os.environ.get('BLUE_DB_INFO'))
    db_green = json.loads(os.environ.get('GREEN_DB_INFO'))
    if db_blue['details']['host'] == host:
        return db_green['app_name']
    return db_blue['app_name']


def get_db_details_by_app_name(app_name: str):
    db_blue = json.loads(os.environ.get('BLUE_DB_INFO'))
    db_green = json.loads(os.environ.get('GREEN_DB_INFO'))
    if db_blue['app_name'] == app_name:
        return db_blue['details']
    return db_green['details']


def clean_database_if_local():
    if LOCAL_DATABASE_URL == DATABASE_URL:
        clean_database()
        clean_views()
        logger.info('[CLEAN DATABASE AND VIEW] Database cleaned')
        return
    logger.info('[CLEAN DATABASE AND VIEW] Cannot clean production database')


def get_token_setup():
    requests.get(f'{METABASE_URL}/setup')
    response = requests.get(f'{METABASE_URL}/session/properties')
    if response.content:
        if "setup-token" in str(response.content):
            return [content for content in str(response.content).split(',') if "setup-token" in content][0].split(':')[1]


def post_create_metabase_superuser(token):
    db_blue = json.loads(os.environ.get('BLUE_DB_INFO'))
    user_email = os.environ.get('METABASE_USER_NAME', 'admin@example.com')
    user_password = os.environ.get('METABASE_PASSWORD', 'user@AZERTY123')
    payload = {"token": token,
    "prefs":{
        "site_name":"pc",
    "allow_tracking":"true"},
    "database":{
        "engine":"postgres",
        "name":"Produit",
        "details":{
            "host":db_blue['details']['host'],
            "port":db_blue['details']['port'],
            "dbname":db_blue['details']['dbname'],
            "user":db_blue['details']['user'],
            "password":db_blue['details']['password'],
            "ssl":False,
            "additional-options":None,
            "tunnel-enabled":False},
        "auto_run_queries":True,
        "is_full_sync":True,"schedules":{
            "cache_field_values":{
                "schedule_day":None,
                "schedule_frame":None,
                "schedule_hour":0,
                "schedule_type":"daily"},
        "metadata_sync":{
            "schedule_day":None,
            "schedule_frame":None,
            "schedule_hour":None,
            "schedule_type":"hourly"}}},
    "user":{
        "first_name":"pc",
        "last_name":"admin",
        "email":user_email,
        "password":user_password,
        "site_name":"pc"}
    }
    response = requests.post(f'{METABASE_URL}/api/setup',
        json=payload)


def initialize_metabase_if_local():
    token = get_token_setup()[1:-1]
    post_create_metabase_superuser(token)