import config
import tweepy
from FlightRadar24.api import FlightRadar24API
from time import sleep


def auth():
    client = tweepy.Client(
        bearer_token=config.BEARER_TOKEN,
        consumer_key=config.API_KEY,
        consumer_secret=config.API_KEY_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_token_secret=config.ACCESS_TOKEN_SECRET
    )

    return client


def find_flight(flight_number):
    fr_api = FlightRadar24API()
    airline_iata = flight_number[0:2]
    airline_icao = flight_number[0:3]
    airlines = fr_api.get_airlines()

    for airline in airlines:
        if airline["Code"] == airline_iata or airline["ICAO"] == airline_icao:
            airline_icao = airline["ICAO"]

    flights = fr_api.get_flights(airline=airline_icao)

    for flight in flights:
        if flight.number == flight_number:
            details = fr_api.get_flight_details(flight.id)
            flight.set_flight_details(details)
            return flight


def create_reply(flight_details):
    if flight_details:
        reply = f"{flight_details.airline_short_name} flight number {flight_details.number} is currently heading from {flight_details.origin_airport_name} to {flight_details.destination_airport_name}."
    else:
        reply = "Flight number was not found or is not currently active."
    return reply


def post_reply(tweet_id, reply):
    try:
        api.create_tweet(in_reply_to_tweet_id=tweet_id, text=reply)
    except tweepy.errors.TweepyException as error:
        print(error)


def process_tweet(tweet):
    global start_id
    try:
        if tweet.in_reply_to_user_id is None:
            flight_number = tweet.text.split(" ")[1]
            flight_details = find_flight(flight_number)
            reply = create_reply(flight_details)
            post_reply(tweet.id, reply)
            start_id = tweet.id
        else:
            start_id = tweet.id
    except Exception as error:
        print(error)


def scan_mentions():
    global start_id
    mentions = api.get_users_mentions(client_id, since_id=start_id, expansions=['in_reply_to_user_id'])
    if mentions.data:
        for tweet in mentions.data:
            process_tweet(tweet)
    sleep(10)


if __name__ == "__main__":
    api = auth()
    client_id = api.get_me().data.id
    start_id = 1
    initialisation_resp = api.get_users_mentions(client_id)
    if initialisation_resp.data:
        start_id = initialisation_resp.data[0].id
    while True:
        scan_mentions()
