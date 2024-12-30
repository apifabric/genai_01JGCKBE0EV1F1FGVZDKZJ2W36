# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Airport(Base):
    """description: Defines the Airport entity with basic attributes like name, location, country, code, and opened_date."""
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    code = Column(String(10), nullable=True)
    opened_date = Column(Date, nullable=True)

class Flight(Base):
    """description: Defines the Flight entity representing each flight with attributes such as flight number, departure and arrival times, and status."""
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String(10), nullable=True)
    departure_airport_id = Column(Integer, ForeignKey('airport.id'))
    arrival_airport_id = Column(Integer, ForeignKey('airport.id'))
    scheduled_departure = Column(DateTime, nullable=True)
    scheduled_arrival = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=True)

class Airline(Base):
    """description: Defines the Airline entity, which includes the airline's name, country, and the date it was founded."""
    __tablename__ = 'airline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    founded_date = Column(Date, nullable=True)

class Aircraft(Base):
    """description: Represents aircraft used in flights, including attributes such as model, manufacturer, and seats."""
    __tablename__ = 'aircraft'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(50), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    seats = Column(Integer, nullable=True)
    airline_id = Column(Integer, ForeignKey('airline.id'), nullable=True)

class AirportRunway(Base):
    """description: Describes the runways at airports, including runway code, length, and surface type."""
    __tablename__ = 'airport_runway'
    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_id = Column(Integer, ForeignKey('airport.id'))
    code = Column(String(10), nullable=True)
    length = Column(Integer, nullable=True)
    surface_type = Column(String(30), nullable=True)

class FlightCrew(Base):
    """description: Junction table to map crew members to flights with positions."""
    __tablename__ = 'flight_crew'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    crew_member_id = Column(Integer, ForeignKey('crew_member.id'))
    position = Column(String(30), nullable=True)

class CrewMember(Base):
    """description: Details for crew members including their name and role."""
    __tablename__ = 'crew_member'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    role = Column(String(50), nullable=True)

class Baggage(Base):
    """description: Baggage information for a flight, including weight and owner."""
    __tablename__ = 'baggage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    weight = Column(Float, nullable=True)
    owner_name = Column(String(100), nullable=True)

class Passenger(Base):
    """description: Contains passenger details for a flight, including name and seat number."""
    __tablename__ = 'passenger'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    name = Column(String(100), nullable=True)
    seat_number = Column(String(10), nullable=True)

class Ticket(Base):
    """description: Represents tickets purchased by passengers for flights."""
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    passenger_id = Column(Integer, ForeignKey('passenger.id'))
    issue_date = Column(Date, nullable=True)
    price = Column(Float, nullable=True)

class MaintenanceRecord(Base):
    """description: Maintenance logs for aircraft, detailing the maintenance performed."""
    __tablename__ = 'maintenance_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    aircraft_id = Column(Integer, ForeignKey('aircraft.id'))
    maintenance_date = Column(Date, nullable=True)
    description = Column(String(200), nullable=True)

