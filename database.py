import sqlite3
from datetime import datetime

DATABASE = "skilltrack.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def add_column_if_missing(table_name, column_name, column_definition):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
    conn.commit()
    conn.close()


def generate_skill_id():
    prefix = "SKL"
    year = datetime.now().strftime("%y")
    state = "GJ"
    random_part = datetime.now().strftime("%d%H%M%S")
    suffix = f"{state}-{year}-{random_part}"
    return f"{prefix}-{suffix}"


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            qualification TEXT,
            field TEXT,
            skills TEXT,
            skill_levels TEXT,
            employment TEXT,
            experience INTEGER,
            skill_id TEXT UNIQUE,
            date_of_birth TEXT,
            state TEXT,
            district TEXT,
            mobile_number TEXT,
            education_level TEXT,
            primary_skill TEXT,
            preferred_job_sector TEXT,
            preferred_job_location TEXT,
            employment_status TEXT,
            employer_name TEXT,
            job_role TEXT,
            monthly_salary TEXT,
            job_seeking_status TEXT,
            preferred_job_role TEXT,
            business_type TEXT,
            monthly_income_range TEXT,
            organisation TEXT,
            apprenticeship_role TEXT,
            training_program TEXT,
            training_centre TEXT,
            registration_date TEXT,
            current_status TEXT,
            password_hash TEXT,
            is_pre_registered INTEGER DEFAULT 0,
            profile_completion INTEGER DEFAULT 0,
            target_role TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employment_outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            employment_status TEXT,
            company TEXT,
            industry TEXT,
            job_role TEXT,
            salary_range TEXT,
            placement_date TEXT,
            employment_after_training TEXT,
            career_progression TEXT
        )
    """)
    add_column_if_missing('employment_outcomes', 'salary_range', 'TEXT')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_name TEXT,
            provider TEXT,
            skill_area TEXT,
            location TEXT,
            duration TEXT,
            enrolled INTEGER,
            completed INTEGER,
            certified INTEGER,
            employed INTEGER,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counsellors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            experience_years INTEGER,
            session_type TEXT,
            fee REAL,
            availability TEXT,
            bio TEXT
        )
    """)
    add_column_if_missing('counsellors', 'languages', 'TEXT')
    cursor.execute("UPDATE counsellors SET languages = 'English, Hindi, Gujarati' WHERE languages IS NULL OR languages = ''")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counselling_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            counsellor_id INTEGER,
            slot_date TEXT,
            start_time TEXT,
            end_time TEXT,
            duration_minutes INTEGER,
            session_type TEXT,
            status TEXT DEFAULT 'available'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counselling_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            counsellor_id INTEGER,
            slot_id INTEGER,
            skill_id TEXT,
            candidate_name TEXT,
            reason TEXT,
            session_date TEXT,
            session_time TEXT,
            duration_minutes INTEGER,
            session_type TEXT,
            status TEXT DEFAULT 'pending_payment',
            payment_status TEXT DEFAULT 'pending',
            total_fee REAL,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counselling_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            candidate_id INTEGER,
            amount REAL,
            payment_method TEXT,
            transaction_id TEXT,
            status TEXT,
            payment_date TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counselling_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER UNIQUE,
            candidate_id INTEGER,
            counsellor_id INTEGER,
            session_summary TEXT,
            identified_challenges TEXT,
            recommended_skills TEXT,
            recommended_courses TEXT,
            recommended_jobs TEXT,
            next_steps TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            started_at TEXT,
            last_message_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            candidate_id INTEGER,
            sender TEXT,
            message TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER,
            category TEXT,
            question_text TEXT,
            question_type TEXT,
            sort_order INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            option_text TEXT,
            option_value TEXT,
            is_correct INTEGER DEFAULT 0,
            sort_order INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            assessment_id INTEGER,
            started_at TEXT,
            submitted_at TEXT,
            overall_score REAL,
            status TEXT DEFAULT 'submitted'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER,
            question_id INTEGER,
            selected_option_id INTEGER,
            answer_text TEXT,
            score_value REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            attempt_id INTEGER,
            assessment_id INTEGER,
            technical_score REAL,
            digital_literacy_score REAL,
            communication_score REAL,
            problem_solving_score REAL,
            aptitude_score REAL,
            career_interest_score REAL,
            overall_score REAL,
            result_summary TEXT,
            generated_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidate_pre_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id TEXT UNIQUE,
            name TEXT,
            mobile_number TEXT,
            email TEXT,
            registration_date TEXT,
            status TEXT DEFAULT 'active',
            training_program TEXT,
            training_centre TEXT,
            notes TEXT
        )
    """)

    add_column_if_missing('candidates', 'skill_id', 'TEXT')
    add_column_if_missing('candidates', 'date_of_birth', 'TEXT')
    add_column_if_missing('candidates', 'state', 'TEXT')
    add_column_if_missing('candidates', 'district', 'TEXT')
    add_column_if_missing('candidates', 'mobile_number', 'TEXT')
    add_column_if_missing('candidates', 'education_level', 'TEXT')
    add_column_if_missing('candidates', 'primary_skill', 'TEXT')
    add_column_if_missing('candidates', 'preferred_job_sector', 'TEXT')
    add_column_if_missing('candidates', 'preferred_job_location', 'TEXT')
    add_column_if_missing('candidates', 'employment_status', 'TEXT')
    add_column_if_missing('candidates', 'employer_name', 'TEXT')
    add_column_if_missing('candidates', 'job_role', 'TEXT')
    add_column_if_missing('candidates', 'monthly_salary', 'TEXT')
    add_column_if_missing('candidates', 'job_seeking_status', 'TEXT')
    add_column_if_missing('candidates', 'preferred_job_role', 'TEXT')
    add_column_if_missing('candidates', 'business_type', 'TEXT')
    add_column_if_missing('candidates', 'monthly_income_range', 'TEXT')
    add_column_if_missing('candidates', 'organisation', 'TEXT')
    add_column_if_missing('candidates', 'apprenticeship_role', 'TEXT')
    add_column_if_missing('candidates', 'training_program', 'TEXT')
    add_column_if_missing('candidates', 'training_centre', 'TEXT')
    add_column_if_missing('candidates', 'registration_date', 'TEXT')
    add_column_if_missing('candidates', 'current_status', 'TEXT')
    add_column_if_missing('candidates', 'password_hash', 'TEXT')
    add_column_if_missing('candidates', 'is_pre_registered', 'INTEGER DEFAULT 0')
    add_column_if_missing('candidates', 'profile_completion', 'INTEGER DEFAULT 0')
    add_column_if_missing('candidates', 'target_role', 'TEXT')

    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_candidates_skill_id ON candidates(skill_id)")
    conn.commit()
    seed_demo_data(conn)
    conn.close()


def seed_demo_data(conn):
    cursor = conn.cursor()

    if cursor.execute("SELECT COUNT(*) FROM counsellors").fetchone()[0] == 0:
        counsellors = [
            ("Dr. Meera Nair", "Career Guidance", 12, "Online", 299, "Mon/Tue/Wed", "Career coach for youth and women-led skilling pathways."),
            ("Rohit Sharma", "Data Analytics", 9, "Online", 399, "Tue/Thu/Fri", "Helps candidates chart analytics and reporting careers."),
            ("Kavita Joshi", "Digital Skills", 8, "In-person", 499, "Mon/Wed/Fri", "Supports digital literacy, IT jobs and customer support upskilling."),
            ("Arjun Patil", "Software Development", 11, "Online", 399, "Mon/Thu/Sat", "Mentor for software learners and freshers."),
            ("Neha Verma", "Career Readiness", 7, "In-person", 349, "Tue/Thu/Sat", "Guides candidates on profile building and communication."),
            ("Saurabh Iyer", "Manufacturing & Skills", 10, "In-person", 449, "Wed/Fri/Sat", "Helps with apprenticeship transitions and placement planning."),
            ("Priya Sen", "Retail & Service Jobs", 6, "Online", 299, "Mon/Tue/Fri", "Specializes in service-sector job matching."),
            ("Vikram Rao", "AI & ML", 14, "Online", 599, "Wed/Thu/Sat", "Mentors in AI, ML, and digital transformation readiness."),
            ("Ananya Kulkarni", "Education & Training", 8, "In-person", 399, "Tue/Fri/Sun", "Guides learners through curriculum selection and training transitions."),
            ("Deepak Shah", "Job Placement", 13, "Online", 499, "Mon/Wed/Sun", "Focuses on placement support and interview readiness."),
        ]
        cursor.executemany(
            "INSERT INTO counsellors (name, specialization, experience_years, session_type, fee, availability, bio) VALUES (?, ?, ?, ?, ?, ?, ?)",
            counsellors
        )

    if cursor.execute("SELECT COUNT(*) FROM counselling_slots").fetchone()[0] == 0:
        slot_rows = []
        for counsellor_id in range(1, 11):
            for day_offset in range(1, 3):
                slot_rows.append((counsellor_id, f"2026-09-{10 + day_offset}", "10:00", "11:00", 60, "Online", "available"))
                slot_rows.append((counsellor_id, f"2026-09-{10 + day_offset}", "14:30", "15:30", 60, "Online", "available"))
        cursor.executemany(
            "INSERT INTO counselling_slots (counsellor_id, slot_date, start_time, end_time, duration_minutes, session_type, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            slot_rows[:20]
        )

    if cursor.execute("SELECT COUNT(*) FROM counselling_bookings").fetchone()[0] == 0:
        sample_bookings = [
            (1, 1, 1, "SKL-GJ-26-8F4A92", "Aarav Patel", "Need help choosing between Power BI and SQL track.", "2026-09-11", "10:00", 60, "Online", "confirmed", "paid", 299.0, "2026-09-10 09:15:00"),
            (2, 2, 2, "SKL-GJ-26-7D2A11", "Sneha Iyer", "Career direction after finishing digital literacy course.", "2026-09-11", "14:30", 60, "Online", "confirmed", "paid", 399.0, "2026-09-10 10:20:00"),
            (3, 3, 3, "SKL-GJ-26-9A4C77", "Rahul Mehta", "Help deciding between frontend and data analytics.", "2026-09-12", "10:00", 60, "In-person", "confirmed", "paid", 499.0, "2026-09-10 11:10:00"),
            (4, 4, 4, "SKL-GJ-26-13B9A4", "Pooja Shah", "Need support with AI course and job fit.", "2026-09-12", "14:30", 60, "Online", "pending_payment", "pending", 399.0, "2026-09-10 12:00:00"),
            (5, 5, 5, "SKL-GJ-26-89BC22", "Kunal Desai", "Need guidance on job search and role selection.", "2026-09-13", "10:00", 60, "In-person", "completed", "paid", 349.0, "2026-09-08 09:00:00"),
        ]
        cursor.executemany(
            "INSERT INTO counselling_bookings (candidate_id, counsellor_id, slot_id, skill_id, candidate_name, reason, session_date, session_time, duration_minutes, session_type, status, payment_status, total_fee, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            sample_bookings
        )

    if cursor.execute("SELECT COUNT(*) FROM candidate_pre_registrations").fetchone()[0] == 0:
        pre_regs = [
            ("SKL-GJ-26-8F4A92", "Aarav Patel", "9876543210", "aarav.patel@example.com", "2026-08-01", "active", "Data Analytics", "Centre 3 Ahmedabad", "Graduated from digital training program."),
            ("SKL-GJ-26-7D2A11", "Sneha Iyer", "9123456780", "sneha.iyer@example.com", "2026-08-03", "active", "Python", "Centre 7 Surat", "Needs placement follow-up."),
            ("SKL-GJ-26-9A4C77", "Rahul Mehta", "9988776655", "rahul.mehta@example.com", "2026-08-06", "active", "AI/ML", "Centre 2 Vadodara", "Completed foundational program."),
            ("SKL-GJ-26-13B9A4", "Pooja Shah", "8899776655", "pooja.shah@example.com", "2026-08-12", "active", "Excel & BI", "Centre 5 Rajkot", "Waiting for assessment follow-up."),
            ("SKL-GJ-26-89BC22", "Kunal Desai", "7788990011", "kunal.desai@example.com", "2026-08-14", "active", "Career Readiness", "Centre 1 Ahmedabad", "Interview support required."),
        ]
        cursor.executemany(
            "INSERT INTO candidate_pre_registrations (skill_id, name, mobile_number, email, registration_date, status, training_program, training_centre, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            pre_regs
        )

    if cursor.execute("SELECT COUNT(*) FROM assessments").fetchone()[0] == 0:
        cursor.execute("INSERT INTO assessments (name, description, created_at) VALUES (?, ?, ?)", ("Skill and Career Assessment", "Demo assessment covering technical, digital, communication, problem solving, aptitude and career preferences.", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        assessment_id = cursor.execute("SELECT id FROM assessments ORDER BY id DESC LIMIT 1").fetchone()[0]

        question_templates = [
            ("Technical Skills", "Which SQL clause is used to filter rows based on a condition?", "multiple_choice", ["WHERE", "GROUP BY", "ORDER BY", "SELECT"], 1),
            ("Technical Skills", "Which Excel feature is most useful for summarizing large datasets quickly?", "multiple_choice", ["Pivot Table", "Header Row", "Spell Check", "Print Preview"], 1),
            ("Technical Skills", "What does Python's .sort() method do on a list?", "multiple_choice", ["Sorts the list in place", "Reverses the list", "Counts elements", "Copies list"], 1),
            ("Technical Skills", "Which is a common visualization used in Power BI for trend analysis?", "multiple_choice", ["Line chart", "Word art", "Pivot chart", "Mail merge"], 1),
            ("Digital Literacy", "Which action is safest before sharing a document online?", "multiple_choice", ["Check privacy settings and permissions", "Send it to everyone", "Save without a password", "Download it twice"], 1),
            ("Digital Literacy", "What does a file extension .xlsx represent?", "multiple_choice", ["Excel workbook", "Image file", "Audio file", "Zip file"], 1),
            ("Digital Literacy", "Which is the best way to protect a digital account?", "multiple_choice", ["Use a strong unique password and MFA", "Share the password with friends", "Use the same password everywhere", "Avoid setting recovery options"], 1),
            ("Digital Literacy", "Which software is usually used for creating presentations?", "multiple_choice", ["PowerPoint", "Photoshop", "Excel", "Notepad"], 1),
            ("Communication", "A good workplace email should primarily be:", "multiple_choice", ["Clear, polite and concise", "Very long with lots of jargon", "Filled with emojis", "Written in all caps"], 1),
            ("Communication", "Which skill helps you explain a technical idea to a non-technical audience?", "multiple_choice", ["Simple communication", "Speed typing", "Data entry", "Complex coding"], 1),
            ("Communication", "Which response is most professional during a conflict?", "multiple_choice", ["Listen calmly, state facts, and propose a solution", "Argue to win", "Avoid the issue completely", "Blame others"], 1),
            ("Communication", "What is the best way to handle a missed meeting?", "multiple_choice", ["Apologize, communicate the reason, and send a follow-up", "Ignore the meeting and move on", "Ask someone else to cover your mistake", "Cancel the whole team"], 1),
            ("Problem Solving", "If a data report is missing values, the best next step is to:", "multiple_choice", ["Identify why data is missing and validate the source", "Ignore the issue", "Delete the whole report", "Change the date manually"], 1),
            ("Problem Solving", "Which approach is best for solving a recurring work issue?", "multiple_choice", ["Analyse root cause and test a solution", "Change process without data", "Assume the problem is random", "Stop working on it"], 1),
            ("Problem Solving", "A project deadline is at risk. What should you do first?", "multiple_choice", ["Assess blockers and re-prioritize tasks", "Wait for failure", "Blame the team", "Stop communication"], 1),
            ("Problem Solving", "If a dashboard shows incorrect results, the first check should be:", "multiple_choice", ["Data source and formula logic", "User satisfaction", "Office lighting", "Printer files"], 1),
            ("Aptitude", "If 12 workers complete a job in 10 days, how many days will 8 workers take if work rate is constant?", "multiple_choice", ["15 days", "8 days", "12 days", "10 days"], 1),
            ("Aptitude", "A number series: 2, 4, 8, 16, ?", "multiple_choice", ["32", "18", "20", "24"], 1),
            ("Aptitude", "Which number is greater than 5/8?", "multiple_choice", ["0.7", "0.4", "0.3", "0.2"], 1),
            ("Aptitude", "If a train travels 60 km in 1 hour, what is its speed in km/h?", "multiple_choice", ["60", "30", "90", "15"], 1),
            ("Career Interests", "Which role best matches someone who enjoys working with data and reporting?", "multiple_choice", ["Data Analyst", "Retail Associate", "Lab Technician", "Travel Consultant"], 1),
            ("Career Interests", "Which work style suits a person who enjoys solving technical problems?", "multiple_choice", ["Analytical and process-driven", "Purely customer-facing", "No planning", "Manual repetitive tasks"], 1),
            ("Career Interests", "Which area is most aligned with digital transformation jobs?", "multiple_choice", ["Power BI and automation", "Classical painting", "Agriculture only", "Manual drafting"], 1),
            ("Career Interests", "Which role is likely to require strong communication and client interaction?", "multiple_choice", ["Customer Success Executive", "Backend Developer", "Data Engineer", "Machine Operator"], 1),
        ]

        for idx, (category, question_text, q_type, options, correct_idx) in enumerate(question_templates * 2):
            cursor.execute(
                "INSERT INTO assessment_questions (assessment_id, category, question_text, question_type, sort_order) VALUES (?, ?, ?, ?, ?)",
                (assessment_id, category, question_text, q_type, idx + 1)
            )
            question_id = cursor.execute("SELECT id FROM assessment_questions ORDER BY id DESC LIMIT 1").fetchone()[0]
            for option_index, option_text in enumerate(options):
                cursor.execute(
                    "INSERT INTO assessment_options (question_id, option_text, option_value, is_correct, sort_order) VALUES (?, ?, ?, ?, ?)",
                    (question_id, option_text, str(option_index + 1), 1 if option_index == correct_idx - 1 else 0, option_index + 1)
                )

    assessment_id = cursor.execute("SELECT id FROM assessments ORDER BY id LIMIT 1").fetchone()[0]
    if cursor.execute("SELECT COUNT(*) FROM assessment_questions WHERE category = 'Job Readiness'").fetchone()[0] == 0:
        readiness_questions = [
            ("Which action best prepares you for a job interview?", ["Review the role and prepare evidence from projects", "Memorize unrelated facts", "Avoid researching the employer", "Wait until the interview starts"], 1),
            ("What should a strong job application include?", ["A role-specific profile and clear examples of skills", "The same generic profile for every job", "Only a list of hobbies", "No contact details"], 1),
            ("When should you follow up after an interview?", ["Send a concise, professional follow-up within a reasonable time", "Send repeated messages every hour", "Never communicate again", "Post private interview details publicly"], 1),
            ("What is the best way to show employability?", ["Demonstrate skills through projects, outcomes and clear communication", "Promise results without evidence", "List skills you have never used", "Avoid discussing learning goals"], 1),
        ]
        next_order = cursor.execute("SELECT COALESCE(MAX(sort_order), 0) FROM assessment_questions WHERE assessment_id = ?", (assessment_id,)).fetchone()[0]
        for offset, (question_text, options, correct_idx) in enumerate(readiness_questions, 1):
            cursor.execute("INSERT INTO assessment_questions (assessment_id, category, question_text, question_type, sort_order) VALUES (?, ?, ?, ?, ?)", (assessment_id, "Job Readiness", question_text, "multiple_choice", next_order + offset))
            question_id = cursor.lastrowid
            for option_index, option_text in enumerate(options, 1):
                cursor.execute("INSERT INTO assessment_options (question_id, option_text, option_value, is_correct, sort_order) VALUES (?, ?, ?, ?, ?)", (question_id, option_text, str(option_index), 1 if option_index == correct_idx else 0, option_index))

    if cursor.execute("SELECT COUNT(*) FROM counselling_payments").fetchone()[0] == 0:
        cursor.execute("INSERT INTO counselling_payments (booking_id, candidate_id, amount, payment_method, transaction_id, status, payment_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (1, 1, 299.0, "UPI", "DEMO-TP-20260910-001", "success", "2026-09-10 09:20:00", "Demo payment approved in test mode."))
        cursor.execute("INSERT INTO counselling_payments (booking_id, candidate_id, amount, payment_method, transaction_id, status, payment_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (2, 2, 399.0, "Card", "DEMO-TP-20260910-002", "success", "2026-09-10 10:25:00", "Card authorization simulated."))

    conn.commit()


def add_candidate(
    name,
    email,
    age,
    gender,
    qualification,
    field,
    skills,
    skill_levels,
    employment,
    experience,
    mobile_number=None,
    state=None,
    district=None,
    education_level=None,
    primary_skill=None,
    preferred_job_sector=None,
    preferred_job_location=None,
    employment_status=None,
    employer_name=None,
    job_role=None,
    monthly_salary=None,
    job_seeking_status=None,
    preferred_job_role=None,
    business_type=None,
    monthly_income_range=None,
    organisation=None,
    apprenticeship_role=None,
    training_program=None,
    training_centre=None,
    date_of_birth=None,
    target_role=None,
    password_hash=None,
    is_pre_registered=0
):
    if not name or not email:
        raise ValueError("Name and email are required.")

    conn = get_connection()
    cursor = conn.cursor()
    skill_id = generate_skill_id()
    registration_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO candidates (
            name, email, age, gender, qualification, field, skills, skill_levels,
            employment, experience, skill_id, date_of_birth, state, district,
            mobile_number, education_level, primary_skill, preferred_job_sector,
            preferred_job_location, employment_status, employer_name, job_role,
            monthly_salary, job_seeking_status, preferred_job_role, business_type,
            monthly_income_range, organisation, apprenticeship_role, training_program,
            training_centre, registration_date, current_status, password_hash,
            is_pre_registered, profile_completion, target_role
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        age,
        gender,
        qualification,
        field,
        skills,
        skill_levels,
        employment,
        experience,
        skill_id,
        date_of_birth,
        state,
        district,
        mobile_number,
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
        training_program,
        training_centre,
        registration_date,
        'New Candidate',
        password_hash,
        is_pre_registered,
        65,
        target_role,
    ))

    conn.commit()
    conn.close()
    return skill_id


def get_candidates():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, age, gender, qualification, field, skills,
               skill_levels, employment, experience, skill_id, date_of_birth,
               state, district, mobile_number, education_level, primary_skill,
               preferred_job_sector, preferred_job_location, employment_status,
               employer_name, job_role, monthly_salary, job_seeking_status,
               preferred_job_role, business_type, monthly_income_range,
               organisation, apprenticeship_role, training_program, training_centre,
               registration_date, current_status, profile_completion, target_role
        FROM candidates ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_candidate(candidate_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, age, gender, qualification, field, skills,
               skill_levels, employment, experience, skill_id, date_of_birth,
               state, district, mobile_number, education_level, primary_skill,
               preferred_job_sector, preferred_job_location, employment_status,
               employer_name, job_role, monthly_salary, job_seeking_status,
               preferred_job_role, business_type, monthly_income_range,
               organisation, apprenticeship_role, training_program, training_centre,
               registration_date, current_status, profile_completion, target_role
        FROM candidates WHERE id = ? OR skill_id = ?
    """, (candidate_id, candidate_id))
    row = cursor.fetchone()
    conn.close()
    return row


