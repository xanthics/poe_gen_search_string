from browser import document as doc
from browser.html import TABLE, TR, TH, TD, INPUT, SELECT, OPTION, DIV, BUTTON, SPAN, LI, H2, H3, IMG, COLGROUP, COL, P, SECTION, BR
from json import load
import gen_items


# Create the static elements of the home page
def init_page():
	# selected
	t = TABLE(TR(TH() + TH('Selection')))
	t <= TR(TD("Keyword(s) Search:", Class="right_text") + TD(INPUT(Type='text', Id="keywords", Class='save')))
	doc['show_hide'] <= t
	doc['show_hide'] <= DIV(BUTTON("Generate String", Id='generate') + " Will generate search strings based on all selected rows.  This will cause many calculations and may take a bit to return a result")
	doc['show_hide'] <= DIV("No strings generated yet.", Id="generated_strings", Class='sec_div grind')
	doc['show_hide'] <= DIV(BUTTON("Select All Visible Only", Id='select_visible') + " This will deselect all hidden rows and select all visible rows.")
	doc['show_hide'] <= BUTTON("Clear Selected", Id='clear_selected')

	# Load and display data
	t = TABLE(TR(TH("Selected", Class='col_1') + TH("Mod")), Class="borders onehundred")
	data = {x['name'] for x in gen_items.gen_bases}
	for base in sorted(data):
		base_l = base.lower()
		searchstring = base_l
		t <= TR(TD(INPUT(Id=f"check-{base_l.replace(' ', '_')}", type='checkbox', data_id=base_l, Class='save')) + TD(base, Class="left_text"), data_id=base_l, data_search=searchstring)

	doc['items'] <= t


init_page()
doc['loading'] <= DIV(Id='prerendered')
