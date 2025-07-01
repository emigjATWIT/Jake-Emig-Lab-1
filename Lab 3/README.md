# Galactic Passport Generator

## Introduction

Welcome to the **Galactic Passport Generator**, a Node.js + Express web service that simulates an intergalactic immigration and visa control system. This project is designed to demonstrate how to create a structured and interactive Express-based web service using various types of routes including HTML responses, query parameters, headers, and body inputs.

---

## Project Description

The Galactic Passport Generator allows fictional users from across the galaxy to:
- View embassy and planet information
- Apply for and view passports
- Greet interplanetary travelers
- Submit and check visa applications
- Search for alien citizens

This project features:
- 10 total routes
- At least 5 HTML responses
- Routes with query, header, and body parameters

---

## Project Design

The project is built with the following structure:

- `server.js`: Main server script that sets up all routes and launches the server
- Express.js: Used to handle routing and middleware
- JSON responses: For APIs like visa application and passport creation
- HTML responses: For web-friendly output like greetings and embassy pages

### Routes Overview

| Route | Type | Description |
|-------|------|-------------|
| `/` | HTML | Welcome message |
| `/planets` | HTML | Lists planets with embassies |
| `/embassy?planet=Mars` | HTML + Query | Displays selected planet embassy |
| `/passport/create` | POST + Body | Create a new passport |
| `/passport/view?id=123` | HTML + Query | View a passport by ID |
| `/citizen/search?species=Zorgon` | HTML + Query | Search citizens by species |
| `/greet` | HTML + Header | Custom greeting using `X-Origin-Planet` header |
| `/immigration-check?passport_id=abc123` | JSON + Query | Checks immigration status |
| `/visa/apply?name=Zorg&destination=Venus` | JSON + Query | Visa application submission |
| `/visa/status?applicant_id=xyz456` | JSON + Query | Check visa application status |

---

## How to Run This Project

### 1. Prerequisites
- Install [Node.js](https://nodejs.org/)

### 2. Setup Instructions

```bash
# Create project folder
mkdir galactic-passport
cd galactic-passport

# Initialize Node.js project
npm init -y

# Install Express
npm install express

# Place the server.js file in this directory
```

### 3. Run the Server

```bash
node server.js
```

You should see:
```
Galactic Passport Service running on http://localhost:3000
```

---

## How to Test the Routes

### Test in Browser (HTML Routes):
- `http://localhost:3000/`
- `http://localhost:3000/planets`
- `http://localhost:3000/embassy?planet=Mars`
- `http://localhost:3000/passport/view?id=123`
- `http://localhost:3000/citizen/search?species=Zorgon`

### Test in Terminal:

#### Header Test:
```bash
curl -H "X-Origin-Planet: Saturn" http://localhost:3000/greet
```
---
