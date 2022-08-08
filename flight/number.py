from FlightRadar24.api import FlightRadar24API

fr_api = FlightRadar24API()


def find_flight(flight_number):
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
