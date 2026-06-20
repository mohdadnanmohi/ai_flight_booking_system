import os
import shutil
import zipfile

def package_submission():
    base_dir = os.getcwd()
    sub_folder_name = "Mohammed_Adnan_Mohiuddin_AI-Enhanced_Flight_Booking_System"
    sub_dir = os.path.join(base_dir, sub_folder_name)
    
    print("Creating structure...")
    if os.path.exists(sub_dir):
        shutil.rmtree(sub_dir)
        
    os.makedirs(os.path.join(sub_dir, "Frontend"))
    os.makedirs(os.path.join(sub_dir, "Backend"))
    os.makedirs(os.path.join(sub_dir, "ML"))
    os.makedirs(os.path.join(sub_dir, "Documentation"))
    
    print("Copying Frontend...")
    shutil.copytree(os.path.join(base_dir, "templates"), os.path.join(sub_dir, "Frontend", "templates"))
    shutil.copytree(os.path.join(base_dir, "static"), os.path.join(sub_dir, "Frontend", "static"))
    
    print("Copying Backend...")
    for f in ["app.py", "config.py", "models.py", "requirements.txt", "vercel.json"]:
        if os.path.exists(os.path.join(base_dir, f)):
            shutil.copy2(os.path.join(base_dir, f), os.path.join(sub_dir, "Backend", f))
    if os.path.exists(os.path.join(base_dir, "db_scripts")):
        shutil.copytree(os.path.join(base_dir, "db_scripts"), os.path.join(sub_dir, "Backend", "db_scripts"))
        
    print("Copying ML...")
    for f in ["dataset.csv", "train_model.py"]:
        if os.path.exists(os.path.join(base_dir, f)):
            shutil.copy2(os.path.join(base_dir, f), os.path.join(sub_dir, "ML", f))
    if os.path.exists(os.path.join(base_dir, "ml_models")):
        shutil.copytree(os.path.join(base_dir, "ml_models"), os.path.join(sub_dir, "ML", "ml_models"))
        
    print("Copying Documentation...")
    docs = [
        "project_report.md", 
        "ppt_presentation.md", 
        "api_documentation.md", 
        "viva_questions.md", 
        "demo_script.md", 
        "evaluation_highlights.md"
    ]
    brain_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "brain", "349ca024-a206-4798-aa16-c62992253af3"))
    for doc in docs:
        src = os.path.join(brain_dir, doc)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(sub_dir, "Documentation", doc))
            
    print("Copying README...")
    if os.path.exists(os.path.join(base_dir, "README.md")):
        shutil.copy2(os.path.join(base_dir, "README.md"), os.path.join(sub_dir, "README.md"))
        
    print("Modifying Backend Paths...")
    app_path = os.path.join(sub_dir, "Backend", "app.py")
    with open(app_path, "r") as f:
        content = f.read()
    
    # Update Flask to point to Frontend folder
    content = content.replace("app = Flask(__name__)", "app = Flask(__name__, template_folder='../Frontend/templates', static_folder='../Frontend/static')")
    
    # Update ML paths to point to ML folder
    content = content.replace("'ml_models/rf_model.pkl'", "'../ML/ml_models/rf_model.pkl'")
    content = content.replace("'ml_models/label_encoders.pkl'", "'../ML/ml_models/label_encoders.pkl'")
    
    with open(app_path, "w") as f:
        f.write(content)
        
    print("Creating ZIP file...")
    zip_name = f"{sub_folder_name}.zip"
    if os.path.exists(zip_name):
        os.remove(zip_name)
        
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(sub_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)
                
    print(f"Successfully packaged {zip_name}!")

if __name__ == '__main__':
    package_submission()
