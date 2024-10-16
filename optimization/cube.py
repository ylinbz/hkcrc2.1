from ibim import IBeam
import random
import json
import os
#单位长度焊缝造价 HKD/mm

psmaw=0.05497
pgmaw=0.03855
pfcaw=0.03566
psaw=0.04105


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
    




#一些物理常数
density=7850 #kg/m^3
g=9.81 #N/kg
p=4500


#单位长度坡口时间 min/mm
bevel_time_atlength=0.05
#bevel_time_attimes=10

#单位焊接时间 min/mm
welding_time=0.02



def calculate_sectional_inertia(w, h, tw, tf):
    """
    计算工字钢的截面惯性矩。

    参数:
    w -- 底部翼缘的宽度（毫米）
    h -- 整个截面的总高度（毫米）
    tw -- 腹板的厚度（毫米）
    tf -- 翼缘的厚度（毫米）

    返回:
    I -- 截面惯性矩（米^4）
    """
    # 单位转换：毫米转换为米
    w_m = w / 1000
    h_m = h / 1000
    tw_m = tw / 1000
    tf_m = tf / 1000

    # 腹板惯性矩
    hw_m = h_m - 2 * tf_m  # 腹板的有效高度
    I_web = (tw_m * hw_m**3) / 12

    # 翼缘惯性矩
    I_flange = (w_m * tf_m**3) / 12
    # 使用平行轴定理调整翼缘惯性矩
    d = (h_m / 2 - tf_m / 2)  # 翼缘中心到截面中性轴的距离
    A_flange = w_m * tf_m  # 翼缘面积
    I_flange_adjusted = I_flange + A_flange * d**2

    # 总惯性矩：两个翼缘和一个腹板
    I_total = 2 * I_flange_adjusted + I_web

    return I_total

#长宽高，腹板翼板最大值限制 mm   来源中建海龙及港府运输手册
length_max=12000
width_max=4500
height_max=4900
flange_thickness_max=500
web_thickness_max=500
beam_height_max= 500
beam_width_max=500


#随机生成长宽高，腹板翼板厚度，跨度1mm
length = random.randrange(0, length_max, 1)  
width = random.randrange(0, width_max, 1) 
height = random.randrange(0, height_max, 1) 
beam_height = random.randrange(0, beam_height_max, 1) 
beam_width = random.randrange(0, beam_width_max, 1) 
flange_thickness =random.randrange(0, flange_thickness_max, 1) 
web_thickness = random.randrange(0, web_thickness_max, 1) 

#deflection_max=10

#构建长宽高方向所用beam类型
width_bim = IBeam(width,beam_height, beam_width, flange_thickness, web_thickness, elastic_modulus=2.1e11)
height_bim = IBeam(height,beam_height, beam_width, flange_thickness, web_thickness, elastic_modulus=2.1e11)
length_bim = IBeam(length,beam_height, beam_width, flange_thickness, web_thickness, elastic_modulus=2.1e11)





