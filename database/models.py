# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 30, 2024 20:16:56
# Database: sqlite:////tmp/tmp.aea16Nrsnp-01JGCKBE0EV1F1FGVZDKZJ2W36/AirlineManagementSystem/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Airline(Base):  # type: ignore
    """
    description: Defines the Airline entity, which includes the airline's name, country, and the date it was founded.
    """
    __tablename__ = 'airline'
    _s_collection_name = 'Airline'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    country = Column(String(100))
    founded_date = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    AircraftList : Mapped[List["Aircraft"]] = relationship(back_populates="airline")



class Airport(Base):  # type: ignore
    """
    description: Defines the Airport entity with basic attributes like name, location, country, code, and opened_date.
    """
    __tablename__ = 'airport'
    _s_collection_name = 'Airport'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    location = Column(String(100))
    country = Column(String(100))
    code = Column(String(10))
    opened_date = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    AirportRunwayList : Mapped[List["AirportRunway"]] = relationship(back_populates="airport")
    FlightList : Mapped[List["Flight"]] = relationship(foreign_keys='[Flight.arrival_airport_id]', back_populates="arrival_airport")
    departureFlightList : Mapped[List["Flight"]] = relationship(foreign_keys='[Flight.departure_airport_id]', back_populates="departure_airport")
    LoungeAccessList : Mapped[List["LoungeAccess"]] = relationship(back_populates="airport")



class CrewMember(Base):  # type: ignore
    """
    description: Details for crew members including their name and role.
    """
    __tablename__ = 'crew_member'
    _s_collection_name = 'CrewMember'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    role = Column(String(50))

    # parent relationships (access parent)

    # child relationships (access children)
    FlightCrewList : Mapped[List["FlightCrew"]] = relationship(back_populates="crew_member")



class Aircraft(Base):  # type: ignore
    """
    description: Represents aircraft used in flights, including attributes such as model, manufacturer, and seats.
    """
    __tablename__ = 'aircraft'
    _s_collection_name = 'Aircraft'  # type: ignore

    id = Column(Integer, primary_key=True)
    model = Column(String(50))
    manufacturer = Column(String(100))
    seats = Column(Integer)
    airline_id = Column(ForeignKey('airline.id'))

    # parent relationships (access parent)
    airline : Mapped["Airline"] = relationship(back_populates=("AircraftList"))

    # child relationships (access children)
    MaintenanceRecordList : Mapped[List["MaintenanceRecord"]] = relationship(back_populates="aircraft")



class AirportRunway(Base):  # type: ignore
    """
    description: Describes the runways at airports, including runway code, length, and surface type.
    """
    __tablename__ = 'airport_runway'
    _s_collection_name = 'AirportRunway'  # type: ignore

    id = Column(Integer, primary_key=True)
    airport_id = Column(ForeignKey('airport.id'))
    code = Column(String(10))
    length = Column(Integer)
    surface_type = Column(String(30))

    # parent relationships (access parent)
    airport : Mapped["Airport"] = relationship(back_populates=("AirportRunwayList"))

    # child relationships (access children)



class Flight(Base):  # type: ignore
    """
    description: Defines the Flight entity representing each flight with attributes such as flight number, departure and arrival times, and status.
    """
    __tablename__ = 'flight'
    _s_collection_name = 'Flight'  # type: ignore

    id = Column(Integer, primary_key=True)
    flight_number = Column(String(10))
    departure_airport_id = Column(ForeignKey('airport.id'))
    arrival_airport_id = Column(ForeignKey('airport.id'))
    scheduled_departure = Column(DateTime)
    scheduled_arrival = Column(DateTime)
    status = Column(String(20))

    # parent relationships (access parent)
    arrival_airport : Mapped["Airport"] = relationship(foreign_keys='[Flight.arrival_airport_id]', back_populates=("FlightList"))
    departure_airport : Mapped["Airport"] = relationship(foreign_keys='[Flight.departure_airport_id]', back_populates=("departureFlightList"))

    # child relationships (access children)
    BaggageList : Mapped[List["Baggage"]] = relationship(back_populates="flight")
    FlightCrewList : Mapped[List["FlightCrew"]] = relationship(back_populates="flight")
    PassengerList : Mapped[List["Passenger"]] = relationship(back_populates="flight")



