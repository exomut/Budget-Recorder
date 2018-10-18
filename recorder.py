import ui
import io
import sound
import logging
from dialogs import alert
from records import reload_records, write_record, copy_records

# Logger Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Constants
# Load categories from text file. Seperated by new lines
CATEGORIES_FILE_NAME = 'categories.txt'
try: 
	with io.open(CATEGORIES_FILE_NAME, 'r', encoding='utf-8') as f:
		CATEGORIES = ui.ListDataSource(f.read().splitlines())
except FileNotFoundError:
	logger.error(f'The "{CATEGORIES_FILE_NAME}" file not found. Please create it.')
	exit()


def button_pressed(sender):
	'@type sender: ui.button'
	title = sender.title
	
	# Give user feedback
	sound.play_effect('ui:click4')
		
	if title in '0123456789':
		if price_amount.text == '0':
			price_amount.text = ''
		elif price_amount.text == '-0':
			price_amount.text = '-'
		price_amount.text += title
			
	if title == '+/-':
		price_amount.text = '-' + price_amount.text
		price_amount.text = price_amount.text.replace('--', '')
		
	if title == '.' and '.' not in price_amount.text:
		price_amount.text += '.'
		
	if title == 'delete':
		price_amount.text = price_amount.text[:-1]

	if title == 'delete_all':
		price_amount.text = ''

	if title == 'clear':
		price_amount.text = ''
		agent_name.text = ''
		category.reload()
		transfer_date.date = transfer_date.date.now()

	# Never leave the price amount blank
	if price_amount.text == '':
		price_amount.text = '-0'


def button_pressed_confirm(sender):
	'@type sender:ui.button'
	if len(category.selected_rows) == 0:
		alert("Please select a category")
		return
	
	# selecte_row: The section and row of the first selected row (as a 2-tuple).
	category_name = category.data_source.items[category.selected_row[1]]

	if agent_name.text == '':
		alert("Please enter an agent name.")
		return
		
	write_record(
		sender,
		transfer_date.date,
		agent_name.text,
		price_amount.text,
		category_name
		)
	reload_records(records)

	
def button_pressed_copy(sender):
	'@type sender:ui.button'
	copy_records()


if __name__ == '__main__':
	# Get main view
	view = ui.load_view()
	view.present('sheet')
	
	# Load essential views
	transfer_date = view['transfer_date']
	agent_name = view['agent_name']
	price_amount = view['price_amount']
	category = view['category']
	records = view['records']
	
	# View setup
	records.allows_selection = False
	
	# Populate the data
	category.data_source = CATEGORIES
	category.reload_data()
	
	reload_records(records)
