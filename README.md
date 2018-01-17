# Laundry Management
This project web application was designed to help control and manage laundry clothes system for Kirirom Institute Of Technology

**Modules**:
  + Account profile, login and register
  + Clothes Management
  + QRCode
  + API
Functionality:
  + User can upload their cloth to their own timeline,
    with image, type
    
  + User can add their dirty clothes to their dirty bucket
  
  + Before their laundry schedule they can decide to take their cloth
    out from dirty bucket
    
  + When each dormitory number laundry schedule come, admin just confirm
    by select collect dirty cloth, so all dirty clothes will transfer to
    laundry.
  
  + Admin can scan QRcode of each cloth to remove it from laundry when done
  
  
  PURPOSE:
    To track id there losing clothes from laundry or messing with user clothes,
    
    
    
  ### Installation
  1 **Using virtualenv for project python interpreter** (__Optional__)
  ```bash
[ProjectRoot]> pip install virtualenv
```
  ```bash
[ProjectRoot]> virtualenv -p python3 env
```
  **See more on how to setup virtualenv** [Virtualenv](https://virtualenv.pypa.io/en/stable/ "virtualenv")

  2 **install python dependencies using pip**
  ```bash
pip install -r requirements.txt
````
  3 **Create .env file and copy sample from .env.example**
  ```bash
[ProjectRoot]> touch .env && cat .env.example >> .env
```
  4 **Migrate database**
  ```bash
[ProjectRoot]> python3 manage.py migrate
```

5 **Collect static files from apps into public folder**
  ```bash
[ProjectRoot]> python3 manage.py collectstatic
```

6 **Create super user**
  ```bash
[ProjectRoot]> python3 manage.py createsuperuser
```

7 **Run demo project**
  ```bash
[ProjectRoot]> python3 manage.py runserver
```

  
  
