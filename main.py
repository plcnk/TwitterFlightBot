from twitter import auth
from time import sleep
from flight import number


def main():
    api = auth.api
    client_id = api.get_me().data.id
    start_id = 1
    initialisation_resp = api.get_users_mentions(client_id)
    if initialisation_resp.data:
        start_id = initialisation_resp.data[0].id

    while True:
        mentions = api.get_users_mentions(client_id, since_id=start_id)

        if mentions.data:
            for tweet in mentions.data:
                try:
                    text = tweet.text.split(" ")
                    flight_details = number.find_flight(text[1])
                    if flight_details:
                        reply = f"{flight_details.airline_short_name} flight number {flight_details.number} is currently heading from {flight_details.origin_airport_name} to {flight_details.destination_airport_name}."
                    else:
                        reply = (
                            "Flight number was not found or is not currently active."
                        )
                    api.create_tweet(in_reply_to_tweet_id=tweet.id, text=reply)
                    start_id = tweet.id
                except Exception as error:
                    print(error)
        sleep(5)


if __name__ == "__main__":
    main()
