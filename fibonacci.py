import random
import math
config = {
    'sizefac': 0.8,
    'sizezoom': 2.5,
    'zoomindex': 4,
    'nodedotsize': 0.2,
    'yoff': 0.5,
    'pagewidth': 19,
    'nodeshrink': 0.6,
    'unit': 'cm'
}
class RabbitCouple:
    def __init__(self, t, m, r) -> None:
        self.traechtig = t
        self.month = m
        self.random = r
        self.children: list = []
        self.maxmoth = 1

    def domonth(self):
        self.maxmoth += 1
        if len(self.children) > 0:
            for child in self.children: child.domonth()
        else:
            self.children.append(RabbitCouple(True, self.month+1, self.random))
            if self.traechtig: self.children.append(RabbitCouple(False, self.month+1, abs(self.random-1)))
    
    def __str__(self) -> str:
        return f'RabbitCouple[{self.traechtig}, {self.month}]'

    def printMe(self):
        print(self)
        for child in self.children: 
            child.printMe()

    def childrenOfMoth(self, m):
        if self.month == m: return [self]
        else:
            res = []
            for child in self.children:
                res += child.childrenOfMoth(m)
            return res
    
    def tikznode(self, x, y, node):
        return "\\node ("+str(id(self))+") at ("+str(round(x, 3))+config['unit']+","+str(round(y, 3))+config['unit']+") "+node+";\n"
    
    def tikzline(self):
        res = ""
        for child in self.children:
            res += "\\draw[ultra thick] ("+str(id(self))+") -- ("+str(id(child))+");\n"
        return res
    
    def tikzpicture(self):
        result = '\\begin{tikzpicture}\n'
        minsize = config['pagewidth']/len(self.childrenOfMoth(self.maxmoth))
        #nthroot = len(self.childrenOfMoth(self.maxmoth))
        #sizefac = math.pow(config['sizezoom'], 1/(nthroot))
        for node in [True, False]:
            ypos = 0
            for m in range(1,self.maxmoth+1):
                monthChildren = self.childrenOfMoth(m)
                for ix in range(len(monthChildren)):
                    size = minsize*(1 + (config['sizezoom']-1)*((self.maxmoth-m))/self.maxmoth)
                    image = "{\\includesvg[width="+str(round(size*config['sizefac'], 3))+config['unit']+"]{svgrabbit"+("T" if monthChildren[ix].traechtig else "N")+("M" if monthChildren[ix].random > 0.5 else "N")+".svg}}"
                    nodedot = "[inner sep="+str(config['nodedotsize'])+"cm, shape=circle, "+("fill" if monthChildren[ix].traechtig else "draw")+"=black, ultra thick] {}"
                    result += monthChildren[ix].tikznode(
                        size*(ix - len(monthChildren)/2), ypos,
                        image if m <= config['zoomindex'] or m == self.maxmoth else nodedot
                    ) if node else monthChildren[ix].tikzline()
                ypos -= (size+config['yoff']) * (config['nodeshrink'] if m > config['zoomindex'] and m < self.maxmoth-1 >= self.maxmoth-1 else 1)
        result += '\\end{tikzpicture}'
        return result



couple = RabbitCouple(False, 1, 0)
for i in range(6): couple.domonth()
#couple.printMe()
print(
"""
\\documentclass{article}
\\usepackage[a4paper, top=1cm, bottom=1cm, left=1cm, right=1cm]{geometry}
\\usepackage{svg}
\\usepackage{graphicx} % Required for inserting images
\\usepackage{mathptmx}
\\usepackage[charter]{mathdesign}
\\usepackage{fontspec}
\\setmainfont{XCharter}
\\usepackage{polyglossia}
\\setdefaultlanguage[spelling=new]{german}
\\usepackage{tikz}
\\begin{document}
\\begin{center}
""" + couple.tikzpicture() +
"""
\\end{center}
\\vspace*{1cm}
\hfill\\textbf{\\fontsize{35}{\\baselineskip}\\selectfont 13. Mathenacht}
\\vspace*{.25cm}

\\hfill\\Huge am Kolleg
\\end{document}
"""
)