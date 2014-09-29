# This sample demonstrates how to use the siem endpoint in the
# REST API.

# This sample is interactive.

# For this scenario to work there must already be offenses on the system the
# sample is being run against.  
# THIS SAMPLE WILL MAKE CHANGES TO THE OFFENSE IT IS RUN AGAINST
# The scenario demonstrates the following actions:
#  - How to get offenses
#  - How to get a single offense given the ID
#  - How to get notes from an offense
#  - How to make a new note for an offense

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import json
import os
import sys
import urllib.parse
sys.path.append(os.path.realpath('../modules'))

from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities

def main():
	# First we have to create our client
	client = RestApiClient()

	# Request the API call only taking a few fields
	SampleUtilities.pretty_print_request(client, 'siem/offenses?fields=id,description,' +
		'status,offense_type,offense_source', 'GET')
	response = client.call_api('siem/offenses?fields=id,description,status,offense_type,offense_source', 'GET')

	# Print out the result for the user to see
	SampleUtilities.pretty_print_response(response)

	# Prompt the user for an ID
	offense_ID = input('Select an offense to post a note to. Please type its ID or quit. ')
	
	# Error checking because we want to make sure the user has selected an offense that exists.
	while True:

		if (offense_ID == 'quit'):
			exit(0)

		# Make the request to 'GET' the offense chosen by the user
		SampleUtilities.pretty_print_request(client, 'siem/offenses/' + str(offense_ID), 'GET')
		response = client.call_api('siem/offenses/' + str(offense_ID), 'GET')

		# Check response code to see if the offense exists
		if (response.code == 200):
			break
		else:
			offense_ID = input('An offense by that ID does not exist. Please try again or type quit. ')

	# Print out the offense the user chose
	SampleUtilities.pretty_print_response(response)

	# Send in the API Call request for the offense's notes
	SampleUtilities.pretty_print_request(client, 'siem/offenses/' + str(offense_ID) + '/notes', 'GET')
	response = client.call_api('siem/offenses/' + str(offense_ID) + '/notes', 'GET')

	# Display all the notes on the offense
	SampleUtilities.pretty_print_response(response)

	# Confirm that the user wants to make a new note for the offense. We have to check this since it will
	# permanently add that note to the offense.
	confirmation = input('Would you like to make a new note for offense ' + str(offense_ID) + '? (YES/no)\n')

	if (confirmation != 'YES'):
		print('You have chosen not to post a new note. Exiting sample.')
		exit(0)

	# Take in the text for the note. Since the note could be multiple words, and the API calls through a
	# url, we are using urllib.parse.quote to preserve the spaces and special characters in the note.
	text = urllib.parse.quote(input('Please enter the content of the note.\n'))
	
	# Send in the request for the new note to be put on the offense.
	SampleUtilities.pretty_print_request(client, 'siem/offenses/' + offense_ID + '/notes?note_text=' + text, 'POST')
	response = client.call_api('siem/offenses/' + offense_ID + '/notes?note_text=' + text, 'POST')

	#Display to the user the new note to confirm that it has been created properly.
	SampleUtilities.pretty_print_response(response)

if __name__ == "__main__":
    main()
