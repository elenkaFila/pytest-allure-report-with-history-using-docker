FROM python:3.12.0a4-alpine3.17

# Установка зависимостей
RUN apk update && apk add --no-cache \
    chromium \
    chromium-chromedriver \
    openjdk11-jre \
    curl \
    tar \
    wget \
    bash \
    git

# Установка Allure
RUN curl -o allure.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz \
    && tar -zxvf allure.tgz -C /opt/ \
    && ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure \
    && rm allure.tgz

WORKDIR /usr/workspace

# Копируем зависимости отдельно — это позволяет кэшировать pip install
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

CMD ["pytest", "-sv", "--alluredir=allure-results", "--html=report.html"]
