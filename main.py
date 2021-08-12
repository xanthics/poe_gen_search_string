from browser import document as doc
from browser import bind, worker, window
from browser.html import P, BR, INPUT


myWorker = worker.Worker("myworker")


# Function handling filtering changes
@bind('.save', 'input')
def save_state(ev):
	if ev.target.id == 'keywords':
		search_terms = ev.target.value.lower().split()
		for el in doc.get(selector="[data-search]"):
			terms = el.attrs['data-search']
			if all(x in terms for x in search_terms):
				if 'hidden_class' in el.class_name:
					el.attrs['class'] = "container"
				elif 'hidden' in el.attrs:
					del el.attrs['hidden']
			else:
				if 'container' in el.class_name:
					el.attrs['class'] = "container hidden_class"
				else:
					el.attrs['hidden'] = ''


@bind(myWorker, 'message')
def onmessage(evt):
	if evt.data[0] == 'overlap':
		doc['generated_strings'] <= P(f"{evt.data[1]} will also match {evt.data[2]} due to being an unavoidable substring match")
	elif evt.data[0] == 'done':
		if evt.data[1]:
			del doc['updates']
			# input size uses 'M' * size to figure out width.  Only correct with fixed width font.
			doc['generated_strings'] <= (P(f'{c}: ' + INPUT(value=x, size=len(x)+1, readonly='', Class='monospace', type="text", Id=f"{c}_search", onClick=f'document.getElementById("{c}_search").select(); document.execCommand("copy");')) for c, x in enumerate(evt.data[1], start=1))
	elif evt.data[0] == 'update':
		doc['updates'].text = evt.data[1]
	elif evt.data[0] == 'debug':
		# print(evt.data[1])
		pass


# Clear keyword box
def clear_keywords(ev):
	doc['keywords'].value = ''
	event = window.Event.new('input')
	doc['keywords'].dispatchEvent(event)


def select_visible(ev):
	for el in doc.get(selector="tr[data-id]"):
		check_id = f'check-{el.attrs["data-id"].replace(" ", "_")}'
		if 'hidden' in el.attrs:
			doc[check_id].checked = False
		else:
			doc[check_id].checked = True


def clear_selected(ev):
	for el in doc.get(selector="tr[data-id]"):
		check_id = f'check-{el.attrs["data-id"].replace(" ", "_")}'
		doc[check_id].checked = False


def generate_string(ev):
	doc['generated_strings'].text = ''
	good_bases = []
	for el in doc.get(selector="input[type=checkbox]"):
		if el.checked:
			good_bases.append(el.attrs['data-id'])

	if good_bases:
		doc['generated_strings'] <= P('Starting web worker', Id='updates')
		myWorker.send(("init", good_bases))
	else:
		doc['generated_strings'] <= P("No bases were selected, so no result to return.")


def first_load():
	doc["generate"].bind("click", generate_string)
	doc["select_visible"].bind("click", select_visible)
	doc["clear_selected"].bind("click", clear_selected)
	doc["clear_keywords"].bind("click", clear_keywords)
	del doc['loading']


first_load()