class LoungeAccess(Base):
    """description: Tracks lounge access for passengers at airports."""
    __tablename__ = 'lounge_access'
    id = Column(Integer, primary_key=True, autoincrement=True)
    passenger_id = Column(Integer, ForeignKey('passenger.id'))
    airport_id = Column(Integer, ForeignKey('airport.id'))
    access_date = Column(Date, nullable=True)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    airport1 = Airport(name="JFK International", location="New York", country="USA", code="JFK", opened_date=date(1948, 7, 1))
    airport2 = Airport(name="Heathrow", location="London", country="UK", code="LHR", opened_date=date(1946, 5, 31))
    airport3 = Airport(name="Haneda", location="Tokyo", country="Japan", code="HND", opened_date=date(1931, 8, 25))
    airport4 = Airport(name="Changi", location="Singapore", country="Singapore", code="SIN", opened_date=date(1981, 7, 1))
    flight1 = Flight(flight_number="AA100", departure_airport_id=1, arrival_airport_id=2, scheduled_departure=datetime(2023, 10, 10, 10, 0, 0), scheduled_arrival=datetime(2023, 10, 10, 20, 0, 0), status="On Time")
    flight2 = Flight(flight_number="BA200", departure_airport_id=2, arrival_airport_id=1, scheduled_departure=datetime(2023, 10, 11, 15, 0, 0), scheduled_arrival=datetime(2023, 10, 11, 17, 30, 0), status="Delayed")
    flight3 = Flight(flight_number="JL300", departure_airport_id=3, arrival_airport_id=4, scheduled_departure=datetime(2023, 10, 10, 14, 0, 0), scheduled_arrival=datetime(2023, 10, 10, 22, 0, 0), status="Cancelled")
    flight4 = Flight(flight_number="SQ400", departure_airport_id=4, arrival_airport_id=3, scheduled_departure=datetime(2023, 10, 12, 8, 0, 0), scheduled_arrival=datetime(2023, 10, 12, 16, 0, 0), status="On Time")
    airline1 = Airline(name="American Airlines", country="USA", founded_date=date(1926, 4, 15))
    airline2 = Airline(name="British Airways", country="UK", founded_date=date(1974, 3, 31))
    airline3 = Airline(name="Japan Airlines", country="Japan", founded_date=date(1951, 8, 1))
    airline4 = Airline(name="Singapore Airlines", country="Singapore", founded_date=date(1947, 5, 1))
    aircraft1 = Aircraft(model="Boeing 737", manufacturer="Boeing", seats=160, airline_id=1)
    aircraft2 = Aircraft(model="Airbus A380", manufacturer="Airbus", seats=500, airline_id=2)
    aircraft3 = Aircraft(model="Boeing 787", manufacturer="Boeing", seats=300, airline_id=3)
    aircraft4 = Aircraft(model="Airbus A350", manufacturer="Airbus", seats=350, airline_id=4)
    airport_runway1 = AirportRunway(airport_id=1, code="4R/22L", length=4000, surface_type="Asphalt")
    airport_runway2 = AirportRunway(airport_id=1, code="13L/31R", length=3500, surface_type="Concrete")
    airport_runway3 = AirportRunway(airport_id=2, code="9L/27R", length=3700, surface_type="Asphalt")
    airport_runway4 = AirportRunway(airport_id=3, code="16L/34R", length=3000, surface_type="Concrete")
    flight_crew1 = FlightCrew(flight_id=1, crew_member_id=1, position="Pilot")
    flight_crew2 = FlightCrew(flight_id=1, crew_member_id=2, position="Co-Pilot")
    flight_crew3 = FlightCrew(flight_id=2, crew_member_id=3, position="Flight Attendant")
    flight_crew4 = FlightCrew(flight_id=3, crew_member_id=4, position="Pilot")
    crew_member1 = CrewMember(name="John Doe", role="Pilot")
    crew_member2 = CrewMember(name="Jane Smith", role="Co-Pilot")
    crew_member3 = CrewMember(name="Alice Brown", role="Flight Attendant")
    crew_member4 = CrewMember(name="Bob White", role="Pilot")
    baggage1 = Baggage(flight_id=1, weight=15.5, owner_name="Michael Roe")
    baggage2 = Baggage(flight_id=2, weight=20.0, owner_name="Anna Watson")
    baggage3 = Baggage(flight_id=3, weight=12.3, owner_name="Charlie Son")
    baggage4 = Baggage(flight_id=4, weight=18.4, owner_name="Susan Hill")
    passenger1 = Passenger(flight_id=1, name="Michael Johnson", seat_number="12A")
    passenger2 = Passenger(flight_id=2, name="Linda Bennett", seat_number="14B")
    passenger3 = Passenger(flight_id=3, name="Paul Green", seat_number="8C")
    passenger4 = Passenger(flight_id=4, name="Laura Blue", seat_number="2D")
    ticket1 = Ticket(passenger_id=1, issue_date=date(2023, 8, 20), price=300.50)
    ticket2 = Ticket(passenger_id=2, issue_date=date(2023, 9, 12), price=450.75)
    ticket3 = Ticket(passenger_id=3, issue_date=date(2023, 10, 5), price=150.00)
    ticket4 = Ticket(passenger_id=4, issue_date=date(2023, 10, 8), price=500.25)
    maintenance_record1 = MaintenanceRecord(aircraft_id=1, maintenance_date=date(2023, 9, 1), description="Engine Check")
    maintenance_record2 = MaintenanceRecord(aircraft_id=2, maintenance_date=date(2023, 8, 25), description="Landing Gear Replacement")
    maintenance_record3 = MaintenanceRecord(aircraft_id=3, maintenance_date=date(2023, 7, 15), description="Fuel System Inspection")
    maintenance_record4 = MaintenanceRecord(aircraft_id=4, maintenance_date=date(2023, 10, 2), description="Cabin Pressure Check")
    lounge_access1 = LoungeAccess(passenger_id=1, airport_id=1, access_date=date(2023, 8, 20))
    lounge_access2 = LoungeAccess(passenger_id=2, airport_id=2, access_date=date(2023, 9, 12))
    lounge_access3 = LoungeAccess(passenger_id=3, airport_id=3, access_date=date(2023, 10, 5))
    lounge_access4 = LoungeAccess(passenger_id=4, airport_id=4, access_date=date(2023, 10, 8))
    
    
    
    session.add_all([airport1, airport2, airport3, airport4, flight1, flight2, flight3, flight4, airline1, airline2, airline3, airline4, aircraft1, aircraft2, aircraft3, aircraft4, airport_runway1, airport_runway2, airport_runway3, airport_runway4, flight_crew1, flight_crew2, flight_crew3, flight_crew4, crew_member1, crew_member2, crew_member3, crew_member4, baggage1, baggage2, baggage3, baggage4, passenger1, passenger2, passenger3, passenger4, ticket1, ticket2, ticket3, ticket4, maintenance_record1, maintenance_record2, maintenance_record3, maintenance_record4, lounge_access1, lounge_access2, lounge_access3, lounge_access4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
