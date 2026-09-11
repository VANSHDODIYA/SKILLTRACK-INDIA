from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from database import (
    create_database,
    add_candidate,
    get_candidates,
    get_candidate,
    get_candidate_by_skill_and_mobile,
    add_employment_outcome,
    get_employment_outcomes,
    add_training_program,
    get_training_programs,
    get_training_stats,
    get_dashboard_stats,
    get_counsellors,
    get_slots_for_counsellor,
    create_booking,
    get_booking_by_id,
    complete_demo_payment,
    get_payment_by_booking,
    get_all_bookings,
    cancel_booking,
    reschedule_booking,
    save_counselling_note,
    get_counselling_notes,
    get_or_create_ai_conversation,
    save_ai_messages,
    get_ai_messages,
    get_assessment_questions,
    save_assessment_attempt,
    get_candidate_assessment_results,
    get_pre_registrations
)

app = Flask(__name__)
CORS(app)

create_database()


# =========================================================
# PAGE ROUTES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sih-preview")
def sih_preview():
    return render_template("Index sih.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/skill-gap")
def skill_gap():
    return render_template("skill_gap.html")


@app.route("/candidate")
def candidate():
    return render_template("candidate.html")


@app.route("/candidates")
def candidates():
    return render_template("candidates.html")


@app.route("/employment")
def employment():
    return render_template("employment.html")


@app.route("/programs")
def programs():
    return render_template("programs.html")


@app.route("/intelligence")
def intelligence():
    return render_template("intelligence.html")


@app.route("/jobs")
def jobs():
    return render_template("jobs.html")


@app.route("/assessments")
def assessments_page():
    return render_template("assessments.html")


@app.route("/counselling")
def counselling_page():
    return render_template("counselling.html")


@app.route("/expert-dashboard")
def expert_dashboard_page():
    return render_template("expert_dashboard.html")


@app.route("/policy")
def policy():
    return render_template("policy.html")


@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")


# =========================================================
# DASHBOARD API
# =========================================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard_api():

    stats = get_dashboard_stats()

    return jsonify(stats)


# =========================================================
# CANDIDATE API
# =========================================================

@app.route("/api/candidate", methods=["POST"])
def candidate_api():

    data = request.get_json() or {}

    name = (data.get("name") or data.get("full_name") or "").strip()
    email = (data.get("email") or "").strip()
    date_of_birth = (data.get("date_of_birth") or "").strip()
    gender = (data.get("gender") or "").strip()
    mobile_number = (data.get("mobile_number") or "").strip()
    state = (data.get("state") or "").strip()
    district = (data.get("district") or "").strip()
    education_level = (data.get("education_level") or "").strip()
    employment_status = (data.get("employment_status") or data.get("employment") or "").strip()
    primary_skill = (data.get("primary_skill") or "").strip()
    preferred_job_sector = (data.get("preferred_job_sector") or "").strip()
    preferred_job_location = (data.get("preferred_job_location") or "").strip()
    employer_name = (data.get("employer_name") or "").strip()
    job_role = (data.get("job_role") or "").strip()
    monthly_salary = (data.get("monthly_salary") or "").strip()
    job_seeking_status = (data.get("job_seeking_status") or "").strip()
    preferred_job_role = (data.get("preferred_job_role") or "").strip()
    business_type = (data.get("business_type") or "").strip()
    monthly_income_range = (data.get("monthly_income_range") or "").strip()
    organisation = (data.get("organisation") or "").strip()
    apprenticeship_role = (data.get("apprenticeship_role") or "").strip()
    password = (data.get("password") or "").strip()
    target_role = (data.get("target_role") or "Data Analyst").strip()

    # Support the original registration form while richer forms provide these fields.
    date_of_birth = date_of_birth or ""
    gender = gender or "Not specified"
    mobile_number = mobile_number or ""
    state = state or "Not specified"
    district = district or "Not specified"
    education_level = education_level or data.get("qualification") or "Not specified"
    primary_skill = primary_skill or data.get("skills") or "Not specified"
    preferred_job_sector = preferred_job_sector or "Not specified"
    preferred_job_location = preferred_job_location or "Not specified"
    employment_status = employment_status or "Not specified"

    required_fields = {
        "Full Name": name,
        "Email": email,
    }
    missing = [label for label, value in required_fields.items() if not value]
    if missing:
        return jsonify({"error": "This field is required.", "missing": missing}), 400

    if mobile_number and (len(mobile_number) < 10 or not mobile_number.isdigit()):
        return jsonify({"error": "Mobile number format is invalid."}), 400
    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"error": "Email format is invalid."}), 400
    if len(password) and len(password) < 8:
        return jsonify({"error": "Password strength is weak. Use 8+ characters."}), 400

    try:
        age = int((datetime.now().year - int(date_of_birth[:4])) if len(date_of_birth) >= 4 and date_of_birth[:4].isdigit() else 0)
    except Exception:
        age = None

    try:
        skill_id = add_candidate(
            name,
            email,
            age,
            gender,
            data.get("qualification") or "",
            data.get("field") or "",
            data.get("skills") or "",
            data.get("skill_levels") or "",
            employment_status,
            data.get("experience") or 0,
            mobile_number,
            state,
            district,
            education_level,
            primary_skill,
            preferred_job_sector,
            preferred_job_location,
            employment_status,
            employer_name,
            job_role,
            monthly_salary,
            job_seeking_status,
            preferred_job_role,
            business_type,
            monthly_income_range,
            organisation,
            apprenticeship_role,
            data.get("training_program") or "",
            data.get("training_centre") or "",
            date_of_birth,
            target_role,
            password or None,
            0,
        )
    except Exception:
        return jsonify({"error": "Candidate registration failed. Please check the submitted details."}), 500

    candidate = get_candidate(skill_id)

    return jsonify({
        "message": "Candidate registered successfully.",
        "skill_id": skill_id,
        "candidate_id": candidate[0] if candidate else None,
        "profile_completion": 100,
    })


