__author__ = 'Xu Zhao'

from datetime import datetime
from flask import render_template, request, redirect, url_for
from ..models import Principal
from .. import db
from . import main

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        prcp = Principal.query.filter_by(Email=request.form["inputEmail"]).first()
        if prcp.Email == request.form["inputEmail"] and prcp.Password == request.form["inputPassword"]:
            return redirect(url_for('.login'))
        else:
            return redirect(url_for('.signup'))
    else:
        return render_template('index.html')

@main.route('/contract')
def contract():
    return render_template('contract.html')

@main.route('/proof')
def proof():
    return render_template('proof.html')

@main.route('/advice')
def advice():
    return render_template('advice.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        new_pcl = Principal(Email=request.form['email'],
                        Password=request.form['password'],
                        Name='ABC',
                        Role='1',
                        Address='DEF',
                        Contacts='ZX',
                        Telephone='123',
                        RegTime=datetime.now())
        db.create_all()
        db.session.add(new_pcl)
        db.session.commit()
        return redirect(url_for(".login"))
    else:
        return render_template('signup.html')
