FROM osgeo/gdal:ubuntu-full-3.1.0

RUN apt-get -y update \
 && apt-get install -y --no-install-recommends python3-pip git \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt

RUN mkdir -p /usr/local/apps/mbutil
RUN git clone https://github.com/mapbox/mbutil.git /usr/local/apps/mbutil
ENV MBUTIL_LOCATION=/usr/local/apps/mbutil/mb-util

RUN mkdir -p /tiledata/areas

COPY data /data
COPY app /app
