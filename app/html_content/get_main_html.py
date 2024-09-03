def get_main_html(data):
	html = '''
		  <div id="drop_image">
		    <p>Drag and drop image here or</p>
		    <input type="file" id="select_image" accept="image/*">
		  </div>

		  <img id="preview_image" src="#" alt="Image Preview" style="max-width: 400px;">

		  <button id="stream_audio">
		  	Stream Audio
		  </button>

		  <div id="chat_log">
		  </div>

    		'''

	return html