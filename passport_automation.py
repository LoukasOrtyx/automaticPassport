import re
import time
import yaml
import email
import imaplib

from datetime import datetime
from playwright.sync_api import sync_playwright

def get_credentials(path):
	with open(path, "r") as stream:
		try:
			credentials = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)
	return credentials

def get_otp(email_data, timeout=300, check_interval=15):
	mail = imaplib.IMAP4_SSL(email_data['host'])
	mail.login(email_data['address'], email_data['pwd'])
	start_time = time.time()
	while time.time() - start_time < timeout:
		mail.select("inbox")
		status, messages = mail.search(None, '(SUBJECT "OTP Code")', 'UNSEEN')
		if status == "OK":
			message_ids = messages[0].split()
			if not message_ids:
				continue
			latest_email_id = message_ids[-1]
			status, message_data = mail.fetch(latest_email_id, '(RFC822)')
			raw_email = message_data[0][1].decode('utf-8')
			message = email.message_from_string(raw_email)
			if message.is_multipart():
				body = message.get_payload(0).get_payload(decode=True).decode()
			else:
				body = message.get_payload(decode=True).decode()
			otp_code = re.search(r"OTP Code:(\d+)", body).group(1)
			break
		time.sleep(check_interval)
	mail.logout()
	return otp_code

def handle_dialog(dialog):
    dialog.accept()

def select_option(page, selector, option):
	page.locator(f'{selector} option[value="{option}"]')
	page.locator(selector).select_option(option)

def schedule_passport():
	cred = get_credentials('credentials.yaml')
	site_data = cred['site']
	email_data = cred['email']
	with sync_playwright() as p:
		browser = p.firefox.launch(headless=False)
		context = browser.new_context(ignore_https_errors=True)
		page = context.new_page()
		page.on('dialog', handle_dialog)
		page.set_default_timeout(120000)
		page.goto(site_data['url'])
		page.locator('#login-email').fill(email_data['address'])
		page.locator('#login-password').fill(site_data['pwd'])
		page.locator('button[type="submit"]').click()
		page.locator('a#advanced').click()
		page.locator('#dataTableServices tbody tr:nth-of-type(9) button').click()
		select_option(page, 'select#typeofbookingddl', site_data['typeofbookingddl'])
		select_option(page, 'select#ddls_0', site_data['ddls_0'])
		formatted_data = datetime.strptime(site_data['passportExpiryDate'], '%d/%m/%Y').strftime('%Y-%m-%d')
		page.locator('input#DatiAddizionaliPrenotante_1___data').fill(formatted_data)
		page.locator('input#File_0').set_input_files(site_data['pathPassport'])
		page.locator('input#File_1').set_input_files(site_data['pathAbroadCert'])
		page.locator('button#otp-send').click()
		otp_code = get_otp(email_data)
		page.locator('input#otp-input').fill(otp_code)
		page.locator('input#PrivacyCheck').check()
		page.locator('button#btnAvanti').click()
		input("Pressione Enter após concluir a ação no navegador...")
		browser.close()

if __name__ == '__main__':
	schedule_passport()