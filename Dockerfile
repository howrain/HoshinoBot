FROM python
ENV LANG C.UTF-8
WORKDIR /HoshinoBot
ADD hoshino hoshino
ADD run.py run.py
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/