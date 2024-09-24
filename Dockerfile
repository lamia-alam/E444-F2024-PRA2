FROM python:3.10
COPY ./ /var
WORKDIR /var
RUN python -m pip install -r requirements.txt
ENV FLASK_APP=hello.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