# =========================================================
# GET ALL CANDIDATES
# =========================================================

@app.route("/api/candidates", methods=["GET"])
def candidates_api():

    rows = get_candidates()

    candidates_list = []

    for row in rows:

        candidates_list.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3],
            "gender": row[4],
            "qualification": row[5],
            "field": row[6],
            "skills": row[7],
            "skill_levels": row[8],
            "employment": row[9],
            "experience": row[10],
            "skill_id": row[11],
            "mobile_number": row[15],
            "preferred_job_role": row[25],
            "training_program": row[30],
            "training_centre": row[31],
            "registration_date": row[32],
            "current_status": row[33],
            "profile_completion": row[34]
        })

    return jsonify(candidates_list)


@app.route("/api/candidate/verify", methods=["POST"])
def verify_candidate_api():
    data = request.get_json() or {}
    skill_id = (data.get("skill_id") or "").strip()
    mobile_or_email = (data.get("mobile_or_email") or "").strip()
    if not skill_id or not mobile_or_email:
        return jsonify({"error": "SkillID and registered mobile/email are required."}), 400
    match = get_candidate_by_skill_and_mobile(skill_id, mobile_or_email)
    if not match:
        return jsonify({"error": "Candidate not found. Please verify your SkillID and registered contact details."}), 404

    candidate = {
        "id": match[0],
        "name": match[1],
        "email": match[2],
        "skill_id": match[11],
        "training_program": match[30],
        "training_centre": match[31],
        "registration_date": match[32],
        "current_status": match[33],
        "profile_completion": match[34],
        "mobile_number": match[15],
    }
    return jsonify({"message": "Candidate Found", "candidate": candidate})


@app.route("/api/candidate/pre-registered", methods=["GET"])
def pre_registered_candidates_api():
    rows = get_pre_registrations()
    records = [{
        "id": row[0],
        "skill_id": row[1],
        "name": row[2],
        "mobile_number": row[3],
        "email": row[4],
        "registration_date": row[5],
        "status": row[6],
        "training_program": row[7],
        "training_centre": row[8],
        "notes": row[9]
    } for row in rows]
    return jsonify(records)


# =========================================================
# SKILL GAP API
# =========================================================

