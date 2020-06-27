import numpy as np
import pandas as pd

from bokeh.io import export_svgs, show
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, ColumnDataSource


class BokehHistogram():
    def __init__(self, color_fill, color_hover, fill_alpha=0.7,
                 height=600, width=600, bins=20):
        self.color_fill = color_fill
        self.color_hover = color_hover
        self.fill_alpha = fill_alpha
        self.height = height
        self.width = width
        self.bins = bins
        self.plot = None
    
    def load_plot(self, df, column, title, x_label, y_label, notebook_handle=False):
        hist, edges = np.histogram(df[column], bins=self.bins)
        hist_df = pd.DataFrame({column: hist,
                                "left": edges[:-1],
                                "right": edges[1:]})
        hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                                right in zip(hist_df["left"], hist_df["right"])]
        self.plot = figure(plot_height=self.height, plot_width=self.width,
                      title=title, x_axis_label=x_label, y_axis_label=y_label)
        
        data_src = ColumnDataSource(hist_df)
        self.plot.quad(bottom=0, top=column, left="left", 
            right="right", source=data_src, fill_color=self.color_fill, 
            line_color="black", fill_alpha=self.fill_alpha,
            hover_fill_alpha=1.0, hover_fill_color=self.color_hover)

        hover = HoverTool(tooltips=[('Interval', '@interval'),
                                    ('Count', str("@" + "num_chars_text"))])
        self.plot.add_tools(hover)
        show(self.plot, notebook_handle=notebook_handle)
    
    def save_plot(self, file_name):
        if self.plot is None:
            print("There is nothing to save. You must load a plot first...")
            return
        try:
            self.plot.output_backend = "svg"
            export_svgs(self.plot, filename=file_name)
        except Exception as e:
            print("There was an error exporting the plot. Please verify that both " 
                  + f"Selenium and Geckodriver are installed: {e}")
