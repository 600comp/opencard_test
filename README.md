# opencard_test

Копирование конкретной ветки simlpe_test с историей из одного коммита
git clone https://github.com/600comp/opencard_test.git -b simlpe_test --depth=1

docker build \
    --no-cache \
    -t git-app:latest \
    --build-arg username=user \
    --build-arg password=qwerty \
    .

Запуск докер файла из текущего директория
docker build -t pytest .

Запуск докер файла из текущего директория с указанием конкретного файла Dockerfile
docker build -t pytest . -f opencard_test/Dockerfile