@app.route("/api/skill-gap", methods=["POST"])
def skill_gap_api():
    data = request.get_json() or {}
    candidate_id = data.get("candidate_id")
    if not candidate_id:
        return jsonify({"error": "Candidate ID is required."}), 400

    candidate_data = get_candidate(candidate_id)
    if not candidate_data:
        return jsonify({"error": "Candidate not found."}), 404

    skill_string = (candidate_data[7] or "")
    candidate_skills = [s.strip().lower() for s in skill_string.split(",") if s.strip()]
    required_skills = ["Python", "SQL", "Excel", "Power BI", "JavaScript", "Data Analytics", "AI / ML"]
    aliases = {
        "ai/ml": "ai / ml",
        "ai ml": "ai / ml",
        "machine learning": "ai / ml",
        "excel": "excel",
        "power bi": "power bi",
        "sql": "sql",
        "python": "python",
        "javascript": "javascript",
        "data analysis": "data analytics"
    }
    normalized = [aliases.get(skill, skill) for skill in candidate_skills]
    strong = []
    needs_improvement = []
    for skill in required_skills:
        if skill.lower() in normalized:
            strong.append(skill)
        else:
            needs_improvement.append(skill)

    target_role = data.get("target_role") or candidate_data[35] or "Data Analyst"
    role_map = {
        "Data Analyst": {
            "strong": ["SQL", "Excel"],
            "gap": "Power BI",
            "training": "Power BI for Data Analytics",
            "jobs": ["Junior Data Analyst", "MIS Executive", "Reporting Analyst"],
            "reason": "Your assessment indicates a gap in Power BI, while 78% of matching Data Analyst jobs require it."
        },
        "Software Developer": {
            "strong": ["Python", "JavaScript"],
            "gap": "SQL",
            "training": "SQL for Application Development",
            "jobs": ["Junior Software Developer", "Web Developer", "QA Analyst"],
            "reason": "Your assessment shows that application readiness is strong, but SQL depth is still needed for full-stack roles."
        },
        "Digital Marketing": {
            "strong": ["Communication"],
            "gap": "Digital Literacy",
            "training": "Digital Marketing Fundamentals",
            "jobs": ["SEO Executive", "Social Media Executive", "Campaign Coordinator"],
            "reason": "Your communication and learner profile are strong, but digital campaign and analytics skills need strengthening."
        }
    }
    recommendation = role_map.get(target_role, role_map["Data Analyst"])

    return jsonify({
        "candidate": candidate_data[1],
        "target_role": target_role,
        "match_percentage": round((len(strong) / len(required_skills)) * 100, 2) if required_skills else 0,
        "strong_skills": strong,
        "needs_improvement": needs_improvement,
        "skill_gap": recommendation["gap"],
        "recommended_training": recommendation["training"],
        "recommended_jobs": recommendation["jobs"],
        "why": recommendation["reason"],
        "required_skills": required_skills
    })


@app.route("/api/assessment/summary/<int:candidate_id>", methods=["GET"])
def assessment_summary(candidate_id):
    result = get_candidate_assessment_results(candidate_id)
    if not result:
        return jsonify({"error": "No assessment result found."}), 404
    return jsonify({
        "candidate_id": result[1],
        "overall_score": result[10],
        "technical_score": result[3],
        "digital_literacy_score": result[4],
        "communication_score": result[5],
        "problem_solving_score": result[6],
        "aptitude_score": result[7],
        "career_interest_score": result[8],
        "result_summary": result[11],
    })


@app.route("/api/assessments/questions", methods=["GET"])
def assessments_questions_api():
    questions = get_assessment_questions()
    return jsonify({"questions": questions})


@app.route("/api/assessments/submit", methods=["POST"])
def assessments_submit_api():
    data = request.get_json() or {}
    candidate_id = data.get("candidate_id")
    answers = data.get("answers") or {}
    target_role = data.get("target_role") or "Data Analyst"
    if not candidate_id:
        return jsonify({"error": "Candidate ID is required."}), 400
    result = save_assessment_attempt(candidate_id, 1, answers, target_role)
    candidate = get_candidate(candidate_id)
    recommendation = {
        "target_role": target_role,
        "overall_score": result["overall_score"],
        "category_scores": result["category_scores"],
        "recommendations": [],
        "summary": result["summary"],
        "strong_areas": [category for category, score in result["category_scores"].items() if score >= 70],
        "areas_to_improve": [category for category, score in result["category_scores"].items() if score < 70],
        "critical_skill_gap": "Power BI" if result["category_scores"].get("Technical Skills", 0) < 50 else "",
        "recommended_counselling": result["overall_score"] < 70 or any(score < 50 for score in result["category_scores"].values()),
    }
    if candidate:
        skill_string = candidate[7] or ""
        skill_list = [s.strip().lower() for s in skill_string.split(",") if s.strip()]
        gaps = []
        for key, score in result["category_scores"].items():
            if score < 70:
                gaps.append({"category": key, "score": score})
        if gaps:
            recommendation["recommendations"] = [{"title": "Recommended Training", "name": "Power BI for Data Analytics", "reason": "Your assessment shows a clear skill gap in Power BI and related business intelligence skills."}, {"title": "Recommended Jobs", "names": ["Junior Data Analyst", "MIS Executive", "Reporting Analyst"], "reason": "These roles match your current profile while targeting the biggest missing capability."}]
        else:
            recommendation["recommendations"] = [{"title": "Recommended Training", "name": "Career Readiness & Analytics Upskilling", "reason": "Your readiness is strong and career progression should focus on practical portfolio-building."}, {"title": "Recommended Jobs", "names": ["Data Analyst", "Operations Analyst", "MIS Executive"], "reason": "Your profile is already aligned with analytics-focused career pathways."}]
    return jsonify(recommendation)


