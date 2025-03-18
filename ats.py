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
import os
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from grammarcheck.ats_grammar_check import check_and_correct_pdf

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('punkt_tab')

jobDesc = {
    'mern': '''We are looking for a highly skilled MERN Stack Developer to join our development team. The ideal candidate will have experience building scalable web applications using MongoDB, Express.js, React, and Node.js. You will be responsible for developing and maintaining full-stack applications, from designing database architecture to implementing the frontend and backend logic.

Responsibilities:

Design, develop, and maintain robust, scalable web applications using the MERN stack (MongoDB, Express.js, React, Node.js).
Build and manage APIs, microservices, and RESTful services.
Collaborate with the UI/UX team to create user-friendly, visually appealing interfaces.
Write clean, maintainable, and efficient code, following best practices and industry standards.
Manage databases and optimize application performance.
Debug and resolve technical issues and identify areas for improvement.
Work closely with project managers and other team members to meet deadlines and deliver high-quality features.
Test and deploy applications using CI/CD pipelines.
Ensure the security of web applications by implementing secure coding practices.
Stay updated with the latest technologies and best practices in web development.

Requirements:

Proven experience as a MERN Stack Developer or similar role.
Strong proficiency in JavaScript, with hands-on experience in React.js, Node.js, Express.js, and MongoDB.
Experience with front-end development using React, including hooks, state management, and component lifecycles.
Knowledge of back-end technologies and RESTful API development using Node.js and Express.js.
Familiarity with database management, especially MongoDB, including database schema design and performance optimization.
Strong understanding of HTML5, CSS3, and modern JavaScript (ES6+).
Experience with version control tools such as Git.
Knowledge of API integration (e.g., third-party APIs, authentication).
Familiarity with testing frameworks such as Jest, Mocha, or similar.
Experience with deployment on cloud platforms like AWS, Azure, or Heroku is a plus.
Good problem-solving skills and attention to detail.
Ability to work in a fast-paced, collaborative environment.

Preferred Qualifications:

Experience with state management libraries like Redux or Context API.
Familiarity with Next.js and SSR (Server-Side Rendering) is a plus.
Understanding of Agile methodologies and tools like Jira.
Knowledge of WebSockets and real-time data handling.
Prior experience with CI/CD pipelines and DevOps practices.''',

    'backend_developer': '''We are seeking a talented Backend Developer to design, implement, and maintain server-side applications. The ideal candidate will have strong programming skills and experience developing high-performance, scalable systems.

Responsibilities:

Design and implement robust, scalable backend services and APIs.
Write clean, maintainable, and efficient code with appropriate documentation.
Collaborate with frontend developers to integrate user-facing elements with server-side logic.
Optimize applications for maximum speed and scalability.
Implement security and data protection measures.
Design and maintain database schemas that represent and support business processes.
Integrate data storage solutions including databases, key-value stores, blob stores, etc.
Create and maintain CI/CD pipelines for automated testing and deployment.
Troubleshoot, debug and upgrade existing systems.
Collaborate with DevOps to ensure system reliability and performance.

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field (or equivalent work experience).
3+ years of experience as a Backend Developer or similar role.
Proficiency in at least one backend programming language (e.g., Python, Java, Go, Ruby, C#, Node.js).
Strong knowledge of databases (SQL and NoSQL) and data modeling.
Experience with RESTful APIs and microservices architecture.
Understanding of server-side templating languages.
Familiarity with version control systems (Git).
Knowledge of cloud services (AWS, Azure, or GCP).
Experience with testing frameworks and methodologies.
Strong problem-solving skills and attention to detail.
Good communication skills and ability to work in a team.

Preferred Qualifications:

Experience with message brokers like RabbitMQ or Kafka.
Knowledge of containerization technologies (Docker, Kubernetes).
Understanding of serverless architectures.
Experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions).
Familiarity with Agile development methodologies.
Knowledge of security best practices and data protection regulations.''',

    'frontend_developer': '''We are looking for a skilled Frontend Developer to join our team. You will be responsible for building the client-side of our web applications. The ideal candidate should have strong skills in HTML, CSS, and JavaScript, and experience with modern frontend frameworks.

Responsibilities:

Implement visual elements and user interactions that users see and interact with in the web application.
Develop new user-facing features and maintain existing ones.
Build reusable code and libraries for future use.
Ensure the technical feasibility of UI/UX designs.
Optimize applications for maximum speed and scalability.
Collaborate with backend developers and web designers to improve usability.
Ensure cross-browser compatibility and responsive design.
Implement responsive design for mobile sites.
Stay up-to-date with emerging technologies and industry trends.
Perform testing and debugging of frontend components.

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field (or equivalent work experience).
2+ years of experience as a Frontend Developer.
Proficient in HTML5, CSS3, and JavaScript (ES6+).
Experience with responsive and adaptive design.
Experience with at least one modern JavaScript framework (React, Angular, Vue.js).
Good understanding of CSS pre-processors (SASS, LESS).
Knowledge of cross-browser compatibility issues and ways to work around them.
Experience with RESTful APIs and integrating with backend services.
Understanding of code versioning tools, such as Git.
Knowledge of frontend build tools (Webpack, Gulp, Grunt).

Preferred Qualifications:

Experience with state management libraries (Redux, MobX, Vuex).
Knowledge of TypeScript.
Experience with testing frameworks (Jest, Mocha, Cypress).
Familiarity with UI/UX design principles.
Experience with GraphQL.
Understanding of server-side rendering and its benefits.
Knowledge of accessibility standards and best practices.
Experience with CI/CD workflows.''',

    'devops_engineer': '''We're seeking a skilled DevOps Engineer to join our team. In this role, you will be responsible for building and maintaining our infrastructure, deployment systems, and operational processes. The ideal candidate should have a strong background in systems administration and software development with experience in cloud platforms.

Responsibilities:

Design, implement, and manage CI/CD pipelines.
Build and maintain infrastructure as code using tools like Terraform, CloudFormation, or Pulumi.
Implement and manage container orchestration platforms (Kubernetes, Docker Swarm).
Deploy and configure cloud services and infrastructure.
Monitor system performance and optimize system resources.
Implement security best practices and maintain security protocols.
Troubleshoot and resolve infrastructure and application issues.
Automate routine operational tasks and processes.
Collaborate with development teams to improve deployment workflows.
Implement disaster recovery and backup strategies.

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field (or equivalent work experience).
3+ years of experience in a DevOps or similar role.
Strong knowledge of Linux/Unix administration.
Experience with cloud platforms (AWS, Azure, GCP).
Knowledge of infrastructure as code tools (Terraform, CloudFormation, Pulumi).
Experience with containerization technologies (Docker, Kubernetes).
Proficiency in scripting languages (Python, Bash, PowerShell).
Experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions, CircleCI).
Understanding of networking concepts (TCP/IP, DNS, HTTP, HTTPS).
Experience with monitoring tools and log management solutions.

Preferred Qualifications:

Knowledge of database administration.
Experience with configuration management tools (Ansible, Chef, Puppet).
Understanding of microservices architecture.
Experience with serverless computing.
Knowledge of security best practices in cloud environments.
Familiarity with Agile methodologies.
Experience with site reliability engineering principles.
Professional certifications (AWS, Azure, GCP, Kubernetes).''',

    'data_scientist': '''We are looking for a skilled Data Scientist to analyze complex data sets and extract valuable insights to help drive business decisions. The ideal candidate will have strong statistical analysis skills, programming experience, and the ability to effectively communicate findings to both technical and non-technical audiences.

Responsibilities:

Collect, process, and analyze large and complex data sets.
Develop machine learning models to solve business problems.
Create data visualizations and dashboards to communicate insights.
Collaborate with stakeholders to understand business needs and goals.
Perform exploratory data analysis to identify patterns and trends.
Design and implement A/B tests to evaluate the impact of product changes.
Develop and maintain data pipelines for model training and inference.
Stay current with emerging technologies and methodologies in data science.
Present findings and recommendations to key stakeholders.
Collaborate with engineering teams to implement and deploy models.

Requirements:

Master's or PhD in Computer Science, Statistics, Mathematics, or related field.
3+ years of experience in data science or related field.
Strong programming skills in Python or R.
Experience with data manipulation and analysis libraries (Pandas, NumPy).
Proficiency in machine learning frameworks (Scikit-learn, TensorFlow, PyTorch).
Knowledge of statistical analysis and modeling techniques.
Experience with SQL and database systems.
Strong problem-solving and critical thinking skills.
Excellent written and verbal communication skills.
Ability to translate complex findings into actionable insights.

Preferred Qualifications:

Experience with big data technologies (Hadoop, Spark).
Knowledge of deep learning techniques and applications.
Experience with cloud-based data platforms (AWS, Azure, GCP).
Familiarity with data visualization tools (Tableau, Power BI, Matplotlib, Seaborn).
Knowledge of natural language processing or computer vision.
Experience with version control systems (Git).
Understanding of software development best practices.
Domain expertise in relevant industry (finance, healthcare, e-commerce, etc.).''',

    'qa_engineer': '''We are seeking a detail-oriented Quality Assurance (QA) Engineer to ensure the quality of our software products. The ideal candidate will have strong analytical skills, testing experience, and the ability to identify and report issues effectively.

Responsibilities:

Design, develop and execute test plans, test cases, and test scripts.
Perform manual and automated testing of web and mobile applications.
Identify, document, and track software defects and verify fixes.
Collaborate with development teams to ensure quality throughout the software development lifecycle.
Analyze requirements, specifications, and technical design documents.
Participate in code reviews and provide feedback on code quality.
Develop and maintain automated test frameworks and scripts.
Monitor and report on testing progress and product quality.
Identify areas for improvement in the QA process.
Stay current with industry trends and testing methodologies.

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field (or equivalent work experience).
2+ years of experience in software testing or quality assurance.
Experience with manual and automated testing methodologies.
Knowledge of test management tools and defect tracking systems.
Familiarity with at least one automated testing tool (Selenium, Cypress, TestComplete).
Understanding of web technologies (HTML, CSS, JavaScript).
Experience with API testing.
Good understanding of software development life cycle.
Strong problem-solving and analytical skills.
Excellent written and verbal communication skills.

Preferred Qualifications:

ISTQB or similar testing certification.
Experience with performance testing tools (JMeter, LoadRunner).
Knowledge of mobile application testing.
Experience with continuous integration and continuous delivery (CI/CD) pipelines.
Familiarity with Agile methodologies.
Scripting skills in Python, JavaScript, or similar languages.
Experience with test-driven development (TDD) or behavior-driven development (BDD).
Knowledge of SQL and database testing.''',

    'solutions_architect': '''We are looking for an experienced Solutions Architect to design and implement innovative technical solutions that address complex business challenges. The ideal candidate will have strong technical knowledge, excellent communication skills, and the ability to translate business requirements into technical specifications.

Responsibilities:

Design and develop technical solutions to meet business requirements.
Create high-level solution designs and architecture diagrams.
Evaluate and recommend technologies, frameworks, and platforms.
Work with stakeholders to understand business objectives and constraints.
Collaborate with development teams to ensure proper implementation of solutions.
Provide technical leadership and guidance to project teams.
Ensure that solutions align with company standards and best practices.
Create technical documentation and specifications.
Identify and mitigate technical risks.
Stay current with emerging technologies and industry trends.

Requirements:

Bachelor's or Master's degree in Computer Science, Engineering, or related field.
5+ years of experience in software development or architecture.
Strong understanding of software development methodologies and best practices.
Experience with cloud platforms (AWS, Azure, GCP).
Knowledge of microservices architecture and distributed systems.
Understanding of security principles and practices.
Experience with databases (SQL and NoSQL).
Strong problem-solving and analytical skills.
Excellent communication and presentation skills.
Ability to work effectively with both technical and non-technical stakeholders.

Preferred Qualifications:

Professional certifications (AWS, Azure, GCP, TOGAF).
Experience with containerization and orchestration technologies.
Knowledge of DevOps practices and tools.
Experience with infrastructure as code (Terraform, CloudFormation).
Understanding of API design and management.
Experience in multiple programming languages.
Familiarity with regulatory compliance requirements.
Prior experience in the relevant industry domain.''',

    'cybersecurity_analyst': '''We are seeking a skilled Cybersecurity Analyst to help protect our organization's digital assets from security threats. The ideal candidate will have experience in security operations, threat detection, and incident response.

Responsibilities:

Monitor security systems and networks for threats and intrusions.
Investigate security breaches and incidents to determine their scope and impact.
Implement and maintain security tools, technologies, and processes.
Conduct vulnerability assessments and penetration testing.
Develop and implement security policies, procedures, and controls.
Perform security risk assessments and provide recommendations.
Stay informed about emerging threats and vulnerabilities.
Collaborate with IT teams to address security issues.
Provide security awareness training to employees.
Document security incidents and prepare reports.

Requirements:

Bachelor's degree in Computer Science, Cybersecurity, or related field.
3+ years of experience in cybersecurity or information security.
Knowledge of security frameworks and best practices (NIST, ISO 27001, CIS).
Experience with security tools and technologies (firewalls, IDS/IPS, SIEM).
Understanding of network security and protocols.
Knowledge of encryption technologies and PKI.
Experience with vulnerability assessment tools.
Familiarity with operating systems security (Windows, Linux).
Strong analytical and problem-solving skills.
Excellent communication and documentation skills.

Preferred Qualifications:

Security certifications (CISSP, CEH, CompTIA Security+, OSCP).
Experience with cloud security (AWS, Azure, GCP).
Knowledge of regulatory compliance requirements (GDPR, HIPAA, PCI DSS).
Experience with threat hunting and advanced persistent threats (APTs).
Familiarity with scripting languages (Python, PowerShell).
Experience with incident response and forensic analysis.
Knowledge of application security testing.
Understanding of DevSecOps principles.''',

    'product_manager': '''We are looking for a dynamic Product Manager to join our team and lead the development of innovative software products. The ideal candidate will have a strong technical background, excellent communication skills, and the ability to translate business needs into product requirements.

Responsibilities:

Define product vision, strategy, and roadmap based on market research and business objectives.
Gather and prioritize product requirements from stakeholders and users.
Create detailed product specifications and user stories for development teams.
Work closely with engineering, design, and marketing teams throughout the product lifecycle.
Conduct market research to identify customer needs and market opportunities.
Track and analyze product metrics to measure success and inform decisions.
Manage product backlog and prioritize features based on business value.
Represent the voice of the customer in product decisions.
Lead product launches and coordinate with marketing for go-to-market strategy.
Stay informed about industry trends and competitive landscape.

Requirements:

Bachelor's degree in Computer Science, Engineering, Business, or related field.
3+ years of experience in product management, preferably in software or technology.
Strong understanding of software development lifecycle and methodologies.
Experience with product management tools (Jira, Asana, Trello).
Excellent analytical and problem-solving skills.
Strong communication and presentation skills.
Ability to work cross-functionally with various teams.
Data-driven approach to decision making.
Good understanding of user experience design principles.
Technical background or ability to quickly understand technical concepts.

Preferred Qualifications:

MBA or Master's degree in relevant field.
Experience with Agile/Scrum methodologies.
Knowledge of data analysis tools and techniques.
Experience with A/B testing and feature experimentation.
Background in software development or engineering.
Product management certification (Pragmatic Marketing, Certified Scrum Product Owner).
Experience in the relevant industry domain.
Knowledge of growth hacking techniques.''',

    'ai_engineer': '''We are seeking an experienced AI Engineer to design, develop, and deploy artificial intelligence and machine learning solutions. The ideal candidate will have strong technical skills, experience with AI frameworks, and the ability to solve complex problems using machine learning techniques.

Responsibilities:

Design, develop, and implement AI models to solve business problems.
Process, clean, and verify the integrity of data used for analysis.
Develop machine learning pipelines and infrastructure for model training and deployment.
Optimize existing machine learning algorithms and models.
Collaborate with data scientists, engineers, and product managers.
Research and implement appropriate ML algorithms and tools.
Develop processes and tools to monitor and analyze model performance.
Transform data science prototypes into production-ready code.
Stay current with the latest AI research and technologies.
Document development processes and maintain technical documentation.

Requirements:

Master's or PhD in Computer Science, Artificial Intelligence, Machine Learning, or related field.
3+ years of experience in AI/ML development or related role.
Strong programming skills in Python or other relevant languages.
Experience with machine learning frameworks (TensorFlow, PyTorch, Scikit-learn).
Understanding of data structures, data modeling, and software architecture.
Knowledge of deep learning techniques and applications.
Experience with deploying ML models to production environments.
Familiarity with cloud platforms (AWS, Azure, GCP) and their ML services.
Strong problem-solving and analytical skills.
Good communication skills and ability to explain complex concepts.

Preferred Qualifications:

Experience with natural language processing or computer vision.
Knowledge of MLOps practices and tools.
Experience with distributed computing and big data technologies.
Familiarity with containerization and orchestration technologies.
Experience with real-time prediction systems.
Knowledge of reinforcement learning techniques.
Understanding of DevOps principles.
Research publications or contributions to open-source projects.''',

    'blockchain_developer': '''We are looking for an innovative Blockchain Developer to design, implement, and support blockchain-based solutions. The ideal candidate will have experience with blockchain protocols, smart contract development, and distributed ledger technologies.

Responsibilities:

Design and implement blockchain architecture and solutions.
Develop and deploy smart contracts using languages like Solidity.
Create secure and efficient code for blockchain applications.
Perform testing and security audits of blockchain applications.
Integrate blockchain solutions with existing systems and applications.
Research and evaluate blockchain protocols and frameworks.
Collaborate with other developers, project managers, and stakeholders.
Troubleshoot and resolve blockchain application issues.
Stay informed about developments in blockchain technology.
Document technical specifications and processes.

Requirements:

Bachelor's or Master's degree in Computer Science, Engineering, or related field.
2+ years of experience in blockchain development or related field.
Proficiency in at least one blockchain platform (Ethereum, Hyperledger, Solana, etc.).
Experience with smart contract development (Solidity, Rust, etc.).
Strong programming skills in at least one general-purpose language (JavaScript, Python, Go).
Understanding of cryptography and security principles.
Knowledge of web3 libraries and technologies.
Familiarity with distributed systems and consensus algorithms.
Experience with full-stack development.
Strong problem-solving and analytical skills.

Preferred Qualifications:

Experience with DeFi (Decentralized Finance) protocols.
Knowledge of NFT (Non-Fungible Token) development.
Experience with Layer 2 solutions (Optimistic Rollups, zkRollups).
Familiarity with cross-chain technologies.
Experience with blockchain testing frameworks.
Knowledge of tokenomics and cryptocurrency economics.
Understanding of regulatory considerations in blockchain.
Contributions to open-source blockchain projects.''',

    'cloud_engineer': '''We are seeking a skilled Cloud Engineer to design, implement, and manage our cloud infrastructure. The ideal candidate will have experience with cloud platforms, infrastructure as code, and automated deployment processes.

Responsibilities:

Design, implement, and manage cloud-based infrastructure on AWS, Azure, or GCP.
Migrate applications and systems from on-premises to cloud environments.
Develop and maintain infrastructure as code using tools like Terraform or CloudFormation.
Implement security best practices and ensure compliance in cloud environments.
Monitor cloud resources for performance, availability, and cost optimization.
Troubleshoot and resolve infrastructure and application issues in cloud environments.
Collaborate with development teams to implement CI/CD pipelines.
Automate routine operational tasks and processes.
Stay current with emerging cloud technologies and services.
Create and maintain documentation for cloud architecture and procedures.

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field (or equivalent work experience).
3+ years of experience with cloud platforms (AWS, Azure, GCP).
Experience with infrastructure as code tools (Terraform, CloudFormation, Pulumi).
Knowledge of containerization and orchestration technologies (Docker, Kubernetes).
Understanding of networking concepts in cloud environments.
Experience with CI/CD tools and practices.
Proficiency in scripting languages (Python, PowerShell, Bash).
Knowledge of security best practices in cloud environments.
Strong problem-solving and analytical skills.
Good communication and documentation skills.

Preferred Qualifications:

Cloud certifications (AWS Solutions Architect, Azure Administrator, GCP Professional Cloud Architect).
Experience with multi-cloud and hybrid cloud architectures.
Knowledge of serverless computing and architectures.
Experience with monitoring and logging tools in cloud environments.
Familiarity with cost optimization strategies in cloud platforms.
Understanding of disaster recovery and business continuity planning.
Experience with database administration in cloud environments.
Knowledge of DevOps practices and culture.''',

    'mobile_developer': '''We are looking for a talented Mobile Developer to design, build, and maintain high-quality mobile applications. The ideal candidate will have experience with mobile app development on iOS or Android platforms and a passion for creating intuitive user experiences.

Responsibilities:

Design and build advanced applications for the iOS or Android platform.
Collaborate with cross-functional teams to define, design, and ship new features.
Work with outside data sources and APIs.
Unit-test code for robustness, including edge cases, usability, and general reliability.
Fix bugs and improve application performance.
Continuously discover, evaluate, and implement new technologies to maximize development efficiency.
Ensure the performance, quality, and responsiveness of applications.
Help maintain code quality, organization, and automatization.
Participate in code reviews and provide constructive feedback to other developers.
Stay up-to-date with the latest industry trends in mobile technologies.

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field (or equivalent work experience).
2+ years of experience in mobile application development.
Proficiency in at least one mobile development platform:
- For iOS: Swift or Objective-C, Xcode, and iOS SDK
- For Android: Kotlin or Java, Android Studio, and Android SDK
Experience with RESTful APIs and JSON.
Understanding of the full mobile development lifecycle.
Familiarity with offline storage, threading, and performance optimization techniques.
Knowledge of mobile UI design principles and best practices.
Experience with version control systems (Git).
Strong problem-solving skills and attention to detail.
Good communication skills and ability to work in a team.

Preferred Qualifications:

Experience with cross-platform development frameworks (React Native, Flutter).
Knowledge of mobile app architecture patterns (MVC, MVVM, MVP).
Experience with mobile app testing frameworks.
Familiarity with continuous integration for mobile applications.
Published applications on the App Store or Google Play.
Experience with push notifications, location services, and other mobile-specific technologies.
Knowledge of app security best practices.
Understanding of app performance optimization techniques.''',

    'data_engineer': '''We are seeking a skilled Data Engineer to build and maintain our data infrastructure. The ideal candidate will have experience with data warehousing, ETL processes, and data modeling, and will be able to transform raw data into formats suitable for analysis.

Responsibilities:

Design, build, and maintain scalable data pipelines and ETL processes.
Develop, construct, test, and maintain architectures such as databases and large-scale processing systems.
Collaborate with data scientists, analysts, and other stakeholders to understand data needs.
Create and maintain optimal data pipeline architecture.
Identify, design, and implement internal process improvements.
Build analytics tools that utilize the data pipeline to provide insights.
Improve data reliability, efficiency, and quality.
Implement data security and privacy measures.
Keep up to date with new technologies and industry trends.
Document data flows, pipelines, and processes.

Requirements:

Bachelor's or Master's degree in Computer Science, Engineering, or related field.
3+ years of experience in data engineering or similar role.
Strong SQL skills and experience with relational databases.
Experience with data warehousing and ETL tools.
Proficiency in programming languages such as Python, Java, or Scala.
Experience with big data technologies (Hadoop, Spark, Hive).
Knowledge of data modeling and database design.
Familiarity with cloud platforms (AWS, Azure, GCP) and their data services.
Understanding of distributed computing principles.
Strong problem-solving and analytical skills.

Preferred Qualifications:

Experience with stream-processing systems (Kafka, Flink).
Knowledge of NoSQL databases (MongoDB, Cassandra, HBase).
Experience with data visualization tools (Tableau, Power BI).
Familiarity with container technologies (Docker, Kubernetes).
Experience with CI/CD for data pipelines.
Knowledge of data governance principles.
Understanding of machine learning pipelines.
Experience with workflow management tools (Airflow, Luigi).''',

    'ui_ux_designer': '''We are looking for a creative UI/UX Designer to design and shape unique, user-centric digital experiences for our products. The ideal candidate will have a strong portfolio demonstrating their design thinking process and UI/UX skills.

Responsibilities:

Create user flows, wireframes, prototypes, and mockups to effectively communicate design ideas.
Design UI elements and build design systems that promote a seamless user experience.
Conduct user research and testing to inform design decisions.
Collaborate with product managers and engineers to define and implement innovative solutions.
Create original graphic designs (e.g., images, sketches, and tables).
Identify and troubleshoot UX problems.
Conduct layout adjustments based on user feedback.
Adhere to style standards on fonts, colors, and images.
Stay up-to-date with design trends, tools, and technologies.
Create and maintain comprehensive design documentation.

Requirements:

Bachelor's degree in Design, Fine Arts, Human-Computer Interaction, or related field (or equivalent work experience).
2+ years of experience in UI/UX design.
Proficiency in design and prototyping tools (Figma, Sketch, Adobe XD, InVision).
Strong portfolio of design projects demonstrating problem-solving skills.
Understanding of user-centered design principles and methodologies.
Knowledge of interaction design and information architecture.
Experience conducting user research and usability testing.
Excellent visual design skills with sensitivity to user-system interaction.
Strong communication and presentation skills.
Ability to work effectively in a collaborative environment.

Preferred Qualifications:

Experience with design systems and component libraries.
Knowledge of HTML, CSS, and JavaScript fundamentals.
Experience with motion design and animation tools.
Understanding of accessibility standards and best practices.
Familiarity with Agile development methodologies.
Experience designing for multiple platforms (web, mobile, desktop).
Knowledge of analytics tools and metrics that drive design decisions.
Experience in the relevant industry domain.''',

    'technical_project_manager': '''We are seeking an experienced Technical Project Manager to lead cross-functional teams in delivering complex software projects. The ideal candidate will have a strong technical background, excellent project management skills, and the ability to communicate effectively with both technical and non-technical stakeholders.

Responsibilities:

Plan, execute, and close software development projects.
Define project scope, goals, and deliverables in collaboration with stakeholders.
Create and maintain project schedules, resource plans, and budgets.
Lead cross-functional teams throughout the project lifecycle.
Manage project risks, issues, and changes.
Track and report project progress to stakeholders.
Facilitate communication between technical teams and business units.
Ensure that projects are delivered on time, within scope, and within budget.
Implement and maintain project management best practices.
Continuously identify process improvements.

Requirements:

Bachelor's degree in Computer Science, Engineering, Business, or related field.
4+ years of experience in technical project management.
Strong understanding of software development methodologies (Agile, Waterfall).
Experience with project management tools (Jira, Microsoft Project, Asana).
Knowledge of software development lifecycle and processes.
Strong leadership and team management skills.
Excellent communication, negotiation, and conflict resolution skills.
Ability to manage multiple projects simultaneously.
Problem-solving orientation and analytical mindset.
Technical background or ability to understand technical concepts.

Preferred Qualifications:

Project Management Professional (PMP) or other project management certification.
Scrum Master certification.
Experience with budget management and resource allocation.
Knowledge of risk management principles and practices.
Experience in the relevant industry domain.
Understanding of DevOps practices and tools.
Experience with product development lifecycles.
Knowledge of change management principles.''',

    'sre_engineer': '''We are looking for a skilled Site Reliability Engineer (SRE) to ensure the reliability, availability, and performance of our systems and services. The ideal candidate will have a strong background in both software development and operations, with experience in automating and optimizing infrastructure.

Responsibilities:

Design, implement, and maintain infrastructure automation using code.
Monitor system performance and availability.
Implement and manage disaster recovery and business continuity planning.
Troubleshoot and resolve production issues and outages.
Design and implement scalable and resilient architecture.
Optimize system performance and resource utilization.
Implement and maintain CI/CD pipelines.
Collaborate with development teams to improve reliability and operational efficiency.
Participate in on-call rotations to provide production support.
Create and maintain documentation for systems and processes.

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field (or equivalent work experience).
3+ years of experience in DevOps, SRE, or similar role.
Strong programming and scripting skills (Python, Go, Bash).
Experience with cloud platforms (AWS, Azure, GCP).
Knowledge of infrastructure as code tools (Terraform, CloudFormation).
Experience with containerization and orchestration technologies (Docker, Kubernetes).
Understanding of monitoring systems and log analysis.
Strong knowledge of networking and security concepts.
Experience with CI/CD tools and practices.
Good problem-solving skills and ability to work under pressure.

Preferred Qualifications:

Experience with observability tools (Prometheus, Grafana, ELK stack).
Knowledge of distributed systems and microservices architecture.
Experience with database administration.
Familiarity with service mesh technologies (Istio, Linkerd).
Experience with chaos engineering principles and practices.
Knowledge of performance tuning and optimization techniques.
Understanding of capacity planning and forecasting.
Cloud or platform-specific certifications.''',

    'data_analyst': '''We are seeking a detail-oriented Data Analyst to translate data into valuable insights. The ideal candidate will have strong analytical skills, experience with data analysis tools, and the ability to present findings in a clear and compelling way.

Responsibilities:

Collect, process, and analyze structured and unstructured data.
Identify trends, patterns, and anomalies in complex data sets.
Create dashboards, reports, and visualizations to communicate insights.
Work with stakeholders to understand data needs and requirements.
Develop and implement databases, data collection systems, and other strategies.
Clean and validate data to ensure accuracy, completeness, and consistency.
Support business decision-making through data analysis and interpretation.
Collaborate with teams to implement changes based on findings.
Maintain and document data processes and methodologies.
Stay current with analytical techniques and tools.

Requirements:

Bachelor's degree in Statistics, Mathematics, Computer Science, Economics, or related field.
2+ years of experience in data analysis or business intelligence.
Strong proficiency in SQL and experience with databases.
Experience with data visualization tools (Tableau, Power BI, Looker).
Proficiency in Excel and data manipulation techniques.
Knowledge of statistical analysis and methods.
Experience with data cleaning and preprocessing.
Strong problem-solving and critical thinking skills.
Excellent communication skills and ability to translate complex findings.
Attention to detail and ability to work with large data sets.

Preferred Qualifications:

Experience with programming languages (Python, R).
Knowledge of business intelligence concepts and practices.
Familiarity with big data technologies.
Experience with A/B testing and experimentation.
Understanding of data warehousing concepts.
Knowledge of machine learning basics.
Experience in the relevant industry domain.
Familiarity with data governance principles.''',
"security_engineer": '''We are seeking a skilled Security Engineer to develop and implement security measures for our systems and networks. The ideal candidate will have experience in security operations, threat detection, and vulnerability management.

Responsibilities:

Design, implement, and maintain security systems and solutions.
Develop and implement security policies, procedures, and controls.
Conduct security assessments, audits, and penetration testing.
Identify and remediate security vulnerabilities.
Monitor and analyze security events and incidents.
Implement and maintain security tools and technologies.
Respond to security incidents and conduct investigations.
Collaborate with IT teams to ensure secure system configurations.
Stay informed about emerging threats and security trends.
Provide security guidance and recommendations to stakeholders.

Requirements:

Bachelor's degree in Computer Science, Cybersecurity, or related field.
3+ years of experience in security engineering or similar role.
Knowledge of security frameworks and best practices (NIST, ISO 27001, CIS).
Experience with security tools and technologies (firewalls, IDS/IPS, SIEM).
Understanding of network security and protocols.
Knowledge of encryption technologies and PKI.
Experience with vulnerability assessment and management.
Familiarity with operating systems security (Windows, Linux).
Strong problem-solving and analytical skills.
Good communication and documentation skills.

Preferred Qualifications:

Security certifications (CISSP, CEH, CompTIA Security+, OSCP).
Experience with cloud security (AWS, Azure, GCP).
Knowledge of regulatory compliance requirements (GDPR, HIPAA, PCI DSS).
Experience with application security testing tools.
Familiarity with scripting languages (Python, PowerShell, Bash).
Knowledge of secure coding practices.
Experience with security in CI/CD pipelines.
Understanding of identity and access management solutions.''',

"system_administrator": '''We are looking for a skilled System Administrator to maintain and manage our IT infrastructure. The ideal candidate will have experience with various operating systems, network administration, and IT security.

Responsibilities:

Install, configure, and maintain operating systems and software.
Monitor system performance and optimize resources.
Manage user accounts, permissions, and access rights.
Implement and maintain security measures and data backups.
Troubleshoot and resolve hardware, software, and network issues.
Perform regular system updates and security patches.
Document system configurations and processes.
Manage and maintain IT infrastructure, including servers and storage.
Provide technical support to end-users when needed.
Plan and implement system upgrades and migrations.

Requirements:

Bachelor's degree in Computer Science, Information Technology, or related field (or equivalent experience).
3+ years of experience as a System Administrator or similar role.
Strong knowledge of Windows and Linux operating systems.
Experience with virtualization technologies (VMware, Hyper-V).
Understanding of networking concepts and protocols.
Knowledge of IT security principles and practices.
Experience with backup and recovery systems.
Familiarity with scripting languages (PowerShell, Python, Bash).
Strong problem-solving and analytical skills.
Good communication and documentation skills.

Preferred Qualifications:

Relevant certifications (CompTIA A+, Network+, MCSA, RHCE).
Experience with cloud platforms (AWS, Azure, GCP).
Knowledge of monitoring tools and systems.
Experience with configuration management tools (Ansible, Puppet, Chef).
Familiarity with containerization technologies.
Understanding of database administration.
Experience with disaster recovery planning.
Knowledge of IT service management frameworks (ITIL).''',

"machine_learning_engineer": '''We are seeking a talented Machine Learning Engineer to develop and implement machine learning models and systems. The ideal candidate will have a strong background in machine learning algorithms, software engineering, and data processing.

Responsibilities:

Design and implement machine learning models to solve complex problems.
Develop and maintain scalable machine learning infrastructure.
Select appropriate datasets and data representation methods.
Run machine learning tests and experiments.
Implement appropriate ML algorithms and tools.
Perform statistical analysis and fine-tune models using test results.
Train and retrain systems when necessary.
Extend existing ML libraries and frameworks.
Keep up to date with latest ML technologies and methodologies.
Collaborate with data scientists and engineers to implement models.

Requirements:

Master's or PhD in Computer Science, Machine Learning, or related field.
3+ years of experience in machine learning engineering or similar role.
Strong programming skills in Python and proficiency with ML libraries (TensorFlow, PyTorch, scikit-learn).
Experience with data science toolkits (NumPy, Pandas, Jupyter).
Understanding of data structures, data modeling, and software architecture.
Knowledge of mathematics, probability, statistics, and algorithms.
Experience in deploying machine learning models to production.
Familiarity with cloud platforms and their ML services.
Strong problem-solving and analytical skills.
Good communication skills and ability to work in a team.

Preferred Qualifications:

Experience with deep learning architectures and applications.
Knowledge of MLOps practices and tools.
Experience with big data technologies (Hadoop, Spark).
Familiarity with containerization and orchestration tools.
Understanding of software development best practices.
Experience with streaming data processing.
Knowledge of data visualization techniques.
Research publications or contributions to open-source projects.'''
}
def processing(resume_copy, choice, role):
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
    job_des = jobDesc.get(role)
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
        resume = docx2txt.process(".static/uploads/" + resume_copy)
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
    base_name, extension = os.path.splitext(resume_copy)

# Append "-1" to the base name
    new_file_name = f"{base_name}-1{extension}"
    # Now you can use the soft_skills_list in your Python code
    corrections= check_and_correct_pdf("./static/uploads/" + resume_copy, './static/uploads/'+new_file_name)


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
        corrections
    )


# processing("pt.pdf", 1, "html ,angular")
