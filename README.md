# Twitter Flight Bot

This bot will return information about a flight when you tag it with its flight number.
To use it, you need to tag it by its Twitter handle [@FlightStatusBot](https://twitter.com/FlightStatusBot) and follow with a flight number like so: `.@FlightStatusBot U2189`.

The bot will reply to you with the following information:

* The airline name with the flight number
* The origin airport name
* The actual departure time in UTC timezone
* The arrival airport name
* The Estimated Time of Arrival in UTC timezone
* The altitude in feet

**Be aware that the flight must be active for the bot to work, meaning the plane's transponder must be on.**

The code is written in Python and uses [Tweepy](https://pypi.org/project/tweepy/) for the Twitter connection and [FlightRadarAPI](https://pypi.org/project/FlightRadarAPI/) for the Flghtradar24 API.
This bot is not affiliated with [Flightradar24](https://www.flightradar24.com/) in any way.

## Setup

To run the code yourself, you will need to create an App on the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard) and generated your tokens to be able to use the API.

After that, there are multiple methods to run this bot.

### First method: Use the Docker image (recommended)

A [Docker image](https://hub.docker.com/r/plck/twitterflightbot) is available for this project, which makes it easier for production environment and is the method I would recommend. You will first need to have [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine for this to work.

First, cd into this repository:

```shell
cd ./TwitterFlightBot
```

Then, edit the `docker-compose.yml` file with your Twitter API credentials:

```yaml
environment:
    TWITTER_API_KEY: "XXXXX"
    TWITTER_API_KEY_SECRET: "XXXXX"
    TWITTER_ACCESS_TOKEN: "XXXXX"
    TWITTER_ACCESS_TOKEN_SECRET: "XXXXX"
    TWITTER_BEARER_TOKEN: "XXXXX"
```

Finally, start the bot using this command:

```shell
docker compose up -d
```

If you want to stop the bot, use this command:

```shell
docker compose down
```

### Second method: Directly run the code

You can directly run the code on your machine or your VM. You will need to have Python3 installed, which comes by default on most Linux distros.

If you don't have it, install pip:

```shell
sudo apt install python3-pip
```

First, cd into this repository:

```shell
cd ./TwitterFlightBot
```

I recommend using a virtual environment to run the code, you can find out how to use this [here](https://docs.python.org/3/tutorial/venv.html). It is not required, but I highly recommend virtualenvs to avoid breaking your main environment.

After that, install the required packages with this command:

```shell
pip install -r requirements.txt
```

Next, you will need to export your Twitter API credentials as environment variables:

```shell
export TWITTER_API_KEY="XXXXX"
export TWITTER_API_KEY_SECRET="XXXXX"
export TWITTER_ACCESS_TOKEN="XXXXX"
export TWITTER_ACCESS_TOKEN_SECRET="XXXXX"
export TWITTER_BEARER_TOKEN="XXXXX"
```

Finally, start the bot with `python main.py`.

## License

This project is licensed under MIT License. See [LICENSE](https://github.com/plcnk/TwitterFlightBot/blob/master/LICENSE) for more details.
