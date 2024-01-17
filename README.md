# Introduction 
This is an automated bot to schedule passport on a Italian Website. A credentials yaml containing
the inputs necessary must be provided. It scans the email for the OTP code and fills the form as fast as possible
reaching the scheduling page. It was supposed to be a test to show in as a proposal for a Workana Project, but it got
accepted before I could formulate my proposal. It would have a tkinter page for GUI so the user could provide the form data more intuitively. This is code is just a test preview of what could have been developed, but I didn't want it to go to waste, so here it is.

# Requirements:
## Google App Password:
Go to this [page](https://support.google.com/accounts/answer/185833?hl=en) to get a app password
for your email address so the code can automatically get the OTP code. This is required for the automatic
retrieval of the OTP code.


Create a `credentials.yaml` containing the following structure:

```yaml
email:
  host: 'Email host (e.g.: for gmail is imap.gmail.com)'
  address: 'Account Email'
  pwd: 'Google App password'
site:
  url: https://prenotami.esteri.it/
  pwd: 'Site account password'
  typeofbookingddl: 'Booking Type: {1 for Individual Booking and 2 for Multiple Booking}'
  ddls_0: 'Holder of Italian expired/soon-to-be expired passport (Y/N) {1 for Yes and 2 for No}'
  passportExpiryDate: 'When the passport expires'
  pathPassport: 'Path to passport pdf'
  pathAbroadCert: 'Path to pdf certifying residence abroad'
```
# Running the code:
Simply run `pip install requirements.txt` then `python passport_automation.py`.
