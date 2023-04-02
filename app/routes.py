from app import app, db_controls
from flask import render_template, request, redirect


@app.route("/")
@app.route("/add_book", methods=["POST", "GET"])
def add_book():
    all_topics = db_controls.get_db()
    all_topics = [str(i[0]).replace("_", " ") for i in all_topics]
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        genre = request.form["genre"]
        language = request.form["language"]
        topic = request.form["topic"]
        topic = topic.replace(" ", "_")
        msg = db_controls.add_new_book(title, author, genre, language, topic_to_insert=topic)
        return render_template("add_book.html", all_topics=all_topics, msg=msg)
    return render_template("add_book.html", all_topics=all_topics)


@app.route("/book_test")
@app.route("/book_test/<topic>", methods=['GET', 'POST'])
def book_test(topic=None):
    if topic:
        topic = topic.replace(" ", "_")
        all_data = db_controls.get_db(topic)
    else:
        all_data = db_controls.get_db("book_test")
    return render_template("book_test.html", all_data=all_data)


@app.route("/add_topic", methods=['GET', 'POST'])
def add_topic():
    all_topics = db_controls.get_db()
    all_topics = [str(i[0]).replace("_", " ") for i in all_topics]
    if request.method == "POST":
        msg = db_controls.add_new_book(topic=request.form["topic"])
        return msg
    return render_template("add_topic.html", all_topics=all_topics)


@app.route("/remove_table/<topic>")
def remove_table(topic):
    topic = topic.replace(" ", "_")
    db_controls.remove_table(topic)
    return redirect("/add_topic")