import ui
import sound
import logging
from dialogs import *

# Constants
DATA_FILE = 'data.csv'

def button_pressed(button):
	# Load Views
	price_amount = view['price_amount']
	agent_name = view['agent_name']
	transfer_date = view['transfer_date']
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

	# Never leave the label blank
	if price_amount.text == '':
		price_amount.text = '0'
		
	if title == 'write':
		with open(DATA_FILE, 'a+') as f:
			f.write('{date},{agent},{price}\n'.format(
				date=transfer_date.date.strftime('%Y-%m-%d'),
				agent=agent_name.text,
				price=price_amount.text
				))
			logger.info('Data appended to data.csv file.')
			
def reload_records():
	records = view['records']
	with open(DATA_FILE, 'r') as f:
		records.datasource = f.read()
	

if __name__ == '__main__':
	# Logger Setup
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	
	view = ui.load_view()
	view.present('sheet')
	
	reload_records()
