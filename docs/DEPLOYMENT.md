# Current Deployment

- [Overview](#overview)
- [How to Deploy](#how-to-deploy)
  - [Backend](#backend)
    - [Set Up the VM](#1-set-up-the-vm)
    - [Set Up Caddy](#2-set-up-caddy)
    - [Set Up systemd Service](#3-set-up-systemd-service)
    - [Set Up Config for GitHub Actions](#4-set-up-config-for-github-actions)
  - [Frontend](#frontend)
  - [Database](#database)

# Overview
**Why this exists:** 

> Before this independent study ends, the project needs to be live rather than only runnable on localhost. A localhost setup that only runs on my own machine is only reachable from devices on the same local network. But the entire point of this application is for Exec and players to use it from their own devices, so a publicly accessible, stable address is needed. This deployment is a stepping stone to satisfy this requirement.

**What it's using:**
> - **Frontend:** [Vercel](https://ladydevils.vercel.app) — deploying the Next.js app directly from the `frontend/` directory of this repo
> - **Backend:** a Duke VM (`vcm-xxxxx.vm.duke.edu`) — running the FastAPI app as a systemd service named `lady-devils-hub`
> - **Database:** [Supabase](https://supabase.com) (managed PostgreSQL) — the backend connects to it remotely rather than running its own database server
> - **CI/CD:** GitHub Actions — pushing and Pull Requests to `main` runs the test suite, builds the frontend, waits for manual approval, then deploys to both Vercel and the Duke VM


For constraints specific to this setup (VM expiring each semester, hosting plan limits), see [Known Issues & Limitations](ARCHITECTURE.md#known-issues--limitations).

# How to Deploy
## Backend
**How the Backend is Set Up:**
1. The database is hosted remotely on Supabase (managed PostgreSQL), so the backend connects to it over a connection string (`DATABASE_URL`) configured in `.env`.
2. Caddy sits in front of the backend, providing a clean HTTPS address (`https://vcm-55838.vm.duke.edu`) with an automatically-managed certificate. Caddy is configured so that every request to the backend has to pass through Caddy first.
3. FastAPI runs on the Duke VM, managed by `systemd`, so it stays up permanently — surviving SSH disconnects, and auto-restarting if it crashes or the VM reboots.
4. GitHub Actions is set up to redeploy the backend automatically by pulling the latest code and restarting the systemd service.

> **NOTE:** These steps build on each other and should be completed in order because each one assumes the previous steps are already in place (e.g., systemd needs the app already runnable before it can manage it, and GitHub Actions' automated redeploy depends on systemd already being set up).

The steps below walk through setting up each of these pieces:
### 1. Set Up the VM

---

**1. Set up your SSH key**

If you don't already have an SSH key on your device, you'll need to generate one before you can connect to the Duke VM.

1. Check if you already have one:
```bash
ls ~/.ssh/id_ed25519.pub
```

If that file exists, skip to step 3 (Copy your public key).

2. Generate a new key pair:
```bash
ssh-keygen -t ed25519 -C "your_netid@duke.edu"
```
Press Enter to accept the default save location. The passphrase is an additional password you would need to enter each time you use the private key. You can set one up or leave the passphrase blank (Press Enter) for convenience if you are working on a personal device. 

3. Copy your public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

4. Paste the output into [Duke's IDMS Self Service (Advanced)](https://idms-web-selfservice.oit.duke.edu/advanced) (make sure you are logged in) under "Public SSH Keys Registered".

---

**2. Create a new Duke VM**
1. Navigate to [Duke's Virtual Computing Manager](https://vcm.duke.edu/) -> navigate to "Request a VM" -> choose "Ubuntu Server 26.04 (Resolute Raccoon)" -> complete VM request
2. Opt out of the "Automatic power down". For the reason, you can simply put:
   > "This VM runs the backend for a live web application and needs to stay running continuously rather than being powered down automatically."
3. Note both the ***Hostname*** (i.e. vcm-xxxxx.vm.duke.edu) and the ***User*** (i.e. your NetID)
4. Open a terminal and confirm you can connect to the VM
   ```bash
    ssh <netid>@vcm-xxxxx.vm.duke.edu
    ```
    > You should replace `<netid>` with your NetID and `xxxxx` with the numbers from your Hostname

---

**3. Configure the VM for This Project**
1. Run the following to confirm everything for the VM is up-to-date:
  ```bash
    sudo apt update && sudo apt upgrade -y
  ```
  The password should be the same password you use to sign into your Duke NetID accounts.
  
2. Check Python version :
  ```bash
    python3 –-version
  ```
  If it's already 3.14.4, continue to the step 3. If it's a different version, install 3.14.4 specifically:​
  ```bash
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.14
  ```

2. Run the following so you have the packages to create a virtual environment later:
  ```bash
    sudo apt install python3.14-venv -y
  ```

4. Check if git is installed:
  ```bash
    git --version
  ```
  If git is installed, continue to step 5. Otherwise, install git: 
  ```bash
    sudo apt install git -y
  ```

5. Clone the repo and cd into the backend directory:
  ```bash
    git clone https://github.com/rakiranelson/lady-devils-hub.git
    cd lady-devils-hub/backend
  ```

6. Create the virtual environment and install required Python packages:
  ```bash
    python3.14 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
  ```

7. Create the `.env` file:
  ```bash
    nano .env
  ```
  This opens a text editor in the terminal. Type in the appropriate values. 
  > Note: Ask a maintainer for DB connection strings.
  ```env
   DATABASE_URL=db_connection_string_here
   TEST_DATABASE_URL=test_db_connection_string_here
   ALLOWED_ORIGINS=https://ladydevils.vercel.app
   API_PREFIX=/api
   DEBUG=False
  ```

8. Save and exit:
  - `ctrl+O`/`command+O` to write the to the .env
  - `enter` to save
  - `ctrl+X`/`command+X` to exit

---

### 2. Set Up Caddy
You can install Caddy, by running each of the lines, in order, below (references [this tutorial](https://vultr.hashnode.dev/installing-caddy-web-server-on-ubuntu-26-04?utm_source=hashnode&utm_medium=feed)):

**1. Install Caddy**
  ```bash
    sudo apt update
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
    sudo apt update
    sudo apt install caddy -y
    caddy version
  ```

**2. Configure Caddy**
1. Edit Caddy's config file:
   ```caddyfile
    vcm-xxxxx.vm.duke.edu {
      reverse_proxy localhost:8000
    }
   ```
   > Where `xxxxx` are the numbers from your Hostname
   
   Then save and exit (`ctrl+O`, `enter`, then `ctrl+X`)

2. Then enable and start Caddy to apply the configurations:
   ```Bash
     sudo systemctl enable caddy
     sudo systemctl start caddy
   ```
  
3. Confirm that caddy is running:
  ```Bash
     sudo systemctl status caddy
   ```

---

### 3. Set Up systemd Service
> The purpose of this service is to allow the backend to run permanently even after the SSH connection disconnects

1. Create the service file
   ```Bash
     sudo nano /etc/systemd/system/lady-devils-hub.service
   ```

2. Paste this in the opened file, replacing `<netid>` with your Duke NetID:
  ```Bash
    [Unit]
    Description=Lady Devils Hub Backend
    After=network.target
    
    [Service]
    User=<netid>
    WorkingDirectory=/home/<netid>/lady-devils-hub/backend
    ExecStart=/home/<netid>/lady-devils-hub/backend/venv/bin/python main.py
    Restart=always
    RestartSec=5
    
    [Install]
    WantedBy=multi-user.target
   ```

  Then save and exit (`ctrl+O`, `enter`, then `ctrl+X`)

3. Reload systemd and start the service:
  ```Bash
    sudo systemctl daemon-reload
    sudo systemctl enable lady-devils-hub
    sudo systemctl start lady-devils-hub 
   ```

4. Confirm the backend is running:
  ```Bash
     sudo systemctl status lady-devils-hub
   ```
---

### 4. Set Up Config for GitHub Actions
> This is important to set up so the CI/CD pipeline works

1. Generate a new SSH key pair for the Github and the VM (This should be done in the VM terminal):
  ```Bash
     ssh-keygen -t ed25519 -f ~/.ssh/github-actions-key -N "" 
   ```
  > Note: `-f ~/.ssh/github-actions-key` is explicitly setting the name of the SSH key and `-N ""` is explicitly setting no passphrase

2. Add this public SSH key to the VM's list of public keys:
  ```Bash
     cat ~/.ssh/github-actions-key.pub >> ~/.ssh/authorized_keys
   ```

3. Print the private SSH key so you can copy it:
  ```Bash
     cat ~/.ssh/github-actions-key
   ```
  Copy the entire, including the `-----BEGIN...-----` and `-----END...-----` lines. 

4. Go to the [GitHub Repo](https://github.com/rakiranelson/lady-devils-hub) -> settings -> Secrets and variables -> Actions -> Manage environment secrets -> production.
   Scroll down and then edit the "VM_SSH_KEY" secret. Paste the private SSH key output you copied.


5. Set up the passwordless sudo rule so GitHub Actions can deploy the backend:
  ```Bash
     sudo visudo -f /etc/sudoers.d/lady-devils-hub
   ```
  And then add this line:
  ```Bash
    <netid> ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart lady-devils-hub 
  ```
  Then save and exit (`ctrl+O`, `enter`, then `ctrl+X`)

6. Check to see if your changes are in the file:
  ```Bash
    sudo visudo
   ```
  Scroll to the bottom of the file, and make sure it's formatted like:
  ```Bash
    <netid> ALL=(ALL) ALL
    @includedir /etc/sudoers.d
   ```
  And **NOT**:
  ```Bash
    @includedir /etc/sudoers.d
    <netid> ALL=(ALL) ALL
  ```

---

The backend is now live and will survive reboots, SSH disconnects, and crashes. You can confirm it's working by visiting `https://vcm-xxxxx.vm.duke.edu`. 

From here on, deploying updates is automatic. Pushing or Pull Requests to `main` triggers the CI/CD pipelin which pulls the latest code and restarts the service without any manual steps.