class Baggage(Base):  # type: ignore
    """
    description: Baggage information for a flight, including weight and owner.
    """
    __tablename__ = 'baggage'
    _s_collection_name = 'Baggage'  # type: ignore

    id = Column(Integer, primary_key=True)
    flight_id = Column(ForeignKey('flight.id'))
    weight = Column(Float)
    owner_name = Column(String(100))

    # parent relationships (access parent)
    flight : Mapped["Flight"] = relationship(back_populates=("BaggageList"))

    # child relationships (access children)



class FlightCrew(Base):  # type: ignore
    """
    description: Junction table to map crew members to flights with positions.
    """
    __tablename__ = 'flight_crew'
    _s_collection_name = 'FlightCrew'  # type: ignore

    id = Column(Integer, primary_key=True)
    flight_id = Column(ForeignKey('flight.id'))
    crew_member_id = Column(ForeignKey('crew_member.id'))
    position = Column(String(30))

    # parent relationships (access parent)
    crew_member : Mapped["CrewMember"] = relationship(back_populates=("FlightCrewList"))
    flight : Mapped["Flight"] = relationship(back_populates=("FlightCrewList"))

    # child relationships (access children)



class MaintenanceRecord(Base):  # type: ignore
    """
    description: Maintenance logs for aircraft, detailing the maintenance performed.
    """
    __tablename__ = 'maintenance_record'
    _s_collection_name = 'MaintenanceRecord'  # type: ignore

    id = Column(Integer, primary_key=True)
    aircraft_id = Column(ForeignKey('aircraft.id'))
    maintenance_date = Column(Date)
    description = Column(String(200))

    # parent relationships (access parent)
    aircraft : Mapped["Aircraft"] = relationship(back_populates=("MaintenanceRecordList"))

    # child relationships (access children)



class Passenger(Base):  # type: ignore
    """
    description: Contains passenger details for a flight, including name and seat number.
    """
    __tablename__ = 'passenger'
    _s_collection_name = 'Passenger'  # type: ignore

    id = Column(Integer, primary_key=True)
    flight_id = Column(ForeignKey('flight.id'))
    name = Column(String(100))
    seat_number = Column(String(10))

    # parent relationships (access parent)
    flight : Mapped["Flight"] = relationship(back_populates=("PassengerList"))

    # child relationships (access children)
    LoungeAccessList : Mapped[List["LoungeAccess"]] = relationship(back_populates="passenger")
    TicketList : Mapped[List["Ticket"]] = relationship(back_populates="passenger")



class LoungeAccess(Base):  # type: ignore
    """
    description: Tracks lounge access for passengers at airports.
    """
    __tablename__ = 'lounge_access'
    _s_collection_name = 'LoungeAccess'  # type: ignore

    id = Column(Integer, primary_key=True)
    passenger_id = Column(ForeignKey('passenger.id'))
    airport_id = Column(ForeignKey('airport.id'))
    access_date = Column(Date)

    # parent relationships (access parent)
    airport : Mapped["Airport"] = relationship(back_populates=("LoungeAccessList"))
    passenger : Mapped["Passenger"] = relationship(back_populates=("LoungeAccessList"))

    # child relationships (access children)



class Ticket(Base):  # type: ignore
    """
    description: Represents tickets purchased by passengers for flights.
    """
    __tablename__ = 'ticket'
    _s_collection_name = 'Ticket'  # type: ignore

    id = Column(Integer, primary_key=True)
    passenger_id = Column(ForeignKey('passenger.id'))
    issue_date = Column(Date)
    price = Column(Float)

    # parent relationships (access parent)
    passenger : Mapped["Passenger"] = relationship(back_populates=("TicketList"))

    # child relationships (access children)
