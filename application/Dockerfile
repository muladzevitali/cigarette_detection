FROM python:3.8.1

WORKDIR /usr/src/application

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt
# Install pytorch
RUN pip install torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

CMD ["gunicorn", "--bind", "0.0.0.0:5090", "wsgi:application"]