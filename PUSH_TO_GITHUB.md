# Push this project to GitHub

Your project is committed locally. Follow these steps to push it to GitHub.

## 1. Create a new repository on GitHub

1. Go to **https://github.com/new**
2. **Repository name:** `AI_FORECASTING` (or any name you like)
3. **Description (optional):** AI Forecasting & Planning Agent – demand, workforce, budget
4. Choose **Public**
5. Do **not** check "Add a README" or .gitignore (you already have them)
6. Click **Create repository**

## 2. Add the remote and push

Open PowerShell in this folder and run (replace `YOUR_USERNAME` with your GitHub username if different):

```powershell
cd C:\Users\GANESH\Desktop\AI_FORECASTING
git remote add origin https://github.com/YOUR_USERNAME/AI_FORECASTING.git
git branch -M main
git push -u origin main
```

If you use **SSH** instead of HTTPS:

```powershell
git remote add origin git@github.com:YOUR_USERNAME/AI_FORECASTING.git
git push -u origin main
```

## 3. If the remote was already added

If you already ran `git remote add origin ...`, just push:

```powershell
git push -u origin main
```

---

After pushing, you can deploy the **Streamlit** app at [share.streamlit.io](https://share.streamlit.io) or the **Docker** app on [Render](https://render.com) by connecting this GitHub repo.
