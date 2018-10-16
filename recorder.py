import io
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
		if len(category.selected_rows) == 0:
			alert("Please select a category")
			return
		
		category_name = category.data_source.items[category.selected_row[1]]

		if agent_name.text == '':
			alert("Please enter an agent name.")
			return
		
		date_format = '%Y-%m-%d'
		formatted_data = (
			f"{transfer_date.date:{date_format}},"
			f"{agent_name.text},"
			f"{price_amount.text},"
			f"{category_name}\n"
			)
					
		with io.open(DATA_FILE, 'a+', encoding='utf8') as f:
			f.write(formatted_data)
			logger.info(f"\"{formatted_data[:-1]}\" appended to \"{DATA_FILE}\" file.")
		reload_records()
		hud_alert(f"Added entry for {agent_name.text}.")


def reload_records():
	try:
		with io.open(DATA_FILE, 'r+', encoding='utf8') as f:
			entries = ui.ListDataSource(f.read().splitlines())
			entries.items.reverse()
			records.data_source = entries
			records.reload_data()
	except FileNotFoundError:
		logger.info(f"\"{DATA_FILE}\" does not exist yet, so data did not load.")


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
	category = view['category']
	transfer_date = view['transfer_date']
	records = view['records_area']['records']
	
	reload_records()