# =========================================================
# AI SKILL INTELLIGENCE
# =========================================================

@app.route(
    "/api/intelligence/<int:candidate_id>",
    methods=["GET"]
)
def intelligence_api(candidate_id):

    candidate_data = get_candidate(candidate_id)

    if not candidate_data:

        return jsonify({
            "error": "Candidate not found."
        }), 404

    name = candidate_data[1]

    skills_text = candidate_data[7] or ""

    skill_levels_text = candidate_data[8] or ""

    experience = candidate_data[10] or 0


    # Industry demand scores

    industry_demand = {

        "python": 90,

        "sql": 85,

        "javascript": 80,

        "cloud computing": 75,

        "ai / ml": 90,

        "cybersecurity": 85,

        "data analytics": 80,

        "docker / devops": 70

    }


    # Proficiency scores

    level_scores = {

        "beginner": 30,

        "basic": 30,

        "intermediate": 60,

        "advanced": 85,

        "expert": 95

    }


    # Skill aliases

    aliases = {

        "ai/ml": "ai / ml",

        "ai ml": "ai / ml",

        "machine learning": "ai / ml",

        "cloud": "cloud computing",

        "devops": "docker / devops",

        "docker": "docker / devops",

        "data analysis": "data analytics"

    }


    # Candidate skills

    candidate_skills = {}

    for skill in skills_text.split(","):

        skill = skill.strip().lower()

        if not skill:
            continue

        skill = aliases.get(
            skill,
            skill
        )

        candidate_skills[skill] = True


    # Candidate skill levels

    candidate_levels = {}

    for item in skill_levels_text.split(","):

        if ":" not in item:
            continue

        skill, level = item.split(":", 1)

        skill = skill.strip().lower()

        level = level.strip().lower()

        skill = aliases.get(
            skill,
            skill
        )

        candidate_levels[skill] = level


    # Build skill profile

    skill_profile = []

    for skill, demand in industry_demand.items():

        if skill in candidate_skills:

            level = candidate_levels.get(
                skill,
                "intermediate"
            )

            proficiency = level_scores.get(
                level,
                60
            )

            status = "Matched"

        else:

            level = "not available"

            proficiency = 0

            status = "Missing"

        skill_profile.append({

            "skill": skill.title(),

            "demand": demand,

            "proficiency": proficiency,

            "level": level.title(),

            "status": status

        })


    # Overall readiness

    if skill_profile:

        total_proficiency = sum(
            item["proficiency"]
            for item in skill_profile
        )

        overall_readiness = (
            total_proficiency /
            len(skill_profile)
        )

    else:

        overall_readiness = 0


    try:

        experience = int(experience)

    except (ValueError, TypeError):

        experience = 0


    if experience >= 3:

        overall_readiness += 5

    elif experience >= 1:

        overall_readiness += 2


    overall_readiness = round(
        min(overall_readiness, 100)
    )


    # Priority skills

    priorities = []

    for item in skill_profile:

        demand = item["demand"]

        proficiency = item["proficiency"]

        if proficiency >= 85:
            continue

        if proficiency == 0:

            priority = demand + 20

        else:

            priority = demand - proficiency

        priorities.append({

            "skill": item["skill"],

            "gap": max(
                demand - proficiency,
                0
            ),

            "priority": priority

        })


    priorities.sort(
        key=lambda item: item["priority"],
        reverse=True
    )


    if priorities:

        priority_skill = priorities[0]["skill"]

        priority_gap = priorities[0]["gap"]

    else:

        priority_skill = "No major gap"

        priority_gap = 0


    # Learning paths

    learning_paths = {

        "Python": [

            "Python Fundamentals",

            "Data Structures & Algorithms",

            "Python Projects",

            "Advanced Python & API Development"

        ],

        "Sql": [

            "SQL Fundamentals",

            "Joins & Subqueries",

            "Database Design",

            "Advanced SQL & Optimization"

        ],

        "Javascript": [

            "JavaScript Fundamentals",

            "DOM & Event Handling",

            "Modern JavaScript",

            "Web Development Projects"

        ],

        "Cloud Computing": [

            "Cloud Fundamentals",

            "AWS / Azure Basics",

            "Cloud Deployment",

            "Cloud Architecture"

        ],

        "Ai / Ml": [

            "Python for AI",

            "Statistics & Data Preparation",

            "Machine Learning Algorithms",

            "AI / ML Projects"

        ],

        "Cybersecurity": [

            "Security Fundamentals",

            "Networking Basics",

            "Threat Detection",

            "Cybersecurity Projects"

        ],

        "Data Analytics": [

            "Data Analysis Fundamentals",

            "Excel & SQL",

            "Python & Pandas",

            "Data Visualization"

        ],

        "Docker / Devops": [

            "Linux & Command Line",

            "Git & Version Control",

            "Docker",

            "CI/CD & Deployment"

        ]

    }


    learning_path = learning_paths.get(

        priority_skill,

        [

            "Identify target job role",

            "Complete relevant training",

            "Build practical projects",

            "Apply for suitable employment"

        ]

    )


    # Intelligence message

    if priority_skill == "No major gap":

        message = (

            "The candidate demonstrates strong readiness "
            "across the currently evaluated industry skills. "
            "Focus should shift toward practical projects, "
            "job applications and career progression."

        )

    else:

        message = (

            f"{priority_skill} is currently the "
            f"highest-priority development area. "
            f"Targeted training in this skill can improve "
            f"industry readiness and employment opportunities."

        )


    return jsonify({

        "candidate": name,

        "overall_readiness":
            overall_readiness,

        "priority_skill":
            priority_skill,

        "priority_gap":
            priority_gap,

        "message":
            message,

        "skill_profile":
            skill_profile,

        "learning_path":
            learning_path

    })


