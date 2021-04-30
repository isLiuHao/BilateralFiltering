from PIL import Image
import matplotlib.pyplot as plt
import math
import copy
import time

# 双边滤波器类
class bilateral_filter(object):
    # 初始化
    def __init__(self, s_sigma, v_sigma, radius):
        self.s_sigma = s_sigma          # 空间域sigma
        self.v_sigma = v_sigma          # 值域sigma
        self.s_weight = []              # 定义域权重
        self.v_weight = []              # 值域权重
        self.radius = radius            # 滤波邻域半径

    # 通道为0-255
    @staticmethod
    def RGB(pixel):
        if pixel < 0:
            return 0
        elif pixel > 255:
            return 255
        else:
            return pixel

    # 定义空间域权重
    def build_space_weight(self):
        for minor_row in range(-self.radius, self.radius + 1):
            self.s_weight.append([])
            for minor_col in range(-self.radius, self.radius + 1):
                delta = -(minor_row * minor_row + minor_col * minor_col) / (2 * (self.s_sigma ** 2))
                self.s_weight[minor_row + self.radius].append(math.exp(delta))

    # 定义值域权重
    def build_value_weight(self):
        for i in range(256):
            delta = -(i * i) / (2 * (self.v_sigma ** 2))
            self.v_weight.append(math.exp(delta))

    # 双边滤波算法
    def start_filter(self, image):
        height = image.size[0]
        width = image.size[1]
        radius = self.radius
        self.build_space_weight()
        self.build_value_weight()
        pixels = image.load()
        raw_data = []
        out_data = copy.deepcopy(image)
        red_sum = green_sum = blue_sum = 0
        cs_sum_red_weight = cs_sum_green_weight = cs_sum_blue_weight = 0
        # 边缘像素不滤波
        for row in range(radius, height - radius):
            for col in range(radius, width - radius):
                # 对每个像素进行滤波
                pixelR = pixels[row, col][0]
                pixelG = pixels[row, col][1]
                pixelB = pixels[row, col][2]
                raw_data.append((pixelR, pixelG, pixelB))
                for minor_row in range(-radius, radius + 1):
                    for minor_col in range(-radius, radius + 1):
                        # 获得模块内的像素
                        row_offset = row + minor_row
                        col_offset = col + minor_col
                        pixelR2 = pixels[row_offset, col_offset][0]
                        pixelG2 = pixels[row_offset, col_offset][1]
                        pixelB2 = pixels[row_offset, col_offset][2]
                        # 卷积计算
                        cs_red_weight = (
                                self.s_weight[minor_row + radius][minor_col + radius]
                                * self.v_weight[(abs(pixelR2 - pixelR))]
                        )
                        cs_green_weight = (
                                self.s_weight[minor_row + radius][minor_col + radius]
                                * self.v_weight[(abs(pixelG2 - pixelG))]
                        )
                        cs_blue_weight = (
                                self.s_weight[minor_row + radius][minor_col + radius]
                                * self.v_weight[(abs(pixelB2 - pixelB))]
                        )

                        cs_sum_red_weight += cs_red_weight
                        cs_sum_blue_weight += cs_blue_weight
                        cs_sum_green_weight += cs_green_weight

                        red_sum += cs_red_weight * float(pixelR2)
                        green_sum += cs_green_weight * float(pixelG2)
                        blue_sum += cs_blue_weight * float(pixelB2)

                # 归一化过程
                pixelR = int(math.floor(red_sum / cs_sum_red_weight))
                pixelG = int(math.floor(green_sum / cs_sum_green_weight))
                pixelB = int(math.floor(blue_sum / cs_sum_blue_weight))

                temp_rgb = (self.RGB(pixelR), self.RGB(pixelG), self.RGB(pixelB))
                out_data.putpixel((row, col), temp_rgb)

                red_sum = green_sum = blue_sum = 0
                cs_red_weight = cs_green_weight = cs_blue_weight = 0
                cs_sum_red_weight = cs_sum_blue_weight = cs_sum_green_weight = 0
        return out_data

if __name__ == '__main__':
    # 图像地址
    image_Path = "1_20.jpg"
    Origin_image = Image.open(image_Path)
    # 原图
    plt.figure(figsize=(18, 12))
    plt.subplot(2, 2, 1)
    plt.title("Origin", fontsize=20)
    plt.imshow(Origin_image)
    plt.axis('off')
    # 不同参数对比
    for i in range(2,5):
        radius = input("滤波邻域半径设置为：")
        s_sigma = input("空间域sigma设置为：")
        v_sigma = input("值域sigma设置为：")
        print('双边滤波正在处理........')
        start_time = time.time()
        bf = bilateral_filter(int(s_sigma), int(v_sigma), int(radius))
        end_time = time.time()
        timex = str(end_time - start_time)
        dest = bf.start_filter(Origin_image)
        dest.save('BF' + str(i) + '_' + image_Path)
        plt.subplot(2, 2, i)
        plt.title('s_sigma=' + s_sigma + ',v_sigma=' + v_sigma + ',r=' + radius + ',time=' + timex[0:5], fontsize=20)
        plt.imshow(dest)
        plt.axis('off')
        print('双边滤波处理结束，处理时间：' + timex[0:5])
    plt.show()
