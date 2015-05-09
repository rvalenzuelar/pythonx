
# Source:
# 1) http://www.rkblog.rk.edu.pl/w/p/qgraphicsview-and-qgraphicsscene/
# 2) http://stackoverflow.com/questions/12433491/is-this-pyqt-4-python-bug-or-wrongly-behaving-code

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg


app = QApplication(sys.argv)

#----------------------------------------------------
"""
Make sure objects are contained within other objects so 
that when they are deleted there is no error message
(see Source #2 )
"""
grview = QGraphicsView()
scene = QGraphicsScene(grview)
#--------------------------------------------------

scene.addPixmap(QPixmap('profile_2001-01-23_21:40:30_fore.png'))
grview.setScene(scene)

grview.show()

sys.exit(app.exec_())