# =========================================================
# EMPLOYMENT API
# =========================================================

@app.route(
    "/api/employment",
    methods=["POST"]
)
def employment_api():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No data received."
        }), 400

    candidate_id = data.get(
        "candidate_id"
    )

    if not candidate_id:

        return jsonify({
            "error": "Candidate ID is required."
        }), 400

    candidate_data = get_candidate(
        candidate_id
    )

    if not candidate_data:

        return jsonify({
            "error": "Candidate does not exist."
        }), 404

    add_employment_outcome(

        candidate_id,

        data.get(
            "employment_status",
            ""
        ),

        data.get(
            "company",
            ""
        ),

        data.get(
            "industry",
            ""
        ),

        data.get(
            "job_role",
            ""
        ),

        data.get(
            "salary_range",
            data.get("salary", "")
        ),

        data.get(
            "placement_date",
            ""
        ),

        data.get(
            "employment_after_training",
            ""
        ),

        data.get(
            "career_progression",
            ""
        )

    )

    return jsonify({

        "message":
            "Employment outcome recorded successfully.",
        "success": True

    })


# =========================================================
# GET EMPLOYMENT OUTCOMES
# =========================================================

@app.route(
    "/api/employment",
    methods=["GET"]
)
def get_employment_api():

    rows = get_employment_outcomes()

    outcomes = []

    for row in rows:

        outcomes.append({

            "id": row[0],

            "candidate_id": row[1],

            "candidate_name": row[2],

            "employment_status": row[3],

            "company": row[4],

            "industry": row[5],

            "job_role": row[6],

            "salary_range": row[7],

            "placement_date": row[8],

            "employment_after_training": row[9],

            "career_progression": row[10]

        })

    return jsonify(outcomes)


# =========================================================
# TRAINING PROGRAM API
# =========================================================

@app.route(
    "/api/programs",
    methods=["POST"]
)
def programs_api():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No data received."
        }), 400

    try:

        enrolled = int(
            data.get(
                "enrolled",
                0
            )
        )

        completed = int(
            data.get(
                "completed",
                0
            )
        )

        certified = int(
            data.get(
                "certified",
                0
            )
        )

        employed = int(
            data.get(
                "employed",
                0
            )
        )

    except (ValueError, TypeError):

        return jsonify({
            "error":
                "Training numbers must be valid integers."
        }), 400


    add_training_program(

        data.get(
            "program_name",
            ""
        ),

        data.get(
            "provider",
            ""
        ),

        data.get(
            "skill_area",
            ""
        ),

        data.get(
            "location",
            ""
        ),

        data.get(
            "duration",
            ""
        ),

        enrolled,

        completed,

        certified,

        employed,

        data.get(
            "status",
            ""
        )

    )

    return jsonify({

        "message":
            "Training program added successfully."

    })


# =========================================================
# GET TRAINING PROGRAMS
# =========================================================

