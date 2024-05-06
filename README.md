# Vendor_Management_System_Server

    ---------------Steps to Run this Django App(for Windows)---------------

1. Download this git repository.
2. Unzip the repository  where you want to keep this project.
3. Go insite the parent folder "Vendor_Management_System_Server-main" using command prompt/any other terminal.
4. Here we have to create a new environment for this django app.
5. Run the command "python -m venv django_env" or "virtualenv django_env" -- Here django_env is the name of environment.
6. Now run "django_env/Scripts/activate" -- This command will activate your django environment.
7. Go to "Vendor_Management_System_Server-main > Core>" 
8. Run "pip install -r requirements.txt" -- This will install all the required packages mentioned
     in the requirements.txt file.
9. Run "python manage.py makemigrations" and then  "python manage.py migrate"
10. Now run "python manage.py runserver"