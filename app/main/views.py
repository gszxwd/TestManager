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
        try:
            session.clear()     # for re-login
            prcp = Principal.query.filter_by(Email=request.form["inputEmail"]).first()
            if prcp is None:
                prcp = Tester.query.filter_by(Email=request.form["inputEmail"]).first()
            if prcp is not None and prcp.Password == request.form["inputPassword"]:
                # login limitation
                if (datetime.now()-prcp.LogTime).seconds < 30*60:
                    flash(u'连续错误登录3次，请等30分钟后再试')
                    return redirect(url_for('.login'))
                session['name'] = prcp.Email
                session['priv'] = prcp.Role
                if session['priv'] == '4':
                    session['checked'] = prcp.IsChecked
                    # black-list filtering
                    blacklists = Supervision.query.filter_by(TName=prcp.Name).filter_by(SType="3").all()
                    isBlacked = False
                    for black in blacklists:
                        if black.EndTime > datetime.now():
                            isBlacked = True
                            break
                    session['black'] = isBlacked
                login_user(prcp)
                #return redirect(url_for('.login'))
            else:
                # login limitation
                if (datetime.now()-prcp.LogTime).seconds < 30*60:
                    flash(u'连续错误登录3次，请等30分钟后再试')
                    return redirect(url_for('.login'))
                if prcp.LogCount == 3:
                    flash(u'连续错误登录3次，请等30分钟后再试')
                    prcp.LogTime = datetime.now()
                    prcp.LogCount = 0
                else:
                    prcp.LogCount = prcp.LogCount + 1
                    flash(u'无效的用户名或密码')
                db.session.commit()
                return redirect(url_for('.login'))
        except:
            flash(u'登录错误，请重试')
            db.session.rollback()
            db.session.flush()
            return redirect(url_for('.login'))
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
                db.session.rollback()
                db.session.flush()
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.contract'))
            return redirect(url_for('.login'))
        else:
            testers = Tester.query.filter_by(IsChecked=True).all()
            temp = []
            for tester in testers:
                # black-list filtering
                blacklists = Supervision.query.filter_by(TName=tester.Name).filter_by(SType="3").all()
                isBlacked = False
                for black in blacklists:
                    if black.EndTime > datetime.now():
                        isBlacked = True
                        break
                if isBlacked == False:
                    temp.append(tester.Name)
            session['testers'] = temp
            return render_template('contract.html', name=session.get('name'), priv=session.get('priv'), testers=session.get('testers'))
    else:
        flash(u'请先登录')
        return redirect(url_for('.login'))

@main.route('/proof', methods=['GET', 'POST'])
def proof():
    if session['checked'] == False:
        flash(u'该机构尚未通过审核，请联系审核员')
        return redirect(url_for('.login'))
    if session['black'] == True:
        flash(u'该机构被列入黑名单，请联系审核员')
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
                db.session.rollback()
                db.session.flush()
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
                db.session.rollback()
                db.session.flush()
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

def password_test(str):
    if len(str) < 8:
        return False
    charFlag = False
    numFlag = False
    for ch in str:
        if ord(ch)>=65 and ord(ch)<=90:
            charFlag = True
        if ord(ch)>=97 and ord(ch)<=122:
            charFlag = True
        if ord(ch)>=32 and ord(ch)<=64:
            numFlag = True
    if charFlag and numFlag:
        return True
    else:
        return False


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if request.form['password'] != request.form['password2']:
            flash(u'密码不匹配，请重新输入')
            return redirect(url_for('.signup'))
        if not password_test(request.form['password']):
            flash(u'请保证数字和字母组合的8位以上密码强度')
            return redirect(url_for('.signup'))
        if request.form['role'] != '4':
            try:
                new_pcl = Principal(Email=request.form['email'],
                                    Password=request.form['password'],
                                    Name=request.form['name'],
                                    Role=request.form['role'],
                                    Address=request.form['address'],
                                    Contacts=request.form['contacts'],
                                    Telephone=request.form['telephone'],
                                    RegTime=datetime.now(),
                                    LogCount=0,
                                    LogTime=datetime(2000,1,1))
                db.create_all()
                db.session.add(new_pcl)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
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
                                EstbTime=datetime(2099,1,1),
                                RegTime=datetime.now(),
                                LogCount=0,
                                LogTime=datetime(2000,1,1))
                db.create_all()
                db.session.add(tester)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.signup'))
            session['name'] = tester.Email
            session['priv'] = tester.Role
            session['checked'] = tester.IsChecked
            # black-list filtering
            blacklists = Supervision.query.filter_by(TName=tester.Name).filter_by(SType="3").all()
            isBlacked = False
            for black in blacklists:
                if black.EndTime > datetime.now():
                    isBlacked = True
                    break
            session['black'] = isBlacked
            return redirect(url_for(".signup2"))
    else:
        return render_template('signup.html', name=session.get('name'))

