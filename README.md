# Order State Machine - Full Stack Challenge

This project implements a distributed state machine for order processing.

## 🏗️ Architecture
- **Backend**: Python 3.11, AWS Lambda, DynamoDB, AWS PowerTools (Hexagonal/3-Layer Architecture).
- **Frontend**: Astro 5.0, React, Tailwind CSS, Mermaid.js.
- **Infrastructure**: AWS SAM (Serverless Application Model).

## 🚀 Live Demo
- **Frontend**: [Link to Vercel/Netlify if deployed]
- **API Endpoint**: `https://j7atkisock.execute-api.us-east-1.amazonaws.com/Prod`

## 🛠️ Setup & Running

### Backend
1. `cd backend`
2. `sam build`
3. `sam local start-api --env-vars env.json` (For local testing)

### Frontend
1. `cd frontend`
2. `pnpm install`
3. `pnpm dev`