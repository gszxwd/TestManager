# -*- coding: utf-8 -*-
__author__ = 'Xu Zhao'

from datetime import datetime, timedelta
import os
from flask import render_template, request, session, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from ..models import Principal, Tester, TestContract, TestEvidence, Advice, Supervision
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
            session['priv'] = prcp.Role
            if session['priv'] == '4':
                session['checked'] = prcp.IsChecked
            login_user(prcp)
            return redirect(url_for('.login'))
        else:
            flash(u'无效的用户名或密码')
            return redirect(url_for('.login'))
    else:
        return render_template('index.html', name=session.get('name'), priv=session.get('priv'))

@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('.login'))

@main.route('/contract', methods=['GET', 'POST'])
def contract():
    if current_user.is_authenticated() and (session['priv']=='1' or session['priv']=='2'):
        if request.method == "POST":
            try:
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
            except:
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.contract'))
            return redirect(url_for('.login'))
        else:
            # TODO: black-list filtering
            testers = Tester.query.filter_by(IsChecked=True).all()
            temp = []
            for tester in testers:
                temp.append(tester.Name)
            session['testers'] = temp
            return render_template('contract.html', name=session.get('name'), priv=session.get('priv'), testers=session.get('testers'))
    else:
        flash(u'请先登录')
        return redirect(url_for('.login'))

@main.route('/proof', methods=['GET', 'POST'])
def proof():
    # TODO: black-list filtering
    if session['checked'] == False:
        flash(u'该机构尚未通过审核，请联系审核员')
        return redirect(url_for('.login'))
    if current_user.is_authenticated() and session['priv']=='4':
        if request.method == "POST":
            try:
                start = request.form['teststart'].split('-')
                end = request.form['testend'].split('-')
                basicreqs = request.form.getlist('basicreq')
                additionreqs = request.form.getlist('additionreq')
                evidence = TestEvidence(Name=request.form['name'],
                                        TMail=session.get('name'),
                                        TestStart=datetime(int(start[0]),int(start[1]),int(start[2])),
                                        TestEnd=datetime(int(end[0]),int(end[1]),int(end[2])),
                                        BasicReq=','.join(basicreqs),
                                        AddtionReq=','.join(additionreqs),
                                        TestEnv=request.form['testenv'],
                                        RegressNum=int(request.form['regressnum']),
                                        Version=request.form['version'],
                                        CodeLines=int(request.form['codelines']),
                                        DesignCases=int(request.form['designcases']),
                                        PassedCases=int(request.form['passedcases']),
                                        FFatalBugs=int(request.form['ffatalbugs']),
                                        RFatalBugs=int(request.form['rfatalbugs']),
                                        FCriticBugs=int(request.form['fcriticbugs']),
                                        RCriticBugs=int(request.form['rcriticbugs']),
                                        FCommBugs=int(request.form['fcommbugs']),
                                        RCommBugs=int(request.form['rcommbugs']),
                                        FAdviseBugs=int(request.form['fadvisebugs']),
                                        RAdviseBugs=int(request.form['radvisebugs']),
                                        UpdateTime=datetime.now())
                db.create_all()
                db.session.add(evidence)
                db.session.commit()
            except:
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.proof'))
            return redirect(url_for('.login'))
        else:
            systems = TestContract.query.filter_by(TName=session.get('name'))
            temp = []
            for system in systems:
                temp.append(system.Name)
            session['systems'] = temp
            return render_template('proof.html', name=session.get('name'), priv=session.get('priv'), systems=session.get('systems'))
    else:
        flash('Please login first')
        return redirect(url_for('.login'))

