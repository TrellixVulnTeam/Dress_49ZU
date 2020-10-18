# -*- coding: cp936 -*-
import cv2
import numpy as np
import pygal
from pygal.style import DarkStyle


class JpegToSvg(object):
    def __init__(self):
        self.JpegAddr='d:\\Dress\\768x847_2.jpg'
        self.SvgAddr='d:\\Dress\\output.svg'
    def __LoadToPath(self):
        '''
            ���ܣ�����jpg���ɳ�Svg˳��·��
        '''
        TempIm=cv2.imread(self.JpegAddr)
        #resizeIm=cv2.resize(TempIm,(400,300),interpolation=cv2.INTER_LINEAR)
        GrayIm = cv2.cvtColor(TempIm, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('To_Gray',flags=cv2.WINDOW_NORMAL)
        cv2.imshow('To_Gray',GrayIm)
        # �ǵ���
        CornerIm = cv2.cornerHarris(GrayIm, 1, 3, 0.04)
        cv2.namedWindow('To_Corner',flags=cv2.WINDOW_NORMAL)
        cv2.imshow('To_Corner',CornerIm)
        #
        GaussianIm=cv2.GaussianBlur(GrayIm,(3,3),4)
        cv2.namedWindow('To_GaussianBlur',flags=cv2.WINDOW_NORMAL)
        cv2.imshow('To_GaussianBlur',GaussianIm)       
        #��ֵ
        ret,ThresholdIm=cv2.threshold(GaussianIm,200,255,cv2.THRESH_BINARY)
        #��ʾ��ֵ���������
        cv2.namedWindow('TwoValue',flags=cv2.WINDOW_NORMAL)
        cv2.imshow('TwoValue',ThresholdIm)
        #CANNY��Ե��ȡ
        EdgeIm=cv2.Canny(ThresholdIm,1,100, apertureSize = 3)
        cv2.namedWindow('Edge',flags=cv2.WINDOW_NORMAL)
        cv2.imshow('Edge',EdgeIm)        
        #�õ�����·���б�
        Rel=None
        LeftPath=[]
        RightPath=[]
        i=0
        for Row in EdgeIm:
            ColIndex=np.ix_(Row>0)[0]
            #��û�е����
            if len(ColIndex)>0:
                XLeft=min(ColIndex)
                XRight=max(ColIndex)    
                LeftPath.append((XLeft,-i))
                RightPath.append((XRight,-i))
            i=1+i
        #����һ��·��
        RightPath.reverse()
        Rel=LeftPath+RightPath
        #�ر���ʾ
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return Rel
    
    def CreateSvg(self):
        '''
            ���ܣ�����·������Svg
        '''
        SvgPath=self.__LoadToPath()
        xy_chart=pygal.XY()
        xy_chart.add('DressEdge',SvgPath)
        #xy_chart.render_in_browser()
        #xy_chart.render()
        xy_chart.render_to_file(self.SvgAddr)
        return True



        
if __name__=='__main__':
    jtsObj=JpegToSvg()
    jtsObj.CreateSvg()

    
