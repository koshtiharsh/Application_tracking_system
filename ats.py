# !pip install docx2txt

# !pip install PyPDF2
# All packages required for ats

from typing import List
from PyPDF2 import PdfReader
import docx2txt
import nltk
import spacy
import string
import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize


def processing(resume_copy, choice, jobDesc):
    # preprocessing
    def clean_text(text):
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        tokens = text.split()
        stop_words = set(stopwords.words("english"))
        tokens = [word for word in tokens if word.lower() not in stop_words]
        cleaned_text = " ".join(tokens)
        return cleaned_text

    def clean_skills(skills_list):
        stop_words = set(stopwords.words("english"))
        punctuation = set(string.punctuation)
        cleaned_skills = [
            word
            for skill in skills_list
            for word in word_tokenize(skill.lower())
            if word.isalnum() and word not in stop_words and word not in punctuation
        ]
        return cleaned_skills

    def match_skills(job_description, skills_list):
        job_keywords = set(word_tokenize(job_description.lower()))
        matched_skills = [
            skill for skill in skills_list if skill.lower() in job_keywords
        ]
        return matched_skills

    def find_matching_skills_web(text, skills_list):
        text_keywords = set(word_tokenize(text.lower()))
        matching_skills = [
            skill for skill in skills_list if skill.lower() in text_keywords
        ]
        missing_skills = [
            skill for skill in skills_list if skill not in matching_skills
        ]

        return matching_skills, missing_skills

    def find_matching_skills_data(text, skill_for_DS):
        text_keywords = set(word_tokenize(text.lower()))
        matching_skills = [
            skill for skill in skill_for_DS if skill.lower() in text_keywords
        ]
        missing_skills = [
            skill for skill in skill_for_DS if skill not in matching_skills
        ]

        return matching_skills, missing_skills

    # taking the user input and resume #pg
    ch = choice
    # print("Choose Your file format")
    # print("1. PDF")
    # print("2. Docx")
    # ch = int(input("Enter the number: "))
    # job_des = input("Enter Job Description: ")
    job_des = jobDesc
    job_des = job_des.lower()
    error = False

    if ch == 1:

        def extract_text_from_pdf(pdf_file: str) -> List[str]:
            try:
                with open(pdf_file, "rb") as pdf:
                    reader = PdfReader(pdf)
                    pdf_text = []
                    for page in reader.pages:
                        content = page.extract_text()
                        pdf_text.append(content)
                    return pdf_text
            except FileNotFoundError:
                # print(f"The file '{pdf_file}' was not found.")
                return []

        extract_txt = extract_text_from_pdf("./static/uploads/" + resume_copy)
        fin_txt = []  # Initialize an empty list outside the loop
        for txt in extract_txt:
            txt = txt.lower()
            # print(txt)
            fin_txt.append(txt)

    elif ch == 2:
        resume = docx2txt.process("res.docx")
        resume = resume.lower()
        # print(resume)

    else:
        error = True

    # converting the array in string $pg
    ok = " ".join(fin_txt)

    # Checking the sections: #pg

    pdf_sections_found = []
    docx_sections_found = []
    section_found = []
    section_score = 0
    if ch == 1:
        if "professional experience" in ok or "projects" in ok or "experience" in ok:
            pdf_sections_found.append("Professional experience section found")

        if "education" in ok or "qualification" in ok:
            pdf_sections_found.append("Education section found")

        if "skills" in ok:
            pdf_sections_found.append("Skills section found")

        if "achievement" in ok:
            pdf_sections_found.append("Achievement section found")

        if "summary" in ok:
            pdf_sections_found.append("Summary section Found")
        section_found = pdf_sections_found

    elif ch == 2:
        if (
            "professional experience" in resume
            or "projects" in resume
            or "experience" in resume
        ):
            docx_sections_found.append("Professional experience section found")

        if "education" in resume or "qualification" in resume:
            docx_sections_found.append("Education section found")

        if "skills" in resume:
            docx_sections_found.append("Skills section found")

        if "achievement" in resume:
            docx_sections_found.append("Achievement section found")

        if "summary" in resume:
            docx_sections_found.append("Summary section Found")
        section_found = docx_sections_found

    # storing length of resume #hk
    resume_length = 0
    word_count = 0
    if ch == 1:
        resume_length = ok.split()
        word_count = len(resume_length)

    elif ch == 2:
        resume_length = resume.split()
        word_count = len(resume_length)

    # print(word_count)

    nltk.download("stopwords")  # hk

    # using the preprocessing function so that the stop words are removed
    if ch == 1:
        ok = clean_text(ok)

    elif ch == 2:
        resume = clean_text(resume)
        # print(resume)
        doc = [resume, job_des]

    job_des = clean_text(job_des)

    # print(job_des)
    z = [ok, job_des]

    a = CountVectorizer()

    # finding the similar key words

    if ch == 1:
        # print("pdf")
        c_at = a.fit_transform(z)
        # print(cosine_similarity(c_at))
        match = cosine_similarity(c_at)[0][1]
        match = match * 100
        match = round(match, 2)
        # print(match)

    elif ch == 2:
        # print("doc")
        c_mat = a.fit_transform(doc)
        # print(cosine_similarity(c_mat))
        match = cosine_similarity(c_mat)[0][1]
        match = match * 100
        match = round(match, 2)
        # print(match)

    nltk.download("punkt")

    skills_list = [
        "html",
        "css",
        "javascript",
        "react.js",
        "reactjs",
        "angular",
        "vue.js",
        "node.js",
        "nodejs",
        "expressjs",
        "express.js",
        "django",
        "flask",
        "ruby on rails",
        "php",
        "laravel",
        "java",
        "spring boot",
        "python",
        "asp.net",
        "asp.net core",
        "mysql",
        "postgresql",
        "mongodb",
        "firebase",
        "restful apis",
        "graphql",
        "git",
        "responsive design",
        "web performance optimization",
        "web security",
        "command line/shell scripting",
        "ui/ux design",
        "adobe creative suite (photoshop, illustrator)",
        "sketch",
        "figma",
        "invision",
        "prototyping",
        "wireframing",
        "typography",
        "color theory",
        "wordpress",
        "drupal",
        "joomla",
        "content management",
        "theme development",
        "plugin development",
        "customization",
        "cms security",
        "sass",
        "less",
        "bootstrap",
        "material-ui",
        "redux",
        "webpack",
        "gatsby.js",
        "next.js",
        "nextjs",
        "nuxt.js",
        "jquery",
        "handlebars.js",
        "ejs",
        "websockets",
        "ci/cd",
        "docker",
        "kubernetes",
        "jest",
        "mocha",
        "chai",
        "cypress",
        "junit",
        "rspec",
        "cucumber",
        "swagger",
        "postman",
        "graphql yoga",
        "apollo client",
        "axios",
        "socket.io",
        "heroku",
        "netlify",
        "aws",
        "azure",
        "google cloud platform",
        "jenkins",
        "travis ci",
        "circleci",
        "nginx",
        "apache",
        "oauth",
        "jwt",
        "oauth2",
        "oauth2.0",
        "openid connect",
        "webassembly",
        "pwa (progressive web apps)",
        "webrtc",
        "tensorflow",
        "keras",
        "pytorch",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "plotly",
        "tableau",
        "power bi",
        "d3.js",
        "natural language toolkit (nltk)",
        "spacy",
        "scrapy",
        "beautiful soup",
        "feature engineering",
        "time series analysis",
        "reinforcement learning",
        "data visualization",
        "a/b testing",
        "git",
        "docker",
        "ci/cd",
        "jupyter notebooks",
        "linux/unix",
        "shell scripting",
        "apis",
        "big data analytics",
        "predictive modeling",
        "neural networks",
        "dimensionality reduction",
        "ensemble learning",
        "cross-validation",
        "optimization techniques",
        "quantitative analysis",
        "feature selection",
        "distributed computing",
        "apache kafka",
        "restful apis",
        "data warehousing",
        "etl (extract, transform, load)",
        "version control",
        "data governance",
        "cybersecurity",
        "blockchain",
        "iot (internet of things)",
        "quantum computing",
        "perl",
        "c/c++",
        "sql",
        "java",
        "sas",
        "hadoop",
        "spark",
        "hive",
        "pig",
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "probability",
        "statistics",
        "web scraping",
        "natural language processing (nlp)",
        "multivariate calculus",
        "linear algebra",
        "database management",
        "mongodb",
        "cloud computing",
        "excel",
        "devops",
        "data extraction",
        "transformation",
        "loading",
        "data collection",
        "cleansing",
        "data preparation",
        "business intelligence",
        "model deployment",
        "data structures",
        "algorithms",
    ]

    # print(skills_list)

    cleaned_skills = clean_skills(skills_list)
    # print(cleaned_skills)

    # Example job description
    job_description = job_des

    # Example usage
    matched_skills = match_skills(job_description, cleaned_skills)
    # print("Matched Skills:")
    # print(matched_skills)

    # Example text
    another_text = ok

    # Example usage
    matching_skills, missing_skills = find_matching_skills_web(
        another_text, matched_skills
    )

    # print("Matching Skills:")
    # print(matching_skills)
    # print("\nMissing Skills:")
    # print(missing_skills)

    word_count_score = 0
    if 500 < word_count and word_count < 700:
        word_count_score = 80
    elif 300 < word_count and word_count < 500:
        word_count_score = 60
    elif 200 < word_count and word_count < 300:
        word_count_score = 50
    elif 100 < word_count and word_count < 200:
        word_count_score = 35
    elif 701 < word_count and word_count < 800:
        word_count_score = 70
    elif 800 < word_count and word_count < 100:
        word_count_score = 65
    elif word_count > 1001:
        word_count_score = 60

    # sectionwise scoring
    section_count = len(section_found)
    if section_count == 5:
        section_score = 70
    elif section_count == 4:
        section_score = 60
    elif section_count == 3:
        section_score = 50
    elif section_count < 3:
        section_score = 45
    # scoring for skills

    skill_score = 0
    desc_skill = len(matched_skills)
    no_match = len(matching_skills)
    no_miss = len(missing_skills)

    if no_match == 0:
        skill_score = 20
    else:
        skill_score = no_match / desc_skill * 100
    # print("skill score", skill_score)
    # print("count score", word_count_score)

    # soft skills scoring
    soft_skills_list = [
        "Communication",
        "Listening",
        "Negotiation",
        "Nonverbal communication",
        "Persuasion",
        "Presentation",
        "Public speaking",
        "Reading body language",
        "Social skills",
        "Storytelling",
        "Verbal communication",
        "Visual communication",
        "Writing reports and proposals",
        "Writing skills",
        "Critical Thinking",
        "Adaptability",
        "Artistic aptitude",
        "Creativity",
        "Critical observation",
        "Critical thinking",
        "Design aptitude",
        "Desire to learn",
        "Flexibility",
        "Innovation",
        "Logical thinking",
        "Problem-solving",
        "Research skills",
        "Resourcefulness",
        "Thinking outside the box",
        "Tolerance of change and uncertainty",
        "Troubleshooting skills",
        "Value education",
        "Willingness to learn",
        "Leadership",
        "Conflict management",
        "Conflict resolution",
        "Deal-making",
        "Decision-making",
        "Delegation",
        "Dispute resolution",
        "Facilitation",
        "Giving clear feedback",
        "Inspiring people",
        "Leadership",
        "Management",
        "Managing difficult conversations",
        "Managing remote/virtual teams",
        "Meeting management",
        "Mentoring",
        "Motivating",
        "Project management",
        "Resolving issues",
        "Successful coaching",
        "Supervising",
        "Talent management",
        "Positive Attitude",
        "Confidence",
        "Cooperation",
        "Courtesy",
        "Energy",
        "Enthusiasm",
        "Friendliness",
        "Honesty",
        "Humor",
        "Patience",
        "Respectability",
        "Respectfulness",
        "Teamwork",
        "Accepting feedback",
        "Collaboration",
        "Customer service",
        "Dealing with difficult situations",
        "Dealing with office politics",
        "Disability awareness",
        "Diversity awareness",
        "Emotional intelligence",
        "Empathy",
        "Establishing interpersonal relationships",
        "Dealing with difficult personalities",
        "Intercultural competence",
        "Interpersonal skills",
        "Influence",
        "Networking",
        "Persuasion",
        "Self-awareness",
        "Selling skills",
        "Social skills",
        "Team building",
        "Teamwork",
        "Work Ethic",
        "Attentiveness",
        "Business ethics",
        "Competitiveness",
        "Dedication",
        "Dependability",
        "Following direction",
        "Independence",
        "Meeting deadlines",
        "Motivation",
        "Multitasking",
        "Organization",
        "Perseverance",
        "Persistence",
        "Planning",
        "Proper business etiquette",
        "Punctuality",
        "Reliability",
        "Resilience",
        "Results-oriented",
        "Scheduling",
        "Self-directed",
        "Self-monitoring",
        "Self-supervising",
        "Staying on task",
        "Strategic planning",
        "Time management",
        "Trainability",
        "Working well under pressure",
        "Assertiveness",
        "Business ethics",
        "Business storytelling",
        "Business trend awareness",
        "Customer service",
        "Effective communicator",
        "Emotion management",
        "Ergonomic sensitivity",
        "Follows instructions",
        "Follows regulations",
        "Follows rules",
        "Functions well under pressure",
        "Good attitude",
        "Highly recommended",
        "Independent",
        "Interviewing",
        "Knowledge management",
        "Meets deadlines",
        "Motivating",
        "Performs effectively in a deadline environment",
        "Performance management",
        "Positive work ethic",
        "Problem-solving",
        "Process improvement",
        "Quick-witted",
        "Results-oriented",
        "Safety conscious",
        "Scheduling",
        "Self-awareness",
        "Self-supervising",
        "Stress management",
        "Team player",
        "Technology savvy",
        "Technology trend awareness",
        "Tolerant",
        "Trainable",
        "Training",
        "Troubleshooting",
        "Willing to accept feedback",
        "Willingness to learn",
        "Work-life balance",
        "Works well under pressure",
    ]
    cleaned_soft = clean_skills(soft_skills_list)

    # Example job description

    # Example usage
    matched_soft = match_skills(job_description, cleaned_soft)
    # print("Matched Skills:")

    # Example text

    # Example usage
    matching_soft, missing_soft = find_matching_skills_web(another_text, matched_soft)
    soft_skill_score = 0
    desc_skill_soft = len(matched_soft)
    no_match_soft = len(matching_soft)
    no_miss_soft = len(missing_soft)

    if no_match_soft == 0:
        soft_skill_score = 20
    else:
        soft_skill_score = no_match_soft / desc_skill_soft * 100
    # print("skill score", soft_skill_score)
    # print("count score", word_count_score)

    # Now you can use the soft_skills_list in your Python code

    final_score = (
        skill_score + section_score + word_count_score + soft_skill_score
    ) / 4
    # print("final score", final_score)

    return (
        final_score,
        matching_skills,
        missing_skills,
        matching_soft,
        missing_soft,
        word_count,
        section_found,
        skill_score,
        soft_skill_score,
        word_count_score,
        section_score,
    )


# processing("Resume (1).pdf", 1, "python ,angular")
