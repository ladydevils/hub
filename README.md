# Table of Contents

* [Project Overview](#project-overview)
* [Quick Start (TL;DR)](#quick-start)
* [Who to Contact](#who-to-contact)

- [Tech Stack Summary](docs/ARCHITECTURE.md#tech-stack-summary)
- [Architecture Overview](docs/ARCHITECTURE.md#architecture-overview)
- [Testing Tutorial](docs/ARCHITECTURE.md#testing-tutorial)
- [Current Deployment](docs/DEPLOYMENT.md)
- [Contributing & Project Management](CONTRIBUTING.md)
- [Known Issues & Limitations](docs/ARCHITECTURE.md#known-issues--limitations)

# Project Overview

### What is it?

> Lady Devils Hub is a team management platform for the Duke Women's Flag Football club, centralizing event scheduling, team announcements, roster management, and playbook access in one place.

### Why does it matter?

> Since becoming a club sport Fall 2026, the team has taken on significantly more logistics to manage. Exec members are also full-time students, with limited time to spend on administrative overhead. Keeping things organized and seamless is essential so Exec spend more time on fundraising, tournaments, player retention, team fun, and community and social events. Before Lady Devils Hub, Exec relied on a mix of software tools that made it easy to lose track of a single source of truth.

<!-- example of mix of tools used When2Meet, Google Sheets, and GroupMe--->

### Who is it for?

> It's built for the whole team! It gives Exec members a place to manage scheduling, announcements, and team logistics, and gives players a consistent place to check practice times, tournament details, and team updates without digging through GroupMe history.


# Quick Start
For those who want to jump in and start running the project locally for development, follow the instructions below:

### Prerequisites
- Git installed
- Python 3.14 installed
- Node.js 26 installed
- Access to the project's database connection strings (ask a maintainer for credentials). Needed in [Backend Setup, step 5](#backend-setup) to fill values for `DATABASE_URL=` and `TEST-DATABASE_URL=`

### Backend Setup
1. Clone the repo and move into the backend folder where the following steps should take place:
   ```bash
   git clone https://github.com/rakiranelson/lady-devils-hub.git
   cd lady-devils-hub/backend
   ```
2. Create a virtual environment:
   - On macOS/Linux (Bash):
     ```bash
     python3.14 -m venv venv
     ```
   - On Windows (PowerShell):
     ```powershell
     py -3.14 -m venv venv
     ```

3. Activate the virtual environment for running the backend:
   - On macOS/Linux (Bash): `source venv/bin/activate`
   - On Windows (PowerShell): `venv\Scripts\activate`
   - > You can deactivate the venv by running `deactivate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a file called `.env` in the same `backend` directory with the structure found in [.env.example](backend/.env.example):
   ```env
   # Example .env file

    DATABASE_URL=db_connection_string_here
    TEST_DATABASE_URL=test_db_connection_string_here

   # the frontend URL(s) allowed to send requests to this backend
    ALLOWED_ORIGINS=http://localhost:3000 # or http://<your machine's local network IP>:3000 (e.g. 10.197.28.231)
    
    API_PREFIX=/api
    DEBUG=False
   ```
   > If you want to use your local network IP, you can find this by typing the following in a terminal:
   > - On macOS/Linux (Bash): `ifconfig`/`ip addr`
   > - On Windows (PowerShell): `ipconfig`
   
   > This IP is assigned by whatever network you're connected to, so it changes when you switch Wi-Fi networks. If it does changes, update it here.
   
6. Run the server:
   ```bash
   python main.py
   ```
   Or, for auto-reload during development:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Move into the frontend folder:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with the following structure:
    ```env
    # the backend URL the frontend sends its API requests to
    NEXT_PUBLIC_API_URL=http://localhost:8000 # or http://<your machine's local network IP>:8000 (e.g. 10.197.28.231)
   ```
   > Want to use your local network IP here too? See [Backend Setup, step 5](#backend-setup) for details

4. Run the dev server:
   ```bash
   npm run dev
   ```

5. Open the app in your browser:
   
   [http://localhost:3000](http://localhost:3000) or whatever port your terminal outputs when you run the command in [step 4](#frontend-setup).

   > - Using the app from another device on your local network? Use your machine's local network IP instead (the same one from [Backend Setup, step 5](#backend-setup)) (e.g. `http://10.197.28.231:3000`)
   > - Whichever address you use here, make sure it matches an entry in `ALLOWED_ORIGINS` in [Backend Setup, step 5](#backend-setup) — otherwise the frontend's requests to the backend will be blocked by CORS.
   

# Who to Contact

**Maintainer:** Ra'Kira Nelson
- GitHub: [@rakiranelson](https://github.com/rakiranelson)
- Email: rakira.nelson@duke.edu

For something that's broken, a feature you'd like to see, or questions about contributing, see [Contributing & Project Management](#-contributing--project-management). For anything else, feel free to reach out directly via GitHub or email.




