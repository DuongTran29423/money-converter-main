from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    curs = ["USD", "EUR", "GBP"]
    cur_values = [24830, 26266, 30426]

    if request.method == "POST":
        src_input = int(request.form['source-input'])
        currency = request.form['currency']
        index = curs.index(currency)
        result = src_input * cur_values[index]
        return render_template('index.html', result=result, prev_input=src_input, curs=curs, cur_values=cur_values)

    else:
        return render_template('index.html', curs=curs, cur_values=cur_values)


if __name__ == "__main__":
    app.run(debug=True)
