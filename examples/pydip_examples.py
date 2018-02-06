import PyDIP as dip

a = dip.Image((10,20),1)
a.Fill(3)
b = a[0:4,4:-1]
b.Fill(55)
a[:3,:10] = 100
a[5:7,10:15] = 200
a.Show('normal')

m = a>=100
m.Show()

a[m].Show('normal')

a[m] = 176
a.Show('normal')

###

from scipy import misc
f = misc.face()
a = dip.Image(f)
a.Show()

b = dip.Uniform(a,15)
b.Convert("UINT8")
b.Show()

###

img = dip.ImageReadICS('cermet')
grad = dip.GradientMagnitude(img,[5]) # TODO: fix syntax: allow scalar as sigma
grad.Show()

a = dip.Watershed(grad)
a.Show()

import numpy as np
seeds = dip.Image(np.random.random(list(reversed(img.Sizes()))))>0.999
b = dip.SeededWatershed(grad,seeds,flags={"labels"})
b.Show()

smooth = dip.Gauss(img,[5])
seeds = dip.Minima(smooth)
b = dip.SeededWatershed(grad,seeds,flags={"labels"})
b.Show()

mask = img < 120
b = dip.SeededWatershed(smooth,seeds,mask,flags={"labels","uphill only"})
b.Show('labels')


###

img = dip.ImageReadTIFF('erika')
h,b = dip.Histogram(img)
import matplotlib.pyplot as pp
pp.clf()
pp.plot(b[0],h)
pp.show(block=False)

###

img = dip.ImageReadTIFF('erika')
x = dip.Gradient(dip.Norm(img))
x.Show()

y = x*dip.Transpose(x)
y.Show()

###

a = dip.Image((20,10),3)
dip.FillXCoordinate(a.TensorElement(0))
dip.FillYCoordinate(a.TensorElement(1))
dip.FillColoredNoise(a.TensorElement(2))
a.Show()

a.SetColorSpace('rgb')
b = dip.ColorSpaceManager.Convert(a,'Lab')
b.Show()

b.TensorElement(1).Show()

b,c = dip.Histogram(a)
print(len(c))
print(b.Dimensionality() == len(c))

a = dip.Image((250,260),3)
a.Fill(0)
import random
color = list([1.0,1.5,0.5])
for ii in range(0,1000):
   random.shuffle(color)
   dip.DrawBandlimitedPoint(a,[random.uniform(-2,252),random.uniform(-2,262)],color,[random.uniform(1,3),random.uniform(1,3)])

a.Show()

###

a = dip.ImageReadICS('cermet')
a.SetPixelSize(dip.PixelSize(dip.PhysicalQuantity(1,"um")))
b = dip.Label(a < 120)
dip.MeasurementTool.Features()
m = dip.MeasurementTool.Measure(b,a,['Size','Feret','Convexity','Statistics'])
print(m)
print(m['Feret'][50][2])
dip.WriteCSV(m,'test.csv')
dip.WriteCSV(m,'test2.csv',{'unicode','simple'})

b = dip.EuclideanSkeleton(a > 120)
dip.GetEndPixels(b).Show()
dip.GetLinkPixels(b).Show()
dip.GetBranchPixels(b).Show()

###

a = dip.ImageReadICS('cermet')
b = dip.Label(a < 120)
b.Show('labels')
dip.GetObjectLabels(b)
c = dip.SmallObjectsRemove(b, 150)
c.Show('labels')
dip.GetObjectLabels(c)
d = dip.Relabel(c)
d.Show('labels')
dip.GetObjectLabels(d)

###

mask = dip.Image([70,70],1,'BIN')
mask.Fill(0)
dip.DrawEllipsoid(mask,[40,50],[30,40])
dip.DrawEllipsoid(mask,[4,5],[40,40],[0])

seed = dip.Image([70,70],1,'BIN')
seed.Fill(0)
dip.DrawBox(seed,[5,70],[20,35])
dip.DrawLine(seed,[14,28],[35,28])
dip.DrawLine(seed,[14,30],[35,30])
dip.DrawLine(seed,[14,40],[35,40])

dip.BinaryPropagation(seed,mask,1,25).Show()
dip.ConditionalThickening2D(seed,mask,25).Show()

import timeit
a = dip.BinaryPropagation(seed,mask,1,0)
b = dip.MorphologicalReconstruction(seed,mask,1)
print(dip.All(a==b)[0][0])
timeit.timeit("dip.BinaryPropagation(seed,mask,1,0)", number=1000, globals=globals())
timeit.timeit("dip.MorphologicalReconstruction(seed,mask,1)", number=1000, globals=globals())

###

a = dip.Image([10,11],1,'UINT8')
a.Fill(0)
a[1,1] = 255
a[-2,-2] = 200
a[1,-2] = 150
a[-2,1] = 100
a[0,5] = 50
a[-1,5] = 50
a[5,0] = 40
a[5,-1] = 40
Show(a)

Show(dip.ExtendImage(a,[45,45],['mirror']))
Show(dip.ExtendImage(a,[45,45],['asym mirror']))
Show(dip.ExtendImage(a,[45,45],['periodic']))
Show(dip.ExtendImage(a,[45,45],['asym periodic']))

###

a = dip.ImageReadICS('trui')
b = a.Similar('UINT8')
b.Fill(0)
b[50,120] = 1
b[225,120] = 2
b[161,61] = 3
c = b==0
m = a.Similar('BIN')
m.Fill(1)
dip.DrawEllipsoid(m,[60,30],[70,180],[0])
dip.DrawEllipsoid(m,[20,80],[85,120],[0])
d1 = dip.GreyWeightedDistanceTransform(a,c)
d2 = dip.GreyWeightedDistanceTransform(a,c,m)
Show(dip.Overlay(dip.Overlay(a,~m),~c,[0,200,0]))
Show(d1)
Show(d2)
r1 = dip.GrowRegionsWeighted(b,a)
r2 = dip.GrowRegionsWeighted(b,a,m)
Show(r1)
Show(r2)
r3 = dip.GrowRegions(b)
r4 = dip.GrowRegions(b,m)
Show(r3)
Show(r4)
