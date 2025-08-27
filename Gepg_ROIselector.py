#
#   G e p g _ R O I s e l e c t o r . p y
#
#   Last Update: IH250827
# 
# 
#
# ------------------------------------------
#   Notes:
# ------------------------------------------

import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import streamlit as st
from streamlit_drawable_canvas import st_canvas

class ROISelector:
    
    def __init__(self,gel_image_8bit):
        self.canvas_1 = None
        self.lane_ROI = [{},{},{}]  #IH250821 we support 3 lanes
        for lane in self.lane_ROI:
            lane = {'left': None, 'top': None, 'width': None, 'height': None, 'angle': None}  

        self.background_image = None
        self.background_image = Image.fromarray(220-gel_image_8bit) # IH250821 invert image for better visibility on canvas
                #IH250821 EXPERIMENTAL enhance high bands (that's why we use 200 and not 255)
        self.canvas_1_height, self.canvas_1_width = gel_image_8bit.shape[:2]
        # st.write(f"W,H: {self.canvas_1_width}, {self.canvas_1_height }") 

        # Scale canvas for display if image is too wide
        self.canvas_scale  = 1.0
        canvas_max_width = 600  #IH250812 HEURISTIC
        if self.canvas_1_width > canvas_max_width:
            self.canvas_scale  = canvas_max_width/self.canvas_1_width 
            aspect_ratio = self.canvas_1_height / self.canvas_1_width
            self.canvas_1_width = canvas_max_width
            self.canvas_1_height = int(self.canvas_1_width * aspect_ratio)


    def select_ROI(self):  
            
        self.canvas_1 = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=2,
            stroke_color="#FCE21B",
            background_image = self.background_image,
            update_streamlit=True, 
            height=self.canvas_1_height,
            width=self.canvas_1_width, 
            drawing_mode="transform",
            initial_drawing=self.canvas_1_initial_drawing(self.background_image,self.canvas_1_width,self.canvas_1_height),
            key="canvas_1",
            )
          
        # st.write(f"Canvas (json_data): {self.canvas_1.json_data}") 
        for index,object in enumerate(self.canvas_1.json_data['objects']):
            for param in ['left','top','width','height','scaleX','scaleY','angle']:
                self.lane_ROI[index][param] = object[param]
                self.lane_ROI[index]['style'] = {
                    'fill': object['fill'],
                    'stroke': object['stroke'],
                    'strokeWidth': object['strokeWidth']
                }       
        #     st.write(f"Object {object['type'], index}:  " +
        #         f"canvas scale: {self.canvas_scale},   " + 
        #         f"original left: {object['left']/self.canvas_scale},   " +
        #         f"original top: {object['top']/self.canvas_scale},   " +
        #         f"original scaledwidth: {object['width']*object['scaleX']/self.canvas_scale},   " +
        #         f"original scaledheight: {object['height']*object['scaleY']/self.canvas_scale},   " +
        #         f"angle: {object['angle']},   " +
        #         "")
        # #IH250821 for the moment, we assume the first object to be the expected ROI 
  
    def get_ROIcenter_X(self,lane_index=0):
        return self.lane_ROI[lane_index]['left']/self.canvas_scale
    
    def get_ROIcenter_Y(self,lane_index=0):
        return self.lane_ROI[lane_index]['top']/self.canvas_scale
    
    def get_ROIwidth(self,lane_index=0):   
        return self.lane_ROI[lane_index]['width']*self.lane_ROI[lane_index]['scaleX']/self.canvas_scale
    
    def get_ROIheight(self,lane_index=0):  
        return self.lane_ROI[lane_index]['height']*self.lane_ROI[lane_index]['scaleY']/self.canvas_scale
    
    def get_ROIangle(self,lane_index=0):  
        return self.lane_ROI[lane_index]['angle']   
    
    def get_ROIstyle(self,lane_index=0):
        return self.lane_ROI[lane_index]['style']
    
    def canvas_1_initial_drawing(self,image: Image.Image, canvas_width: int, canvas_height):
        
        rect_object_template = {
            'type': 'rect',             
            'version': '4.4.0', 
            'originX': 'center', 'originY': 'center', 
                'left': canvas_width*(0.5-0.04/2),   
                'top': canvas_height*0.5, 
                'width':  1,    #IH250826 this works in concert with scaleX 
                'height': 1,    #IH250826 this works in concert with scaleY
            'fill': 'rgba(255, 165, 0, 0.3)', 
            'stroke': '#FCE21B', 
                'strokeWidth': 2, 
                'strokeDashArray': None, 
                'strokeLineCap': 'butt', 
                'strokeDashOffset': 0, 
                'strokeLineJoin': 'miter', 
                'strokeUniform': True, 
                'strokeMiterLimit': 4, 
            'scaleX': canvas_width*0.04,  #IH250826 this works in concert with width, 
            'scaleY': canvas_height*0.65, #IH250826 this works in concert with height
            'angle': 0, 
            'flipX': False, 'flipY': False, 
            'opacity': 1, 
            'shadow': None, 
            'visible': True, 
            'backgroundColor': '', 
            'fillRule': 'nonzero', 
            'paintFirst': 'fill', 
            'globalCompositeOperation': 
            'source-over', 
            'skewX': 0, 'skewY': 0, 
            'rx': 0, 'ry': 0}
        
        rect_lane1 = rect_object_template.copy()
        rect_lane2 = rect_object_template.copy()
        rect_lane3 = rect_object_template.copy()

        rect_lane1['left']  = canvas_width*(0.1)
        rect_lane1['fill']  = 'rgba(255, 165, 0, 0.3)',
        rect_lane1['stroke']= "#8F33C7"

        rect_lane2['left']  = canvas_width*(0.2)
        rect_lane2['fill']  ='rgba(255, 165, 0, 0.3)' 
        rect_lane2['stroke']= "#1B80FC"

        rect_lane3['left']  = canvas_width*(0.3)
        rect_lane3['fill']  = 'rgba(255, 165, 0, 0.3)',
        rect_lane3['stroke']= "#13C391"

        
        return {
        'version': '4.4.0', 
        'objects': [
            rect_lane1,
            rect_lane2,
            rect_lane3
            ]}

    def crop_rotated_rect(self,image: np.ndarray, centerleft: int, centertop: int, width: int, height: int, angle: float, interpolation: int = cv2.INTER_LINEAR) -> np.ndarray:
        """
        Origin: Gemini

        Crops a slanted rectangular region of interest (ROI) from an image.

        Args:
            image (np.ndarray): The source image in OpenCV format (NumPy array).
            centerleft (int): The x-coordinate of center of the rectangle's bounding box.
            centertop (int): The y-coordinate of the center corner of the rectangle's bounding box.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            angle (float): The rotation angle of the rectangle in degrees.
            interpolation (int, optional): The interpolation method to use for rotation. 
                                        Defaults to cv2.INTER_LINEAR.

        Returns:
            np.ndarray: The cropped image of the specified ROI.
        """
        # 1. Get the center of the rectangle
        center = (centerleft, centertop)

        # 2. Get the rotation matrix
        # The angle is negated to "un-rotate" the rectangle in the image
        rotation_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1.0)

        # 3. Get the image dimensions
        img_height, img_width = image.shape[:2]

        # 4. Rotate the entire image
        rotated_image = cv2.warpAffine(
            src=image,
            M=rotation_matrix,
            dsize=(img_width, img_height),
            flags=interpolation
        )

        # 5. Calculate the coordinates for the axis-aligned crop
        crop_x = int(centerleft - width / 2)
        crop_y = int(centertop - height / 2)

        # 6. Perform the crop on the rotated image and return it
        cropped_image = rotated_image[crop_y : crop_y + int(height), crop_x : crop_x + int(width)]
        
        return cropped_image