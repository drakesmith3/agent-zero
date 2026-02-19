# Deployment Guide (Testing Mode, No Authentication)

This guide deploys AgentStation/Agent Zero for **testing only** with auth disabled.

## 0) Clone and run locally first (recommended)

Before any cloud deployment, validate locally from source:

```bash
git clone https://github.com/agent0ai/agent-zero.git
cd agent-zero
python run_ui.py
```

Open the URL printed in the console (commonly `http://127.0.0.1:5000` or configured port).

If you need a custom port:

```bash
WEB_UI_PORT=5005 python run_ui.py
```

This local-first check helps catch environment issues early and confirms your branch works before pushing to Cloud Run or another host.

## 1) Docker quick deploy (recommended)

```bash
docker pull agent0ai/agent-zero
mkdir -p ./agentstation-data/usr

docker run -d \
  --name agentstation-test \
  -p 50001:80 \
  -v "$(pwd)/agentstation-data/usr:/a0/usr" \
  agent0ai/agent-zero
```

Open UI: `http://localhost:50001`

### Keep auth disabled for testing
Do **not** set `AUTH_LOGIN` / `AUTH_PASSWORD` in `.env`.

## 2) Local dev run (backend + web UI)

```bash
python run_ui.py
```

Default URL is printed in console. Usually `http://127.0.0.1:80` or configured port.

## 3) Deploy backend + UI to Cloud Run (testing)

Build and push image, then:

```bash
gcloud run deploy agentstation-test \
  --image REGION-docker.pkg.dev/PROJECT/REPO/agentstation:latest \
  --platform managed \
  --allow-unauthenticated \
  --port 80 \
  --set-env-vars "AUTH_LOGIN=,AUTH_PASSWORD="
```

Then open the Cloud Run service URL.

## 4) Optional static WebUI-only hosting (debug only)
If you need to inspect frontend rendering only:

```bash
cd webui
python -m http.server 7860
```

Open: `http://127.0.0.1:7860/index.html`

> Note: static mode does not provide working backend APIs/websocket.

## 5) Post-deploy smoke checks
- Open dashboard and start a session
- Verify streaming output appears
- Open settings and save
- Open scheduler modal and create/edit a task
- Open projects modal and create/activate a project

## 6) Local-first pre-cloud checklist
- `python run_ui.py` starts without import/runtime errors
- UI loads and websocket connects
- Start at least one session and verify streaming
- File browser/editor opens and saves
- Scheduler add/edit flows work
- Only after this baseline passes, deploy the same commit hash to cloud
