# Analyze-Sentiment
Simple Flask site that uses external API

## Deployment steps
1. Create virtual environment
```bash
python3 -m virtualenv ~/Analyze-Sentiment -p /usr/bin/python3
source bin/activate
```
2. Install requirements
```bash
pip install -r requirements.txt
pip install gunicorn
```
3. Create service
```bash
sudo nano /etc/systemd/system/flask_sentiment.service
```
4. Copy the following to the flask_sentiment.service file
```
[Unit]
Description=Gunicorn instance to serve Flask_sentiment
After=network.target

[Service]
User=root
Group=www-data
PIDFile=/tmp/gunicorn_Flask_sentiment.pid
WorkingDirectory=/root/Analyze-Sentiment
Environment="PATH=/root/Analyze-Sentiment/bin"
ExecStart=/root/Analyze-Sentiment/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 -m 007 wsgi:app --error-log /var/log/gunicorn/error.log --access-logfile /var/log/gunicorn/access.log --log-file /var/log/gunicorn/gunicorn.log

[Install]
WantedBy=multi-user.target
```
5. Activate service
```bash
sudo mkdir /var/log/gunicorn
sudo systemctl start flask_sentiment
sudo systemctl enable flask_sentiment
```
6. Configuring Nginx to Proxy Requests
```bash
sudo nano /etc/nginx/sites-available/default
```
7. Copy the following to the end of /etc/nginx/sites-available/default file
```
location /analyzesentiment {
      include proxy_params;
      proxy_pass http://127.0.0.1:5000;
    }
```