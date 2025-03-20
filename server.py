from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Keeps the current vote counts for each category (excluding "undo" from display)
votes = {
    "got it": 0,
    "confused": 0,
    "example needed": 0
}

# Tracks each student's latest vote (keyed by student_id)
student_votes = {}

@app.route('/')
@app.route('/teacher')
def teacher_ui():
    """ Serves the teacher's dashboard """
    return render_template('teacher.html')

@app.route('/api/votes', methods=['GET'])
def get_votes():
    """ Provides vote counts as JSON for the frontend chart (excluding undo) """
    return jsonify(votes)

@app.route('/api/vote', methods=['POST'])
def submit_vote():
    """ Handles student votes with session-based logic """
    global votes, student_votes

    data = request.get_json()
    student_id = data.get('student_id')
    vote_type = data.get('vote')

    if not student_id or vote_type not in ["got it", "confused", "example needed", "undo"]:
        return jsonify({"error": "Invalid request"}), 400

    # Handle "undo" logic
    if vote_type == "undo":
        if student_id in student_votes:
            last_vote = student_votes.pop(student_id)  # Remove student's last vote
            votes[last_vote] -= 1  # Decrease its count
        return jsonify(votes), 200  # Return updated votes (without "undo")

    # If the student has already voted in this session and hasn't undone, reject the new vote
    if student_id in student_votes:
        return jsonify({"error": "Vote already submitted, undo first"}), 400

    # Register new vote
    votes[vote_type] += 1
    student_votes[student_id] = vote_type

    return jsonify(votes), 200

@app.route('/api/reset_votes', methods=['POST'])
def reset_votes():
    """ Starts a new voting session (clears votes & student records) """
    global votes, student_votes
    votes = {"got it": 0, "confused": 0, "example needed": 0}  # Reset votes (excluding "undo")
    student_votes = {}  # Reset student tracking
    return jsonify(votes)

# def populate_dummy_data():
#     """
#     Populates the votes dictionary with dummy data for testing purposes.
#     """
#     global votes, student_votes
    
#     # Example dummy data
#     dummy_votes = {
#         "got it": 10,
#         "confused": 5,
#         "example needed": 3,
#         "undo": 2
#     }
    
#     # Update the votes dictionary with dummy data
#     votes.update(dummy_votes)
    
#     # Optionally, populate student_votes with dummy data
#     student_votes = {
#         "student_1": "got it",
#         "student_2": "confused",
#         "student_3": "example needed",
#         "student_4": "got it",
#         "student_5": "undo"
#     }

# Call this function to populate the UI with dummy data
#populate_dummy_data()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)