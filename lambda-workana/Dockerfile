FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

RUN dnf update -y && \
    dnf install -y \
    chromium \
    && dnf clean all

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright
RUN playwright install chromium

COPY app.py ./

CMD ["app.lambda_handler"]
