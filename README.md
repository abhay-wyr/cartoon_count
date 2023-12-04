# Flask App Deployment on AWS EC2

This guide explains how to deploy a Flask app on an AWS EC2 instance using Gunicorn as the application server and Nginx as a reverse proxy.

## Step 1: Install Dependencies on EC2

Connect to your EC2 instance and install the required dependencies:

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install Flask gunicorn

## Step 2: Run Flask App with Gunicorn

```bash
cd /home/ubuntu/cartoon_count
gunicorn -w 4 -b 0.0.0.0:5000 app:app

## Step 3: Install Nginx

```bash
sudo apt install nginx


## Step 4: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/cartoon_count
### Add the following configuration:

```bash
server {
    listen 80;
    server_name your_domain_or_public_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/cartoon_count/static;
    }

    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:5000;
    }
}

## Step 5: Enable Nginx Site
```bash
sudo ln -s /etc/nginx/sites-available/cartoon_count /etc/nginx/sites-enabled

## Step 6: Restart Nginx
```bash
sudo service nginx restart