class Cubic:
    def __init__(self,  width_bim, height_bim,length_bim):
        # 几何属性
        self.width_bim = width_bim
        self.height_bim = height_bim
        self.length_bim = length_bim 
        x1=width_bim.length
        
        
        
        x2=length_bim.length
        x3=height_bim.length
        x4=length_bim.width
        x5=length_bim.flange_thickness
        x6=length_bim.web_thickness
        x7=length_bim.height





        

    def deflection_x(x2,x41,x5,x6,x71):
        #挠度确认 X方向

        x7=x71+2*x5
        x4=2*x41+x6
        Iner = calculate_sectional_inertia(x4,x7,x6,x5)
        #q=((2 * ( (x4/1000) * (x5/1000)) + ((x6/1000) * ((x7 - 2 * x5)/1000)))*x1/1000)*g*density/(x1/1000)
        #w=q*x1*x1*x1*x1/(384*210000000000*Iner)

        w_max = x2/250000

        q=1000000000000*w_max*(384*210000000000*Iner)/(x2*x2*x2*x2)

        G=q*(x2/1000)-(((2 * ( (x4/1000) * (x5/1000)) + ((x6/1000) * ((x7 - 2 * x5)/1000)))*x2/1000)*g*density)


    

        return 1-((G-5.6)/30643082)
        



        
            


        


    def deflection_y(x1,x41,x5,x6,x71):
        #挠度确认  Y方向
        x7=x71+2*x5
        x4=2*x41+x6
        Iner = calculate_sectional_inertia(x4,x7,x6,x5)
        #q=((2 * ( (x4/1000) * (x5/1000)) + ((x6/1000) * ((x7 - 2 * x5)/1000)))*x1/1000)*g*density/(x1/1000)
        #w=q*x1*x1*x1*x1/(384*210000000000*Iner)

        w_max = x1/250000

        q=1000000000000*w_max*(384*210000000000*Iner)/(x1*x1*x1*x1)

        G=q*(x1/1000)-(((2 * ( (x4/1000) * (x5/1000)) + ((x6/1000) * ((x7 - 2 * x5)/1000)))*x1/1000)*g*density)


    

        return 1-((G-5.6)/277309468)



    




#目标函数1
    def total_volume(x1,x2,x3):
        # 计算整个框架的体积
        return 1-((x1*x2*x3-216000000)/234984000000)
    def total_surface_area(x1,x2):
        # 计算框架面积        
        return 1-((x1*x2-360000)/58440000)

#目标函数3
    def beam_cost(x1,x2,x3,x41,x5,x6,x71):
        # 计算整个框架的材料成本
        x7=x71+2*x5
        x4=2*x41+x6
        flange_area = (x4/1000) * (x5/1000)
        web_area = (x6/1000) * ((x7 - 2 * x5)/1000)
        price1 = (2 * flange_area + web_area)*(x1/1000)*p*density*4
        price2 = (2 * flange_area + web_area)*(x2/1000)*p*density*4
        price3 = (2 * flange_area + web_area)*(x3/1000)*p*density*4




        #return width_bim.price()+height_bim.price()+length_bim.price()
        return ((price1+price2+price3)-1780)/561100520
    
#目标函数4
    def product_cost(x41,x5,x6,x71):
        x7=x71+2*x5
        x4=2*x41+x6
        # 计算整个框架的生产成本
        weld_price=  (x4 * 4 - x6 * 2 )*weld_judge(x5,8,32)
        +(x7-2*x5)*2*weld_judge(x6,8,32)
        




        return (weld_price*24-9.252)/2216
    

    
    
  
    
 #目标函数5   
    def calculate_welding(x41,x5,x6,x71):

        x7=x71+2*x5
        x4=2*x41+x6
        #计算焊缝长度


        welding_length = x7 * 2 + x4 * 4 - x6 * 2 
        weldinglength = welding_length*2.4

        return (weldinglength-38.4)/9562
 #目标函数6   
    def welding_time(x41,x5,x6,x71):
        x7=x71+2*x5
        x4=2*x41+x6
        #计算总时间 min
        weldingtime = ( (
            bevel_judge(x5,8,16)*(x4*2-x6)+(x7 - 2 * x5)*bevel_judge(x6,8,16)
        )*bevel_time_atlength+(
             x7 * 2 + x4 * 4 - x6 * 2 -x5*4
        )*welding_time)*24
        return (weldingtime-5.76)/6042
     

