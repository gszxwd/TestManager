__author__ = 'Xu Zhao'

from datetime import datetime
import os
from flask import render_template, request, session, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from ..models import Principal, Tester, TestContract
from .. import db
from . import main

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        prcp = Principal.query.filter_by(Email=request.form["inputEmail"]).first()
        if prcp is None:
            prcp = Tester.query.filter_by(Email=request.form["inputEmail"]).first()
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

@main.route('/contract', methods=['GET', 'POST'])
def contract():
    if current_user.is_authenticated():
        if request.method == "POST":
            temps = request.form['onlinetime'].split('-')
            isupdated = False
            if request.form.get('isupdated') == u'y':
                isupdated = True
            additionreqs = request.form.getlist('additionreq')
            testrank = max(int(request.form['rangerate']),
                           int(request.form['capacityrate']),
                           int(request.form['safetyrate']))
            test_contract = TestContract(Name=request.form['name'],
                                         TName=request.form['tname'],
                                         Category=request.form['category'],
                                         Function=request.form['function'],
                                         Version=request.form['version'],
                                         Budgetary=request.form['budgetary'],
                                         OnlineTime=datetime(int(temps[0]), int(temps[1]), int(temps[2])),
                                         IsUpdated=isupdated,
                                         RangeRate=request.form['rangerate'],
                                         CapacityRate=request.form['capacityrate'],
                                         SafetyRate=request.form['safetyrate'],
                                         TestRank=str(testrank),
                                         AdditionReq=','.join(additionreqs),
                                         PMail=session.get('name'),
                                         RecordTime=datetime.now())
            db.create_all()
            db.session.add(test_contract)
            db.session.commit()
            return redirect(url_for('.login'))
        else:
            testers = Tester.query.all()
            temp = []
            for tester in testers:
                temp.append(tester.Name)
            session['testers'] = temp
            return render_template('contract.html', name=session.get('name'), testers=session.get('testers'))
    else:
        flash('Please login first')
        return redirect(url_for('.login'))

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

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@main.route('/signup2', methods=['GET', 'POST'])
def signup2():
    if request.method == "POST":
        tester = Tester.query.filter_by(Email=session.get('name')).first()
        types = request.form.getlist('certtype')
        for ty in types:
            if ty == u"hascma":
                tester.HasCMA = True
            if ty == u"hascnas":
                tester.HasCNAS = True
            if ty == u"hascert":
                tester.HasCert = True
        if request.form['estbtime']:
            temps = request.form['estbtime'].split('-')
            tester.EstbTime = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
        if request.form['cmastart'] and request.form['cmaend']:
            temps = request.form['cmastart'].split('-')
            tester.CMAStart = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
            temps = request.form['cmaend'].split('-')
            tester.CMAEnd = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
        if request.form['cnasstart'] and request.form['cnasend']:
            temps = request.form['cnasstart'].split('-')
            tester.CNASStart = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
            temps = request.form['cnasend'].split('-')
            tester.CNASEnd = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
        if request.form['certstart'] and request.form['certend']:
            temps = request.form['certstart'].split('-')
            tester.CMAStart = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
            temps = request.form['certend'].split('-')
            tester.CMAEnd = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
        # TODO: absolute and unique path & create directory
        cmafile = request.files['cmafile']
        if cmafile and allowed_file(cmafile.filename):
            tester.CMAPath = os.path.join("D://uploads//", cmafile.filename)
            cmafile.save(tester.CMAPath)
        cnasfile = request.files['cnasfile']
        if cnasfile and allowed_file(cnasfile.filename):
            tester.CNASPath = os.path.join("D://uploads//", cnasfile.filename)
            cnasfile.save(tester.CNASPath)
        certfile = request.files['certfile']
        if certfile and allowed_file(certfile.filename):
            tester.CertPath = os.path.join("D://uploads//", certfile.filename)
            certfile.save(tester.CertPath)
        testrange = request.form.getlist('testrange')
        tester.TestRange = ','.join(testrange)
        db.session.commit()
        login_user(tester)
        return redirect(url_for(".login"))
    else:
        return render_template('signup2.html', name=session.get('name'))