ALLOWED_EXTENSIONS = set(['gif', 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@main.route('/signup2', methods=['GET', 'POST'])
def signup2():
    if request.method == "POST":
        try:
            tester = Tester.query.filter_by(Email=session.get('name')).first()
            #types = request.form.getlist('certtype')
            #for ty in types:
            #    if ty == u"hascma":
            #        tester.HasCMA = True
            #    if ty == u"hascnas":
            #        tester.HasCNAS = True
            #    if ty == u"hascert":
            #        tester.HasCert = True
            if request.form['estbtime']:
                temps = request.form['estbtime'].split('-')
                tester.EstbTime = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
            else:
                tester.EstbTime = datetime(2099,1,1)
            if request.form['cmastart'] and request.form['cmaend']:
                temps = request.form['cmastart'].split('-')
                tester.CMAStart = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
                temps = request.form['cmaend'].split('-')
                tester.CMAEnd = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
            else:
                tester.CMAStart = datetime(2099,1,1)
                tester.CMAEnd = datetime(2099,1,1)
            if request.form['cnasstart'] and request.form['cnasend']:
                temps = request.form['cnasstart'].split('-')
                tester.CNASStart = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
                temps = request.form['cnasend'].split('-')
                tester.CNASEnd = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
            else:
                tester.CNASStart = datetime(2099,1,1)
                tester.CNASEnd = datetime(2099,1,1)
            if request.form['certstart'] and request.form['certend']:
                temps = request.form['certstart'].split('-')
                tester.CertStart = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
                temps = request.form['certend'].split('-')
                tester.CertEnd = datetime(int(temps[0]), int(temps[1]), int(temps[2]))
            else:
                tester.CertStart = datetime(2099,1,1)
                tester.CertEnd = datetime(2099,1,1)
            cmafile = request.files['cmafile']
            tempdir = "app/static/"+datetime.now().strftime("%Y%m%d%H%M%S")
            os.makedirs(os.path.abspath(tempdir))
            if cmafile:
                if not allowed_file(cmafile.filename):
                    flash(u"不支持的图片格式")
                    return redirect(url_for('.signup2'))
                tester.CMAPath = os.path.abspath(os.path.join(tempdir, cmafile.filename))
                cmafile.save(tester.CMAPath)
                tester.HasCMA = True
            cnasfile = request.files['cnasfile']
            if cnasfile:
                if not allowed_file(cnasfile.filename):
                    flash(u"不支持的图片格式")
                    return redirect(url_for('.signup2'))
                tester.CNASPath = os.path.abspath(os.path.join(tempdir, cnasfile.filename))
                cnasfile.save(tester.CNASPath)
                tester.HasCNAS = True
            certfile = request.files['certfile']
            if certfile:
                if not allowed_file(certfile.filename):
                    flash(u"不支持的图片格式")
                    return redirect(url_for('.signup2'))
                tester.CertPath = os.path.abspath(os.path.join(tempdir, certfile.filename))
                certfile.save(tester.CertPath)
                tester.HasCert = True
            testrange = request.form.getlist('testrange')
            tester.TestRange = ','.join(testrange)
            db.session.commit()
            login_user(tester)
        except:
            db.session.rollback()
            db.session.flush()
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
                dirstr = '/'.join(dirstr.split('\\'))
                temp.append(dirstr.replace(" ", "%20"))                                 #6
                temp.append(tester.CMAStart.strftime("%Y-%m-%d"))   #7
                temp.append(tester.CMAEnd.strftime("%Y-%m-%d"))     #8
            if tester.HasCNAS == True:
                pos = tester.CNASPath.find('static')
                dirstr = tester.CNASPath[pos:]
                dirstr = '/'.join(dirstr.split('\\'))
                temp.append(dirstr.replace(" ", "%20"))
                temp.append(tester.CNASStart.strftime("%Y-%m-%d"))
                temp.append(tester.CNASEnd.strftime("%Y-%m-%d"))
            if tester.HasCert == True:
                pos = tester.CertPath.find('static')
                dirstr = tester.CertPath[pos:]
                dirstr = '/'.join(dirstr.split('\\'))
                temp.append(dirstr.replace(" ", "%20"))
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
                db.session.rollback()
                db.session.flush()
                flash(u'填写错误，请重新检查后再提交')
                return redirect(url_for('.supervise'))
            flash(u'提示：提交成功')
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

@main.route('/browse', methods=['GET', 'POST'])
def browse():
    if current_user.is_authenticated() and session['priv']=='5':
        if request.method == "POST":
            return redirect(url_for('.login'))
        else:
            advices = Advice.query.all()
            temp = []
            for advice in advices:
                temp.append(advice.AdviceTime.strftime("%Y-%m-%d"))
                temp.append(advice.TName)
                temp.append(advice.Content)
            session['advices'] = temp
            return render_template('browse.html', name=session.get('name'), priv=session.get('priv'), advices=session.get('advices'))
    else:
        flash('Please login first')
        return redirect(url_for('.login'))
