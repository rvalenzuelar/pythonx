
# source:
# https://groups.google.com/forum/#!msg/pyqtgraph/vdYXled3uBU/9ZejuB8o8pwJ

import pyqtgraph as pg
import numpy as np

## build a QApplication before building other widgets
app=pg.mkQApp()
win = pg.GraphicsLayoutWidget()
win.show()

vb = win.addViewBox()
vb.setAspectLocked()
grad = pg.GradientEditorItem(orientation='right')
win.addItem(grad, 0, 1)
img = pg.ImageItem()
vb.addItem(img)


def update():
    lut = grad.getLookupTable(512)
    img.setLookupTable(lut)

grad.sigGradientChanged.connect(update)

img.setImage(np.random.normal(size=(100,100)))

app.exec_()