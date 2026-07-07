from flask import Flask, request, jsonify, render_template
from database import engine, SessionLocal
from models import Base, Student

Base.metadata.create_all(bind=engine)

app = Flask(__name__)  

PREFERRED_DEPARTMENTS = {"CS", "CSE", "IT"}

def check_eligibility(student):
    if student.active_backlogs.strip().upper() == "YES":
        return "Not Eligible"

    if student.percentage < 60:
        return "Not Eligible"

    if student.department.strip().upper() in PREFERRED_DEPARTMENTS:
        return "Eligible"

    return "Review Required"


@app.get("/")
def home():
    return render_template("index.html")

@app.get("/add-candidate")
def add_candidate_page():
    return render_template("add_candidate.html")


@app.get("/candidates-page")
def candidates_page():
    return render_template("candidates.html")


@app.get("/round1-page")
def round1_page():
    return render_template("round1.html")


@app.get("/shortlisted-page")
def shortlisted_page():
    return render_template("shortlisted.html")

@app.post("/candidates")
def create_candidate():
    
    data = request.get_json()

    session = SessionLocal()

    student = Student(
        name=data["name"],
        email=data["email"],
        mobile=data["mobile"],
        department=data["department"],
        percentage=data["percentage"],
        active_backlogs=data["active_backlogs"],
        prefered_techstack=data.get("prefered_techstack"),
        eligibility=None,
        requirement_understanding=None,
        feature_implementation=None,
        validation_edge_cases=None,
        code_structure=None,
        ai_usage=None,
        round_1_score=None,
        final_shortlist=None
    )

    session.add(student)
    session.commit()
    session.refresh(student)

    result = student.to_dict()

    session.close()

    return jsonify(result), 201

@app.get("/candidates")
def get_candidates():
    session = SessionLocal()

    query = session.query(Student)

    # Query parameters
    name = request.args.get("name")
    department = request.args.get("department")
    eligibility = request.args.get("eligibility")
    final_shortlist = request.args.get("final_shortlist")
    min_score = request.args.get("min_score", type=int)

    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))

    if department:
        query = query.filter(Student.department == department)

    if eligibility:
        query = query.filter(Student.eligibility == eligibility)

    if final_shortlist:
        query = query.filter(Student.final_shortlist == final_shortlist)

    if min_score is not None:
        query = query.filter(Student.round_1_score >= min_score)


    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "asc")

    if sort_by == "round_1_score":
        if order.lower() == "desc":
            query = query.order_by(Student.round_1_score.desc())
        else:
            query = query.order_by(Student.round_1_score.asc())
    students = query.all()

    result = [student.to_dict() for student in students]

    session.close()

    return jsonify(result)
@app.get("/candidates/<int:candidate_id>")
def get_candidate(candidate_id):
    session = SessionLocal()

    student = session.get(Student, candidate_id)

    if student is None:
        session.close()
        return jsonify({"error": "Candidate not found"}), 404

    result = student.to_dict()

    session.close()

    return jsonify(result)


@app.delete("/candidates/<int:candidate_id>")
def delete_candidate(candidate_id):
    session = SessionLocal()

    student = session.get(Student, candidate_id)

    if student is None:
        session.close()
        return jsonify({"error": "Candidate not found"}), 404

    session.delete(student)
    session.commit()

    session.close()

    return jsonify({
        "message": "Candidate deleted successfully"
    })

@app.put("/candidates/<int:candidate_id>/round1")
def update_round1(candidate_id):
    session = SessionLocal()

    student = session.get(Student, candidate_id)

    if student is None:
        session.close()
        return jsonify({"error": "Candidate not found"}), 404

    data = request.get_json()

    student.requirement_understanding = data["requirement_understanding"]
    student.feature_implementation = data["feature_implementation"]
    student.validation_edge_cases = data["validation_edge_cases"]
    student.code_structure = data["code_structure"]
    student.ai_usage = data["ai_usage"]

    # Calculate total score
    student.round_1_score = (
        student.requirement_understanding +
        student.feature_implementation +
        student.validation_edge_cases +
        student.code_structure +
        student.ai_usage
    )

    # Calculate eligibility
    student.eligibility = check_eligibility(student)

    # Final shortlist
    if student.eligibility == "Eligible" and student.round_1_score >= 70:
        student.final_shortlist = "Selected"
    elif student.eligibility == "Review Required":
        student.final_shortlist = "Review Required"
    else:
        student.final_shortlist = "Rejected"

    session.commit()
    session.refresh(student)

    result = student.to_dict()

    session.close()

    return jsonify(result), 200


@app.post("/candidates/<int:candidate_id>/check-eligibility")
def run_eligibility(candidate_id):

    session = SessionLocal()

    student = session.get(Student, candidate_id)

    if student is None:
        session.close()
        return jsonify({"error": "Candidate not found"}), 404

    student.eligibility = check_eligibility(student)

    session.commit()
    session.refresh(student)

    result = student.to_dict()

    session.close()

    return jsonify(result)

@app.put("/candidates/<int:candidate_id>/final-shortlist")
def update_final_shortlist(candidate_id):
    session = SessionLocal()

    student = session.get(Student, candidate_id)

    if student is None:
        session.close()
        return jsonify({"error": "Candidate not found"}), 404

    data = request.get_json()

    student.final_shortlist = data["final_shortlist"]

    session.commit()
    session.refresh(student)

    result = student.to_dict()

    session.close()

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)

