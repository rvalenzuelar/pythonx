import xalglib

#
# This example shows how to build models with RBF-ML algorithm. Below
# we assume that you already know basic concepts shown in the example
# on RBF-QNN algorithm.
#
# RBF-ML is a multilayer RBF algorithm, which fits a sequence of models
# with decreasing radii. Each model is fitted with fixed number of
# iterations of linear solver. First layers give only inexact approximation
# of the target function, because RBF problems with large radii are
# ill-conditioned. However, as we add more and more layers with smaller
# and smaller radii, we get better conditioned systems - and more precise models.
#

#
# We have 2-dimensional space and very simple interpolation problem - all
# points are distinct and located at straight line. We want to solve it
# with RBF-ML algorithm. This problem is very simple, and RBF-QNN will
# solve it too, but we want to evaluate RBF-ML and to start from the simple
# problem.
#     X        Y
#     -2       1
#     -1       0
#      0       1
#     +1      -1
#     +2       1
#
model = xalglib.rbfcreate(2, 1)
xy0 = [[-2,0,1],[-1,0,0],[0,0,1],[+1,0,-1],[+2,0,1]]
xalglib.rbfsetpoints(model, xy0)

# First, we try to use R=5.0 with single layer (NLayers=1) and moderate amount
# of regularization.... but results are disappointing: Model(x=0,y=0)=-0.02,
# and we need 1.0 at (x,y)=(0,0). Why?
#
# Because first layer gives very smooth and imprecise approximation of the
# function. Average distance between points is 1.0, and R=5.0 is too large
# to give us flexible model. It can give smoothness, but can't give precision.
# So we need more layers with smaller radii.
xalglib.rbfsetalgomultilayer(model, 5.0, 1, 1.0e-3)
rep = xalglib.rbfbuildmodelnp(model)
print(rep.terminationtype) # expected 1
v = xalglib.rbfcalc2(model, 0.0, 0.0)
print(v) # expected -0.021690

# Now we know that single layer is not enough. We still want to start with
# R=5.0 because it has good smoothness properties, but we will add more layers,
# each with R[i+1]=R[i]/2. We think that 4 layers is enough, because last layer
# will have R = 5.0/2^3 = 5/8 ~ 0.63, which is smaller than the average distance
# between points. And it works!
xalglib.rbfsetalgomultilayer(model, 5.0, 5, 1.0e-3)
rep = xalglib.rbfbuildmodel(model)
print(rep.terminationtype) # expected 1
v = xalglib.rbfcalc2(model, 0.0, 0.0)
print(v) # expected 1.000000

# BTW, if you look at v, you will see that it is equal to 0.9999999997, not to 1.
# This small error can be fixed by adding one more layer.