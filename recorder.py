import io
import ui
import sound
import clipboard
import types
import logging
from dialogs import *

# Constants
DATA_FILE = 'data.tsv'
CATEGORIES = ui.ListDataSource([
	'水道光熱費',
	'旅費交通費',
	'通信費',
	'広告宣伝費',
	'接待交際費',
	'消耗品費',
	'地代家賃',
	'個人事業税',
	'固定資産税',
	'国民健康保険',
	'国民年金',
	'特別区民税',
	'生命保険',
	'売上'
	])


def button_pressed(button):
	'@type button: ui.button'
	title = button.title
	
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


def write_record(sender):
	'@type sender: ui.button'
	if len(category.selected_rows) == 0:
		alert("Please select a category")
		return
	
	category_name = category.data_source.items[category.selected_row[1]]

	if agent_name.text == '':
		alert("Please enter an agent name.")
		return
	
	date_format = '%Y-%m-%d'
	formatted_data = (
		f"{transfer_date.date:{date_format}}\t"
		f"{agent_name.text.replace('	','')}\t"  # Remove tabs
		f"{price_amount.text}\t"
		f"{category_name}\n"
		)
				
	with io.open(DATA_FILE, 'a+', encoding='utf-8') as f:
		f.write(formatted_data)
		logger.info(f"\"{formatted_data[:-1]}\" appended to \"{DATA_FILE}\" file.")
	reload_records()
	hud_alert(f"Added entry for {agent_name.text}.")


def copy_records(sender):
	'@type sender: ui.button'
	try:
		with io.open(DATA_FILE, 'r', encoding='utf-8') as f:
			clipboard.set(f.read()[:-1])
			hud_alert("Records copied to clipboard.")
	except FileNotFoundError:
		logger.info(f"\"{DATA_FILE}\" does not exist yet, so data did not load.")


def reload_records():
	try:
		with io.open(DATA_FILE, 'r', encoding='utf-8') as f:
			entries = ui.ListDataSource(f.read().splitlines())
			entries.items.reverse()
			records.data_source = entries
			records.reload_data()
			records.allows_selection = False
						
	except FileNotFoundError:
		logger.info(f"\"{DATA_FILE}\" does not exist yet, so data did not load.")


if __name__ == '__main__':
	# Logger Setup
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	
	# Get main view
	view = ui.load_view()
	view.present('sheet')
	
	# Load essential views
	transfer_date = view['transfer_date']
	agent_name = view['agent_name']
	price_amount = view['price_amount']
	category = view['category']
	records = view['records']
	
	# Populate the data
	category.data_source = CATEGORIES
	category.reload_data()
	
	reload_records()
