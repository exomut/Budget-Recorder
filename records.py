import ui
import io
import clipboard
import logging
from dialogs import hud_alert, alert

# Constants
DATA_FILE = 'data.tsv'
SEPERATOR = '\t'
NEW_LINE = '\n'
CATEGORY_DISPLAY_LENGTH = 6
AGENT_DISPLAY_LENGTH = 16
RECORDS_FONT_SIZE = 12
RECORDS_FONT = 'Courier'

# Logger Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def copy_records():
	try:
		with io.open(DATA_FILE, 'r', encoding='utf-8') as f:
			clipboard.set(f.read()[:-1])
			hud_alert("Records copied to clipboard.")
	except FileNotFoundError:
		logger.info(f"\"{DATA_FILE}\" does not exist yet, so data did not load.")


def reload_records(records):
	try:
		with io.open(DATA_FILE, 'r', encoding='utf-8') as f:
			entries = DataSource(f.read().splitlines())
			entries.items.reverse()
			records.data_source = entries
			records.reload_data()
			records.allows_selection = False
						
	except FileNotFoundError:
		logger.info(f"\"{DATA_FILE}\" does not exist yet, so data did not load.")

		
def write_record(
	sender, transfer_date, agent_name, price_amount, category_name):
	'@type sender: ui.button'
	
	date_format = '%Y-%m-%d'
	formatted_data = (
		f"{transfer_date:{date_format}}{SEPERATOR}"
		f"{agent_name.replace(SEPERATOR,'')}{SEPERATOR}"  # Remove tabs
		f"{price_amount}{SEPERATOR}"
		f"{category_name}{NEW_LINE}"
		)
				
	with io.open(DATA_FILE, 'a+', encoding='utf-8') as f:
		f.write(formatted_data)
		logger.info(f"\"{formatted_data[:-1]}\" appended to \"{DATA_FILE}\" file.")
	
	hud_alert(f"Added entry for {agent_name.replace(SEPERATOR, '')}.")


class DataSource(ui.ListDataSource):
	
	def __init__(self, items=None):
		super().__init__(items)
	
	def tableview_cell_for_row(self, tv, section, row):
		item = self.items[row]

		# Veiw styles (default, subtitle, value1, value2)
		cell = ui.TableViewCell('value1')
		cell.text_label.number_of_lines = self.number_of_lines
		cell.text_label.font = (RECORDS_FONT, RECORDS_FONT_SIZE)
		cell.detail_text_label.font = (RECORDS_FONT, RECORDS_FONT_SIZE)
		
		# Demystify the data
		columns = ('date', 'agent', 'amount', 'category')
		data_dict = dict(zip(columns, str(item).split(SEPERATOR)))
		
		# Add data to cell labels
		cell.text_label.text = \
			f'({data_dict["date"]}) ' \
			f'{data_dict["agent"][0:AGENT_DISPLAY_LENGTH]}' \
			f'{".." if len(data_dict["agent"]) > AGENT_DISPLAY_LENGTH else ""}'
		cell.detail_text_label.text = \
			f'{data_dict["amount"]} ' \
			f'{data_dict["category"][0:CATEGORY_DISPLAY_LENGTH]}' \
			f'{".." if len(data_dict["category"]) > CATEGORY_DISPLAY_LENGTH else "  "}'
		
		return cell
