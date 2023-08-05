# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hybrid_django_react']

package_data = \
{'': ['*'],
 'hybrid_django_react': ['assets/*',
                         'assets/.vscode/*',
                         'assets/frontend/*',
                         'assets/frontend/components/forms/*',
                         'assets/frontend/components/forms/Radio/*',
                         'assets/frontend/components/forms/Select/*',
                         'assets/frontend/components/forms/TextField/*',
                         'assets/frontend/components/layout/*',
                         'assets/frontend/components/layout/navigation/NavBar/*',
                         'assets/frontend/services/*',
                         'assets/frontend/services/LocalStorage/*',
                         'assets/frontend/store/*',
                         'assets/frontend/utils/constants/*',
                         'assets/frontend/utils/helpers/*',
                         'assets/frontend/views/Login/LoginForm/*',
                         'assets/frontend/views/Login/LoginPage/*',
                         'assets/locale/*',
                         'assets/static/*',
                         'assets/templates/*']}

entry_points = \
{'console_scripts': ['create-django-react-app = hybrid_django_react.run:main']}

setup_kwargs = {
    'name': 'hybrid-django-react',
    'version': '0.2.2',
    'description': 'Django starter project template. Dockerized Django serving a static React app',
    'long_description': "## Starter project template\n# 🤠⚛️ Dockerized hybrid Django React app \nStarter project template using Docker to build a Django app that serves React apps statically (as JavaScript files)\n\n## Tech stack\n  - Django (with Rest framework, PostgreSQL, SMTP gmail backend, whitenoise, etc.)\n  - React (bundled with webpack and transpiled with babel)\n  - Docker\n  - Deployment to Heroku\n\n## Prerequisites\n  - Docker\n  - pip, poetry, pyenv or a similar tool to access [pypi](https://pypi.org/)\n\n## Installation\nInstall with the following command\n```\npip install hybrid-django-react\n```\n\n## Usage\nRun the scripts with the following command:\n```\ncreate-django-react-app\n```\n\nYou will be prompted for some information like project name, email, etc. This data is needed to change the configuration files accordingly\n\nAfter the script has run, you don't need this tool anymore 😀\n\nSimply start the docker container to start working:\n```\ndocker-compose up -d\n```\n\nYou can then work as usual on your Django project.\n\nThe entry point of the React render can be edited from the file `frontend/index.js`\n\n## Debugging with Docker and VSCode\n\nSupport for debugging remotely with VSCode is supported out-of-the-box.\n\nTo debug with Docker:\n\n1. Run your Docker containers as usual: `docker-compose up -d --build`\n\n3. Start the debug session from VS Code for the `[django:docker] runserver` configuration (either from the Debugger menu or with `F5`)\n\n   - Logs will redirect to your integrated terminal as well.\n\n4. Set some breakpoints in functions or methods executed when needed. Usually it's Model methods or View functions\n\n## Adding external libraries\n\nIt's better to install external libraries from from Docker directly\n\n### Python libraries:\n   - Production libraries\n   ```\n   docker-compose exec web poetry add [pip_package]\n   ```\n   - Development libraries\n   ```\n   docker-compose exec web poetry add [pip_package] --dev\n   ```\n### JavaScript libraries:\n   - Production libraries\n   ```\n   docker-compose exec web npm install [npm_package]\n   ```\n   - Development libraries\n   ```\n   docker-compose exec web npm install -D [npm_package]\n   ```\n\n## Deploy to Heroku\n### First setup\n1. [Create an account](https://www.heroku.com) and [install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)  \n2. Create a new app on Heroku\n   ```\n   heroku create\n   ```\n   Your app will get a randomly generated name, like _lazy-beyond-52146_. Let's call this name _[APP_NAME]_\n3. Add environment variables that Django needs to read:\n   1. DJANGO_ENVIRONMENT:\n      ```\n      heroku config:set DJANGO_ENVIRONMENT=production\n      ```\n   2. DJANGO_SECRET_KEY:\n      You can create a safe secret key [using this site](https://djecrety.ir/)\n      ```\n      heroku config:set DJANGO_SECRET_KEY=[secret_key]\n      ```\n   3. DJANGO_DEBUG:\n      ```\n      heroku config:set DJANGO_DEBUG=False\n      ```\n4. Set the stack to Docker containers using the app's name\n   ```\n   heroku stack:setcontainer -a [APP_NAME]\n   ```\n5. Create a managed postgresql database on Heroku\n   ```\n   heroku addons:create heroku-postgresql:hobby-dev -a [APP_NAME]\n   ```\n6. Create a heroku remote repository and push changes to it\n   ```\n   heroku git:remote -a [APP_NAME]\n   git push heroku main\n   ```\n7. Migrate Database and create superuser\n   ```\n   heroku run python manage.py migrate\n   heroku run python manage.py createsuperuser\n   ```\n8. After deployment, check that the site's [security audit shows no warnings](https://djcheckup.com/)\n\n### Consecutive deployments to production\nDeploy by pushing to Heroku git repository:\n```\ngit push heroku main\n```\n",
    'author': 'gmso',
    'author_email': 'german.mene@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gmso/hybrid-django-react',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
