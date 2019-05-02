#! /usr/bin/env python3

__version__= '1.0'

import argparse
import sys
import os
import numpy as np
import warnings
import xml.etree.ElementTree as ET
from tqdm import tqdm
import cv2

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

__doc__=\
"""
tool to extract 2d or 3d RGB images from page xml data. In former case output will be 1
2D image array which each class has filled with a pixel value. In the case of 3D RGB image 
each class will be defined with a RGB value and beside images a text file of classes also will be produced.
This classes.txt file is required for dhsegment tool.
"""

class pagexml2img:
    def __init__(self,dir_in, out_dir,output_type):
        self.dir=dir_in
        self.output_dir=out_dir
        self.output_type=output_type

    def get_content_of_dir(self):
        """
        Listing all ground truth page xml files. All files are needed to have xml format.
        """

        gt_all=os.listdir(self.dir)
        self.gt_list=[file for file in gt_all if file.split('.')[ len(file.split('.'))-1 ]=='xml' ]

    def get_images_of_ground_truth(self):
        """
        Reading the page xml files and write the ground truth images into given output directory.
        """

        if self.output_type=='3d' or self.output_type=='3D':
            classes=np.array([ [0,0,0],[255,0,0],[0,255,0],[0,0,255]])
            

            

            for index in tqdm(range(len(self.gt_list))):
                try:
                    tree1 = ET.parse(self.dir+'/'+self.gt_list[index])
                    root1=tree1.getroot()
                   
                   
                    for jj in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Page'):
                        y_len=int(jj.attrib['imageHeight'])
                        x_len=int(jj.attrib['imageWidth'])
                   
                    co_text=[]
                    co_sep=[]
                    co_img=[]
                
                    for nn in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}TextRegion'):
                        c_t_in=[]
                        for ll in nn.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Point'):
                            c_t_in.append([ int(np.float(ll.attrib['x'])) , int(np.float(ll.attrib['y'])) ])
                        co_text.append(np.array(c_t_in))
                  
                
                    for nn in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}ImageRegion'):
                        c_i_in=[]
                        for ll in nn.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Point'):
                            c_i_in.append([ int(np.float(ll.attrib['x'])) , int(np.float(ll.attrib['y'])) ])
                        co_img.append(np.array(c_i_in))
                       
                    for nn in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}SeparatorRegion'):
                        c_s_in=[]
                        for ll in nn.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Point'):
                            c_s_in.append([ int(np.float(ll.attrib['x'])) , int(np.float(ll.attrib['y'])) ])
                        co_sep.append(np.array(c_s_in))
                       
                    img = np.zeros( (y_len,x_len,3) ) 
                    img_poly=cv2.fillPoly(img, pts =co_text, color=(255,0,0))
                    img_poly=cv2.fillPoly(img, pts =co_img, color=(0,255,0))
                    img_poly=cv2.fillPoly(img, pts =co_sep, color=(0,0,255))
                    
                    try: 
                        cv2.imwrite(self.output_dir+'/'+self.gt_list[index].split('-')[1].split('.')[0]+'.png',img_poly )
                    except:
                        cv2.imwrite(self.output_dir+'/'+self.gt_list[index].split('.')[0]+'.png',img_poly )
                except:
                    pass
            np.savetxt(self.output_dir+'/../classes.txt',classes)
    
        if self.output_type=='2d' or self.output_type=='2D':
            
            for index in tqdm(range(len(self.gt_list))):
                try:
                
                    tree1 = ET.parse(self.dir+'/'+self.gt_list[index])
                    root1=tree1.getroot()
                   
                    for jj in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Page'):
                        y_len=int(jj.attrib['imageHeight'])
                        x_len=int(jj.attrib['imageWidth'])
                   
                    co_text=[]
                    co_sep=[]
                    co_img=[]
                
                    for nn in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}TextRegion'):
                        c_t_in=[]
                        for ll in nn.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Point'):
                            c_t_in.append([ int(np.float(ll.attrib['x'])) , int(np.float(ll.attrib['y'])) ])
                        co_text.append(np.array(c_t_in))
                  
                
                    for nn in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}ImageRegion'):
                        c_i_in=[]
                        for ll in nn.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Point'):
                            c_i_in.append([ int(np.float(ll.attrib['x'])) , int(np.float(ll.attrib['y'])) ])
                        co_img.append(np.array(c_i_in))
                       
                    for nn in root1.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}SeparatorRegion'):
                        c_s_in=[]
                        for ll in nn.iter('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19}Point'):
                            c_s_in.append([ int(np.float(ll.attrib['x'])) , int(np.float(ll.attrib['y'])) ])
                        co_sep.append(np.array(c_s_in))
                       
                    img = np.zeros( (y_len,x_len) ) 
                    img_poly=cv2.fillPoly(img, pts =co_text, color=(1,1,1))
                    img_poly=cv2.fillPoly(img, pts =co_img, color=(2,2,2))
                    img_poly=cv2.fillPoly(img, pts =co_sep, color=(3,3,3))
                    try: 
                        cv2.imwrite(self.output_dir+'/'+self.gt_list[index].split('-')[1].split('.')[0]+'.png',img_poly )
                    except:
                        cv2.imwrite(self.output_dir+'/'+self.gt_list[index].split('.')[0]+'.png',img_poly )
                except:
                    pass
    def run(self):
        self.get_content_of_dir()
        self.get_images_of_ground_truth()
def main():
    parser=argparse.ArgumentParser()

    parser.add_argument('-dir_in','--dir_in', dest='inp1', default=None, help='directory of page-xml files')
    parser.add_argument('-dir_out','--dir_out', dest='inp2', default=None, help='directory where ground truth images would be written')
    parser.add_argument('-type','--type', dest='inp3', default=None, help='this defines how output should be. A 2d image array or a 3d image array encoded with RGB color. Just pass 2d or 3d. The file will be saved one directory up. 2D image array is 3d but only information of one channel would be enough since all channels have the same values.')
    options=parser.parse_args()
    
    possibles=globals()
    possibles.update(locals())
    x=pagexml2img(options.inp1,options.inp2,options.inp3)
    x.run()
if __name__=="__main__":
    main()

    
    
