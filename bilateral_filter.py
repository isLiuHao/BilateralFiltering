from PIL import Image
import matplotlib.pyplot as plt
import math
import copy
import time

class BilateralFilter(object):
    """
    定义双边滤波器类：通过空间域和值域进行滤波
    变量：
        ds：distance sigma
        rs: range sigma
        c_weight_table：定义域核
        s_weight_table: 值域核
        radius: 模块半径，即模块大小为（2*radius+1）
    """

    def __init__(self, ds, rs, radiu):
        """初始化变量"""
        self.ds = ds
        self.rs = rs
        self.c_weight_table = []
        self.s_weight_table = []
        self.radius = radiu

    def build_distance_weight_table(self):
        """定义空间域核"""
        #        size = 2 * self.radius + 1
        for semi_row in range(-self.radius, self.radius + 1):
            self.c_weight_table.append([])
            for semi_col in range(-self.radius, self.radius + 1):
                # calculate Euclidean distance between center point and close pixels
                delta = -(semi_row * semi_row + semi_col * semi_col) / (2 * (self.ds ** 2))
                self.c_weight_table[semi_row + self.radius].append(
                    math.exp(delta))

    def build_similarity_weight_table(self):
        """定义值域核"""
        for i in range(256):  # since the color scope is 0 ~ 255
            delta = -(i * i) / (2 * (self.rs ** 2))
            self.s_weight_table.append(math.exp(delta))

    def clamp(self, p):
        """return RGB color between 0 and 255"""
        if p < 0:
            return 0
        elif p > 255:
            return 255
        else:
            return p

    def bilateral_filter(self, src):
        """ 
        双边滤波器的方法：对原始图进行双边滤波，并返回滤波过后的图
        """

        height = src.size[0]
        width = src.size[1]
        radius = self.radius
        self.build_distance_weight_table()
        self.build_similarity_weight_table()
        in_pixels = src.load()
        raw_data = []
        out_data = copy.deepcopy(src)
        red_sum = green_sum = blue_sum = 0
        cs_sum_red_weight = cs_sum_green_weight = cs_sum_blue_weight = 0
        # 边缘像素不滤波
        for row in range(radius, height - radius):
            for col in range(radius, width - radius):
                # 对每个像素进行滤波
                tr = in_pixels[row, col][0]
                tg = in_pixels[row, col][1]
                tb = in_pixels[row, col][2]
                raw_data.append((tr, tg, tb))
                for semi_row in range(-radius, radius + 1):
                    for semi_col in range(-radius, radius + 1):
                        # 获得模块内的像素
                        row_offset = row + semi_row
                        col_offset = col + semi_col
                        tr2 = in_pixels[row_offset, col_offset][0]
                        tg2 = in_pixels[row_offset, col_offset][1]
                        tb2 = in_pixels[row_offset, col_offset][2]
                        # 卷积计算
                        cs_red_weight = (
                                self.c_weight_table[semi_row + radius][semi_col + radius]
                                * self.s_weight_table[(abs(tr2 - tr))]
                        )
                        cs_green_weight = (
                                self.c_weight_table[semi_row + radius][semi_col + radius]
                                * self.s_weight_table[(abs(tg2 - tg))]
                        )
                        cs_blue_weight = (
                                self.c_weight_table[semi_row + radius][semi_col + radius]
                                * self.s_weight_table[(abs(tb2 - tb))]
                        )

                        cs_sum_red_weight += cs_red_weight
                        cs_sum_blue_weight += cs_blue_weight
                        cs_sum_green_weight += cs_green_weight

                        red_sum += cs_red_weight * float(tr2)
                        green_sum += cs_green_weight * float(tg2)
                        blue_sum += cs_blue_weight * float(tb2)

                # 归一化过程
                tr = int(math.floor(red_sum / cs_sum_red_weight))
                tg = int(math.floor(green_sum / cs_sum_green_weight))
                tb = int(math.floor(blue_sum / cs_sum_blue_weight))

                temp_rgb = (self.clamp(tr), self.clamp(tg), self.clamp(tb))
                out_data.putpixel((row, col), temp_rgb)

                red_sum = green_sum = blue_sum = 0
                cs_red_weight = cs_green_weight = cs_blue_weight = 0
                cs_sum_red_weight = cs_sum_blue_weight = cs_sum_green_weight = 0
        return out_data


def main():
    try:
        flag = 1
        while flag == 1:
            image_path = input("输入滤波的图片路径：")
            image = str(image_path)
            img0 = Image.open(image)
            file = image[0:image.index('.')]

            flag1 = 1
            count = 1
            plt.figure(figsize=(18, 12))
            plt.subplot(2, 2, 1)
            plt.title("Origin", fontsize=20)
            plt.imshow(img0)
            plt.axis('off')
            while flag1 == 1 and count < 4:
                ds = input("请输入空间域sigma：")
                rs = input("请输入值域sigma：")
                radius = input("请输入模块半径：")
                tim1 = time.time()
                bf = BilateralFilter(int(ds), int(rs), int(radius))
                dest = bf.bilateral_filter(img0)
                dest.save(file + '_out_' + str(count) + '.jpg')
                tim2 = time.time() - tim1
                ti = str(tim2)
                count += 1
                plt.subplot(2, 2, count)
                plt.title('d=' + ds + ',r=' + rs + ',m=' + radius + 'time=' + ti[0:5], fontsize=20)
                plt.imshow(dest)
                plt.axis('off')
                ans = input("是否继续输入不同sigma值(y/n)：")
                if ans == 'y' or ans == 'Y':
                    flag1 = 1

                else:
                    flag1 = 0
                    count = 1

            ans = input("是否显示不同距离的对比图(y/n)：")
            if ans == 'y' or ans == 'Y':
                plt.show()

            ans = input("是否继续选择图片滤波(y/n)：")
            if ans == 'y' or ans == 'Y':
                flag = 1
            else:
                flag = 0

    except IOError:
        print("该路径找不到图像文件")


if __name__ == '__main__':
    main()
