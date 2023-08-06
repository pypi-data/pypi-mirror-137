
import json
import numpy as np
import os,sys
import shapefile
import itertools

import matplotlib.pyplot as plt
from pathlib import Path
from descartes import PolygonPatch
from .bounding_boxes import bounding_boxes

def get_bounding_box(countrycode):
    """
    called by PlotMap
    boundingboxes for all countries by official 2-digit countrycode
    can be used to set xlim, ylim of the European map in plots
    """
    if countrycode != None:
    
        result = bounding_boxes[countrycode][1]
    else:
        result = []

    return result


def PlotMap(
    countrycode="EU",
    figureNum=1,
    MapColor=True,
    SupTitleStr="",
    MapAlpha=1,
    Axis=True,
    BackGroundAlpha=0,
    TM_Borders_filename='../TM_World_Borders/TM_WORLD_BORDERS-0.3.shp'
    ):
    """
    Plotting contour of Country or Europe
    """
    fig = plt.figure(figureNum, figsize=(12.5, 8.5), facecolor=("#FFFFFF"))
    ax = fig.gca()
    if countrycode != None:
        if TM_Borders_filename == '':
            TM_Borders_filename = os.path.join(
             "Eingabe/GraphischeDaten/TM_WORLD_BORDERS-0.3.shp"
            )
            

        sf = shapefile.Reader(TM_Borders_filename)
        color_list = [
            "#ffffe5",
            "#c7e9c0",
            "#F5FFFA",
            "#f7fcf5",
            "#a8ddb5",
            "#F8F8FF",
            "#FFF5EE",
            "#FFEFD5",
            "#eafff5",
            "#e5f5e0",
        ]
        if MapColor == False:
            ax.set_facecolor("xkcd:light grey")
            countrycolors = itertools.cycle(["#ffffff"])
        else:
            countrycolors = itertools.cycle(color_list)
            ####old color
            ax.set_facecolor("#f7fbff")

        if MapAlpha > 0:
            for poly in sf.shapes():
                poly_geo = poly.__geo_interface__
                ax.add_patch(
                    PolygonPatch(
                        poly_geo,
                        fc=next(countrycolors),
                        ec="#000000",
                        alpha=MapAlpha,
                        zorder=1,
                        linewidth=0.25,
                    )
                )

        if type(countrycode) == list:
            xmin, ymin = countrycode[0], countrycode[1]
            xmax, ymax = countrycode[2], countrycode[3]
        else:
            [xmin, ymin, xmax, ymax] = get_bounding_box(countrycode)
            
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])

        if Axis:

            ax.set_xlabel("long [°]")
            ax.set_ylabel("lat [°]")
            plt.xticks(np.arange(xmin, xmax, 2.0))
            plt.yticks(np.arange(ymin, ymax, 2.0))
        if len(SupTitleStr) > 0:
            plt.suptitle(SupTitleStr)
    return fig, ax
