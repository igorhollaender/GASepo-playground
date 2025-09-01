#
#   G e p g _ l a n e p r o f i l e p r e s e n t e r . p y
#
#   Last Update: IH250901
#  
# 
#
# ------------------------------------------
#   Notes:
# ------------------------------------------


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class LaneProfilePresenter:
    def __init__(self,lane_image16bit: np.ndarray):
        self.lane_image16bit = lane_image16bit
        
    def plot_image_and_column_sums(self) -> go.Figure:
        """
        Origin: gemini

        Draws a figure with an image and a plot of its column-wise pixel sums.

        The function creates a two-part figure:
        1. Top: The input image displayed in grayscale.
        2. Bottom: A line plot showing the sum of pixel values for each column.

        The plot is precisely aligned with the image, so each point on the plot
        corresponds to the column directly above it.

        Args:
            image (np.ndarray): A 2D NumPy array representing a 16-bit grayscale image.
        """
        # Ensure input is a 2D NumPy array
        if not isinstance(self.lane_image16bit, np.ndarray) or self.lane_image16bit.ndim != 2:
            raise ValueError("Input must be a 2D NumPy array.")

        #IH250828 transpose the image to make columns vertical
        self.lane_image16bit = self.lane_image16bit.T

        # Get image dimensions for plot axes
        height, width = self.lane_image16bit.shape
        column_indices = np.arange(width)

        # Calculate the sum of pixel values for each column
        column_sums = np.sum(self.lane_image16bit, axis=0)
        column_avg = column_sums / height  # Average pixel value per column

        # Create a figure with two subplots stacked vertically
        # shared_xaxes=True is the key to aligning the image and the plot
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            row_heights=[0.4, 0.6]  # Allocate 40% of the height to the image
        )

        # --- Top Subplot: Image ---
        # Add the image trace. We use a grayscale color scale.
        fig.add_trace(
            go.Heatmap(z=self.lane_image16bit, colorscale='gray',showscale=False, 
                       zmin=0, zmax=256*256-1, zsmooth='best'),
                       #IH250828 TODO adapt this to show true 16bit depth
            row=1, col=1
        )

        # --- Bottom Subplot: Column Sums Plot ---
        # Add the line plot of column sums
        fig.add_trace(
            go.Scatter(x=column_indices, y=column_avg, mode='lines'),
            row=2, col=1
        )

        # --- Layout and Alignment ---
        fig.update_layout(
            margin=dict(l=20, r=20, t=50, b=20), # Adjust margins for a clean look
            showlegend=False # Hide the legend as there's only one trace in the plot
        )
        
        # Hide tick labels
        fig.update_xaxes(showticklabels=False, row=1, col=1)
        fig.update_yaxes(showticklabels=False, row=1, col=1)

        # Add axis titles for clarity
        # fig.update_yaxes(title_text="Row", row=1, col=1)
        fig.update_xaxes(title_text="Row Index", row=2, col=1)
        fig.update_yaxes(title_text="Avg Pixel Value", row=2, col=1)

        return fig


# # --- Example Usage ---
# if __name__ == '__main__':
#     # Create a sample 16-bit NumPy array to simulate an OpenCV image
#     # The image will be 200px high and 600px wide
#     img_height = 200
#     img_width = 600

#     # Start with a base of random noise
#     dummy_image = (np.random.rand(img_height, img_width) * 5000).astype(np.uint16)

#     # Add a horizontal gradient
#     y_gradient = np.linspace(0, 10000, img_height, dtype=np.uint16).reshape(-1, 1)
#     dummy_image += y_gradient
    
#     # Add two bright vertical bands to make the column sums more interesting
#     dummy_image[:, 150:250] += 20000
#     dummy_image[:, 450:500] += 12000

#     # Call the function with the dummy image
#     plot_image_and_column_sums(dummy_image)