def get_candidate_by_skill_and_mobile(skill_id, mobile_or_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, age, gender, qualification, field, skills,
               skill_levels, employment, experience, skill_id, date_of_birth,
               state, district, mobile_number, education_level, primary_skill,
               preferred_job_sector, preferred_job_location, employment_status,
               employer_name, job_role, monthly_salary, job_seeking_status,
               preferred_job_role, business_type, monthly_income_range,
               organisation, apprenticeship_role, training_program, training_centre,
               registration_date, current_status, profile_completion, target_role
        FROM candidates
        WHERE skill_id = ?
          AND (LOWER(COALESCE(email, '')) = LOWER(?) OR LOWER(COALESCE(mobile_number, '')) = LOWER(?))
    """, (skill_id, mobile_or_email, mobile_or_email))
    row = cursor.fetchone()
    conn.close()
    return row


def get_pre_registrations():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM candidate_pre_registrations ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def add_employment_outcome(
    candidate_id,
    employment_status,
    company,
    industry,
    job_role,
    salary_range,
    placement_date,
    employment_after_training,
    career_progression
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employment_outcomes
        (candidate_id, employment_status, company, industry, job_role, salary_range,
         placement_date, employment_after_training, career_progression)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (candidate_id, employment_status, company, industry, job_role, salary_range, placement_date, employment_after_training, career_progression))
    conn.commit()
    conn.close()


def get_employment_outcomes():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("""
        SELECT e.id, e.candidate_id, c.name, e.employment_status, e.company, e.industry, e.job_role,
               e.salary_range, e.placement_date, e.employment_after_training, e.career_progression
        FROM employment_outcomes e LEFT JOIN candidates c ON e.candidate_id = c.id ORDER BY e.id DESC
    """).fetchall()
    conn.close()
    return rows


def add_training_program(
    program_name,
    provider,
    skill_area,
    location,
    duration,
    enrolled,
    completed,
    certified,
    employed,
    status
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO training_programs
        (program_name, provider, skill_area, location, duration, enrolled, completed, certified, employed, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (program_name, provider, skill_area, location, duration, enrolled, completed, certified, employed, status))
    conn.commit()
    conn.close()


def get_training_programs():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM training_programs ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_training_stats():
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute("SELECT COALESCE(SUM(enrolled), 0), COALESCE(SUM(completed), 0), COALESCE(SUM(certified), 0), COALESCE(SUM(employed), 0) FROM training_programs").fetchone()
    conn.close()
    enrolled = result[0]
    completed = result[1]
    certified = result[2]
    employed = result[3]
    completion_rate = round((completed / enrolled) * 100, 2) if enrolled else 0
    employment_rate = round((employed / completed) * 100, 2) if completed else 0
    return {"enrolled": enrolled, "completed": completed, "certified": certified, "employed": employed, "completion_rate": completion_rate, "employment_rate": employment_rate}


def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    total_candidates = cursor.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
    employed = cursor.execute("SELECT COUNT(*) FROM candidates WHERE LOWER(COALESCE(employment, '')) = 'employed'").fetchone()[0]
    unemployed = cursor.execute("SELECT COUNT(*) FROM candidates WHERE LOWER(COALESCE(employment, '')) = 'unemployed'").fetchone()[0]
    employment_records = cursor.execute("SELECT COUNT(*) FROM employment_outcomes").fetchone()[0]
    counselling_bookings = cursor.execute("SELECT COUNT(*) FROM counselling_bookings").fetchone()[0]
    pending_counselling = cursor.execute("SELECT COUNT(*) FROM counselling_bookings WHERE status = 'pending_payment' OR status = 'confirmed'").fetchone()[0]
    assessments_completed = cursor.execute("SELECT COUNT(*) FROM assessment_attempts WHERE status = 'submitted'").fetchone()[0]
    average_assessment_score = cursor.execute("SELECT ROUND(AVG(overall_score), 2) FROM assessment_results").fetchone()[0] or 0
    high_skill_gap_candidates = cursor.execute("SELECT COUNT(*) FROM assessment_results WHERE overall_score < 50").fetchone()[0]
    ai_assistant_usage = cursor.execute("SELECT COUNT(*) FROM ai_messages WHERE sender = 'user'").fetchone()[0]
    pre_registered = cursor.execute("SELECT COUNT(*) FROM candidate_pre_registrations").fetchone()[0]
    profile_completion = round((cursor.execute("SELECT AVG(COALESCE(profile_completion, 0)) FROM candidates").fetchone()[0] or 0), 2)
    conn.close()
    employment_rate = round((employed / total_candidates) * 100, 2) if total_candidates else 0
    return {
        "total_candidates": total_candidates,
        "employed": employed,
        "unemployed": unemployed,
        "employment_records": employment_records,
        "employment_rate": employment_rate,
        "counselling_sessions": counselling_bookings,
        "pending_counselling": pending_counselling,
        "pending_assessments": max(0, 25 - assessments_completed),
        "candidates_assessed": assessments_completed,
        "pre_registered_candidates": pre_registered,
        "profile_completion_rate": profile_completion,
        "average_assessment_score": average_assessment_score,
        "high_skill_gap_candidates": high_skill_gap_candidates,
        "ai_assistant_usage": ai_assistant_usage,
        "job_recommendations": 0,
        "training_recommendations": 0,
    }


def get_counsellors():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM counsellors ORDER BY id").fetchall()
    conn.close()
    return rows


def get_slots_for_counsellor(counsellor_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM counselling_slots WHERE counsellor_id = ? ORDER BY slot_date, start_time", (counsellor_id,)).fetchall()
    conn.close()
    return rows


def create_booking(candidate_id, counsellor_id, slot_id, reason, candidate_name=None, skill_id=None, payment_status='pending', session_type=None, duration_minutes=None):
    conn = get_connection()
    cursor = conn.cursor()
    slot = cursor.execute("SELECT * FROM counselling_slots WHERE id = ?", (slot_id,)).fetchone()
    counsellor = cursor.execute("SELECT * FROM counsellors WHERE id = ?", (counsellor_id,)).fetchone()
    if not slot or not counsellor:
        conn.close()
        return None
    selected_duration = int(duration_minutes or slot['duration_minutes'])
    selected_session_type = session_type or slot['session_type']
    booking_id = cursor.execute("INSERT INTO counselling_bookings (candidate_id, counsellor_id, slot_id, skill_id, candidate_name, reason, session_date, session_time, duration_minutes, session_type, status, payment_status, total_fee, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (candidate_id, counsellor_id, slot_id, skill_id or '', candidate_name or '', reason or '', slot['slot_date'], slot['start_time'], selected_duration, selected_session_type, 'pending_payment', payment_status, counsellor['fee'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))).lastrowid
    conn.commit()
    conn.close()
    return booking_id


def get_booking_by_id(booking_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM counselling_bookings WHERE id = ?", (booking_id,)).fetchone()
    conn.close()
    return row


def get_all_bookings():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM counselling_bookings ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def cancel_booking(booking_id, candidate_id):
    conn = get_connection()
    booking = conn.execute("SELECT status FROM counselling_bookings WHERE id = ? AND candidate_id = ?", (booking_id, candidate_id)).fetchone()
    if not booking or booking['status'] in ('completed', 'cancelled'):
        conn.close()
        return False
    conn.execute("UPDATE counselling_bookings SET status = 'cancelled' WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return True


def reschedule_booking(booking_id, candidate_id, slot_id):
    conn = get_connection()
    booking = conn.execute("SELECT status FROM counselling_bookings WHERE id = ? AND candidate_id = ?", (booking_id, candidate_id)).fetchone()
    slot = conn.execute("SELECT * FROM counselling_slots WHERE id = ?", (slot_id,)).fetchone()
    if not booking or not slot or booking['status'] in ('completed', 'cancelled'):
        conn.close()
        return False
    conn.execute("UPDATE counselling_bookings SET slot_id = ?, session_date = ?, session_time = ?, session_type = ?, status = 'confirmed' WHERE id = ?", (slot_id, slot['slot_date'], slot['start_time'], slot['session_type'], booking_id))
    conn.commit()
    conn.close()
    return True


def complete_demo_payment(booking_id, candidate_id, payment_method='UPI'):
    conn = get_connection()
    cursor = conn.cursor()
    booking = cursor.execute("SELECT * FROM counselling_bookings WHERE id = ?", (booking_id,)).fetchone()
    if not booking:
        conn.close()
        return None
    txn_id = f"DEMO-TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{booking_id}"
    cursor.execute("INSERT INTO counselling_payments (booking_id, candidate_id, amount, payment_method, transaction_id, status, payment_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (booking_id, candidate_id, booking['total_fee'], payment_method, txn_id, 'success', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Demo payment successful in prototype mode.'))
    cursor.execute("UPDATE counselling_bookings SET status = 'confirmed', payment_status = 'paid' WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return txn_id


def get_payment_by_booking(booking_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM counselling_payments WHERE booking_id = ? ORDER BY id DESC LIMIT 1", (booking_id,)).fetchone()
    conn.close()
    return row


def save_counselling_note(booking_id, candidate_id, counsellor_id, note_data):
    conn = get_connection()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("""
        INSERT INTO counselling_notes
        (booking_id, candidate_id, counsellor_id, session_summary,
         identified_challenges, recommended_skills, recommended_courses,
         recommended_jobs, next_steps, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(booking_id) DO UPDATE SET
            session_summary = excluded.session_summary,
            identified_challenges = excluded.identified_challenges,
            recommended_skills = excluded.recommended_skills,
            recommended_courses = excluded.recommended_courses,
            recommended_jobs = excluded.recommended_jobs,
            next_steps = excluded.next_steps,
            updated_at = excluded.updated_at
    """, (
        booking_id, candidate_id, counsellor_id,
        note_data.get('session_summary', ''),
        note_data.get('identified_challenges', ''),
        note_data.get('recommended_skills', ''),
        note_data.get('recommended_courses', ''),
        note_data.get('recommended_jobs', ''),
        note_data.get('next_steps', ''), now, now
    ))
    conn.execute("UPDATE counselling_bookings SET status = 'completed' WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()


def get_counselling_notes(candidate_id=None):
    conn = get_connection()
    if candidate_id:
        rows = conn.execute("SELECT * FROM counselling_notes WHERE candidate_id = ? ORDER BY id DESC", (candidate_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM counselling_notes ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_or_create_ai_conversation(candidate_id=None):
    conn = get_connection()
    row = conn.execute("SELECT * FROM ai_conversations WHERE candidate_id = ? ORDER BY id DESC LIMIT 1", (candidate_id,)).fetchone()
    if not row:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conversation_id = conn.execute("INSERT INTO ai_conversations (candidate_id, started_at, last_message_at) VALUES (?, ?, ?)", (candidate_id, now, now)).lastrowid
        row = conn.execute("SELECT * FROM ai_conversations WHERE id = ?", (conversation_id,)).fetchone()
    conn.close()
    return row


def save_ai_messages(conversation_id, candidate_id, user_message, assistant_message):
    conn = get_connection()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.executemany(
        "INSERT INTO ai_messages (conversation_id, candidate_id, sender, message, created_at) VALUES (?, ?, ?, ?, ?)",
        [(conversation_id, candidate_id, 'user', user_message, now), (conversation_id, candidate_id, 'assistant', assistant_message, now)]
    )
    conn.execute("UPDATE ai_conversations SET last_message_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()


def get_ai_messages(candidate_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ai_messages WHERE candidate_id = ? ORDER BY id", (candidate_id,)).fetchall()
    conn.close()
    return rows


def get_assessment_questions():
    conn = get_connection()
    rows = conn.execute("SELECT q.id, q.category, q.question_text, q.question_type, q.sort_order, q.assessment_id FROM assessment_questions q ORDER BY q.sort_order").fetchall()
    collated = []
    for row in rows:
        options = conn.execute("SELECT id, option_text, option_value, is_correct, sort_order FROM assessment_options WHERE question_id = ? ORDER BY sort_order", (row['id'],)).fetchall()
        collated.append({"id": row['id'], "category": row['category'], "question_text": row['question_text'], "question_type": row['question_type'], "options": [dict(o) for o in options]})
    conn.close()
    return collated


def save_assessment_attempt(candidate_id, assessment_id, answers, target_role=None):
    conn = get_connection()
    cursor = conn.cursor()
    attempt_id = cursor.execute("INSERT INTO assessment_attempts (candidate_id, assessment_id, started_at, submitted_at, overall_score, status) VALUES (?, ?, ?, ?, ?, ?)",
        (candidate_id, assessment_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 'submitted')).lastrowid
    question_rows = cursor.execute("SELECT * FROM assessment_questions WHERE assessment_id = ? ORDER BY sort_order", (assessment_id,)).fetchall()
    category_totals = {
        "Technical Skills": 0,
        "Digital Literacy": 0,
        "Communication": 0,
        "Problem Solving": 0,
        "Aptitude": 0,
        "Career Interests": 0,
        "Job Readiness": 0,
    }
    category_scores = {k: 0 for k in category_totals}
    for question in question_rows:
        selected = answers.get(str(question['id']))
        if selected is None:
            continue
        correct_option = cursor.execute("SELECT id, is_correct FROM assessment_options WHERE question_id = ? AND is_correct = 1", (question['id'],)).fetchone()
        score = 0.0
        if correct_option and str(selected) == str(correct_option['id']):
            score = 100.0
        category_totals[question['category']] += 1
        category_scores[question['category']] += score
        cursor.execute("INSERT INTO assessment_answers (attempt_id, question_id, selected_option_id, answer_text, score_value) VALUES (?, ?, ?, ?, ?)",
                       (attempt_id, question['id'], int(selected) if str(selected).isdigit() else None, selected, score))
    final_category_scores = {}
    for key, total in category_totals.items():
        if total:
            final_category_scores[key] = round((category_scores[key] / total), 2)
        else:
            final_category_scores[key] = 0
    overall_score = round(sum(final_category_scores.values()) / len(final_category_scores), 2) if final_category_scores else 0
    summary = f"Overall readiness score: {overall_score}%"
    cursor.execute("INSERT INTO assessment_results (candidate_id, attempt_id, assessment_id, technical_score, digital_literacy_score, communication_score, problem_solving_score, aptitude_score, career_interest_score, overall_score, result_summary, generated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (candidate_id, attempt_id, assessment_id, final_category_scores.get('Technical Skills', 0), final_category_scores.get('Digital Literacy', 0), final_category_scores.get('Communication', 0), final_category_scores.get('Problem Solving', 0), final_category_scores.get('Aptitude', 0), final_category_scores.get('Career Interests', 0), overall_score, summary, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    cursor.execute("UPDATE assessment_attempts SET overall_score = ? WHERE id = ?", (overall_score, attempt_id))
    if candidate_id:
        cursor.execute("UPDATE candidates SET target_role = ?, profile_completion = 100 WHERE id = ?", (target_role or 'Data Analyst', candidate_id))
    conn.commit()
    conn.close()
    return {"overall_score": overall_score, "category_scores": final_category_scores, "summary": summary, "attempt_id": attempt_id}


def get_candidate_assessment_results(candidate_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM assessment_results WHERE candidate_id = ? ORDER BY id DESC LIMIT 1", (candidate_id,)).fetchone()
    conn.close()
    return row


create_database()