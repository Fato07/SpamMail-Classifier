# SpamMail-Classifier
- This Script takes in .eml files as an input and determines if the file is Spam or Not Spam
- special Thanks to stackOverflow for the hack parsing .eml files with some tweaking and refactorings from my side: https://stackoverflow.com/questions/31392361/how-to-read-eml-file-in-python

## Setup and work around to run the script
- Please follow the following steps in running this script and checking spam mails

1. To Get Started, Clone this repository to a desired location of your choice
    ```bash
       git clone https://github.com/Fato07/SpamMail-Classifier.git
   ```
2. Open in your editor and add your desired .eml files to [ScamMails](./ScamMails) folder.

      - **NOTE**: the file format has to be **.eml** or the script would not work.
 3. You can add a list of BlackListed Email addresses that you know are from known scammers in [main.py](./main.py) file.
 For example:
    ```bash
    blackList_eml_addresses = ['"Euro-Millions.com" <verification@euro-millions.com>',
                               'Euromillions with Streamail <info@est.zebozut.com>',
                               'XE Money Transfer via Streamail <info@infor.sasonud.eu>',
                               'Webull <noreply@mail.webull.com>',
                               'iFlirts <service@info.iflirts.com>',
                               '=?utf-8?q?The_Compensation_Experts=C2=AE_with_Streamail?= <info@form.furosoyu.com>',
                               'sasi21 <service@crm.mydates.com>',
                               'Mail Delivery System <Mailer-Daemon@server.tempmailgen.com>',
                               'Euromillion Draw with Streamail <info@news.zadeput.com>',
                               '=?utf-8?q?The_Compensation_Experts=C2=AE_with_Streamail?= <info@est.3dflashworld.com>',
                               '"WarbyParker Promo" <wrbp44223@3ab61jnp01oogr.w8591-c42f.vcouzwmu.ga>']
    ``` 
 4. Run the code from your editor
 5. The Expected Result is saved to [overView.txt](./overView.txt) file categorizing the emails as spam or not spam
    ```
    Emails                                    Results
    ===========================================================  
    Grab 10 EuroMillions lines for £1.eml:            It is a spam
    Fathin you could be entitled to thousands.eml:    It is a spam
    ```
  6.Congrats you have successfully categorised your email as spam or not spam 
  
  ## Algorithm 🔗
  I have not Implemented Machine Learning in this Task. However, I have used a hard coded basis on solving this task.
  This program works in such a way that it determines a spam by the email address of the email sender. 
  If the e-mail address of the sender is not on the black List of email addresses. Then unfortunately, 
  the program would classify the email as not spam.
  
  
