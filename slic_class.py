"""
SLIC implementation in Python 3
"""
import sys, math
import numpy as np
from skimage import io, color
import cv2


class SLIC:

    def __init__(self, k, m = 20):
        """ Constructor.
        k: the number of superpixels.
        m: a parameter to weigh the relative importance of spatial proximity.
        """
        self.k = k
        self.m = m
        self.iter_max = 10 # c.f. the paper.


    def fit(self, image_cv2):
        """ Calculate superpixels.
        Returns the mask array.
        """
        # self.img_path = img_path
        self.fit_init(image_cv2)
        self.fit_iter()
        return self.l


    def fit_init(self, image_cv2):
        """
        Read the image from img_path,
        convert to Lab color space,
        and initialize cluster centers.
        """
        # img_rgb = io.imread(img_path)
        img_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
        if img_rgb.ndim != 3 or img_rgb.shape[2] != 3:
            raise Exception("Non RGB file. The shape was {}.".format(img_rgb.shape))
        img_lab = color.rgb2lab(img_rgb)
        self.height = img_lab.shape[0]
        self.width = img_lab.shape[1]
        self.pixels = []
        for h in range(self.height):
            for w in range(self.width):
                self.pixels.append(np.array([img_lab[h][w][0], img_lab[h][w][1], img_lab[h][w][2], h, w]))
        self.size = len(self.pixels)
        # Initialize cluster centers to be regularly spaced.
        self.cluster_center = []
        k_w = int(math.sqrt(self.k * self.width / self.height)) + 1
        k_h = int(math.sqrt(self.k * self.height / self.width)) + 1
        for h_cnt in range(k_h):
            h = (2 * h_cnt + 1) * self.height // (2 * k_h)
            for w_cnt in range(k_w):
                w = (2 * w_cnt + 1) * self.width // (2 * k_w)
                self.cluster_center.append(self.pixels[h*self.width + w])
        self.k = k_w*k_h
        self.l = [None] * self.size # The cluster labels
        self.d = [math.inf] * self.size # The distance between a pixel and the nearest cluster center
        self.S = int(math.sqrt(self.size/self.k)) # The approximate distance between cluster centers
        self.metric = np.diagflat([1/(self.m**2)]*3 +  [1/(self.S**2)]*2)


    def fit_iter(self):
        """ Iteration step.
        """
        for iter_cnt in range(self.iter_max):
            for center_idx, center in enumerate(self.cluster_center):
                for h in range(max(0, int(center[3])-self.S), min(self.height, int(center[3])+self.S)):
                    for w in range(max(0, int(center[4])-self.S), min(self.width, int(center[4])+self.S)):
                        d = self.distance(self.pixels[h*self.width + w], center)
                        if d < self.d[h*self.width + w]:
                            self.d[h*self.width + w] = d
                            self.l[h*self.width + w] = center_idx
            self.calc_new_center()


    def distance(self, x, y):
        return (x-y).dot(self.metric).dot(x-y)
        self.iter_max = 10 # c.f. the paper.


    def fit(self, image_cv2):
        """ Calculate superpixels.
        Returns the mask array.
        """
        self.fit_init(image_cv2)
        self.fit_iter()
        return self.l


    def fit_init(self, image_cv2):
        """
        Read the image from img_path,
        convert to Lab color space,
        and initialize cluster centers.
        """
        # img_rgb = io.imread(img_path)
        img_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
        if img_rgb.ndim != 3 or img_rgb.shape[2] != 3:
            raise Exception("Non RGB file. The shape was {}.".format(img_rgb.shape))
        img_lab = color.rgb2lab(img_rgb)
        self.height = img_lab.shape[0]
        self.width = img_lab.shape[1]
        self.pixels = []
        for h in range(self.height):
            for w in range(self.width):
                self.pixels.append(np.array([img_lab[h][w][0], img_lab[h][w][1], img_lab[h][w][2], h, w]))
        self.size = len(self.pixels)
        # Initialize cluster centers to be regularly spaced.
        self.cluster_center = []
        k_w = int(math.sqrt(self.k * self.width / self.height)) + 1
        k_h = int(math.sqrt(self.k * self.height / self.width)) + 1
        for h_cnt in range(k_h):
            h = (2 * h_cnt + 1) * self.height // (2 * k_h)
            for w_cnt in range(k_w):
                w = (2 * w_cnt + 1) * self.width // (2 * k_w)
                self.cluster_center.append(self.pixels[h*self.width + w])
        self.k = k_w*k_h
        self.l = [None] * self.size # The cluster labels
        self.d = [math.inf] * self.size # The distance between a pixel and the nearest cluster center
        self.S = int(math.sqrt(self.size/self.k)) # The approximate distance between cluster centers
        self.metric = np.diagflat([1/(self.m**2)]*3 +  [1/(self.S**2)]*2)


    def fit_iter(self):
        """ Iteration step.
        """
        for iter_cnt in range(self.iter_max):
            for center_idx, center in enumerate(self.cluster_center):
                for h in range(max(0, int(center[3])-self.S), min(self.height, int(center[3])+self.S)):
                    for w in range(max(0, int(center[4])-self.S), min(self.width, int(center[4])+self.S)):
                        d = self.distance(self.pixels[h*self.width + w], center)
                        if d < self.d[h*self.width + w]:
                            self.d[h*self.width + w] = d
                            self.l[h*self.width + w] = center_idx
            self.calc_new_center()


    def distance(self, x, y):
        """ Squared distance between x and y.
        """
        return (x-y).dot(self.metric).dot(x-y)


    def calc_new_center(self):
        """ Caluclate new cluster centers.
        """
        cnt = [0] * self.k
        new_cluster_center = [np.array([0., 0., 0., 0. ,0.]) for _ in range(self.k)]
        for i in range(self.size):
            new_cluster_center[self.l[i]] += self.pixels[i]
            cnt[self.l[i]] += 1
        for i in range(self.k):
            new_cluster_center[i] /= cnt[i]
        self.cluster_center = new_cluster_center


    def transform(self):
        """ Returns new image RGB ndarray """
        cnt = [0] * self.k
        cluster_color = [np.array([0., 0., 0.]) for _ in range(self.k)]
        for i in range(self.size):
            cluster_color[self.l[i]] += self.pixels[i][:3]
            cnt[self.l[i]] += 1
        for i in range(self.k):
            cluster_color[i] /= cnt[i]
        new_img_lab = np.zeros((self.height, self.width, 3))
        for h in range(self.height):
            for w in range(self.width):
                new_img_lab[h][w] = cluster_color[self.l[h*self.width + w]]

        # print("self.l:" + str(len(self.l)))
        # print("self.d:" + str(len(self.d)))
        # print("self.k:" + str(self.k))
        # print("self.pixels:" + str(self.pixels))
        # print("self.size:" + str(self.size))
        # print("self.metrics:" + str(len(self.metrics)))

        return color.lab2rgb(new_img_lab)


    def segment_saliency(self, img_path):
        """ Returns new image saliency ndarray """

        img = cv2.imread(img_path)

        # サリエンシーディテクション
        saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
        bool, map = saliency.computeSaliency(img)
        out = (map * 255).astype("uint8")

        ### save saliency map
        # io.imsave("img\\saliency_out.jpeg", out)


        # outの一次元化
        self.saliency_out_1 = []
        for h in range(self.height):
            for w in range(self.width):
                self.saliency_out_1.append(np.array(out[h][w]))

        ### test
        # print(out)
        # print(type(out))
        # print(len(out))
        # print(self.saliency_out_1)
        # print(len(self.saliency_out_1))


        cnt = [0] * self.k
        # cluster_saliency = [np.array([0.]) for _ in range(self.k)]
        cluster_saliency = np.zeros(self.k)
        for i in range(self.size):
            # cluster_saliency[self.l[i]] += self.pixels[i][:3]
            cluster_saliency[self.l[i]] += self.saliency_out_1[i]
            cnt[self.l[i]] += 1
        for i in range(self.k):
            cluster_saliency[i] /= cnt[i]
        new_img_saliency = np.zeros((self.height, self.width))
        for h in range(self.height):
            for w in range(self.width):
                new_img_saliency[h][w] = cluster_saliency[self.l[h*self.width + w]]


        # return color.lab2rgb(new_img_saliency)
        return new_img_saliency



# slic = SLIC(k = 100)
# img = io.imread("img\\ramen.jpeg")
# slic.fit(img)
# res = slic.transform()
# # saliency = slic.segment_saliency("img\\ramen.jpeg")
# io.imsave("img\\test.jpeg", res)

# io.imshow(res)
# io.imsave("img\\out.jpeg", res)
