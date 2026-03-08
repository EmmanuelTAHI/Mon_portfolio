"""
Management command to pre-populate the database with portfolio initial data.
Run: python manage.py load_initial_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.projects.models import Project
from apps.skills.models import Skill
from apps.experience.models import Experience
from apps.blog.models import BlogPost


class Command(BaseCommand):
    help = "Load initial portfolio data (projects, skills, experience, blog)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before loading (optional)",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            BlogPost.objects.all().delete()
            Experience.objects.all().delete()
            Project.objects.all().delete()
            Skill.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing data."))

        self._load_skills()
        self._load_projects()
        self._load_experience()
        self._load_blog()
        self.stdout.write(self.style.SUCCESS("Initial data loaded successfully."))

    def _load_skills(self):
        skills_data = [
            # Penetration Testing
            ("Nmap", "pentesting", 85, ""),
            ("Metasploit", "pentesting", 80, ""),
            ("Burp Suite", "pentesting", 82, ""),
            ("Wireshark", "pentesting", 78, ""),
            # Networking
            ("TCP/IP", "networking", 88, ""),
            ("Routing", "networking", 75, ""),
            ("Firewalls", "networking", 72, ""),
            # Programming
            ("Python", "programming", 90, ""),
            ("JavaScript", "programming", 85, ""),
            ("TypeScript", "programming", 82, ""),
            ("C#", "programming", 70, ""),
            ("Bash", "programming", 80, ""),
            # Web
            ("Angular", "web", 85, ""),
            ("Next.js", "web", 78, ""),
            ("HTML", "web", 92, ""),
            ("CSS", "web", 88, ""),
            ("Tailwind", "web", 90, ""),
            # Security
            ("OWASP Top 10", "security", 85, ""),
            ("Web Exploitation", "security", 80, ""),
            ("Privilege Escalation", "security", 75, ""),
            ("CTF", "security", 82, ""),
        ]
        for name, category, level, desc in skills_data:
            Skill.objects.get_or_create(
                name=name,
                defaults={"category": category, "level": level, "description": desc},
            )
        self.stdout.write(f"  Loaded {len(skills_data)} skills.")

    def _load_projects(self):
        projects_data = [
            {
                "title": "Web Scraping Platform (Python MVC)",
                "slug": "web-scraping-platform-python-mvc",
                "short_description": "Python scraping project for Alibaba with multi-category scraping, CSV export and image downloads.",
                "description": "A full-featured web scraping platform built with Python following MVC architecture. Targets Alibaba with support for multiple categories, CSV export, and image downloads. Includes rate limiting and error handling.",
                "category": "web",
                "technologies": "Python, MVC, Requests, BeautifulSoup, CSV, Image Download",
                "github_url": "https://github.com",
                "is_featured": True,
            },
            {
                "title": "Cybersecurity Tools",
                "slug": "cybersecurity-tools",
                "short_description": "Pentesting scripts, reconnaissance automation, and security testing utilities.",
                "description": "Collection of custom cybersecurity tools including reconnaissance automation, vulnerability scanning helpers, and security testing scripts for learning and lab environments.",
                "category": "tool",
                "technologies": "Python, Bash, Nmap, Security",
                "github_url": "https://github.com",
                "is_featured": True,
            },
            {
                "title": "Pentesting Scripts",
                "slug": "pentesting-scripts",
                "short_description": "Automation and attack simulations for penetration testing practice.",
                "description": "Scripts for automating common pentesting tasks and simulating attack scenarios. Used in personal labs and CTF practice.",
                "category": "script",
                "technologies": "Python, Bash, Metasploit, Nmap",
                "github_url": "https://github.com",
                "is_featured": True,
            },
            {
                "title": "Stock Investment Optimization Algorithm",
                "slug": "stock-investment-optimization",
                "short_description": "Algorithm to optimize short-term stock investments with constraints.",
                "description": "Algorithmic project to optimize short-term stock investments under given constraints. Includes backtesting and constraint handling.",
                "category": "other",
                "technologies": "Python, Algorithms, Data Analysis",
                "github_url": "https://github.com",
                "is_featured": False,
            },
            {
                "title": "CTF Writeups Platform",
                "slug": "ctf-writeups-platform",
                "short_description": "Platform to organize CTF writeups and challenges.",
                "description": "Web platform to organize and display CTF writeups and challenges. Search, filter by category, and share solutions.",
                "category": "ctf",
                "technologies": "Angular, Django, PostgreSQL, CTF",
                "github_url": "https://github.com",
                "is_featured": True,
            },
        ]
        for p in projects_data:
            Project.objects.get_or_create(slug=p["slug"], defaults=p)
        self.stdout.write(f"  Loaded {len(projects_data)} projects.")

    def _load_experience(self):
        from datetime import date

        exp_data = [
            {
                "title": "Cybersecurity Student",
                "organization": "University / Training",
                "experience_type": "education",
                "location": "",
                "start_date": date(2022, 9, 1),
                "end_date": None,
                "is_current": True,
                "description": "Focused on penetration testing, network security, and secure development. Active in CTFs and lab practice.",
                "order": 10,
            },
            {
                "title": "Personal Pentesting Labs",
                "organization": "Home Lab",
                "experience_type": "lab",
                "location": "",
                "start_date": date(2021, 6, 1),
                "end_date": None,
                "is_current": True,
                "description": "Running vulnerable VMs (TryHackMe, HackTheBox, VulnHub) and custom setups for hands-on practice.",
                "order": 20,
            },
            {
                "title": "Capture The Flag Competitions",
                "organization": "CTF Teams / Solo",
                "experience_type": "ctf",
                "location": "",
                "start_date": date(2022, 1, 1),
                "end_date": None,
                "is_current": True,
                "description": "Regular participation in CTF events. Web, forensics, reverse engineering, and crypto challenges.",
                "order": 30,
            },
            {
                "title": "Web Development Projects",
                "organization": "Freelance / Personal",
                "experience_type": "project",
                "location": "",
                "start_date": date(2020, 9, 1),
                "end_date": None,
                "is_current": True,
                "description": "Full-stack web applications with Angular and Django. Security-conscious development and API design.",
                "order": 40,
            },
            {
                "title": "TryHackMe Certified",
                "organization": "TryHackMe",
                "experience_type": "certification",
                "location": "Online",
                "start_date": date(2023, 5, 1),
                "end_date": None,
                "is_current": False,
                "description": "Completed learning paths in penetration testing and defensive security.",
                "order": 50,
            },
            {
                "title": "HackTheBox Labs",
                "organization": "HackTheBox",
                "experience_type": "certification",
                "location": "Online",
                "start_date": date(2023, 3, 1),
                "end_date": None,
                "is_current": False,
                "description": "Active on HackTheBox platforms and challenges.",
                "order": 51,
            },
            {
                "title": "Networking Fundamentals",
                "organization": "Networking Certifications",
                "experience_type": "certification",
                "location": "Online",
                "start_date": date(2022, 8, 1),
                "end_date": None,
                "is_current": False,
                "description": "Understanding of TCP/IP, routing, and network security.",
                "order": 52,
            },
        ]
        for i, e in enumerate(exp_data):
            Experience.objects.get_or_create(
                title=e["title"],
                organization=e["organization"],
                defaults=e,
            )
        self.stdout.write(f"  Loaded {len(exp_data)} experience entries.")

    def _load_blog(self):
        now = timezone.now()
        blog_data = [
            {
                "title": "Getting Started with CTF Web Challenges",
                "slug": "getting-started-ctf-web",
                "post_type": "tutorial",
                "excerpt": "A beginner-friendly guide to approaching web challenges in Capture The Flag competitions.",
                "content": "Web challenges in CTFs often focus on OWASP Top 10 vulnerabilities. Start with basic SQL injection and XSS, then move to SSRF and deserialization. Use Burp Suite and browser dev tools as your best friends.",
                "tags": "ctf, web, tutorial, owasp",
                "is_published": True,
                "published_at": now,
            },
            {
                "title": "Nmap: From Basic Scans to Scripting",
                "slug": "nmap-basic-to-scripting",
                "post_type": "article",
                "excerpt": "How to leverage Nmap for reconnaissance and when to use NSE scripts.",
                "content": "Nmap is the go-to tool for network discovery and port scanning. We cover -sV, -sC, and custom NSE scripts for vulnerability detection. Always get proper authorization before scanning.",
                "tags": "nmap, pentesting, reconnaissance",
                "is_published": True,
                "published_at": now,
            },
            {
                "title": "Writeup: Easy Box on HackTheBox",
                "slug": "writeup-easy-box-htb",
                "post_type": "ctf",
                "excerpt": "Step-by-step writeup of an easy Linux machine.",
                "content": "Spoiler-free summary: enumeration leads to a web app, then to credentials, then to user and root. Key takeaway: always check for misconfigurations and default credentials.",
                "tags": "writeup, hackthebox, linux, pentesting",
                "is_published": True,
                "published_at": now,
            },
        ]
        for b in blog_data:
            BlogPost.objects.get_or_create(slug=b["slug"], defaults=b)
        self.stdout.write(f"  Loaded {len(blog_data)} blog posts.")