#目标函数7
    def calculate_weldingprice(x41,x5,x6,x71):
        x7=x71+2*x5
        x4=2*x41+x6

        weld_price=  (x4 * 4 - x6 * 2 )*weld_judge(x5,8,32)
        +(x7-2*x5)*2*weld_judge(x6,8,32)
        
        
        
        
        
        
        weldprice=weld_price*240
        return (weldprice/10-9.252)/2216
    
    def return_json(self):
        data = [{'beam': 1 ,'type': 'H','length_direction':'x','width_direction':'y','height_direction':'z','length':length_bim.length,
     'data1': {'p':'1',
                #'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2], 
                #'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                'center':[0,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                'width':length_bim.width,'height':length_bim.flange_thickness},
     'data2': {'p':'1',
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center': [0,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'width':length_bim.web_thickness,'height':length_bim.height-2*length_bim.flange_thickness},
     'data3': {'p':'1', 
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center': [0,(width_bim.length+length_bim.width)/2,-(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'width':length_bim.width,'height':length_bim.flange_thickness}
     },
     {'beam': 2 ,'type': 'H','length_direction':'y','width_direction':'x','height_direction':'z','length':width_bim.length,
     'data1': {'p':'2',
                'center1': [(length_bim.length+width_bim.width)/2,width_bim.length/2,-(height_bim.length+width_bim.flange_thickness)/2], 
                'center2': [(length_bim.length+width_bim.width)/2,-width_bim.length/2,-(height_bim.length+width_bim.flange_thickness)/2],
                'center':[(length_bim.length+width_bim.width)/2,0,-(height_bim.length+width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness},
     'data2': {'p':'2',
               'center1': [(length_bim.length+width_bim.width)/2,width_bim.length/2,-(height_bim.length+width_bim.height)/2],
               'center2': [(length_bim.length+width_bim.width)/2,-width_bim.length/2,-(height_bim.length+width_bim.height)/2],
               'center': [(length_bim.length+width_bim.width)/2,0,-(height_bim.length+width_bim.height)/2],
               'width':width_bim.web_thickness,'height':width_bim.height-2*width_bim.flange_thickness},
     'data3': {'p':'2',
                'center1': [(length_bim.length+width_bim.width)/2,width_bim.length/2,-(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2], 
                'center2': [(length_bim.length+width_bim.width)/2,-width_bim.length/2,-(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'center':[(length_bim.length+width_bim.width)/2,0,-(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness}
     },
     {'beam': 3,'type': 'H','length_direction':'x','width_direction':'y','height_direction':'z','length':length_bim.length,
     'data1': {'p':'3',
                'center1': [-length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2], 
                'center2': [length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                'center':[0,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                'width':length_bim.width,'height':length_bim.flange_thickness},
     'data2': {'p':'3',
               'center1': [-length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center': [0,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'width':length_bim.web_thickness,'height':length_bim.height-2*length_bim.flange_thickness},
     'data3': {'p':'3', 
               'center1': [-length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center2': [length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center': [0,-(width_bim.length+length_bim.width)/2,-(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'width':length_bim.width,'height':length_bim.flange_thickness}
     }, {'beam': 4 ,'type': 'H','length_direction':'y','width_direction':'x','height_direction':'z','length':width_bim.length,
     'data1': {'p':'4',
                'center1': [-(length_bim.length+width_bim.width)/2,width_bim.length/2,-(height_bim.length+width_bim.flange_thickness)/2], 
                'center2': [-(length_bim.length+width_bim.width)/2,-width_bim.length/2,-(height_bim.length+width_bim.flange_thickness)/2],
                'center':[-(length_bim.length+width_bim.width)/2,0,-(height_bim.length+width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness},
     'data2': {'p':'4',
               'center1': [-(length_bim.length+width_bim.width)/2,width_bim.length/2,-(height_bim.length+width_bim.height)/2],
               'center2': [-(length_bim.length+width_bim.width)/2,-width_bim.length/2,-(height_bim.length+width_bim.height)/2],
               'center': [-(length_bim.length+width_bim.width)/2,0,-(height_bim.length+width_bim.height)/2],
               'width':width_bim.web_thickness,'height':width_bim.height-2*width_bim.flange_thickness},
     'data3': {'p':'4',
                'center1': [-(length_bim.length+width_bim.width)/2,width_bim.length/2,-(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2], 
                'center2': [-(length_bim.length+width_bim.width)/2,-width_bim.length/2,-(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'center':[-(length_bim.length+width_bim.width)/2,0,-(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness}
     },{'beam': 5 ,'type': 'H','length_direction':'z','width_direction':'x','height_direction':'y','length':height_bim.length,
     'data1': {'p':'5',
                'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2], 
                'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                #5~8只改中心
                'center': [(length_bim.length+height_bim.width)/2,(width_bim.length+height_bim.flange_thickness)/2,0],
                'width':height_bim.width,'height':height_bim.flange_thickness},
     'data2': {'p':'5',
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [(length_bim.length+height_bim.width)/2,(width_bim.length+height_bim.height)/2,0],
               'width':height_bim.web_thickness,'height':height_bim.height-2*height_bim.flange_thickness},
     'data3': {'p':'5', 
               'center1': [-length_bim.length/2,(width_bim.length+height_bim.flange_thickness)/2,-(height_bim.length-length_bim.height)/2+length_bim.height],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [(length_bim.length+height_bim.width)/2,(width_bim.length+2*height_bim.height-height_bim.flange_thickness)/2,0],
               'width':height_bim.width,'height':height_bim.flange_thickness}
     },{'beam': 6 ,'type': 'H','length_direction':'z','width_direction':'x','height_direction':'y','length':height_bim.length,
     'data1': {'p':'6',
                'center1': [-length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2], 
                'center2': [length_bim.length/2,-(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                #5~8只改中心
                'center': [(length_bim.length+height_bim.width)/2,-(width_bim.length+height_bim.flange_thickness)/2,0],
                'width':height_bim.width,'height':height_bim.flange_thickness},
     'data2': {'p':'6',
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [(length_bim.length+height_bim.width)/2,-(width_bim.length+height_bim.height)/2,0],
               'width':height_bim.web_thickness,'height':height_bim.height-2*height_bim.flange_thickness},
     'data3': {'p':'6', 
               'center1': [-length_bim.length/2,(width_bim.length+height_bim.flange_thickness)/2,-(height_bim.length-length_bim.height)/2+length_bim.height],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [(length_bim.length+height_bim.width)/2,-(width_bim.length+2*height_bim.height-height_bim.flange_thickness)/2,0],
               'width':height_bim.width,'height':height_bim.flange_thickness}
     },{'beam': 7 ,'type': 'H','length_direction':'z','width_direction':'x','height_direction':'y','length':height_bim.length,
     'data1': {'p':'7',
                'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2], 
                'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                #5~8只改中心
                'center': [-(length_bim.length+height_bim.width)/2,(width_bim.length+height_bim.flange_thickness)/2,0],
                'width':height_bim.width,'height':height_bim.flange_thickness},
     'data2': {'p':'7',
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [-(length_bim.length+height_bim.width)/2,(width_bim.length+height_bim.height)/2,0],
               'width':height_bim.web_thickness,'height':height_bim.height-2*height_bim.flange_thickness},
     'data3': {'p':'7', 
               'center1': [-length_bim.length/2,(width_bim.length+height_bim.flange_thickness)/2,-(height_bim.length-length_bim.height)/2+length_bim.height],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [-(length_bim.length+height_bim.width)/2,(width_bim.length+2*height_bim.height-height_bim.flange_thickness)/2,0],
               'width':height_bim.width,'height':height_bim.flange_thickness}
     },{'beam': 8 ,'type': 'H','length_direction':'z','width_direction':'x','height_direction':'y','length':height_bim.length,
     'data1': {'p':'8',
                'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2], 
                'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
                #5~8只改中心
                'center': [-(length_bim.length+height_bim.width)/2,(width_bim.length+height_bim.flange_thickness)/2,0],
                'width':height_bim.width,'height':height_bim.flange_thickness},
     'data2': {'p':'8',
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [-(length_bim.length+height_bim.width)/2,(width_bim.length+height_bim.height)/2,0],
               'width':height_bim.web_thickness,'height':height_bim.height-2*height_bim.flange_thickness},
     'data3': {'p':'8', 
               'center1': [-length_bim.length/2,(width_bim.length+height_bim.flange_thickness)/2,-(height_bim.length-length_bim.height)/2+length_bim.height],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,-(height_bim.length+length_bim.flange_thickness)/2],
               'center': [-(length_bim.length+height_bim.width)/2,(width_bim.length+2*height_bim.height-height_bim.flange_thickness)/2,0],
               'width':height_bim.width,'height':height_bim.flange_thickness}
     },{'beam': 9 ,'type': 'H','length_direction':'x','width_direction':'y','height_direction':'z','length':length_bim.length,
     'data1': {'p':'9',
                'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.flange_thickness)/2], 
                'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.flange_thickness)/2],
                'center':[0,(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.flange_thickness)/2],
                'width':length_bim.width,'height':length_bim.flange_thickness},
     'data2': {'p':'9',
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.height)/2],
               'center': [0,(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.height)/2],
               'width':length_bim.web_thickness,'height':length_bim.height-2*length_bim.flange_thickness},
     'data3': {'p':'9', 
               'center1': [-length_bim.length/2,(width_bim.length+length_bim.width)/2,(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center2': [length_bim.length/2,(width_bim.length+length_bim.width)/2,(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center': [0,(width_bim.length+length_bim.width)/2,(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'width':length_bim.width,'height':length_bim.flange_thickness}
     }, {'beam': 10 ,'type': 'H','length_direction':'y','width_direction':'x','height_direction':'z','length':width_bim.length,
     'data1': {'p':'10',
                'center1': [(length_bim.length+width_bim.width)/2,width_bim.length/2,(height_bim.length+width_bim.flange_thickness)/2], 
                'center2': [(length_bim.length+width_bim.width)/2,-width_bim.length/2,(height_bim.length+width_bim.flange_thickness)/2],
                'center':[(length_bim.length+width_bim.width)/2,0,(height_bim.length+width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness},
     'data2': {'p':'10',
               'center1': [(length_bim.length+width_bim.width)/2,width_bim.length/2,(height_bim.length+width_bim.height)/2],
               'center2': [(length_bim.length+width_bim.width)/2,-width_bim.length/2,(height_bim.length+width_bim.height)/2],
               'center': [(length_bim.length+width_bim.width)/2,0,(height_bim.length+width_bim.height)/2],
               'width':width_bim.web_thickness,'height':width_bim.height-2*width_bim.flange_thickness},
     'data3': {'p':'10',
                'center1': [(length_bim.length+width_bim.width)/2,width_bim.length/2,(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2], 
                'center2': [(length_bim.length+width_bim.width)/2,-width_bim.length/2,(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'center':[(length_bim.length+width_bim.width)/2,0,(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness}
     },{'beam': 11 ,'type': 'H','length_direction':'x','width_direction':'y','height_direction':'z','length':length_bim.length,
     'data1': {'p':'11',
                'center1': [-length_bim.length/2,-(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.flange_thickness)/2], 
                'center2': [length_bim.length/2,-(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.flange_thickness)/2],
                'center':[0,-(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.flange_thickness)/2],
                'width':length_bim.width,'height':length_bim.flange_thickness},
     'data2': {'p':'11',
               'center1': [-length_bim.length/2,-(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.height)/2],
               'center2': [length_bim.length/2,-(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.height)/2],
               'center': [0,-(width_bim.length+length_bim.width)/2,(height_bim.length+length_bim.height)/2],
               'width':length_bim.web_thickness,'height':length_bim.height-2*length_bim.flange_thickness},
     'data3': {'p':'11', 
               'center1': [-length_bim.length/2,-(width_bim.length+length_bim.width)/2,(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center2': [length_bim.length/2,-(width_bim.length+length_bim.width)/2,(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'center': [0,-(width_bim.length+length_bim.width)/2,(height_bim.length+2*length_bim.height-length_bim.flange_thickness)/2],
               'width':length_bim.width,'height':length_bim.flange_thickness}
     }, {'beam': 12 ,'type': 'H','length_direction':'y','width_direction':'x','height_direction':'z','length':width_bim.length,
     'data1': {'p':'12',
                'center1': [-(length_bim.length+width_bim.width)/2,width_bim.length/2,(height_bim.length+width_bim.flange_thickness)/2], 
                'center2': [-(length_bim.length+width_bim.width)/2,-width_bim.length/2,(height_bim.length+width_bim.flange_thickness)/2],
                'center':[-(length_bim.length+width_bim.width)/2,0,(height_bim.length+width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness},
     'data2': {'p':'12',
               'center1': [-(length_bim.length+width_bim.width)/2,width_bim.length/2,(height_bim.length+width_bim.height)/2],
               'center2': [-(length_bim.length+width_bim.width)/2,-width_bim.length/2,(height_bim.length+width_bim.height)/2],
               'center': [-(length_bim.length+width_bim.width)/2,0,(height_bim.length+width_bim.height)/2],
               'width':width_bim.web_thickness,'height':width_bim.height-2*width_bim.flange_thickness},
     'data3': {'p':'12',
                'center1': [-(length_bim.length+width_bim.width)/2,width_bim.length/2,(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2], 
                'center2': [-(length_bim.length+width_bim.width)/2,-width_bim.length/2,(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'center':[-(length_bim.length+width_bim.width)/2,0,(height_bim.length+2*width_bim.height-width_bim.flange_thickness)/2],
                'width':width_bim.width,'height':width_bim.flange_thickness}
     }
    ]

        json_file_name = 'group.json'

# 获取当前工作目录
        current_working_directory = os.getcwd()
        json_file_path = os.path.join(current_working_directory, json_file_name)

# 打开文件进行写入
        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
        # 将列表写入文件，每个列表元素都是一组数据
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"File '{json_file_name}' successfully written to directory '{current_working_directory}'.")
        except IOError as e:
            print(f"An I/O error occurred: {e.strerror}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


a = Cubic(width_bim,height_bim,length_bim)

a.return_json()









#ibeam = IBeam(height=0.2, width=0.1, flange_thickness=0.01, web_thickness=0.005, elastic_modulus=2.1e11)

# 
#deflection = ibeam.calculate_deflection(force=1000, length=2)
"""
input_range = [[600, 4900], [600, 12000], [600, 4000], [1, 300], [1, 100], [1, 100], [1, 500]]



print(Cubic.total_volume(4900, 12000, 4000), 
      Cubic.total_volume(600, 600, 600),
      

            Cubic.total_surface_area(12000, 4900), 
            Cubic.total_surface_area(600, 600), 
            

            Cubic.beam_cost(4900,12000,4000,300,100,100,500),
            Cubic.beam_cost(600,600,600,1,1,1,1),
            

            Cubic.product_cost(300, 100, 100, 500),
            Cubic.product_cost(1,1,1,1),
           

            Cubic.calculate_welding(300, 100,100, 500),
            Cubic.calculate_welding(1,1,1,1),
            

            Cubic.welding_time(300, 100,100,500),
            Cubic.welding_time(1,1,1,1),
            

            Cubic.calculate_weldingprice(300, 100,100,500),
            Cubic.calculate_weldingprice(1,1,1,1),
            
            
            
            Cubic.deflection_x(12000,300,100,100,500),
            Cubic.deflection_x(600,1,1,1,1),
            



            Cubic.deflection_y(4000,300,100,100,500),
            Cubic.deflection_y(600,1,1,1,1),
               

)

"""
