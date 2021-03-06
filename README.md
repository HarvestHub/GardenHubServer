![GardenHub Promo Banner](https://raw.githubusercontent.com/HarvestHub/GardenHub/master/gardenhub-promo.png)

[![Build Status](https://travis-ci.org/HarvestHub/GardenHub.svg?branch=master)](https://travis-ci.org/HarvestHub/GardenHub)
[![Coverage Status](https://coveralls.io/repos/github/HarvestHub/GardenHub/badge.svg?branch=master)](https://coveralls.io/github/HarvestHub/GardenHub?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/831094bb6605cfd9ec68/maintainability)](https://codeclimate.com/github/HarvestHub/GardenHub/maintainability)
[![Known Vulnerabilities](https://snyk.io/test/github/harvesthub/gardenhub/badge.svg)](https://snyk.io/test/github/harvesthub/gardenhub)
[![Requirements Status](https://requires.io/github/HarvestHub/GardenHub/requirements.svg?branch=master)](https://requires.io/github/HarvestHub/GardenHub/requirements/?branch=master)
[![Documentation Status](https://readthedocs.org/projects/gardenhub/badge/?version=latest)](http://gardenhub.readthedocs.io/en/latest/?badge=latest)
[![Docker Automated build](https://img.shields.io/docker/automated/harvesthub/gardenhub.svg)](https://hub.docker.com/r/harvesthub/gardenhub/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Matrix ID](https://img.shields.io/badge/matrix-%23gardenhub%3Amatrix.org-brightgreen.svg)](https://riot.im/app/#/room/#gardenhub:matrix.org)

# GardenHub

Formed around the simple idea that food should not go to waste, GardenHub is the solution to the problem of community garden food waste. Despite the best efforts of community gardeners, far too often food produced in community gardens rots on the vine.

GardenHub is building technology to enable gardeners to collaborate and act upon what's growing, ripening, and available for harvest in their gardens. Using this information, GardenHub notifies gardeners, local charities, restaurants, and other stakeholders of the availability of this food.

[Read the full documentation on Read the Docs.](https://gardenhub.readthedocs.io/en/latest/)

## Local development

GardenHub provides a script called `dev.sh` to make local development easy. As long as you have [Docker](https://www.docker.com/) installed, you do not need Python, Django, Postgres, or anything else running on your computer for local development with `dev.sh`. This is because `dev.sh` automatically configures a local development environment with Docker containers where all of that is already installed.

**Note:** This has been tested on GNU/Linux. Your mileage may vary using Docker on other operating systems.

You will need the following packages installed to develop on GardenHub:

* docker-ce
* docker-compose
* git
* bash

### Installing Docker

To check if you already have Docker installed, run `docker -v` in your terminal. GardenHub has been tested with version 17. **If you already have it, skip to the next section.**

[![asciicast](https://asciinema.org/a/158200.png)](https://asciinema.org/a/158200)

On most GNU/Linux distros, you can use the following command to install Docker:

```
sudo sh -c "wget -nv -O - https://get.docker.com/ | sh"
```

After Docker is installed, you'll want to add your user to the docker group so you don't need `sudo` to run Docker commands.

```
sudo usermod -aG docker $(whoami)
```

Finally, log out and back into your computer, and then head to the next section.

#### Installing Docker Compose

You will also need [Docker Compose](https://docs.docker.com/compose/install/#install-compose) for local development. Check if you already have it by typing `docker-compose version`.

If you need to install it, follow the link and select your platform for specific instructions.

### Starting the development server

[![asciicast](https://asciinema.org/a/158203.png)](https://asciinema.org/a/158203)

With Docker installed and ready to go, just follow these commands:

```
# Clone the repo
git clone https://github.com/HarvestHub/GardenHub.git

# Enter the project folder
cd GardenHub

# Run the local development server
./dev.sh start
```

It may take a few minutes to download everything the first time, then it will run more quickly on subsequent attempts.

`dev.sh` has a few options you can take advantage of.

| Command   | Description                                                                                                           |
|-----------|-----------------------------------------------------------------------------------------------------------------------|
| start     | Launches a Postgres container and a GardenHub app container then starts `manage.py runserver`.                        |
| build     | Rebuilds the app container. You must do this **manually** if you change requirements.txt.                             |
| manage.py | Same as running `python manage.py` in the app container. Useful for running migrations and other management commands. |
| setup     | Installs Docker. Works on many GNU/Linux distros.                                                                     |
| docs      | Runs a local server for editing the docs. Uses sphinx-autobuild within the container.                                 |

**Hint:** `./dev.sh start` will run migrations every time before it starts the development server. To skip that, you can run `./dev.sh manage.py runserver` to run the development server directly.

### Running migrations and management commands

To run migrations, you can use:

```
# Migrate
./dev.sh manage.py migrate

# Make migrations
./dev.sh manage.py makemigrations
```

Any other management command may also be run this way.

### Rebuilding the container (you have to, sometimes)

Changing application code shouldn't require rebuilding the container. However, you must **manually rebuild the container** any time you edit `requirements.txt`. This is because the requirements get installed into the container at build time. You can rebuild the container like so:

```
./dev.sh build
```

## License

GardenHub is copyright © 2017 HarvestHub. Except where otherwise noted, the code in this repo is licensed under the GNU AGPL version 3 or later. View the `LICENSE` file for a copy of the full license.

The documentation (in the `docs` subdirectory) is licensed under the GNU FDL version 1.3 or greater. View `docs/LICENSE` for a copy of the full license.

Finally, the file `gardenhub/templates/gardenhub/email_invitation.html` is copyright Lee Munroe and licensed under MIT. The copyright notice and full license text is inside of the source code of the file.
