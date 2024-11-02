def get_sign_in_html() -> str:
	html = '''
			<h1>Sign In</h1>
			<input type="email" id="email" placeholder="Enter your email">
			<button id="send_magic_link">Send Magic Link</button>
			'''
			
	return html