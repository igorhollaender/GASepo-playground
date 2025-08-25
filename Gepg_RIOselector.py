#
#   G e p g _ R O I s e l e c t o r . p y
#
#   Last Update: IH250825
# 
# 
#
# ------------------------------------------
#   Notes:
# ------------------------------------------


import numpy as np
from PIL import Image
import plotly.express as px
import streamlit as st
from streamlit_drawable_canvas import st_canvas

class ROISelector:
    
    def __init__(self,gel_image_8bit):
        self.canvas_1 = None
        self.background_image = Image.fromarray(220-gel_image_8bit) # IH250821 invert image for better visibility on canvas
                #IH250821 EXPERIMENTAL enhance high bands (thats why we use 200 and not 255)
        self.canvas_1_height, self.canvas_1_width = gel_image_8bit.shape[:2]
        # Scale canvas for display if image is too wide
        if self.canvas_1_width > 800:  #IH250812 HEURISTIC
            aspect_ratio = self.canvas_1_height / self.canvas_1_width
            self.canvas_1_width = 800
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
            st.write(f"Object {object['type'], index}:  " + 
                f"left: {object['left']},   " +
                f"top: {object['top']},   " +
                f"width: {object['width']},   " +
                f"height: {object['height']},   " +
                f"angle: {object['angle']},   " +
                "")
        #IH250821 we assume the first object to be the expected ROI 
  
    def canvas_1_initial_drawing(self,image: Image.Image, canvas_width: int, canvas_height):
        
        rect_object_template = {
            'type': 'rect',             
            'version': '4.4.0', 
            'originX': 'left', 'originY': 'top', 
                'left': canvas_width*(0.5-0.04/2),   
                'top': canvas_height*0.2, 
                'width': canvas_width*0.04,
                'height': canvas_height*0.65, 
            'fill': 'rgba(255, 165, 0, 0.3)', 
            'stroke': '#FCE21B', 
                'strokeWidth': 2, 
                'strokeDashArray': None, 
                'strokeLineCap': 'butt', 
                'strokeDashOffset': 0, 
                'strokeLineJoin': 'miter', 
                'strokeUniform': True, 
                'strokeMiterLimit': 4, 
            'scaleX': 1, 'scaleY': 1, 
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