@app.route(
    "/api/programs",
    methods=["GET"]
)
def get_programs_api():

    rows = get_training_programs()

    programs_list = []

    for row in rows:

        programs_list.append({

            "id": row[0],

            "program_name": row[1],

            "provider": row[2],

            "skill_area": row[3],

            "location": row[4],

            "duration": row[5],

            "enrolled": row[6],

            "completed": row[7],

            "certified": row[8],

            "employed": row[9],

            "status": row[10]

        })

    return jsonify(programs_list)


# =========================================================
# TRAINING STATS API
# =========================================================

@app.route(
    "/api/training-stats",
    methods=["GET"]
)
def training_stats_api():

    stats = get_training_stats()

    return jsonify(stats)


@app.route("/api/counselling/counsellors", methods=["GET"])
def counselling_counsellors_api():
    counsellors = get_counsellors()
    candidate_id = request.args.get("candidate_id")
    candidate = get_candidate(candidate_id) if candidate_id else None
    target_role = (candidate[35] if candidate else "") or ""
    profile_text = " ".join(str(candidate[index] or "") for index in (7, 9, 17, 18, 19, 20)) if candidate else ""
    match_text = f"{target_role} {profile_text}".lower()
    if any(term in match_text for term in ("data", "analyst", "analytics", "sql", "power bi", "excel")):
        match_text += " data analytics"
    if any(term in match_text for term in ("ai", "ml", "machine learning")):
        match_text += " ai ml"
    if any(term in match_text for term in ("software", "developer", "javascript", "python", "web")):
        match_text += " software development"
    if any(term in match_text for term in ("unemployed", "job seeking", "placement")):
        match_text += " job placement career readiness"
    payload = []
    for row in counsellors:
        specialization = (row[2] or "").lower()
        matching_terms = [term for term in specialization.replace("&", " ").split() if len(term) > 3 and term in match_text]
        match_score = min(98, 68 + len(matching_terms) * 14) if candidate else 70
        reason = "Recommended based on the expert's broad career guidance experience."
        if matching_terms:
            reason = f"Recommended because this expert specializes in {row[2]} and matches your {target_role or 'career'} profile."
        payload.append({
            "id": row[0],
            "name": row[1],
            "specialization": row[2],
            "experience_years": row[3],
            "session_type": row[4],
            "fee": row[5],
            "availability": row[6],
            "bio": row[7],
            "languages": row[8] if len(row) > 8 else "English, Hindi",
            "match_score": match_score,
            "match_reason": reason,
        })
    payload.sort(key=lambda item: (-item["match_score"], item["id"]))
    return jsonify(payload)


@app.route("/api/counselling/slots/<int:counsellor_id>", methods=["GET"])
def counselling_slots_api(counsellor_id):
    rows = get_slots_for_counsellor(counsellor_id)
    payload = [{
        "id": row[0],
        "counsellor_id": row[1],
        "slot_date": row[2],
        "start_time": row[3],
        "end_time": row[4],
        "duration_minutes": row[5],
        "session_type": row[6],
        "status": row[7],
    } for row in rows]
    return jsonify(payload)


@app.route("/api/counselling/book", methods=["POST"])
def counselling_book_api():
    data = request.get_json() or {}
    candidate_id = data.get("candidate_id")
    counsellor_id = data.get("counsellor_id")
    slot_id = data.get("slot_id")
    reason = (data.get("reason") or "").strip()
    session_type = (data.get("session_type") or "").strip()
    duration_minutes = data.get("duration_minutes")
    candidate_name = (data.get("candidate_name") or "").strip()
    skill_id = (data.get("skill_id") or "").strip()
    if not candidate_id or not counsellor_id or not slot_id:
        return jsonify({"error": "Candidate, counsellor and slot are required."}), 400
    if duration_minutes and str(duration_minutes) not in {"30", "45", "60"}:
        return jsonify({"error": "Session duration must be 30, 45, or 60 minutes."}), 400
    if session_type and session_type not in {"Online", "In-person"}:
        return jsonify({"error": "Session type must be Online or In-person."}), 400
    booking_id = create_booking(candidate_id, counsellor_id, slot_id, reason, candidate_name, skill_id, session_type=session_type, duration_minutes=duration_minutes)
    if not booking_id:
        return jsonify({"error": "Booking could not be created."}), 400
    return jsonify({"message": "Counselling booking created.", "booking_id": booking_id, "status": "pending_payment"})


