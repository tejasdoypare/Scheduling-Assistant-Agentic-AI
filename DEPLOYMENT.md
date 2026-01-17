# Deployment Guide for Streamlit Cloud

## Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Google AI API Key from https://ai.google.dev/

---

## Step 1: Prepare Your Repository

### 1.1 Ensure .gitignore is Updated
Make sure `.streamlit/secrets.toml` is in `.gitignore` to prevent exposing secrets.

### 1.2 Commit and Push All Changes
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 1.3 Verify Required Files Exist
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version (3.11)
- ✅ `ui/app.py` - Main application file
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.gitignore` - Excludes secrets

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign In to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click **Sign in**
3. Sign in with your GitHub account

### 2.2 Create New App
1. Click **"New app"** button
2. Select your repository:
   - **Repository**: `your-username/scheduling-assistant`
   - **Branch**: `main`
   - **Main file path**: `ui/app.py`
3. Click **"Advanced settings"** (optional but recommended)

### 2.3 Configure Advanced Settings
**Python version**: 3.11 (should auto-detect from runtime.txt)

**Secrets** (CRITICAL - Click "Secrets" in sidebar after deployment):
```toml
# Add this in the Secrets section
GOOGLE_API_KEY = "your-actual-api-key-here"
```

### 2.4 Deploy
1. Click **"Deploy!"**
2. Wait 2-5 minutes for initial build
3. Monitor logs for any errors

---

## Step 3: Configure Secrets (IMPORTANT!)

After deployment, you MUST add secrets:

1. Go to your app on Streamlit Cloud
2. Click **"Settings"** (⚙️ icon) → **"Secrets"**
3. Add your secrets in TOML format:

```toml
# Streamlit Cloud Secrets
GOOGLE_API_KEY = "your-actual-google-gemini-api-key"
```

4. Click **"Save"**
5. App will automatically restart with secrets

---

## Step 4: Verify Deployment

### 4.1 Test Core Features
- [ ] App loads without errors
- [ ] Can upload calendar files
- [ ] Can create meeting requests
- [ ] Negotiation runs successfully
- [ ] Visualizations display correctly
- [ ] Messages generate properly

### 4.2 Check Logs
If something fails:
1. Click **"Manage app"** → **"Logs"**
2. Look for error messages
3. Common issues:
   - Missing dependencies → Update requirements.txt
   - Import errors → Check file paths
   - API errors → Verify secrets configured

---

## Step 5: Customize Your App

### 5.1 Custom URL (Optional)
1. Go to app settings
2. Click **"General"**
3. Change app URL (e.g., `ai-scheduling-assistant`)

### 5.2 Custom Subdomain
Streamlit provides URLs like:
`https://your-app-name-username.streamlit.app`

---

## Step 6: Share Your App

Once deployed, share your app:
- **Public URL**: `https://your-app-name.streamlit.app`
- Add to resume/portfolio
- Share on LinkedIn
- Include in GitHub README

---

## Troubleshooting

### Error: "No module named 'X'"
**Solution**: Add missing package to `requirements.txt`

### Error: "FileNotFoundError: [Errno 2] No such file or directory"
**Solution**: Check file paths are relative to project root

### Error: API Key not found
**Solution**: 
1. Verify secrets configured in Streamlit Cloud
2. Check secret name matches: `GOOGLE_API_KEY`
3. Restart app after adding secrets

### Error: "Port already in use"
**Solution**: This shouldn't happen on Streamlit Cloud (only local)

### Build Failed
**Solution**:
1. Check logs for specific error
2. Verify Python version in runtime.txt
3. Ensure all dependencies in requirements.txt
4. Test locally first: `streamlit run ui/app.py`

### Secrets Not Loading
**Solution**:
```python
# In your code, ensure you're accessing secrets correctly:
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API key not configured in Streamlit Cloud secrets")
```

---

## Local Testing Before Deployment

Always test locally before deploying:

```bash
# 1. Create .streamlit/secrets.toml with your API key
# 2. Run the app
streamlit run ui/app.py

# 3. Test all features
# 4. If everything works, deploy!
```

---

## Updating Deployed App

Any push to your GitHub repository automatically redeploys:

```bash
git add .
git commit -m "Update feature X"
git push origin main
# Streamlit Cloud will auto-detect and redeploy
```

---

## Monitoring Your App

### View Analytics
Streamlit Cloud provides:
- Number of visitors
- Resource usage
- Error rates

Access via: **App → Analytics**

### Check Logs
Real-time logs available at: **App → Logs**

---

## Security Best Practices

1. ✅ Never commit secrets to Git
2. ✅ Use Streamlit secrets for production
3. ✅ Use environment variables for local development
4. ✅ Rotate API keys if accidentally exposed
5. ✅ Monitor API usage quotas
6. ✅ Enable XSRF protection in config.toml

---

## Cost Considerations

**Streamlit Cloud Free Tier**:
- 1 app (can have multiple, but 1 at a time)
- 1 GB resources
- Public apps only
- Auto-sleep after inactivity

**Paid Tiers** (if needed):
- More apps
- Private apps
- More resources
- Custom domains

---

## Next Steps After Deployment

1. ✅ Test all features in production
2. ✅ Add URL to README
3. ✅ Update resume/portfolio
4. ✅ Share on social media
5. ✅ Monitor for errors
6. ✅ Gather user feedback

---

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: Report bugs in your repo

---

## Quick Reference: Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] secrets.toml in .gitignore
- [ ] requirements.txt complete
- [ ] runtime.txt with Python version
- [ ] Tested locally
- [ ] Streamlit Cloud account created
- [ ] App deployed
- [ ] Secrets configured in Streamlit Cloud
- [ ] Features tested in production
- [ ] URL shared in README
- [ ] Monitoring enabled

**Status**: Ready to deploy! 🚀
