# eshop_project

## [preview]

![فروشگاه تاپ لرن _ صفحه اصلی - Google Chrome 6_9_2024 5_09_36 PM](https://github.com/mehdi-shoqeyb/eshop_project/assets/168349368/4f562750-0a58-4592-9bf4-662b3bd4b341)

![_-GoogleChrome2024-06-0917-02-00-ezgif com-video-to-gif-converter](https://github.com/mehdi-shoqeyb/eshop_project/assets/168349368/18ffd468-0dee-4c04-ba0f-62ac18d22e06)

## Running the Project Locally

0. First, clone the repository to your local machine:
```bash
https://github.com/mehdi-shoqeyb/eshop_project.git
cd eshop_project
```

1. Ideally, create a [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) and install the projects dependencies:
```bash
python3 -m venv env
source env/bin/activate
```

2. Install requirements
```bash
pip install -r requirements.txt
```

3. Init database and runserver
```bash
./manage.py migrate
./manage.py runserver
```
