from flask import Flask, render_template, request,redirect, url_for
from flask import session
from opt import *

app = Flask(__name__)
app.secret_key = '555555'
s = '<a href="/"> 返回首页</a>'
@app.route("/")
def Login():
    return render_template('home.html')

@app.route("/fansIndex")
def Fans():
    return render_template('fansIndex.html')

@app.route("/logout")
def Logout():
    session.pop("username", None)
    return redirect(url_for("Login"))

@app.route("/re")
def Register():
    return render_template("register.html")

@app.route("/index")
def Index():
    if "username" in session: # 检测是否登录
        return render_template("index.html")
    else :
        return redirect(url_for("Login"))

@app.route("/login", methods = ["post"]) # 登录
def login():
    name = request.form.get("username")
    pwd = request.form.get("password")
    sql1 = "select * from login where username = '%s'" % (name)
    ans = conMySql(sql1)
    ansSelect = ans.fetchall()
    # 判断用户是否存在
    if len(ansSelect) == 0:
        return "用户不存在或输入账号错误，请重新登录！" + s
    # 判断用户密码错误
    if pwd != ansSelect[0]['password']:
        return "密码错误，请重新登录！" + s
    
    session["username"] = name
    # 先写个fan专门用的index
    print(ansSelect, ansSelect[0]["type"])
    if ansSelect[0]["type"] == "fan":
        return redirect(url_for("Fans"))
    else :
        return redirect(url_for("Index"))

@app.route("/register", methods = ["post"])
def register():
    name = request.form.get("username")
    pwd = request.form.get("password")
    pwd2 = request.form.get("password2")
    typeU = request.form.get("userType")
    sql1 = "select * from login where username = '%s'" % (name)
    ans = conMySql(sql1).fetchall()
    print(ans)
    if len(ans) != 0: # 这个用户存在
        return "该用户名已经存在!" + s
    else :
        if pwd2 != pwd:
            return "两次用户密码不一致，请重新注册！" + s
        if typeU == '':
            return  "请选择用户类型！" + s
        sql2 = "INSERT INTO login(username, password, type) VALUES ('%s', '%s', '%s')" % (name, pwd, typeU)
        conMySql(sql2)
        return "注册成功，请返回登录吧" + s

@app.route("/bands")
def Bands():
    sql = "select * from band;"
    bands = conMySql(sql).fetchall()
    print(bands)
    return render_template("bands.html", bands = bands)

if __name__ == '__main__':
    app.run()