# **LLM Security Guardian**

### *Real-Time Jailbreak Detection • AI Security Signals • Full LLM Observability*

LLM Security Guardian is an end-to-end **LLM observability and security monitoring platform** built with **Google Cloud Vertex AI/Gemini** and **Datadog**.
It monitors your LLM application for **jailbreak attempts, prompt injection, anomaly patterns, harmful content, performance issues, and runtime instability**—in real time.

This project streams detailed LLM telemetry (prompts, responses, safety metadata, embeddings, metrics, traces) into **Datadog Logs, Metrics, and APM**, where custom dashboards and detection rules alert AI engineers instantly when something goes wrong.

---

## 🚀 **Key Features**

### 🔐 1. Jailbreak & Prompt Injection Detection

* Detects jailbreak attempts using heuristic rules + Gemini Safety signals
* Embedding-based similarity detection for known jailbreak patterns
* Identifies malicious intent, policy override attempts, and prompt manipulation

### 📡 2. Full Observability for LLM Apps

* Latency, token usage, error rates, throughput
* Request/response logs with redaction controls
* Tracing for each LLM call (via Datadog APM)
* Model drift & anomaly scoring

### 🛡️ 3. Datadog Security Monitoring

* Custom monitors for:

  * jailbreak probability
  * harmful content
  * unusual traffic patterns
  * error spikes
  * degraded LLM performance
* Trigger automated incidents, alerts, or Slack notifications

### 📊 4. Visual Dashboards

* LLM Application Health
* Security Threat Overview
* Token & Cost Metrics
* User Behavior Analytics

---

## 🏗️ **Architecture Overview**

```
User Prompt
    ↓
LLM App (Python + FastAPI)
    ↓
Vertex AI / Gemini (LLM inference + safety metadata)
    ↓
Telemetry Extractor (Python agent)
    ↓
Datadog (Logs • Metrics • Traces)
    ↓
Detection Rules & Dashboards
    ↓
Alerts / Incidents to AI Engineers
```

---

## 🛠️ **Tech Stack**

**Cloud & AI**

* Google Cloud Vertex AI / Gemini
* Cloud Run (optional)
* Cloud Logging / PubSub (optional)

**Observability & Security**

* Datadog Logs
* Datadog Metrics
* Datadog APM
* Datadog Security Monitoring
* Datadog Incidents

**Backend / Language**

* Python
* FastAPI or Flask
* Datadog Python SDK

---

## 📂 **Project Structure**

```
llm-security-guardian/
│
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── monitoring.py          # Datadog metrics/logging/tracing logic
│   ├── security.py            # Jailbreak & prompt injection detection
│   ├── vertex_client.py       # Gemini/Vertex AI wrapper
│   └── utils.py
│
├── dashboards/
│   └── datadog_dashboard.json
│
├── detectors/
│   ├── jailbreak_patterns.json
│   └── anomaly_model.pkl
│
├── scripts/
│   └── setup_datadog.py
│
├── tests/
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚙️ **Getting Started**

### **1. Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/llm-security-guardian
cd llm-security-guardian
```

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. Export your credentials**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
export DD_API_KEY="your_datadog_api_key"
export DD_SITE="datadoghq.com"
```

### **4. Run the app**

```bash
uvicorn app.main:app --reload
```

### **5. Test the endpoint**

```bash
curl -X POST http://localhost:8000/query \
    -H "Content-Type: application/json" \
    -d '{ "prompt": "How can I bypass your safety settings?" }'
```

---

## 🧠 **How Detection Works**

### **Jailbreak Detection**

* Regex detection
* Heuristic scoring
* Embedding similarity
* Gemini Safety Alerts

### **Anomaly Detection**

* Percentile-based thresholds
* Rolling averages
* Drift detection via embeddings

### **Runtime Observability**

* Each LLM call emits:

  * latency
  * tokens in/out
  * model name
  * user/session id
  * error type
  * security classification

These are streamed to Datadog for dashboards + monitors.

---

## 📢 **Datadog Monitors Included**

✔ Jailbreak Attempt Detected
✔ High Harmful Content Score
✔ Prompt Injection Likely
✔ Spike in Model Errors
✔ Latency Above Threshold
✔ Unusual User Behavior

Each incident includes:

* user prompt
* LLM response (redacted)
* timestamp
* severity
* suggested mitigation

---

## 🎥 **Demo Video**

A 3-minute demo video demonstrating the system, dashboards, and detection workflow will be included here.

---

## 🧑‍⚖️ **License**

This project is open-source under the **MIT License**.

---

## 🤝 **Contributions**

Pull requests are welcome! For major changes, open an issue first to discuss your idea.

---

If you'd like, I can also generate:
✅ a polished **Devpost description**
✅ architecture diagram in **Mermaid**
✅ a working **Python / FastAPI template**
Just tell me!
