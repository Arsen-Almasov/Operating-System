!whoami
!pwd
!uname -a
!lsb_release -a
root
/content
Linux d82fcbdff524 6.6.159+ #1 SMP Thu Oct 22 03:07:54 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04.5 LTS
Release:	24.04
Codename:	noble
!mkdir -p ~/os-course/pr01
%cd /root/os-course/pr01
!echo "Практическая работа №1" > about.txt
!echo "Знакомство с терминалом Linux" >> about.txt
!cat about.txt
!ls -la
/root/os-course/pr01
Практическая работа №1
Знакомство с терминалом Linux
total 12
drwxr-xr-x 2 root root 4096 Oct 27 04:55 .
drwxr-xr-x 3 root root 4096 Oct 27 04:55 ..
-rw-r--r-- 1 root root   94 Oct 27 04:55 about.txt
!sudo apt-get update -qq
!sudo apt-get install -y git python3 build-essential
!git --version
!python3 --version
!ls -la about.txt
!stat about.txt
W: Skipping acquire of configured file 'main/source/Sources' as repository 'https://r2u.stat.illinois.edu/ubuntu noble InRelease' does not seem to provide it (sources.list entry misspelt?)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
git is already the newest version (1:2.43.0-1ubuntu7.4).
python3 is already the newest version (3.12.3-0ubuntu2.1).
python3 set to manually installed.
build-essential is already the newest version (12.10ubuntu1).
0 upgraded, 0 newly installed, 0 to remove and 17 not upgraded.
git version 2.43.0
Python 3.13.16
-rw-r--r-- 1 root root 94 Oct 27 04:55 about.txt
  File: about.txt
  Size: 94        	Blocks: 8          IO Block: 4096   regular file
Device: 0,55	Inode: 4068865     Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2026-10-27 04:55:40.610886998 +0000
Modify: 2026-10-27 04:55:40.504887056 +0000
Change: 2026-10-27 04:55:40.504887056 +0000
 Birth: 2026-10-27 04:55:40.400887113 +0000
 %%bash
mkdir -p /root/os-course/pr01
cd /root/os-course/pr01

{
  echo "# Практическая работа №1"
  echo "## Диагностическое тестирование. Linux и терминал"
  echo
  echo "### 1. Информация об окружении"
  echo '```text'
  whoami
  pwd
  uname -a
  lsb_release -a 2>&1
  echo '```'
  echo
  echo "### 2. Создание файла"
  echo '```text'
  echo 'Практическая работа №1' > about.txt
  echo 'Знакомство с терминалом Linux' >> about.txt
  cat about.txt
  echo '```'
  echo
  echo "### 3. Список файлов"
  echo '```text'
  ls -la
  echo '```'
  echo
  echo "### 4. Пояснение столбцов ls -la"
  echo "1. Тип объекта и права доступа."
  echo "2. Количество жестких ссылок."
  echo "3. Владелец файла."
  echo "4. Группа файла."
  echo "5. Размер файла в байтах."
  echo "6–8. Дата и время последнего изменения."
  echo "9. Имя файла."
  echo
  echo "### 5. Установка и проверка инструментов"
  echo '```text'
  git --version
  python3 --version
  g++ --version | head -n 1
  echo '```'
  echo
  echo "### 6. Вывод"
  echo "В облачной среде Google Colab выполнены базовые команды Linux,"
  echo "создан текстовый файл и проверена информация о файлах."
  echo
  echo "Примечание: проверка выполнена в Google Colab, а не в локальной"
  echo "установке Ubuntu. При необходимости локальную среду нужно проверить отдельно."
} > README.md

cat README.md
# Практическая работа №1
## Диагностическое тестирование. Linux и терминал

### 1. Информация об окружении
```text
root
/root/os-course/pr01
Linux d82fcbdff524 6.6.159+ #1 SMP Thu Oct 22 03:07:54 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04.5 LTS
Release:	24.04
Codename:	noble
```

### 2. Создание файла
```text
Практическая работа №1
Знакомство с терминалом Linux
```

### 3. Список файлов
```text
total 16
drwxr-xr-x 2 root root 4096 Oct 27 04:57 .
drwxr-xr-x 3 root root 4096 Oct 27 04:55 ..
-rw-r--r-- 1 root root   94 Oct 27 04:57 about.txt
-rw-r--r-- 1 root root  587 Oct 27 04:57 README.md
```

### 4. Пояснение столбцов ls -la
1. Тип объекта и права доступа.
2. Количество жестких ссылок.
3. Владелец файла.
4. Группа файла.
5. Размер файла в байтах.
6–8. Дата и время последнего изменения.
9. Имя файла.

### 5. Установка и проверка инструментов
```text
git version 2.43.0
Python 3.13.16
g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
```

### 6. Вывод
В облачной среде Google Colab выполнены базовые команды Linux,
создан текстовый файл и проверена информация о файлах.

Примечание: проверка выполнена в Google Colab, а не в локальной
установке Ubuntu. При необходимости локальную среду нужно проверить отдельно.
from google.colab import files
files.download('/root/os-course/pr01/README.md')
