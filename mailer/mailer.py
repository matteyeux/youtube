import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import os


def send_mail(var_type, var_mail):
    # define var
    type_mail = ['Nouveau Compte',
                 'Modification du mot de passe',
                 'l\'encodage de votre vidéo vient d\'être finalisé']

    html_msg = ['<p>Bonjour,<br>Bienvenue sur le site My YouTube<br>Votre compte à correctement été enregistré.</p>',
                '<p>Bonjour,<br>Votre nouveau mot de passe à bien été enregistré.</p>',
                '<p>Bonjour,<br>L\'encodage de votre vidéo vient d\'être finalisé.</p>']

    # Mailing
    msg = MIMEMultipart()
        
    me = 'lepage_boris@orange.fr'
    you = ['lepage_b@etna-alternance.net',
           'hauteb_m@etna-alternance.net',
           'hummeau_y@etna-alternance.net',
           var_mail]

    msg['From'] = me
    msg['To'] = ','.join(you)
    msg['Subject'] = type_mail[var_type]

    # We reference the image in the IMG SRC attribute by the ID we give it below
    #msgText = MIMEText('<p>Bonjour, <i>HTML</i> <br><br>text<br> and an image.</p><br><img src="cid:image1"><br>', 'html')

    msgText = MIMEText(html_msg[var_type], 'html')
    msg.attach(msgText)

    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()
