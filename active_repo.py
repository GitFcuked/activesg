import datetime
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--user", required=True,
	help="username for login")
ap.add_argument("-p", "--password", required=True,
	help="password for login")
ap.add_argument("-c", "--pin", required=True,
	help="activesg pin")
ap.add_argument("-s", "--schedule", required=True,
	help="days of the week")
ap.add_argument("-i", "--index", default='1',
	help="index of timeslot")
ap.add_argument("-t", "--time", default='12:30:00',
	help="time to commence booking")
args = vars(ap.parse_args())

#func for getting schedule from input
def get_booking_schedule(pin):
	days =[]
	for c in pin:
		day = str((int(c) - 3) % 7)
		days.append(day)
	return days

#links and paths
path = r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe'
link = 'https://members.myactivesg.com/auth'
cck = 'https://members.myactivesg.com/facilities/view/activity/1031/venue/154'
cart = 'https://members.myactivesg.com/cart'

#credentials
username = args["user"]
pass_ = args["password"]
booking_password = args["pin"]

while True:
	if datetime.datetime.now().strftime("%X") == args["time"] and datetime.datetime.now().strftime("%w") in get_booking_schedule(args["schedule"]):
		not_booked = True
		while not_booked == True:
			try:
				#instantiating selenium webdriver
				driver = webdriver.Chrome(path)
				driver.get(link)

				#filling in details/logging in
				email = driver.find_element_by_id('email')
				email.send_keys(username)
				# email.send_keys(Keys.RETURN)

				password = driver.find_element_by_id('password')
				password.send_keys(pass_)
				password.send_keys(Keys.RETURN)

				#navigating to cck gym page
				driver.get(cck)

				#selecting slot, div[index], where index = 1 => first slot
				slot_index = args["index"]
				slot = driver.find_element_by_xpath('//div[@class="row timeslot-grid"]/div[%s]' % slot_index)
				slot.click()

				#pressing checkout button
				checkout = driver.find_element_by_id('paynow')
				checkout.click()

				#navigating to cart page
				driver.get(cart)

				#entering activesg password
				for idx, key in enumerate(args["pin"]):
					idx+=1
					password = driver.find_element_by_xpath('//*[@id="formCartPayment"]/div[1]/div/div/div[1]/input[%s]' % idx)
					pass_1.send_keys(key)

				#pressing confirm button
				confirm = driver.find_element_by_name('pay')
				confirm.click()

				#exiting browser
				driver.quit()

				#sleep to prevent multiple calls
				time.sleep(1)
				not_booked = False				
				print("Slot booked!")

			except:
				print("Retrying...")