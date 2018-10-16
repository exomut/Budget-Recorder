import ui
import sound
import logging
from dialogs import *

# Constants
DATA_FILE = 'data.csv'


def button_pressed(button):
	title = button.title
	
	# Give user feedback
	sound.play_effect('ui:click4')
		
	if title in '0123456789':
		if price_amount.text == '0':
			price_amount.text = ''
		price_amount.text += title
			
	if title == '+/-':
		price_amount.text = '-' + price_amount.text
		price_amount.text = price_amount.text.replace('--', '')
		
	if title == '.' and '.' not in price_amount.text:
		price_amount.text += '.'
		
	if title == 'delete':
		price_amount.text = price_amount.text[:-1]

	# Never leave the price amount blank
	if price_amount.text == '':
		price_amount.text = '0'
		
	if title == 'write':
		if agent_name.text == '':
			alert('Please enter an agent name.')
			return
		formatted_data = '{date:{date_format}},{agent},{price}\n'.format(
				date=transfer_date.date,
				date_format='%Y-%m-%d',
				agent=agent_name.text,
				price=price_amount.text
				)
				
		with open(DATA_FILE, 'a+') as f:
			f.write(formatted_data)
			logger.info('"{data}" appended to "{file_name}" file.'.format(
				data=formatted_data.replace('\n', ''),
				file_name=DATA_FILE
				))
		reload_records()
		hud_alert('Added entry for {agent}.'.format(agent=agent_name.text))


def reload_records():
	try:
		with open(DATA_FILE, 'r+') as f:
			entries = ui.ListDataSource(f.read().splitlines())
			entries.items.reverse()
			records.data_source = entries
			records.reload_data()
	except FileNotFoundError:
		logger.info(
			'"{file_name}" does not exist yet, so data did not load.'
			.format(file_name=DATA_FILE)
			)
	

if __name__ == '__main__':
	# Logger Setup
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	
	# Get main view
	view = ui.load_view()
	view.present('sheet')
	
	# Load Essential Views
	price_amount = view['price_amount']
	agent_name = view['agent_name']
	transfer_date = view['transfer_date']
	records = view['records']
	
	reload_records()
