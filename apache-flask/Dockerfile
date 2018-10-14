FROM debian:latest

# Install software via apt
RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi \
    python \
    python-pip \
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Redirect apache logs to stdout
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log

# Copy the requirements list and install
COPY ./requirements.txt /var/www/apache-flask/requirements.txt
RUN pip install -r /var/www/apache-flask/requirements.txt

# Copy the application
COPY ./app/ /var/www/apache-flask/app/
COPY ./config/ /var/www/apache-flask/config/
COPY ./run.py /var/www/apache-flask/
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf

# Configure apache
RUN a2enmod headers
RUN a2dissite 000-default
RUN a2ensite apache-flask

EXPOSE 80

WORKDIR /var/www/apache-flask

CMD  /usr/sbin/apache2ctl -D FOREGROUND
