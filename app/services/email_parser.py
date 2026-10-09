from email import policy
from email.parser import BytesParser
import os
from app.core.config import get_settings
from pathlib import Path



def email_parser(directory: str,userEmail:dict):
    paths = [p for p in directory.iterdir()]
    for path in paths:
        with open(Path(path),"rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            sender = msg["From"]
            recipient = msg["To"]
            subject = msg["Subject"]
            date = msg["Date"]
            body = msg.get_body(preferencelist=("plain","html"))
            
            if body: 
                body = body.get_content()
                userEmail[""]
            
        

# config = get_settings()

# data_dir = Path(config.data_dir)

# user_dir = [p for p in data_dir.iterdir() if p.is_dir()]
# for user in user_dir:
#     user_name=str(user_dir[0]).split("/")[-1]
    
#     with open(user)