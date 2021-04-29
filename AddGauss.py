from PIL import Image
from pylab import *
import random

def main():
    # 读取图片并转为数组
    tmp = input('输入加噪图片路径：')
    try:
        im = array(Image.open(tmp))
        # 设定高斯函数的偏移
        means = 0

        # 设定高斯函数的标准差
        tmp1 = input('请输入加噪sigma值：')
        sigma = int(tmp1)

        # r通道
        r = im[:, :, 0].flatten()
        # g通道
        g = im[:, :, 1].flatten()
        # b通道
        b = im[:, :, 2].flatten()

        # 计算新的像素值
        for i in range(im.shape[0] * im.shape[1]):
            pr = int(r[i]) + random.gauss(0, sigma)
            pg = int(g[i]) + random.gauss(0, sigma)
            pb = int(b[i]) + random.gauss(0, sigma)

            if pr < 0:
                pr = 0
            if pr > 255:
                pr = 255
            if pg < 0:
                pg = 0
            if pg > 255:
                pg = 255
            if pb < 0:
                pb = 0
            if pb > 255:
                pb = 255

            r[i] = pr
            g[i] = pg
            b[i] = pb

        im[:, :, 0] = r.reshape([im.shape[0], im.shape[1]])
        im[:, :, 1] = g.reshape([im.shape[0], im.shape[1]])
        im[:, :, 2] = b.reshape([im.shape[0], im.shape[1]])

        # 显示图像
        imshow(im)
        im1 = Image.fromarray(im)
        im1.save(tmp[0:tmp.index('.')] + '_' + tmp1 + '.jpg')
        show()
        #
    except IOError:
        print('请输入正确的图片路径！')

if __name__ == '__main__':
    main()