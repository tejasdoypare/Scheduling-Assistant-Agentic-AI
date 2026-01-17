# 🚨 URGENT: Security Fix Required

## ⚠️ CRITICAL SECURITY ISSUE DETECTED

Your API key was found hardcoded in the source code at:
- **File**: `ui/app.py`
- **Line**: 31
- **Exposed Key**: `AIzaSyAz4mGir6Uh2fC090GSo1RpCZhZ7QJMrhY`

---

## 🔥 Immediate Actions Required (Do This NOW!)

### Step 1: Rotate Your API Key (5 minutes)

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikey
2. **Delete the exposed key**: `AIzaSyAz4mGir6Uh2fC090GSo1RpCZhZ7QJMrhY`
3. **Generate a new API key**
4. **Copy the new key** (you'll need it in Step 3)

---

### Step 2: Update Your Local Code (ALREADY DONE ✅)

The file `ui/app.py` has been updated to use secure secret management.

**New code uses**:
- Streamlit secrets (for Streamlit Cloud)
- Environment variables (for local development)
- No hardcoded keys ✅

---

### Step 3: Configure Your Local Secrets (2 minutes)

**Option A: Using Streamlit Secrets (Recommended)**

1. Open `.streamlit/secrets.toml`
2. Replace the placeholder with your NEW API key:
```toml
GOOGLE_API_KEY = "your-NEW-api-key-here"
```

**Option B: Using Environment Variables**

Windows PowerShell:
```powershell
$env:GOOGLE_API_KEY="your-NEW-api-key-here"
streamlit run ui/app.py
```

Or create a `.env` file:
```bash
GOOGLE_API_KEY=your-NEW-api-key-here
```

---

### Step 4: Clean Git History (CRITICAL if already pushed)

If you've already pushed the exposed key to GitHub, you MUST remove it from history:

#### Option A: Using BFG Repo-Cleaner (Easier)

1. **Download BFG**: https://rtyley.github.io/bfg-repo-cleaner/
2. **Create backup**:
   ```powershell
   cd "E:\Hackathon\Scheduling Assistant"
   git clone --mirror . ../scheduling-assistant-backup.git
   ```
3. **Run BFG** (replace with actual key):
   ```powershell
   java -jar bfg.jar --replace-text passwords.txt ../scheduling-assistant-backup.git
   ```
4. **Force push**:
   ```powershell
   cd ../scheduling-assistant-backup.git
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```

#### Option B: Using git filter-branch (Manual)

```powershell
# Backup first!
git clone . ../backup

# Remove the exposed key from all commits
git filter-branch --force --index-filter `
  "git rm --cached --ignore-unmatch ui/app.py || true" `
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: This rewrites history)
git push origin --force --all
```

#### Option C: Simplest - Delete and Recreate Repository

If this is a new project with minimal history:

1. **Delete GitHub repository**
2. **Remove .git folder locally**: `Remove-Item -Recurse -Force .git`
3. **Re-initialize**: 
   ```powershell
   git init
   git add .
   git commit -m "Initial commit with secure configuration"
   ```
4. **Create new GitHub repo and push**

---

### Step 5: Verify Security (2 minutes)

Run these checks:

```powershell
# 1. Check no secrets in code
Select-String -Path "ui\*.py" -Pattern "AIzaSy"
# Should return NO results

# 2. Check .gitignore includes secrets
Get-Content .gitignore | Select-String "secrets.toml"
# Should show: .streamlit/secrets.toml

# 3. Verify secrets file is ignored
git status
# Should NOT show .streamlit/secrets.toml
```

---

## ✅ Verification Checklist

Before proceeding, verify:

- [ ] Old API key deleted from Google AI Studio
- [ ] New API key generated
- [ ] New key added to `.streamlit/secrets.toml`
- [ ] `.streamlit/secrets.toml` in `.gitignore`
- [ ] No hardcoded keys in code
- [ ] Git history cleaned (if key was pushed)
- [ ] App tested locally with new key
- [ ] Ready to deploy to Streamlit Cloud

---

## 🔐 For Streamlit Cloud Deployment

When you deploy to Streamlit Cloud:

1. **Go to your app** → Settings → Secrets
2. **Add your NEW API key**:
```toml
GOOGLE_API_KEY = "your-NEW-api-key-here"
```
3. **Save** → App will restart automatically

**NEVER** commit secrets.toml to Git!

---

## 🛡️ Prevention: Best Practices

### Always Use This Pattern:

```python
# ✅ CORRECT - Use secrets/env vars
import streamlit as st
import os

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY", "")

if not api_key:
    st.error("Please configure your API key")
```

### Never Do This:

```python
# ❌ WRONG - Hardcoded key
api_key = "AIzaSyAz4mGir6Uh2fC090GSo1RpCZhZ7QJMrhY"

# ❌ WRONG - Default value is real key
api_key = os.getenv("API_KEY", "AIzaSy...")
```

---

## 📞 What If Key Was Already Exposed?

If your key was public for any time:

1. **Assume it's compromised** - Rotate immediately
2. **Check API usage** in Google Cloud Console
3. **Set up usage alerts** to detect abuse
4. **Monitor your quotas** for unexpected spikes
5. **Consider restricting API key** (by IP, referrer, etc.)

---

## 🚀 You're Now Secure!

Once completed:
- ✅ API key secure
- ✅ No secrets in code
- ✅ Ready for public GitHub
- ✅ Ready for Streamlit Cloud deployment

**Next**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) for Streamlit Cloud setup.

---

## Questions?

- **Streamlit Secrets**: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
- **Google AI Security**: https://ai.google.dev/gemini-api/docs/api-key
- **Git History Cleanup**: https://rtyley.github.io/bfg-repo-cleaner/

---

**Status**: Security fix implemented. Please complete Steps 1-5 above!