@app.route("/api/counselling/pay", methods=["POST"])
def counselling_pay_api():
    data = request.get_json() or {}
    booking_id = data.get("booking_id")
    candidate_id = data.get("candidate_id")
    payment_method = (data.get("payment_method") or "UPI").strip()
    if not booking_id or not candidate_id:
        return jsonify({"error": "Booking and candidate ID are required."}), 400
    txn_id = complete_demo_payment(booking_id, candidate_id, payment_method)
    if not txn_id:
        return jsonify({"error": "Payment could not be processed."}), 400
    booking = get_booking_by_id(booking_id)
    payment = get_payment_by_booking(booking_id)
    return jsonify({
        "message": "Demo Payment Successful",
        "transaction_id": txn_id,
        "booking_id": booking_id,
        "status": booking["status"],
        "counsellor_id": booking["counsellor_id"],
        "session_date": booking["session_date"],
        "session_time": booking["session_time"],
        "payment_method": payment_method,
        "payment_date": payment["payment_date"] if payment else None,
        "amount": payment["amount"] if payment else booking["total_fee"],
    })


@app.route("/api/counselling/bookings", methods=["GET"])
def counselling_bookings_api():
    rows = get_all_bookings()
    candidate_id = request.args.get("candidate_id")
    if candidate_id:
        rows = [row for row in rows if str(row[1]) == str(candidate_id)]
    payload = [{
        "id": row[0],
        "candidate_id": row[1],
        "counsellor_id": row[2],
        "slot_id": row[3],
        "skill_id": row[4],
        "candidate_name": row[5],
        "reason": row[6],
        "session_date": row[7],
        "session_time": row[8],
        "duration_minutes": row[9],
        "session_type": row[10],
        "status": row[11],
        "payment_status": row[12],
        "total_fee": row[13],
        "created_at": row[14],
    } for row in rows]
    return jsonify(payload)


@app.route("/api/counselling/bookings/<int:booking_id>/cancel", methods=["POST"])
def counselling_cancel_api(booking_id):
    data = request.get_json() or {}
    if not cancel_booking(booking_id, data.get("candidate_id")):
        return jsonify({"error": "This booking cannot be cancelled."}), 400
    return jsonify({"message": "Counselling booking cancelled.", "success": True})


@app.route("/api/counselling/bookings/<int:booking_id>/reschedule", methods=["POST"])
def counselling_reschedule_api(booking_id):
    data = request.get_json() or {}
    if not reschedule_booking(booking_id, data.get("candidate_id"), data.get("slot_id")):
        return jsonify({"error": "This booking cannot be rescheduled."}), 400
    return jsonify({"message": "Counselling booking rescheduled.", "success": True})


@app.route("/api/counselling/notes", methods=["POST"])
def counselling_notes_create_api():
    data = request.get_json() or {}
    booking_id = data.get("booking_id")
    booking = get_booking_by_id(booking_id) if booking_id else None
    if not booking:
        return jsonify({"error": "Booking not found."}), 404
    save_counselling_note(booking_id, booking["candidate_id"], booking["counsellor_id"], data)
    return jsonify({"message": "Counselling outcome saved.", "success": True})


@app.route("/api/counselling/notes", methods=["GET"])
def counselling_notes_api():
    rows = get_counselling_notes(request.args.get("candidate_id"))
    return jsonify([{
        "id": row[0], "booking_id": row[1], "candidate_id": row[2], "counsellor_id": row[3],
        "session_summary": row[4], "identified_challenges": row[5],
        "recommended_skills": row[6], "recommended_courses": row[7],
        "recommended_jobs": row[8], "next_steps": row[9],
        "created_at": row[10], "updated_at": row[11]
    } for row in rows])


