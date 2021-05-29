from flask import *
import random, string, flask, os, time, json

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

@app.route('/refresh=<code>')
def refresh(code):
    def readcode():
        while True:
            json_data = json.dumps(
                {'value': open('sessions/' + code, 'r').read()})
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    return Response(readcode(), mimetype='text/event-stream')
  
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
                return flask.render_template("session.html", content=open("sessions/" + code, 'r').read(), syntax=syntax, code=code)
        except Exception as e:
            print(e)
            return "Session not found"
    else:
        try:
            with open("sessions/" + code, "w") as program:
                program.write(flask.request.form['body'].replace('\n', ''))
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
    if os.path.exists("sessions/" + password):
        for _ in range(3):
            password += random.choice(string.ascii_lowercase)
            password += random.choice(string.ascii_uppercase)
            password += random.choice(string.digits)
    else:
        open("sessions/" + password, 'a').close()
    return password
    
if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, threaded=True)