@main.route('/advice', methods=['GET', 'POST'])
def advice():
    if current_user.is_authenticated() and (session['priv']=='1' or session['priv']=='2' or session['priv']=='3'):
        if request.method == "POST":
            try:
                advice = Advice(TName=request.form['tname'],
                                Content=request.form['content'],
                                AdviceTime=datetime.now())
                db.create_all()
                db.session.add(advice)
                db.session.commit()
            except:
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.advice'))
            return redirect(url_for('.login'))
        else:
            # testers = Tester.query.all()
            testers = Tester.query.filter_by(IsChecked=True).all()
            temp = []
            for tester in testers:
                temp.append(tester.Name)
            session['testers'] = temp
            return render_template('advice.html', name=session.get('name'), priv=session.get('priv'), testers=session.get('testers'))
    else:
        flash('Please login first')
        return redirect(url_for('.login'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if request.form['role'] != '4':
            try:
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
            except:
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.signup'))
            session['name'] = new_pcl.Email
            session['priv'] = new_pcl.Role
            login_user(new_pcl)
            return redirect(url_for(".login"))
        else:
            try:
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
            except:
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.signup'))
            session['name'] = tester.Email
            session['priv'] = tester.Role
            return redirect(url_for(".signup2"))
    else:
        return render_template('signup.html', name=session.get('name'))

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@main.route('/signup2', methods=['GET', 'POST'])
def signup2():
    if request.method == "POST":
        try:
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
            cmafile = request.files['cmafile']
            tempdir = "app/static/"+datetime.now().strftime("%Y%m%d%H%M%S")
            os.makedirs(os.path.abspath(tempdir))
            if cmafile and allowed_file(cmafile.filename):
                tester.CMAPath = os.path.abspath(os.path.join(tempdir, cmafile.filename))
                cmafile.save(tester.CMAPath)
            cnasfile = request.files['cnasfile']
            if cnasfile and allowed_file(cnasfile.filename):
                tester.CNASPath = os.path.abspath(os.path.join(tempdir, cnasfile.filename))
                cnasfile.save(tester.CNASPath)
            certfile = request.files['certfile']
            if certfile and allowed_file(certfile.filename):
                tester.CertPath = os.path.abspath(os.path.join(tempdir, certfile.filename))
                certfile.save(tester.CertPath)
            testrange = request.form.getlist('testrange')
            tester.TestRange = ','.join(testrange)
            db.session.commit()
            login_user(tester)
        except:
            flash(u'填写错误，请重新检查后再提交')
            return redirect(url_for('.signup2'))
        return redirect(url_for(".login"))
    else:
        return render_template('signup2.html', name=session.get('name'))


@main.route('/audit', methods=['GET', 'POST'])
def audit():
    if current_user.is_authenticated() and session['priv']=='5':
        if request.method == 'POST':
            session['tname'] = request.form['tname']
            return redirect(url_for(".audit2"))
        else:
            testers = Tester.query.all()
            temp = []
            for tester in testers:
                if tester.IsChecked == False:
                    temp.append(tester.Name)
            session['testers'] = temp
            return render_template('audit.html', name=session.get('name'), priv=session.get('priv'), testers=session.get('testers'))
    else:
        flash('Please login first')
        return redirect(url_for(".login"))


@main.route('/audit2', methods=['GET', 'POST'])
def audit2():
    if current_user.is_authenticated() and session['priv']=='5':
        if request.method == 'POST':
            tester = Tester.query.filter_by(Name=session.get('tname')).first()
            tester.IsChecked = True
            tester.CheckName = session.get('name')
            tester.CheckTime = datetime.now()
            db.session.commit()
            return redirect(url_for('.audit'))
        else:
            tester = Tester.query.filter_by(Name=session.get('tname')).first()
            temp = []
            temp.append(tester.Address)                             #0
            temp.append(tester.EstbTime.strftime("%Y-%m-%d"))       #1
            temp.append(tester.Contacts)                            #2
            temp.append(tester.Telephone)                           #3
            temp.append(tester.TestRange)                           #4
            temp.append(tester.RegTime.strftime("%Y-%m-%d"))        #5
            if tester.HasCMA == True:
                pos = tester.CMAPath.find('static')
                dirstr = tester.CMAPath[pos:]
                dirstr.replace('\\', '/')
                temp.append(dirstr)                                 #6
                temp.append(tester.CMAStart.strftime("%Y-%m-%d"))   #7
                temp.append(tester.CMAEnd.strftime("%Y-%m-%d"))     #8
            if tester.HasCNAS == True:
                pos = tester.CNASPath.find('static')
                dirstr = tester.CNASPath[pos:]
                dirstr = dirstr.replace('\\', '/')
                temp.append(dirstr)
                temp.append(tester.CNASStart.strftime("%Y-%m-%d"))
                temp.append(tester.CNASEnd.strftime("%Y-%m-%d"))
            if tester.HasCert == True:
                pos = tester.CertPath.find('static')
                dirstr = tester.CertPath[pos:]
                dirstr = dirstr.replace('\\', '/')
                temp.append(dirstr)
                temp.append(tester.CertStart.strftime("%Y-%m-%d"))
                temp.append(tester.CertEnd.strftime("%Y-%m-%d"))
            session['tester'] = temp
            return render_template('audit2.html', tname=session.get('tname'), name=session.get('name'), priv=session.get('priv'), tester=session.get('tester'))
    else:
        flash('Please login first')
        return redirect(url_for('.login'))


@main.route('/supervise', methods=['GET', 'POST'])
def supervise():
    if current_user.is_authenticated() and session['priv']=='5':
        if request.method == 'POST':
            try:
                end_time = datetime.now()
                if request.form['stype'] == '3':
                    end_time = end_time + timedelta(365)
                superv = Supervision(TName=request.form['tname'],
                                     SType=request.form['stype'],
                                     Content=request.form['content'],
                                     Time=datetime.now(),
                                     EndTime=end_time,
                                     AName=session.get('name'))
                db.create_all()
                db.session.add(superv)
                db.session.commit()
            except:
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.supervise'))
            return redirect(url_for(".supervise"))
        else:
            testers = Tester.query.filter_by(IsChecked=True).all()
            temp = []
            for tester in testers:
                temp.append(tester.Name)
            session['testers'] = temp
            return render_template('supervise.html', name=session.get('name'), priv=session.get('priv'), testers=session.get('testers'))
    else:
        flash('Please login first')
        return redirect(url_for('.login'))
