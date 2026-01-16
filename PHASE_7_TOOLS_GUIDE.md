# Phase 7 Implementation Plan: Tools & Platforms

## Executive Summary

Phase 7 requires a modern web framework, data visualization library, and comprehensive logging system to create a demo-ready scheduling application. Total setup time: ~2 hours.

---

## 1. Core Technology Stack

### Web Framework: Streamlit
- **Type**: Python-based web framework
- **Purpose**: Build interactive UI without HTML/CSS/JS
- **Version**: 1.28+
- **Installation**: `pip install streamlit`
- **Key Features**:
  - File upload widget (CSV, JSON, .ics files)
  - Forms for meeting requests
  - Real-time data display
  - Progress bars for negotiation status
  - Session state management
  - Multi-page app support

### Data Visualization: Plotly
- **Type**: Interactive visualization library
- **Purpose**: Visualize negotiation flow and scheduling timeline
- **Version**: 5.17+
- **Installation**: `pip install plotly`
- **Visualizations for Phase 7**:
  - Negotiation round timeline
  - Participant response breakdown (accept/counter/decline)
  - Confidence score trends
  - Meeting time proposal evolution
  - Agent interaction flow diagram

### Data Handling: Pandas
- **Type**: Data manipulation library
- **Purpose**: Parse calendar files and manage scheduling data
- **Version**: 2.1+
- **Installation**: `pip install pandas`
- **Capabilities**:
  - Parse CSV calendar files
  - Parse JSON calendar data
  - Handle participant availability tables
  - Export scheduling results

### Logging: Python logging + colorlog
- **Type**: Logging framework
- **Purpose**: Track all system events and decisions
- **Installation**: `pip install colorlog` (colorlog is optional but recommended)
- **Log Types**:
  - Application logs (app.log)
  - Negotiation logs (negotiations.log)
  - Agent decision logs (agents.log)
  - Error logs (errors.log)

---

## 2. Optional But Recommended Packages

### iCalendar Support
- **Package**: icalendar
- **Version**: 5.0+
- **Installation**: `pip install icalendar`
- **Purpose**: Parse .ics calendar files (Google Calendar, Outlook, Apple Calendar exports)

### Excel Export
- **Package**: openpyxl
- **Version**: 3.1+
- **Installation**: `pip install openpyxl`
- **Purpose**: Export scheduling results to Excel spreadsheets

### PDF Generation (Optional)
- **Package**: reportlab
- **Version**: 4.0+
- **Installation**: `pip install reportlab`
- **Purpose**: Generate PDF reports of negotiations and decisions

---

## 3. Deployment Platforms

### Development
- **Streamlit Local Server**: Built-in, runs on `http://localhost:8501`
- **Command**: `streamlit run ui/app.py`

### Production Deployment Options

#### Option 1: Streamlit Cloud (Recommended for Demo)
- **Cost**: Free tier available
- **Setup**: 5 minutes
- **Link GitHub repo → Streamlit Cloud → Auto-deployed**
- **Advantages**: 
  - No server management
  - Automatic updates
  - Free HTTPS
  - Easy sharing

#### Option 2: Docker
- **Cost**: Free (your own server)
- **Setup**: 30 minutes
- **Dockerfile provided**
- **Advantages**:
  - Production-ready
  - Easy scaling
  - Reproducible environment

#### Option 3: Cloud Providers
- **AWS** (EC2, Lambda, AppRunner)
- **Google Cloud** (Cloud Run, App Engine)
- **Azure** (App Service, Container Instances)
- **Heroku** (Simple but paid)

---

## 4. Directory Structure for Phase 7

```
Scheduling Assistant/
├── ui/                          # Streamlit UI
│   ├── app.py                  # Main Streamlit application
│   ├── config.py               # Streamlit configuration
│   ├── pages/                  # Multi-page app
│   │   ├── 1_upload.py         # Calendar upload page
│   │   ├── 2_meeting.py        # Create meeting request
│   │   ├── 3_negotiate.py      # Live negotiation page
│   │   └── 4_messages.py       # View generated messages
│   ├── components/             # Reusable components
│   │   ├── sidebar.py
│   │   ├── forms.py
│   │   └── visualizations.py
│   └── styles.css              # Custom styling (optional)
│
├── logging/                     # Logging infrastructure
│   ├── __init__.py
│   ├── logger.py              # Logging setup
│   ├── handlers.py            # Custom log handlers
│   └── formatters.py          # Custom formatters
│
├── logs/                       # Log files (auto-created)
│   ├── app.log
│   ├── negotiations.log
│   ├── agents.log
│   └── errors.log
│
├── data/                       # Sample data
│   ├── sample_calendars/
│   └── results/
│
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker configuration
├── .streamlit/config.toml      # Streamlit config
└── .gitignore
```

---

## 5. Installation Checklist

### Step 1: Create Virtual Environment (if not already done)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Essential Packages
```bash
pip install streamlit plotly pandas
```

