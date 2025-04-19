import smtplib
from email.mime.text import MIMEText
def send_email(subject, body):
    me = "stylehaven1024@gmail.com"  
    password = "fosv yima bfmr rnyx" 
    you = "stylehaven1024@gmail.com"  
    
    msg = MIMEText(body) 
    msg['From'] = me 
    msg['To'] = you 
    msg['Subject'] = subject 

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(me, password)
        server.sendmail(me, you, msg.as_string()) 
        server.quit() 
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
