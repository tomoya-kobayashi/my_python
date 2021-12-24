from skimage import io, segmentation, color
img = io.imread("C:\\Users\\mieli\\my_python\\img\\cat1.jpeg")
label = segmentation.slic(img, compactness=20, start_label=1)
out = color.label2rgb(label, img, kind = 'avg', bg_label=0)
io.imsave("C:\\Users\\mieli\\my_python\\img\\cat1_slic.jpeg", out)

print(type(img))
print(type(out))