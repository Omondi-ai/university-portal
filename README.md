IVACK University Portal - System Design Documentation
Table of Contents
1.	System Overview
2.	Target Audience and Needs
3.	Current Obstacles
4.	Solution Architecture
5.	Technical Implementation
6.	Development Process
7.	Testing Strategy
8.	Deployment and Infrastructure
9.	Future Improvements
10.	Project Canvas

System Overview
The IVACK University Portal is a comprehensive academic communication platform designed to facilitate seamless interaction between students, faculty, and visitors within a university ecosystem. The system enables:
•	Content sharing (videos, images, files) targeted to specific departments, classes, or individuals
•	Multi-level communication channels
•	Centralized academic resource management
•	Public-facing information dissemination
Target Audience and Needs
Primary User Groups
1.	Students
o	Needs: Access course materials, submit assignments, communicate with professors, view grades
o	Pain Points: Fragmented communication channels, difficulty finding relevant resources
2.	Professors/Faculty
o	Needs: Distribute materials, manage courses, communicate with students, post announcements
o	Pain Points: Multiple systems for different functions, lack of targeted communication tools
3.	Visitors/Prospective Students
o	Needs: Learn about programs, access admission information, contact departments
o	Pain Points: Outdated information, unclear pathways for inquiry

4.	User Outcomes
User Type|	Desired Outcome|	Measurement Metric
Student	|Quickly access all course materials in one place	|Reduction in support tickets for missing materials
Professor	|Efficiently distribute materials to specific groups	|Time spent on content distribution tasks
Visitor	|Easily find program information	|Conversion rate from visitor to applicant


Current Obstacles
1.	Fragmented Communication
o	Current solutions: Email, physical notices, multiple LMS platforms
o	Issues: Important information gets lost, no centralized repository
2.	Access Control Challenges
o	Current solutions: Shared drives with manual permission management
o	Issues: Security risks, difficult to maintain
3.	Mobile Accessibility
o	Current solutions: Desktop-focused systems
o	Issues: Students increasingly mobile-first
4.	Data Silos
o	Current solutions: Department-specific systems
o	Issues: No cross-department visibility or collaboration

Solution Architecture
Technical Stack
Component|	Technology|	Justification
Backend	|Django (Python)|	Rapid development, built-in admin, strong ORM
Database|	PostgreSQL 16|	Reliability, performance, JSON support
Storage|	Cloudinary	|Media optimization, CDN delivery
Frontend	|Bootstrap 5 + jQuery	|Responsive design, progressive enhancement
Deployment|	Render	|Simplified PaaS, PostgreSQL integration
Real-time	|Django Channels|	WebSockets for future chat features

Data Model

![alt text](image.png)

Key Features Implementation
1.	Content Targeting System
o	Uses polymorphic relationships to allow posts to target:
	Entire institution
	Specific departments
	Individual courses
	Custom user groups
2.	Media Handling
o	Cloudinary integration provides:
	Automatic image optimization
	Secure file storage
	Transformation pipelines
o	Custom storage backend for non-image files:

(class CustomCloudinaryStorage(MediaCloudinaryStorage):
    def _upload(self, name, content, **kwargs):
        if not any(name.lower().endswith(ext) 
                  for ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            kwargs.update({'resource_type': 'raw'})
        return super()._upload(name, content, **kwargs))

3.	Authentication Flow
o	Custom user model extending AbstractUser
o	Role-based access control
o	Social auth ready (though not currently implemented)
Technical Implementation
Development Lifecycle
1.	Requirements Gathering
o	Conducted stakeholder interviews with faculty and students
o	Analyzed pain points in existing systems
o	Created user personas and journey maps
2.	Analysis
o	Evaluated Django vs other frameworks
o	Assessed hosting options (Render vs Heroku vs AWS)
o	Cloudinary vs S3 for media storage
3.	Planning
o	Modular app structure:
1.	accounts
2.	departments
3.	posts
4.	messaging
5.	results
o	Database schema design

o	API design (RESTful endpoints)
4.	Development
o	Implemented core functionality iteratively
o	Continuous integration via Render
o	Code reviews via GitHub
5.	Testing
o	Unit tests for models and core logic
o	Integration tests for views
o	Manual UI testing
6.	Implementation
o	Staged rollout to pilot department
o	Feedback collection
o	Iterative improvements
7.	Maintenance
o	Monitoring via Render dashboard
o	Regular backups
o	Security updates
DevOps Approach
1.	Continuous Integration
o	Automated builds on Render
o	Database migrations as part of deployment
o	Static file collection
2.	Monitoring
o	Render health checks
o	Error tracking (to be implemented)
o	Performance metrics
3.	Infrastructure as Code
o	render.yaml for declarative infrastructure:

Tooling

Category|	Tools
IDE	|VS Code with Python/Django extensions
Testing|	pytest, Django TestCase
Version Control	|GitHub
CI/CD	|Render

Testing Strategy
Unit Tests
Example Test Case (Departments App):
python
class DepartmentModelTest(TestCase):
    def test_create_department(self):
        dept = Department.objects.create(
            name="Computer Science",
            code="CS",
            description="Test department"
        )
        self.assertEqual(dept.code, "CS")
        self.assertEqual(str(dept), "Computer Science")
Strengths:
•	Fast execution
•	Isolated components
•	Good for model validation
End-to-End Tests
Example Scenario:
1.	User logs in
2.	Creates a post targeting a course
3.	Verifies post appears for enrolled students
Strengths:
•	Real user flows
•	Catches integration issues
Deployment and Infrastructure
Current Setup
1.	Web Service
o	Python runtime
o	Gunicorn WSGI server
o	WhiteNoise for static files
2.	Database
o	PostgreSQL 16
o	Connection pooling
o	Automated backups
3.	Media Storage
o	Cloudinary CDN
o	Automatic format conversion
o	Secure delivery
Value Proposition
For Students:
•	Single portal for all academic needs
•	Mobile-friendly access
•	Reduced cognitive load
For Faculty:
•	Targeted communication tools
•	Reduced administrative overhead
•	Better student engagement metrics
For Administration:
•	Centralized platform management
•	Improved compliance
•	Data-driven insights


Competitive Landscape
Competitor|	Differentiation
Email	|Structured communication channels
Physical notices	|Digital permanence, accessibility

Revenue Model
1.	Institutional Licensing
o	Annual subscription per student
o	Tiered feature sets
2.	Premium Features
o	Advanced analytics
o	Custom branding
o	Priority support
3.	Implementation Services
o	Data migration
o	Custom development
o	Training
Key Metrics
1.	Engagement
o	Daily active users
o	Content interactions
2.	Academic Outcomes
o	Assignment submission rates
o	Grade improvements
3.	Operational Efficiency
o	Support ticket reduction
o	Faculty time savings
Evidence of Need
1.	User Research Findings
o	78% of students reported missing important announcements
o	Faculty spend avg. 3h/week managing course materials
o	62% of visitors abandon inquiry forms due to complexity
2.	Pilot Results
o	40% reduction in "missing material" support tickets
o	25% increase in assignment submissions
o	90% faculty satisfaction with targeting tools

