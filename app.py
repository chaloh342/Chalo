# Flask Voting App for Chama / Group
from flask import Flask, render_template_string, request

app = Flask(__name__)

# ------------------------
# POSTS & CANDIDATES
# ------------------------
posts = {
    "Chairperson": ["Alice", "Brian"],
    "Vice Chairperson": ["Carol", "David"],
    "Secretary": ["Eve", "Frank"],
    "Assistant Secretary": ["Grace", "Henry"],
    "Treasurer": ["Ivy", "Jack"],
    "Assistant Treasurer": ["Karen", "Leo"],
    "Organizing Secretary": ["Mona", "Nate"],
    "Welfare Officer": ["Olivia", "Paul"],
    "Discipline Officer": ["Quinn", "Ray"],
    "Public Relations Officer": ["Sara", "Tom"]
}

# ------------------------
# REGISTERED VOTERS (sample IDs)
# ------------------------
registered_voters = {"001", "002", "003", "004", "005"}
voted = set()

# ------------------------
# VOTE COUNTER
# ------------------------
votes = {post: {c: 0 for c in posts[post]} for post in posts}

# ------------------------
# HTML TEMPLATE
# ------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Group Voting</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h2>Chama / Group Voting</h2>
<form method="post">
Voter ID:<br>
<input name="voter" required><br><br>

{% for post, cands in posts.items() %}
<b>{{ post }}</b><br>
{% for c in cands %}
<input type="radio" name="{{ post }}" value="{{ c }}" required> {{ c }}<br>
{% endfor %}
<br>
{% endfor %}

<button type="submit">Submit Vote</button>
</form>
<p style="color:red;">{{ msg }}</p>
</body>
</html>
"""

# ------------------------
# ROUTES
# ------------------------
@app.route("/", methods=["GET", "POST"])
def vote():
    msg = ""
    if request.method == "POST":
        voter = request.form["voter"]

        if voter not in registered_voters:
            msg = "❌ Not a registered voter"
        elif voter in voted:
            msg = "❌ You have already voted"
        else:
            for post in posts:
                choice = request.form[post]
                votes[post][choice] += 1
            voted.add(voter)
            return "<h3>✔ Vote submitted successfully!</h3>"

    return render_template_string(HTML, posts=posts, msg=msg)

@app.route("/results")
def results():
    return str(votes)

# ------------------------
# RUN SERVER
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