@app.route("/api/expert-dashboard", methods=["GET"])
def expert_dashboard_api():
    bookings = get_all_bookings()
    notes = get_counselling_notes()
    notes_by_booking = {row[1]: row for row in notes}
    payload = []
    for booking in bookings:
        candidate = get_candidate(booking[1])
        result = get_candidate_assessment_results(booking[1])
        payload.append({
            "booking_id": booking[0], "candidate_id": booking[1], "candidate_name": booking[5],
            "counsellor_id": booking[2], "session_date": booking[7], "session_time": booking[8],
            "status": booking[11], "reason": booking[6],
            "assessment_score": result[10] if result else None,
            "target_role": candidate[35] if candidate else "Data Analyst",
            "skills": candidate[7] if candidate else "",
            "employment_status": candidate[9] if candidate else "",
            "note": notes_by_booking.get(booking[0])[4] if notes_by_booking.get(booking[0]) else None,
        })
    return jsonify({
        "today": [item for item in payload if item["session_date"] == datetime.now().strftime("%Y-%m-%d")],
        "upcoming": payload,
        "pending_requests": [item for item in payload if item["status"] == "pending_payment"],
        "completed": [item for item in payload if item["status"] == "completed"]
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/chatbot", methods=["POST"])
def chatbot_api():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip()
    candidate_id = data.get("candidate_id")
    if not message:
        return jsonify({"error": "Please enter a career or skill question."}), 400

    candidate = get_candidate(candidate_id) if candidate_id else None
    skills_text = (candidate[7] if candidate else "") or ""
    target_role = (candidate[35] if candidate else "") or data.get("target_role") or "Data Analyst"
    assessment = get_candidate_assessment_results(candidate_id) if candidate_id else None
    assessment_score = assessment[10] if assessment else None
    normalized = message.lower()

    if any(keyword in normalized for keyword in ["data analyst", "analytics", "power bi", "sql", "excel", "reporting"]):
        response = (
            "For a Data Analyst path, prioritize Power BI, SQL, Excel, and dashboard storytelling. "
            "Start with SQL joins and Power BI dashboard design, then build one portfolio project using a real dataset."
        )
        suggestions = ["Power BI for Data Analytics", "SQL for Reporting", "Excel Dashboard Fundamentals"]
        action = "Complete a mini portfolio project and apply for Junior Data Analyst roles."
    elif any(keyword in normalized for keyword in ["software", "developer", "python", "javascript", "web", "full stack"]):
        response = (
            "A software developer roadmap should focus on one language, one framework, and deployment. "
            "For example: Python + Flask or JavaScript + React, then project-based learning and Git practice."
        )
        suggestions = ["Python for Web Development", "JavaScript Fundamentals", "Git & Deployment Basics"]
        action = "Practice 2 projects and build a GitHub portfolio before job applications."
    elif any(keyword in normalized for keyword in ["ai", "ml", "machine learning", "artificial intelligence"]):
        response = (
            "AI and ML careers need math basics, Python, and practical model building. "
            "Focus on statistics, data cleaning, and at least one supervised learning project."
        )
        suggestions = ["Python for AI", "Statistics for ML", "Machine Learning Fundamentals"]
        action = "Build one classification model and document the workflow clearly."
    elif any(keyword in normalized for keyword in ["digital marketing", "marketing", "seo", "social media", "campaign"]):
        response = (
            "Digital marketing roles reward content strategy, analytics, and campaign optimization. "
            "Strengthen SEO, content planning, and digital campaign reporting to improve readiness."
        )
        suggestions = ["Digital Marketing Fundamentals", "SEO & Content Strategy", "Campaign Analytics"]
        action = "Create a campaign case study and track results with metrics."
    elif any(keyword in normalized for keyword in ["career", "job", "role", "path", "future"]):
        response = (
            "Based on your skills and career goals, aim for a role where your strongest skills match market demand and your most important gaps are short-term. "
            "Use assessment results to target one realistic path and upskill in 2-3 core areas."
        )
        suggestions = ["Skill Gap Review", "Career Match Analysis", "Portfolio Preparation"]
        action = "Identify the top 2 job roles that align with your assessment score and start practicing them."
    else:
        response = (
            "You are on the right track. I recommend starting with a focused skill plan: identify your target role, improve the top 2 gaps, and build 1 practical project to show evidence."
        )
        suggestions = ["Career Readiness Assessment", "Skill Gap Review", "Targeted Training Recommendations"]
        action = "Tell me your target job role and I can guide a tailored roadmap."

    if skills_text:
        present_skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        if present_skills:
            response += f" Your current profile includes: {', '.join(present_skills[:4])}."

    if assessment_score is not None:
        response += f" Your latest assessment score is {assessment_score}%."

    needs_counselling = (
        any(keyword in normalized for keyword in ["confused", "confusion", "counsellor", "counselor", "human help"])
        or (assessment_score is not None and assessment_score < 70)
    )
    if needs_counselling:
        response += " Expert counselling can provide personalized human guidance; it does not guarantee a job outcome."
        suggestions.append("Book Expert Counselling")

    conversation = get_or_create_ai_conversation(candidate_id)
    save_ai_messages(conversation[0], candidate_id, message, response)

    return jsonify({
        "message": response,
        "suggestions": suggestions,
        "recommended_action": action,
        "target_role": target_role,
        "assessment_score": assessment_score,
        "needs_counselling": needs_counselling,
        "status": "ok"
    })


@app.route("/api/chatbot/history/<int:candidate_id>", methods=["GET"])
def chatbot_history_api(candidate_id):
    rows = get_ai_messages(candidate_id)
    return jsonify([{"sender": row[3], "message": row[4], "created_at": row[5]} for row in rows])


@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "status": "ok",

        "message":
            "SkillTrack India backend is running."

    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )