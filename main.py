import config
from logs import logger
import tweepy
from FlightRadar24.api import FlightRadar24API
from time import sleep
from datetime import datetime
from datetime import timezone


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
    airline_iata_check = 0
    airline_icao_check = 0
    airlines = fr_api.get_airlines()

    for airline in airlines:
        # If IATA matches, assign it to a check variable, same with ICAO
        if airline["Code"] == airline_iata:
            airline_iata_check = airline["ICAO"]
            log.info("Found airline IATA: %s", airline["Code"])
        elif airline["ICAO"] == airline_icao:
            airline_icao_check = airline["ICAO"]
            log.info("Found airline ICAO %s", airline["ICAO"])

    # If both IATA and ICAO are assigned, assign the one that matches the ICAO
    if airline_iata_check != 0 and airline_icao_check != 0:
        airline_icao_new = airline_icao_check
    elif airline_iata_check == 0 and airline_icao_check == 0:
        airline_icao_new = None
    else:
        airline_icao_new = airline_iata_check

    if airline_icao_new is None:  # Don't search for the flight if airline is not found
        log.warning("Airline not found: %s", airline_iata)
        return None

    flights = fr_api.get_flights(airline=airline_icao_new)

    for flight in flights:
        # If a flight number / callsign matches, we get all flight details
        if flight.number == flight_number or flight.callsign == flight_number:
            details = fr_api.get_flight_details(flight.id)
            flight.set_flight_details(details)
            return flight


def process_timestamp(timestamp, flight_number, timestamp_type):
    if timestamp and timestamp != 0:  # Timestamps can be None or 0
        date = datetime.fromtimestamp(timestamp, timezone.utc)  # Convert timestamp into datetime
        t = date.strftime("%Y/%m/%d, %H:%M UTC")  # Format datetime
    else:
        t = "Unknown"
        log.warning("Could not process timestamp: %s (%s)", flight_number, timestamp_type)
    return t


def process_number(flight_details):
    if flight_details.number == "N/A":
        number = f"callsign {flight_details.callsign}"
        log.warning("No flight number, using callsign: %s", flight_details.callsign)
    else:
        number = f"number {flight_details.number}"
    return number


def create_reply(flight_details, flight_number):  # Formulate the tweet reply depending on the data we got
    if flight_details:
        flight_eta_timestamp = flight_details.time_details["other"]["eta"]
        flight_dep_timestamp = flight_details.time_details["real"]["departure"]
        flight_departure = process_timestamp(flight_dep_timestamp, flight_number, "departure")
        flight_eta = process_timestamp(flight_eta_timestamp, flight_number, "eta")
        altitude = "On ground" if flight_details.on_ground == 1 else f"{flight_details.altitude} feet"
        number_reply = process_number(flight_details)
        reply = f"""
{flight_details.airline_short_name} flight {number_reply}:
Origin: {flight_details.origin_airport_name}
Departure time: {flight_departure}
Destination: {flight_details.destination_airport_name}
ETA: {flight_eta}
Altitude: {altitude}
        """
        log.info("Flight found: %s", flight_details.number)
    else:
        reply = "Flight number was not found or is not currently active."
        log.warning("Flight not found: %s", flight_number)
    return reply


def post_reply(tweet_id, reply):  # Post the reply on Twitter
    try:
        api.create_tweet(in_reply_to_tweet_id=tweet_id, text=reply)
        log.info("Posted reply to tweet ID: %s", tweet_id)
    except tweepy.errors.TweepyException as error:
        log.error(error)


def process_tweet(tweet):  # Big function that runs everything else
    global start_id
    try:
        # Tweet only if it's not a mention and if split text has more than 1 index to avoid out of range error
        if tweet.in_reply_to_user_id is None and len(tweet.text.split(" ")) > 1:
            flight_number = tweet.text.split(" ")[1]  # Separate the mention from the actual flight number
            flight_number = flight_number.upper()
            log.info("Mention - User ID: %s, number: %s", tweet.author_id, flight_number)
            flight_details = find_flight(flight_number)
            reply = create_reply(flight_details, flight_number)
            post_reply(tweet.id, reply)
            start_id = tweet.id
        else:
            start_id = tweet.id  # Skip the tweet and move on
    except Exception as error:
        log.error(error)


def scan_mentions():  # Perpetually scan for mentions (every 10 seconds)
    global start_id
    mentions = api.get_users_mentions(client_id, since_id=start_id, expansions=["in_reply_to_user_id", "author_id"])
    if mentions.data:
        for tweet in mentions.data:
            process_tweet(tweet)
    sleep(10)


if __name__ == "__main__":
    log = logger.create_logger()
    api = auth()
    client_id = api.get_me().data.id
    start_id = 1
    init = api.get_users_mentions(client_id)
    if init.data:
        start_id = init.data[0].id  # Initialize with the latest mention
    while True:
        scan_mentions()
