###########################################################################
TCSS 573A: Internet of Things (IoT)
Park Smart – Final Project ReadMe.txt
Group01: Deepthi Warrier Edakunni, Tejashri Anil Joshi
############################################################################

Files Needed to test the project:

Python Scripts - 
--------------------------
1. parksmartTest.py
2. blinkled.py
3. Turn_ON_BlueLED.py
4. motor_control.py

NODE-RED Flow file -
--------------------------
ParkSmart.json

Development Platform used -
----------------------------------
Raspberry Pi, Grove Pi Plus, python, Javascript, NODE-Red, IBM Watson cloud platform


Steps to follow to test the project - 
-------------------------------------------
1. Start node-red from command prompt using the command node-red start
2. Open the url : http://127.0.0.1:1880/ on a browser
3. Export the flow called ParkSmart.json
4. check the path for above mentioned python scripts for respective nodes in the flow.
5. Deploy the flow.
6. Create table called parking_spot_details - trigger node createparking_spot_details node in the flow. parking_spot_details table will be created.
7. Create table called reservation_details - trigger node createreservation_details  node in the flow. reservation_details table will be created.

Testing the app:
---------------------------
6. Set up the users on the flow by going to the rightmost dropdown option and clicking on the users and setting up the account.
7. Below are some of the users that are setup by the prototype.
	1. userId: jack password: password123
	2. userId: john password: password123
	3. userId: jane password: password123
8. Open 127.0.0.1/login on the browser to log in.
9. Enter the wrong userid and password. 
	An unathorized message would be shown on the ui.
10. Enter the correct userid and password.
	1. userId: jack password: password123
	2. userId: john password: password123
	3. userId: jane password: password123
11. Once succssfully logged in, it takes the user to the reservation page: http://127.0.0.1:1880/reserve
12. The current status of the parking spots will be shown.
13. The user can also reserve the parking spot 3 from the reservation page.
14. Once the reservation details are entered and form submitted, the email and message will sent to entered email and phone number.

IoT Analytics Dashboard:
-------------------------------------
The local node-red dashboard can be accessed at 127.0.0.1/ui
The dashboard displays bar charts for the number of reservations done per day for the last one mnth and also the number of reservations doen per month for the last one year.

IBM Cloud Dashboard:
----------------------------------------
For the user id set up for IBM cloud, the dashboard displays the status of the parking spots, the total available parking spots and the total number of reservations done for todays date.

########################################################################################################################################################################################################################################################################################################



 