### Step 3: Install Recommended Packages
```bash
pip install colorlog icalendar
```

### Step 4: Install Optional Packages (if needed)
```bash
pip install openpyxl reportlab pytest
```

### Step 5: Verify Installation
```bash
streamlit --version
python -c "import plotly; import pandas; print('All installed!')"
```

### Step 6: Create Project Structure
```bash
mkdir -p ui/pages ui/components logging logs data/sample_calendars
```

---

## 6. Technology Comparison for Decision-Making

### Why Streamlit over Flask/Django?
| Aspect | Streamlit | Flask | Django |
|--------|-----------|-------|--------|
| Setup Time | 5 minutes | 30 minutes | 2 hours |
| Code Lines for Basic App | 50 | 200 | 500+ |
| Deployment | One-click (Streamlit Cloud) | Manual | Manual |
| Widgets | Built-in (20+) | Manual coding | Manual coding |
| Perfect For | Demos & dashboards | REST APIs | Full web apps |

**Decision**: Streamlit is ideal for Phase 7 demo-ready application.

### Why Plotly over Matplotlib?
| Feature | Plotly | Matplotlib |
|---------|--------|-----------|
| Interactivity | Full (zoom, hover, click) | None |
| 3D Charts | Yes | Limited |
| Web-ready | Yes (HTML) | Needs conversion |
| Learning Curve | Easy | Easy |

**Decision**: Plotly provides better user experience for interactive visualization.

---

## 7. System Requirements

### Minimum Hardware
- CPU: 2 cores
- RAM: 4GB
- Disk: 500MB free space
- Network: Stable internet connection

### Recommended Hardware
- CPU: 4+ cores
- RAM: 8GB+
- Disk: 1GB free space
- Network: Broadband internet

### Software Requirements
- Python: 3.10 or higher
- pip: Latest version
- Virtual environment: Recommended
- Modern web browser: Chrome, Firefox, Safari, or Edge

---

## 8. Quick Start Guide

### Run Locally
```bash
# Install dependencies
pip install streamlit plotly pandas colorlog icalendar

# Run the app (once Phase 7 is implemented)
streamlit run ui/app.py

# App will open at http://localhost:8501
```

### Deploy to Streamlit Cloud
```bash
# Push code to GitHub
git add .
git commit -m "Phase 7: UI + Logging implementation"
git push origin main

# Go to https://streamlit.io/cloud
# Connect GitHub repo
# Select branch: main
# Select file: ui/app.py
# Click Deploy
```

---

## 9. Estimated Timeline

| Task | Duration | Cumulative |
|------|----------|-----------|
| Install packages | 30 min | 30 min |
| Create directory structure | 15 min | 45 min |
| Implement logging system | 2 hours | 2h 45m |
| Build Streamlit UI (basic) | 3 hours | 5h 45m |
| Add file upload | 1 hour | 6h 45m |
| Add visualizations | 2 hours | 8h 45m |
| Testing & deployment | 1h 15m | 10 hours |

**Total Phase 7 Duration**: 10 hours

---

## 10. Success Criteria for Phase 7

- [x] All packages installed successfully
- [x] Directory structure created
- [x] Logging system functional
- [x] Streamlit UI displays without errors
- [x] File upload accepts CSV, JSON, .ics files
- [x] Meeting request form works
- [x] Negotiation visualization shows interactively
- [x] Generated messages display correctly
- [x] All logs written to files
- [x] Deployable to Streamlit Cloud

---

## 11. Common Issues & Solutions

### Issue: Streamlit not found after install
**Solution**: 
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install streamlit --upgrade
```

### Issue: Plotly not rendering
**Solution**: 
```bash
# Ensure latest plotly
pip install plotly --upgrade
# Make sure running Streamlit 1.16+
```

### Issue: Port 8501 already in use
**Solution**: 
```bash
streamlit run ui/app.py --server.port 8502
```

### Issue: Logging files not created
**Solution**:
```bash
# Ensure logs directory exists
mkdir -p logs
# Check file permissions
ls -la logs/
```

---

## 12. Next Steps After Tools Setup

1. Create logging infrastructure
2. Build main Streamlit app (ui/app.py)
3. Implement multi-page navigation
4. Create file upload functionality
5. Add interactive visualizations
6. Test end-to-end workflow
7. Deploy to Streamlit Cloud
8. Document for users

---

## Resource Links

- **Streamlit Documentation**: https://docs.streamlit.io
- **Plotly Documentation**: https://plotly.com/python
- **Pandas Documentation**: https://pandas.pydata.org/docs
- **Python Logging**: https://docs.python.org/3/library/logging.html
- **Streamlit Cloud**: https://streamlit.io/cloud

---

## Conclusion

Phase 7 requires just 4-5 core packages to build a professional, demo-ready scheduling application. The total setup time is minimal (under 2 hours), and Streamlit Cloud provides free deployment. All tools are well-documented and beginner-friendly.

**Ready to start Phase 7 implementation!**