import config
import tweepy
from FlightRadar24.api import FlightRadar24API
from time import sleep


def auth():  # Twitter API authentication, done with environment variables declared in config.py
    client = tweepy.Client(
        bearer_token=config.BEARER_TOKEN,
        consumer_key=config.API_KEY,
        consumer_secret=config.API_KEY_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_token_secret=config.ACCESS_TOKEN_SECRET,
    )

    return client


def find_flight(flight_number):  # Cannot search flights only by number, we first need to retrieve the airline
    fr_api = FlightRadar24API()
    airline_iata = flight_number[0:2]  # IATA code is the first 2 characters in the flight number
    airline_icao = flight_number[0:3]  # Same but it's the first 3 characters
    airlines = fr_api.get_airlines()

    for airline in airlines:
        if airline["Code"] == airline_iata or airline["ICAO"] == airline_icao:
            airline_icao = airline["ICAO"]  # If any code matches an airline, use its ICAO code

    flights = fr_api.get_flights(airline=airline_icao)

    for flight in flights:
        if flight.number == flight_number:  # If a flight number matches, we get all flight details
            details = fr_api.get_flight_details(flight.id)
            flight.set_flight_details(details)
            return flight


def create_reply(flight_details):  # Formulate the tweet reply depending on the data we got
    if flight_details:
        reply = f"{flight_details.airline_short_name} flight number {flight_details.number} is currently heading from {flight_details.origin_airport_name} to {flight_details.destination_airport_name}."
    else:
        reply = "Flight number was not found or is not currently active."
    return reply


def post_reply(tweet_id, reply):  # Post the reply on Twitter
    try:
        api.create_tweet(in_reply_to_tweet_id=tweet_id, text=reply)
    except tweepy.errors.TweepyException as error:
        print(error)


def process_tweet(tweet):  # Big function that runs everything else
    global start_id
    try:
        if tweet.in_reply_to_user_id is None:  # Tweet only if it's not a mention
            flight_number = tweet.text.split(" ")[1]  # Separate the mention from the actual flight number
            flight_details = find_flight(flight_number)
            reply = create_reply(flight_details)
            post_reply(tweet.id, reply)
            start_id = tweet.id
        else:
            start_id = tweet.id  # Skip the tweet and move on
    except Exception as error:
        print(error)


def scan_mentions():  # Perpetually scan for mentions (every 10 seconds)
    global start_id
    mentions = api.get_users_mentions(client_id, since_id=start_id, expansions=["in_reply_to_user_id"])
    if mentions.data:
        for tweet in mentions.data:
            process_tweet(tweet)
    sleep(10)


if __name__ == "__main__":
    api = auth()
    client_id = api.get_me().data.id
    start_id = 1
    init = api.get_users_mentions(client_id)
    if init.data:
        start_id = init.data[0].id  # Initialize with the latest mention
    while True:
        scan_mentions()
