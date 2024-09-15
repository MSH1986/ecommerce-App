from multiprocessing import connection
from flask import render_template, url_for


def clients_display():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users_table"
    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('dashboard/clients.html', clients=records)
