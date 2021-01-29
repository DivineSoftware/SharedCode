from flask import Flask
import random, string, flask, os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template("codeindex.html")
    else:
        if flask.request.form['captcha']==flask.request.form['solution']:
            password = create_session()
            syntax = flask.request.form['syntax']
            return flask.redirect("/sessions/" + password + "&syntax=" + syntax)
        else:
            return "Wrong captcha"
        
@app.route("/sessions/<code>&syntax=<syntax>", methods=['GET', 'POST'])
def sessions(code, syntax):
    if flask.request.method == 'GET':
        try:
                if syntax == "java":
                  syntax = "clike"
                  syntax_arg = "clike-java"
                elif syntax == "cpp":
                  syntax = "clike"
                  syntax_arg = "clike-cpp"
                elif syntax == "csharp":
                  rsyntax = "clike"
                  syntax_arg = "clike-csharp"
                else:
                  syntax_arg = "None"
                content = os.getenv(code)
                return flask.render_template("session.html", content=content, syntax=syntax, syntax_arg=syntax_arg)
        except Exception as e:
            print(e)
            return "Session not found"
    else:
        try:
            with open("sessions/" + code, "w") as program:
                program.write(flask.request.form['body'])
                return ('', 204)
        except Exception as e:
            print(e)
            return "Error when saving"
                    
def create_session():
    password = ""
    for _ in range(3):
        password += random.choice(string.ascii_lowercase)
        password += random.choice(string.ascii_uppercase)
        password += random.choice(string.digits)
    if oos.path.exists("sessions/" + password):
        for _ in range(3):
            password += random.choice(string.ascii_lowercase)
            password += random.choice(string.ascii_uppercase)
            password += random.choice(string.digits)
    else:
        open("sessions/" + password, 'a').close()
    return password
    
if __name__ == '__main__':
    app.run("0.0.0.0")