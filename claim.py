# -*- coding: utf-8 -*-

import sys
import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import argparse

class ClaimJob(unittest.TestCase):
    def setUser(self, userData):
        self.userData = userData

    def setJourney(self, journey):
        self.journey = journey

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://garantie.nah.sh/kmi/kundengarantie"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def submit(self, no_review=False):
        driver = self.driver
        userData = self.userData
        journey = self.journey
        driver.get("https://garantie.nah.sh/kmi/kundengarantie?execution=e1s1")
        driver.find_element_by_id("bedingung").click()
        driver.find_element_by_id("_eventId_weiter").click()
        driver.find_element_by_id("fahrkartenart").click()
        Select(driver.find_element_by_id("fahrkartenart")).select_by_visible_text(userData.get('fahrkartenart'))
        driver.find_element_by_name("fahrkarte").click()
        Select(driver.find_element_by_name("fahrkarte")).select_by_visible_text(userData.get('fahrkarte'))
        driver.find_element_by_id("fknummer").click()
        driver.find_element_by_id("fknummer").clear()
        driver.find_element_by_id("fknummer").send_keys(userData.get("fknummer"))
        driver.find_element_by_id("gueltigkeit").clear()
        driver.find_element_by_id("gueltigkeit").send_keys(userData.get('gueltigkeit'))
        driver.find_element_by_id("verspaetung").clear()
        driver.find_element_by_id("verspaetung").send_keys(journey.get('delay'))
        driver.find_element_by_id("body").click()
        driver.find_element_by_id("_eventId_weiter").click()
        driver.find_element_by_id("haltestelleVon").click()
        driver.find_element_by_id("haltestelleVon").clear()
        driver.find_element_by_id("haltestelleVon").send_keys(journey.get('startLocation'))
        driver.find_element_by_xpath("//div[@id='divHaltestelleVon']/div/div[2]").click()
        driver.find_element_by_id("haltestelleNach").click()
        driver.find_element_by_id("haltestelleNach").clear()
        driver.find_element_by_id("haltestelleNach").send_keys(journey.get('endLocation'))
        driver.find_element_by_xpath("//div[@id='divHaltestelleNach']/div").click()
        driver.find_element_by_id("datum").click()
        driver.find_element_by_link_text(journey.get('day')).click()
        driver.find_element_by_id("uhrzeit").click()
        driver.find_element_by_id("uhrzeit").clear()
        driver.find_element_by_id("uhrzeit").send_keys(journey.get('departureTime'))
        driver.find_element_by_id("_eventId_weiter").click()
        driver.find_element_by_id("div-i-verbindung-1").click()
        driver.find_element_by_id("_eventId_fahrtabschnitt").click()
        driver.find_element_by_id("geschlecht").click()
        Select(driver.find_element_by_id("geschlecht")).select_by_visible_text(userData.get("geschlecht"))
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(userData.get("email"))
        driver.find_element_by_id("emailKontrolle").clear()
        driver.find_element_by_id("emailKontrolle").send_keys(userData.get("email"))
        driver.find_element_by_id("vorname").click()
        driver.find_element_by_xpath("//div[@id='nameDiv']/div").click()
        driver.find_element_by_id("name").click()
        driver.find_element_by_id("name").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys(userData.get("name"))
        driver.find_element_by_id("vorname").clear()
        driver.find_element_by_id("vorname").send_keys(userData.get("vorname"))
        driver.find_element_by_id("strasse").clear()
        driver.find_element_by_id("strasse").send_keys(userData.get("strasse"))
        driver.find_element_by_id("hausnummer").clear()
        driver.find_element_by_id("hausnummer").send_keys(userData.get("hausnummer"))
        driver.find_element_by_id("plz").clear()
        driver.find_element_by_id("plz").send_keys(userData.get("plz"))
        driver.find_element_by_id("ort").clear()
        driver.find_element_by_id("ort").send_keys(userData.get("ort"))
        driver.find_element_by_id("land").clear()
        driver.find_element_by_id("land").send_keys("Deutschland")
        driver.find_element_by_id("telgesch").clear()
        driver.find_element_by_id("telgesch").send_keys(userData.get("telgesch"))
        driver.find_element_by_id("iban").click()
        driver.find_element_by_id("iban").clear()
        driver.find_element_by_id("iban").send_keys(userData.get("iban"))
        driver.find_element_by_id("swift").click()
        driver.find_element_by_id("swift").clear()
        driver.find_element_by_id("swift").send_keys(userData.get("swift"))
        driver.find_element_by_id("datenschutz").click()
        driver.find_element_by_id("_eventId_weiter").click()
        driver.find_element_by_id('bestaetigungsmail').click()
        # TODO: review before submitting
        if no_review:
            driver.find_element_by_id("_eventId_weiter").click()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Claim money for NAH.SH train delays')
    parser.add_argument('--departureHour', '-d', type=str,help='Departure hour, for example 07', required=True)
    parser.add_argument('--profileFilename', '-f', help='profile.json filename', required=True)
    parser.add_argument('--day', help='Provide day as 5, by default today', required=False)
    parser.add_argument('--delay', help='Provide delay in minutes, for example 22', required=True)
    args = parser.parse_args()

    job = ClaimJob()
    userData = json.loads(open(args.profileFilename).read())
    standardJourneys = userData.get('standardJourneys')
    def filter_departures(dTimes, departureHour):
        return [d for d in dTimes if d.startswith(str(departureHour)+":")]
    journeys = [standardJourneys[x] for x in standardJourneys if len(filter_departures(standardJourneys[x].get('departureTimes'), args.departureHour)) > 0]
    if len(journeys) > 1:
        raise Exception("More than one journey: " + str(journeys))

    journey = journeys[0]
    dtimes = filter_departures(journey['departureTimes'], args.departureHour)
    if len(dtimes) > 1:
        raise Exception("More than one departure time" + str(dtimes))

    day = datetime.datetime.today().day
    if args.day:
        day = args.day
    journey.update({
        'day': str(day),
        'departureTime' : dtimes[0],
        'delay':args.delay})
    print(journey)
    if True:
        job.setUser(userData)
        job.setJourney(journey)
        job.setUp()
        job.submit()
