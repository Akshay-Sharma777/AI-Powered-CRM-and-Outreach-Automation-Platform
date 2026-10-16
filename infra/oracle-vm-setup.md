# Oracle Cloud Always Free VM Setup Guide

This guide walks through configuring an Oracle Cloud Always Free VM instance (Ubuntu 22.04 LTS / 24.04 LTS) for running FastAPI, n8n, Playwright workers, and Caddy.

---

## 1. Instance Creation
- **Shape**: `VM.Standard.E2.1.Micro` (or `VM.Standard.A1.Flex` with up to 4 OCPUs and 24 GB RAM if available in your region).
- **OS**: Ubuntu 22.04 / 24.04 Minimal LTS.
- **Boot Volume**: 50 GB.

---

## 2. Security List & Ingress Rules
Open only the following ports in the Oracle Cloud VCN Security List:
- **Port 22**: SSH (Restricted to team admin IP where possible)
- **Port 80**: HTTP (Caddy ACME challenge & HTTPS redirect)
- **Port 443**: HTTPS (Public secured API endpoints)

*All other ports (5678 for n8n, 8000 for FastAPI, 5432 for Postgres) remain internal to Docker networks only.*

---

## 3. Host System Setup & Docker Installation
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git ufw ca-certificates

# Configure host firewall (UFW)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

---

## 4. Deploying the Monorepo
```bash
git clone https://github.com/Akshay-Sharma777/AI-Powered-CRM-and-Outreach-Automation-Platform.git
cd AI-Powered-CRM-and-Outreach-Automation-Platform

# Copy and edit production environment file
cp .env.example .env
nano .env

# Start services via Docker Compose
docker compose up -d --build
```

Verify service status:
```bash
docker compose ps
curl http://localhost:8000/api/v1/health
```
