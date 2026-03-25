# Distribution Guide - Two Approaches

## ⭐ RECOMMENDED APPROACH: Folder Distribution

For a professional, reliable distribution, use the folder-based approach:

### What Users Get:
- A folder containing:
  - `RUN_APP.bat` - Double-click to launch (or custom shortcut)
  - `app.py`, `doe_model.py` - Your application files
  - `requirements.txt` - List of dependencies
  - README.md, LICENSE.txt - Documentation

### How to Distribute:
1. Create a folder: `DOE_Simulator_v1.0`
2. Copy these files into it:
   - `RUN_APP.bat`
   - `app.py`
   - `doe_model.py`
   - `requirements.txt`
   - `README.md`
   - `LICENSE.txt`
3. Zip the folder
4. Share the .zip file

### User Installation:
1. Unzip to any location
2. Double-click `RUN_APP.bat`
3. Application launches (Python must be installed)

### Advantages:
✅ Works perfectly - no PyInstaller issues
✅ Easy to update - just replace Python files
✅ Professional - matches industry standard
✅ Lightweight - just your code, not bundled Python
✅ Cross-platform ready - batch files work on Windows

---

## Alternative: Single EXE (Advanced)

If you need a true single-file executable:

### Challenges:
- PyInstaller + Streamlit are difficult to integrate
- Larger file size (400+ MB)
- More complex to update
- Platform-specific

### If Still Needed:
You would need to use commercial tools like:
- **PyApp** (advanced)
- **cx_Freeze** (alternative bundler)
- **Nuitka** (Python compiler)
- Or build your own installer

---

## RECOMMENDED DISTRIBUTION STEPS

### Step 1: Prepare Distribution Folder
```bash
mkdir DOE_Simulator_v1.0
cd DOE_Simulator_v1.0
copy ..\RUN_APP.bat .
copy ..\app.py .
copy ..\doe_model.py .
copy ..\requirements.txt .
copy ..\README.md .
copy ..\LICENSE.txt .
```

### Step 2: Test on Fresh Computer
1. Unzip to a folder
2. Double-click RUN_APP.bat
3. Verify it works

### Step 3: Create Installer (Optional)
Use Inno Setup with this configuration:

```ini
[Files]
Source: "DOE_Simulator_v1.0\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\DOE Simulator"; Filename: "{app}\RUN_APP.bat"
Name: "{commondesktop}\DOE Simulator"; Filename: "{app}\RUN_APP.bat"
```

### Step 4: Distribution
- Users can:
  - Run `DOE_Simulator_v1.0.zip` directly
  - Or install via Inno Setup installer

---

## System Requirements for End Users

### Minimum:
- Windows 10 or later
- Python 3.8+ installed (from https://www.python.org/)

### Optional (Better):
- Create a portable Python environment:
  ```bash
  python -m venv env
  .\env\Scripts\activate
  pip install -r requirements.txt
  ```

---

## Why This Approach Is Better

| Feature | Folder Dist. | Single .EXE |
|---------|-------------|-----------|
| Development | ✅ Easy | ❌ Complex |
| Updates | ✅ Simple | ❌ Rebuild needed |
| File Size | ✅ Small | ❌ 400+ MB |
| Debugging | ✅ Easy | ❌ Hard |
| Compatibility | ✅ Reliable | ❌ PyInstaller issues |
| Professional | ✅ Industry standard | ❓ Less common |

---

## Quick Test

To test your distribution works:

1. Double-click `RUN_APP.bat`
2. Command window appears
3. Browser opens to `http://localhost:8501`
4. Application loads

If this works, your distribution is ready!
