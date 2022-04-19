from os.path import isfile
from sqlite3 import connect

DB_PATH = "./dc_bot_i_pass_butter/data/db/database.db"
BUILD_PATH = "./dc_bot_i_pass_butter/data/db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cursor = cxn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
        
    return inner

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)
    
        
def commit():
    cxn.commit()
    
def close():
    cxn.close()
    
def field(command, *values):
    cursor.execute(command, tuple(values))
    if (fetch := cursor.fetchone()) is not None:
        return fetch[0]
    
def record(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchone()

def records(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchall()

def column(command, *values):
    cursor.execute(command, tuple(values))
    return [item[0] for item in cursor.fetchall()]

def execute(command, *values):
    cursor.execute(command, tuple(values))
    
def multiexec(command, valueset):
    cursor.executemany(command, valueset)
    
def scriptexec(path):
    with open(path, encoding="utf-8") as script:
        cursor.executescript(script.read())
        
    