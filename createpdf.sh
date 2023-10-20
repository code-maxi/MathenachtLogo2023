echo 'creating tex file...'
/usr/bin/python3 /home/maxi/Programmieren/Mathnacht2023Logo/fibonacci.py > /home/maxi/Programmieren/Mathnacht2023Logo/fibonacci_rabbits.tex
echo 'creating pdf...'
lualatex -synctex=1 -interaction=nonstopmode --shell-escape /home/maxi/Programmieren/Mathnacht2023Logo/fibonacci_rabbits.tex 