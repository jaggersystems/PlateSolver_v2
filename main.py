"""
- Store target object name or coordinates
- Plate Solve image
- Calculate offset in hms (or decimal) to determine movement direction
- Readout up/down/left/right (close = fast blink, far away = slow blink)
- Monitor for new images in 15s loop
- Repeat
"""

import re

from time import time, sleep

from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time

from solve import plate_solve


TARGET_NAME = "M101"
# NGC 2976 = (<Angle 1.05851339 deg>, <Angle -0.8701005 deg>)
# M82 = (<Angle -0.16647478 deg>, <Angle 0.5973768 deg>)
# NGC 2950 = (<Angle 7.5492307 deg>, <Angle -7.03363531 deg>)

# Val 1 positive = left
# Val 2 positive = down

INPUT_FILENAME = "images\m81.jpg"
SOLVED_FILENAME = "images\m81.ini"

CURRENT_DATETIME = Time('2021-04-05T22:20:00') - 1 * u.hour
CURRENT_LONGITUDE = 1.153970
CURRENT_LATITUDE = 51.313068
CURRENT_LATITUDE = 51.313068
CURRENT_HEIGHT = 20


# import pdb; pdb.set_trace()


"""
Returns the current Time
"""
def get_current_time():
    # Todo : Calculate +1hr for Daylight Savings Automatically
    return CURRENT_DATETIME

"""
Returns the current EarthLocation
"""
def get_current_location():
    return EarthLocation(lon=CURRENT_LONGITUDE * u.deg, lat=CURRENT_LATITUDE * u.deg, height=CURRENT_HEIGHT * u.m)

"""
Return the Frame (Alt/Az) of our observation site
"""
def get_observation_site_location():
    current_time = get_current_time()
    observation_site = get_current_location()
    observation_site_frame = AltAz(obstime=current_time, location=observation_site)
    return observation_site_frame

"""
Returns the SkyCoord (RA/Dec) of our target location 
"""
def get_target_location(target_name):
    return SkyCoord.from_name(target_name)

"""
Return the Frame (Alt/Az) of our target location
"""
def get_frame_by_target_name(target_name, location):
    target_location = get_target_location(target_name)
    target_location_frame = target_location.transform_to(location)
    return target_location_frame

def file_read(fname):
    input = {}
    with open(fname) as f:
        for line in f.readlines():
            try:
                key, value = line.rstrip("\n").split("=")
                input[key] = value
            except:
                print("Failed to unpack line. Scale was inaccurate or increase down sampling!")

    return input

def get_frame_from_file(filename, location):
    input = file_read(filename)

    try:
        dec_RA = input["CRVAL1"]
        dec_DEC = input["CRVAL2"]
    except:
        raise Exception("Failed to retrieve RA/Dec.")

    # print(dec_RA)
    # print(dec_DEC)

    frame = SkyCoord(dec_RA, dec_DEC, frame='icrs', unit='deg')
    frame_alt_az = frame.transform_to(location)

    # print("Plate Solved Az./Alt.: " + str(frame_alt_az))
    return frame_alt_az

def figure_it_out():
    # while True:
    # plate_solve(INPUT_FILENAME)

    observation_site_location = get_observation_site_location()

    target_frame = get_frame_by_target_name(TARGET_NAME, observation_site_location)
    file_frame = get_frame_from_file(SOLVED_FILENAME, observation_site_location)

    alt_diff = file_frame.alt - target_frame.alt
    azimuth_diff = file_frame.az - target_frame.az
    # azimuth_diff = target_frame.az - file_frame.az

    if azimuth_diff > 180:
        new_azimuth_diff = 360 - file_frame.az + target_frame.az

    # print("Target Alt: " + str(target_frame.alt))
    print("Target Az: " + str(target_frame.az))
    # print("File Alt: " + str(file_frame.alt))
    print("File Az: " + str(file_frame.az) + "\n")

    # if (str(alt_diff).startswith("-1")):
    #     print("Adjust camera Altitude UP by " + str(alt_diff) + " degrees")
    # else:
    #     print("Adjust camera Altitude DOWN by " + str(alt_diff) + " degrees")
    #
    # if (str(azimuth_diff).startswith("-1")):
    #     print("Adjust camera Azimuth LEFT by " + str(azimuth_diff) + " degrees")
    # else:
    #     print("Adjust camera Azimuth RIGHT by " + str(azimuth_diff) + " degrees")
    # sleep(10 - time() % 10)

    print("Alt diff: " + str(alt_diff))
    print("Az diff: " + str(azimuth_diff))

figure_it_out()


# TODO: Draw the rest of the OWL