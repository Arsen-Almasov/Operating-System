%%writefile stats.sh
#!/usr/bin/env bash

set -u

total=0
max_errors=-1
max_file=""

for f in data/*.log; do
    [[ -f "$f" ]] || continue

    count=$(grep -c "ERROR" "$f" || true)

    total=$((total + count))

    if (( count > max_errors )); then
        max_errors=$count
        max_file=$f
    fi

    printf '%s: %s\n' "$f" "$count"
done

printf '\nTotal ERROR lines: %s\n' "$total"

if [[ -n "$max_file" ]]; then
    printf 'File with most errors: %s (%s)\n' \
        "$max_file" "$max_errors"
else
    printf 'No log files found.\n'
fi
Writing stats.sh
!chmod +x stats.sh
!./stats.sh
Total ERROR lines: 0
No log files found.
!shellcheck stats.sh
/bin/bash: line 1: shellcheck: command not found
!dos2unix stats.sh
!bash -n stats.sh
/bin/bash: line 1: dos2unix: command not found
!mkdir -p results
!strace -c ls > results/ls_output.txt 2> results/strace_ls.txt
!cat results/strace_ls.txt
/bin/bash: line 1: strace: command not found
!strace -c cat data/01.log > /dev/null 2> results/strace_cat.txt
!cat results/strace_cat.txt
/bin/bash: line 1: strace: command not found
!tail -n 25 results/strace_ls.txt
!tail -n 25 results/strace_cat.txt
/bin/bash: line 1: strace: command not found
/bin/bash: line 1: strace: command not found
!strace -e trace=openat cat data/01.log > /dev/null 2> results/strace_openat.txt
!cat results/strace_openat.txt
/bin/bash: line 1: strace: command not found
Ответь на контрольные вопросы
Вопрос 1. Почему нельзя обратиться к диску напрямую из пользовательской программы? Пользовательская программа работает в пользовательском режиме и не имеет права произвольно управлять аппаратными устройствами. Доступ к диску организует операционная система через ядро, драйверы и системные вызовы.

Это необходимо для безопасности, изоляции процессов и правильного распределения ресурсов. Например, программа запрашивает чтение файла, а ядро проверяет права доступа и организует получение данных.
Вопрос 2. Что дороже — вызов функции или системный вызов, и почему? Обычно системный вызов дороже обычного вызова функции.

Обычный вызов функции происходит в рамках выполнения программы: процессор передаёт управление функции, выполняет её код и возвращается обратно.

Системный вызов требует перехода из пользовательского режима в режим ядра. Процессор и операционная система должны обеспечить безопасное выполнение операции с привилегиями ядра, что добавляет накладные расходы.

При этом системный вызов не обязательно вызывает полноценное переключение на другой процесс. Его стоимость зависит от конкретного вызова и условий выполнения.
