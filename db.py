from flask import g
import pymysql

def get_db():
    
    if 'db' not in g:
        g.db = pymysql.connect('localhost','root','test','todolist_borntodev')
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()