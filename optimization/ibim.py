import numpy as np
import random





deflection_max=10

#单位钢材造价
p=4500
density=7850 #kg/m^3


#单位长度焊缝造价 HKD/mm
psmaw=0.05497
pgmaw=0.03855
pfcaw=0.03566
psaw=0.04105

#单位长度坡口时间 min/mm
bevel_time_atlength=0.05
#bevel_time_attimes=10

#单位焊接时间 min/mm
welding_time=0.02


def weld_judge(value, low_threshold, high_threshold):
    #工艺判断
    if value < low_threshold:
        return pgmaw
    elif low_threshold <= value <= high_threshold:
        return psmaw
    else:
        return pfcaw
    

def bevel_judge(value, low_threshold, high_threshold):
    #开坡口判断
    if value < low_threshold:
        return 0
    elif low_threshold <= value <= high_threshold:
        return 1
    else:
        return 2


class IBeam:
    def __init__(self, length,height, width, flange_thickness, web_thickness, elastic_modulus, ):
        # 几何属性
        self.height = height  # 工字钢的高度
        self.length = length  # 工字钢的高度
        self.width = width  # 工字钢的宽度
        self.flange_thickness = flange_thickness  # 翼缘的厚度
        self.web_thickness = web_thickness  # 腹板的厚度
        self.beamcoding = np.array([1,0,0,0])

        
        # 坡口长度判断
        self.bevel_length = bevel_judge(self.flange_thickness,8,16)*(self.width*2-self.web_thickness)+(self.height - 2 * self.flange_thickness)*bevel_judge(self.web_thickness,8,16)
        # 焊缝长度
        self.welding_length = self.height * 2 + self.width * 4 - self.web_thickness * 2 -self.flange_thickness*4
        
        # 材料属性
        self.elastic_modulus = elastic_modulus  # 弹性模量
        
        # 计算几何矩
        self.area = self.calculate_area()  # 面积
        self.moment_of_inertia = self.calculate_moment_of_inertia()  # 惯性矩
        
    def calculate_area(self):
        # 计算翼缘面积和腹板面积
        flange_area = self.width * self.flange_thickness
        web_area = self.web_thickness * (self.height - 2 * self.flange_thickness)
        return 2 * flange_area + web_area
    
    def price(self):
        #计算钢材成本 单位
        flange_area = (self.width/1000) * (self.flange_thickness/1000)
        web_area = (self.web_thickness/1000) * ((self.height - 2 * self.flange_thickness)/1000)
        return (2 * flange_area + web_area)*(self.length/1000)*p*density
    
    
    def volume (self):
        #计算钢梁体积用于重量分布 m^3（待添加荷载）
        flange_area = (self.width/1000) * (self.flange_thickness/1000)
        web_area = (self.web_thickness/1000) * ((self.height - 2 * self.flange_thickness)/1000)
        volume = (2 * flange_area + web_area)*self.length/1000
    

    def calculate_welding(self):
        #计算焊缝长度 mm
        welding_length = self.height * 2 + self.width * 4 - self.web_thickness * 2 

        return welding_length
    
    def bevellength(self):

        #计算坡口长度 mm

        

        return self.bevel_length
    

    def weldtime(self):

        #计算焊接总时间 min

        twelding = self.bevel_length*bevel_time_atlength+self.welding_length*welding_time
        return twelding
    






    
    def calculate_weldprice(self):

        #  计算焊接总成本  HKD
        
        weld_price=  (self.width * 4 - self.web_thickness * 2 )*weld_judge(self.flange_thickness,8,32)
        +(self.height-2*self.flange_thickness)*2*weld_judge(self.web_thickness,8,32)
        
        
        

        return weld_price


    
        
    
    def calculate_moment_of_inertia(self):
        
        # 翼缘对中性轴的惯性矩
        flange_inertia = (self.width * self.flange_thickness**3) / 12
        # 腹板对中性轴的惯性矩
        web_inertia = (self.web_thickness * (self.height - 2 * self.flange_thickness)**3) / 12
        return 2 * flange_inertia + web_inertia
    
    
    #原挠度计算
    """"
    def calculate_deflection(self, force):
        
        return (force * self.length**3) / (3 * self.elastic_modulus * self.moment_of_inertia)
    

    def check(self):
        if deflection_max>self.calculate_deflection(500):
            return True
        else:
            return False
    """

    
    



