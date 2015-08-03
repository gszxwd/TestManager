__author__ = 'Xu Zhao'

from datetime import datetime
from flask import render_template, request, session, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from ..models import Principal, Tester
from .. import db
from . import main

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        prcp = Principal.query.filter_by(Email=request.form["inputEmail"]).first()
        if prcp is not None and prcp.Email == request.form["inputEmail"] and prcp.Password == request.form["inputPassword"]:
            session['name'] = prcp.Email
            login_user(prcp)
            return redirect(url_for('.login'))
        else:
            flash('Invalid User/Password')
            return redirect(url_for('.signup'))
    else:
        return render_template('index.html', name=session.get('name'))

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.login'))

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
        if request.form['role'] != '4':
            new_pcl = Principal(Email=request.form['email'],
                                Password=request.form['password'],
                                Name=request.form['name'],
                                Role=request.form['role'],
                                Address=request.form['address'],
                                Contacts=request.form['contacts'],
                                Telephone=request.form['telephone'],
                                RegTime=datetime.now())
            db.create_all()
            db.session.add(new_pcl)
            db.session.commit()
            session['name'] = new_pcl.Email
            login_user(new_pcl)
            return redirect(url_for(".login"))
        else:
            tester = Tester(Email=request.form['email'],
                            Password=request.form['password'],
                            Name=request.form['name'],
                            Role=request.form['role'],
                            Address=request.form['address'],
                            Contacts=request.form['contacts'],
                            Telephone=request.form['telephone'],
                            HasCMA=False,
                            HasCNAS=False,
                            HasCert=False,
                            IsChecked=False,
                            RegTime=datetime.now())
            db.create_all()
            db.session.add(tester)
            db.session.commit()
            session['name'] = tester.Email
            return redirect(url_for(".signup2"))
    else:
        return render_template('signup.html')

@main.route('/signup2', methods=['GET', 'POST'])
def signup2():
    if request.method == "POST":
        tester = Tester.query.filter_by(Email=session.get('name')).first()
        tester.HasCMA = True
        db.session.commit()
        login_user(tester)
        return redirect(url_for(".login"))
    else:
        return render_template('signup2.html', name=session.get('name'))
