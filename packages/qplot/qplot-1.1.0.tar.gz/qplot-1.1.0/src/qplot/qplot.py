# -*- coding: utf-8 -*-
"""
q_plot - The SciGRID_Gas Visualization Library
----
"""


import json
import os, sys
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib

import numpy as np
import configparser
import itertools
import mplcursors
import shapefile  # pyshp

from pathlib import Path
from descartes import PolygonPatch
from adjustText import adjust_text
from itertools import cycle

#import Code.C_colors as CC
from .packages import plot_objects  as PO
from .packages.wheels import linewidthwheel, parawheel, colorwheel
from .packages.plot_map import get_bounding_box, PlotMap
from .packages.color_schema import Comp_Style
from .packages.cursor import PlotCursor


def PlotPoints(
    fig,
    ax,
    elements,
    cursor=False,
    cursor_data="",
    Size="",
    Symbol="",
    color="",
    fontsize="",
    legend="_nolegend_",
    alpha="",
    names="",
    Info=[],
    selectList=[],
    parameter=""):

    if cursor_data=="":
        cursor_data = {"point": {}, "line": {}}
    Size = Info.get("Size", 15) if Size == "" else Size
    Symbol = Info.get("Symbol", ".") if Symbol == "" else Symbol
    color = Info.get("color", "b") if color == "" else color
    alpha = Info.get("alpha", 1) if alpha == "" else alpha
    names = Info.get("names", False) if names == "" else names
    names = bool(names == "True" or names == True)
    fontsize = int(Info.get("fontsize", 13)) if fontsize == "" else int(fontsize)
#    if parameter == "":
#        [long, lat, labels] = elements
#    else:
    [long, lat, labels, paras] = elements
    y, x = np.array(lat), np.array(long)

    color_list = ["b", "g", "r", "c", "m", "y", "k"]
    colors_generator = itertools.cycle(color_list)

    if selectList != []:
        x = x[selectList]
        y = y[selectList]
        color_setting= colorwheel(color, colors_generator)
    else:
        color_setting=color
        
    #if parameter != "":
 #   entrycheck=[entry for entry in paras if entry!=""]
 #   if entrycheck!=[]:    
 #       c, cmap, norm = parawheel(paras) 
 #       color_setting=c
 
        
    ma = plt.scatter(
        x,
        y,
        s=float(Size),
        marker=Symbol,
        edgecolor="black",
        linewidths=0.5,
        c=color_setting,#colorwheel(color, colors_generator),
        zorder=3,
        alpha=int(alpha),
        label=legend,
    )
    # Plot ScalarLegend
#    if parameter != "" and entrycheck!=[]:
#        if len(set(paras))>3:
#            fig2, ax2 = plt.subplots(figsize=(6, 1))
#            fig2.subplots_adjust(bottom=0.5)   
#            fig2.colorbar(
#                matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
#                cax=ax,
#                orientation="horizontal",
#                label=parameter,
#            )
    if legend != "_nolegend_":
        ax.legend()

    npx, npy = np.asarray(x, dtype=np.float32), np.asarray(y, dtype=np.float32)
    nplabeltype = np.asarray(labels, dtype=np.str)
    nanlist = np.argwhere(np.isnan(npx))
    nplabels = np.delete(nplabeltype, nanlist)
    npx, npy = np.delete(npx, nanlist), np.delete(npy, nanlist)

    if names == True:
        texts = [
            plt.text(
                npx[i], npy[i], nplabels[i], fontsize=fontsize, ha="center", va="center"
            )
            for i in range(len(npx))
        ]
        adjust_text(texts)

    cursor_data["point"].update({ma: nplabels})
    #if cursor == True:
    #    PlotCursor(cursor_data['point'], multiple=False, hover=True)
    return


def PlotLines(
    fig,
    ax,
    elements,
    PlotOptions="",
    Cursor_Lines=False,
    cursor_data="deactivate",
    linewidth="",
    linestyle="",
    color="colorwheel",
    legend="_nolegend_",
    alpha=0.5,
    loops=True,
    Info=[],
    selectList=[],
    parameter="",
    random_colors=False,
    thicklines=False,):

    alpha = float(Info.get("alphalines", 1)) if alpha == "" else float(alpha)
    linewidth = int(Info.get("linewidth", 1)) if linewidth == "" else int(linewidth)
    colors = itertools.cycle(["b", "g", "r", "c", "m", "y", "k"])
    thicknesses = itertools.cycle(["2.0", "3.0", "4", "5", "6", "7", "8"])
    if cursor_data=="":
        cursor_data = {"point": {}, "line": {}}
    paras = []
    thickness = []
    linethicknesses = linewidth
    if parameter != "":
        for element in elements:
            paras.append(element[3])
        if set(paras)=={0}:
            print('No none Zero Values for',parameter)
            sys.exit() 

        entrycheck=[entry for entry in paras if entry!=""]
        if entrycheck!=[]:
            #print('entrycheck not empty')    
            c, cmap, norm = parawheel(paras) 
            color_setting=c
        else:
            color_setting=color  
               
       # try:
       #     c, cmap, norm = parawheel(paras)
       # except Parameter_Error:
       #     print('No values for parameter in at least one component-type:', parameter)
            

            
    if thicklines == True:
        for element in elements:
            thickness.append(element[-1])
        linethicknesses = linewidthwheel(thickness, parameter)

    colortmp = "colorwheel"


    if loops == True:            
        pipelist=[]
        doublette_list=[]
        for pipe in elements:
            doubles=pipelist.count((pipe[0],pipe[1]))
            pipelist.append((pipe[0],pipe[1]))
            doublette_list.append(doubles)                


    for count, element in enumerate(elements):
        if element in selectList or selectList == []:
            x, y = element[0], element[1]
            label = str(element[2])
            # if parameter=='' and thicklines==False:
            #     l  = lines.Line2D(x,y,
            #                                 color       = colorwheel(colortmp,color_generator),
            #                                 linewidth   = linethicknesswheel(linewidth_string,thicknesses),
            #                                 label       = legend,
            #                                 alpha       = alpha,
            #                                 linestyle   = linestyle)
        
            #if parameter == "": 
            linewidth_setting=linewidth
            color_setting='k'
            
            if thicklines == False:
                linewidth_setting=linewidth
            
            if color!='colorwheel':
                color_setting=color
             
            if parameter!="" and entrycheck!=[]:
                color_setting=c[count]
              
            if random_colors:
                color_setting=next(colors)

            if  thicklines == True and entrycheck!=[]:
                #linewidth_setting=linewidth        
                #color_setting=colorwheel(colortmp, colors)
                linewidth_setting=linethicknesses[count]
                            
         #   if (parameter!="" and thicklines==True) and entrycheck!=[]:
         #       color_setting=c[count]
         #       linewidth_setting=linethicknesses[count]
         #       
            if loops==False:   

                l = lines.Line2D(
                    x,
                    y,
                    color=color_setting,
                    linewidth=linewidth_setting,
                    label=legend,
                    alpha=alpha,
                    linestyle=linestyle,
                    picker=True,
                    pickradius=5
                )

            else:                           
                Color_list=["k","b","g","r","c","m","y","gold","magenta","lawngreen","aquamarine"]                
                l = lines.Line2D(
                    x,
                    y,
                    color=Color_list[doublette_list[count]],
                    linewidth=linewidth_setting,
                    label=legend,
                    alpha=alpha,
                    linestyle=linestyle,
                    picker=True,
                    pickradius=5
                )


                

            l.url = element[2]
            ax.add_line(l)
            legend = "_nolegend_"

            #            if cursor_data!='' and cursor_data!='deactivate':
            cursor_data["line"].update({l: label})

            #if Cursor_Lines:
            #    PlotCursor(cursor_data["line"], multiple=False, hover=True)
                # cursor_data.get("line").update({l:label})

    if legend != "_nolegend_":
        ax.legend()

    param_list = ["max_pressure_bar","pressure_bar", "diameter_mm", "max_cap_M_m3_per_d"]

    if loops==False:
        if parameter in param_list:
            cbaxes = fig.add_axes([0.123, 0.05, 0.777, 0.008])
            if entrycheck!=[]:
                fig.colorbar(
                    matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
                    cax=cbaxes,
                    orientation="horizontal",
                    label=parameter,
                )

    if loops==True:
       
       loops_legend=[lines.Line2D([0],[0],color=Color_list[i],
                     lw=3,label=str(i+1)) for i in set(doublette_list)]


       # [lines.Line2D([0],[0],color="k",lw=4,label='1'),
             # lines.Line2D([0],[0],color="r",lw=4,label='2')]

       leg1=ax.legend()
       leg2=ax.legend(handles=loops_legend,loc='lower right',title='Line-Count')      
       ax.add_artist(leg1)
    
    return


def getLegendStr(Legend,LegendStyle, key, Num=0):
    """Creation of the legend string, based on **LegendStyle** value"""
    LegendString = "_nolegend_"
    if Legend==True:
        if LegendStyle.lower() == "Str".lower():
            LegendString = str(key)
        elif LegendStyle.lower() == "Str(Num)".lower():
            LegendString = str(key) + " (" + str(Num) + ")"
            
    return LegendString


def SaveFig(fname, dpi=600):
    """
    use plt.savefig for quickplot

    Parameters
    ----------
    fname : namepathstring of save file
    """

    plt.savefig(
        fname,
        dpi=None,
        facecolor="w",
        edgecolor="w",
        orientation="portrait",
        papertype=None,
        format=None,
        transparent=False,
        bbox_inches=None,
        pad_inches=0.1,
        frameon=None,
        metadata=None,
    )
    return





def quickplot(
    Netz,
    Info="",
    FigSize=(12.5,8.5),
    Names=False,
    alpha=1,
    SingleColor="",
    SingleMarker="",
    SingleLineWidth="",
    tagstyle=2,
    Cursor_Points=True,
    Cursor_Lines=False,
    SingleLabel="",
    SingleSize="",
    SingleAlpha="",
    loops=False,
    SingleLineStyle="solid",
    savefile="",
    PlotList=[],
    IgnoreList=["all"],
    MapColor=True,
    countrycode="EU",
    GridOn=False,
    figureNum=1,
    Save=False,
    Axis=True,
    Frame=True,
    savedpi=300,
    SupTitleStr="",
    LegendStyle="Str",
    selectList=[],
    orig_path=False,
    Legend=True,
    MapAlpha=1,
    Fig=False,
    hold=False,
    BackGroundAlpha=0,
    fontsize=13,
    linewidth=0.8,
    parameter="",
    randomlinecolors=False,
    thicklines=False,
    TM_Borders_filename=None,
    dictionary="param",):
    """
    Creates Plot of Netz-Class object

    Fast Usage Example (with tuple):

        quickplot( (Netz,'PipeLines','Nodes') )

    Normal Usage:

    Parameters
    ----------
    Netz                An Instance of a SciGRID_gas network class
    countrycode         str, 2-digit countrycode - will be used to cut basemap [default: 'EU']

    Overplotting
    -----------
    Fig                 matplotlib fig-object, the return value of quickplot() can be used to print on top of the last plot
    hold                boolean, if true quickplot will not plot

    Options
    ------------
    loops               boolean, show double pipelines in color default[False]

    Single Style Object
    -----------------
    alpha               [default: 1],transparency
    SingleColor         str, same as in Matplotlib [default: '']
    SingleMarker        str, same as in Matplotlib [default: '']
    SingleLineWidth     str, same as in Matplotlib [default: '']
    SingleLabel         str, same as in Matplotlib [default: '']
    SingleSize          str, same as in Matplotlib [default: '']
    SingleAlpha         str, same as in Matplotlib [default: '']

    
    Style Parameters
    ----------------
    MapColor            boolean, background map in color (True) or in blackwhite (False) [default: True]
    FigSize             (x,y)=(float,float); [default: (12.5,8.5)
    figureNum           int, number of the figure [default: 1]
    SupTitleStr         str, of title of plot [default: '']
    LegendStyle         'Str' or 'Str(Num)', only Names ->'Str'; Names with count-> 'Str(Num)' [default: 'Str']
    Legend              boolean, shows legend [default=False]
    Names               boolean, show component names on map [default: False]
    Cursor_Points       boolean, if true you can get details on mouseclick [default: True]
    Cursor_Lines        boolean, if true you can get details in Window on mouseclick [default: False]
                           

    Save Figure
    ---------------
    savefile            str, namepath [default: '']
    Save                boolean, to save the plot [default: False]
    save_dpi            int, nuber indicating the dots per inch [default: 300]

    Developer Parameters
    ------------------
    PlotList            List of plotable NetClass.Elements (e.g. Nodes, Pipelines)
    IgnoreList          List of ignorable NetClass.Elements (e.g. Nodes, PipeLines)
    GridOn              boolean to plot a mash grid as background [default: False]
    Axis                boolean,turn off x and y axis
    Frame               boolean,turn off outer frame
    tagstyle            int=1,2,3 or 4, how much details mpl cursor shows [default: 1]
    Info                Info object to Customize quickplot [Default: '']
    
    """
    

    if countrycode == None or type(countrycode) == list:
        if type(savefile)!=str: 
            savefile = (
            str(Info.get("savefile", os.path.join("./Ausgabe/Plots/Quickplot.pdf"))
            ))
    else:
        if type(savefile)!=str: 
            savefile = (
                str(
                    Info.get(
                        "savefile",os.path.join("./Ausgabe/Plots/Quickplot_" + countrycode + ".pdf",
                    )
                )
            ))
    if Fig==False:
        Fig = [fig, ax] = PlotMap(
            countrycode=countrycode,
            figureNum=figureNum,
            FigSize=FigSize,
            MapColor=MapColor,
            Axis=Axis,
            SupTitleStr=SupTitleStr,
            MapAlpha=MapAlpha,
            BackGroundAlpha=BackGroundAlpha,
            TM_Borders_filename=TM_Borders_filename
    )
    if Netz == None:
        keys = []
    # Now you can quickplot( (Netz,'Pipeline') )
    elif isinstance(Netz, tuple):
        keys = [
            *Netz[1:],
        ]
        Netz = Netz[0]
        IgnoreList = []
        PlotList = keys

    else:
        keys = list(Netz.__dict__.keys())

    if PlotList == []:
        PlotList = Netz.CompLabels()

    #print(keys)
    linekeys = ["PipeSegments", "PipeLines"]

    #Garantie none Line elements last
    for comp in PlotList:
        if comp in linekeys:
            PlotList.remove(comp)
            PlotList.append(comp)

    
    colors = cycle(["b", "g", "r", "m", "c", "y", "k"])
    markers = cycle(["o", "x", "+", "P", "D", "s", "^"])

    size_default = 25#18
    line_size_default = 1
    linestyle = SingleLineStyle
    if SingleSize != "":
        size = SingleSize

    if SingleLineWidth != "":
        line_size_default = SingleLineWidth

    small = 20
    cursor_data = {"point": {}, "line": {}}

    if "all" not in IgnoreList:
        for key in keys:
            if key not in IgnoreList and key not in PlotList:
                if (len(Netz.__dict__[key])) > 0:
                    if key in linekeys:
                        
                        color = Comp_Style(line_size_default,size_default,small).get(str(key), {}).get("color", next(colors))
                        SingleLineWidth = Comp_Style(line_size_default,size_default,small).get(str(key), {}).get(
                            "size", size_default
                        )
                        QuickObject = PO.Ways2Lines(
                            Netz.__dict__[key],
                            tagstyle=tagstyle,
                            parameter=parameter,
                            thicklines=thicklines,
                            orig_path=orig_path,
                            dictionary=dictionary,
                        )
                        color = SingleColor if SingleColor != "" else color
                        key = SingleLabel if SingleLabel != "" else key
                        alpha = SingleAlpha if SingleAlpha != "" else alpha
                        linestyle = (
                            SingleLineStyle if SingleLineStyle != "" else linestyle
                        )
                        if len(selectList) == 0:
                            cursor_data=cursor_data
                            LegendList=Netz.__dict__[key]
                        else:
                            cursor_data="deactivate"
                            LegendList=selectList
                                                              
                        LegendString = getLegendStr(Legend,
                            LegendStyle, key, len(LegendList))
                        

                            # Plotting
                        PlotLines(
                            *Fig,
                            QuickObject,
                            linestyle=SingleLineStyle,
                            linewidth=int(SingleLineWidth),
                            cursor_data=cursor_data,
                            Cursor_Lines=Cursor_Lines,#
                            loops=loops,
                            alpha=alpha,
                            color=color,
                            legend=LegendString,
                            Info=Info,                    
                            selectList=selectList,
                            parameter=parameter,
                            thicklines=thicklines
                        )

        # Plotting of point data (e.g. Storages)

        for key in keys:
            if key not in IgnoreList and key not in PlotList:
                if (len(Netz.__dict__[key])) > 0:
                    if key not in linekeys:

                        color = Comp_Style(line_size_default,size_default,small).get(key, {}).get("color", next(colors))
                        marker = Comp_Style(line_size_default,size_default,small).get(key, {}).get("marker", next(markers))
                        size = Comp_Style(line_size_default,size_default,small).get(key, {}).get("size", size_default)

                        QuickObject = PO.Nodes2Points(
                            Netz.__dict__[key],
                            tagstyle=tagstyle,
                            parameter=parameter,
                            dictionary=dictionary,
                        )
                        color = SingleColor if SingleColor != "" else color
                        key = SingleLabel if SingleLabel != "" else key
                        marker = SingleMarker if SingleMarker != "" else marker
                        size = SingleSize if SingleSize != "" else size
                        alpha = SingleAlpha if SingleAlpha != "" else alpha
                        linestyle = (
                            SingleLineStyle if SingleLineStyle != "" else linestyle
                        )
                        if len(selectList) == 0:
 
                            LegendString = getLegendStr(Legend,
                                LegendStyle, key, len(Netz.__dict__[key])
                            )
 
                        else:

                            LegendString = getLegendStr(Legend,
                                LegendStyle, key, len(selectList)
                            )

                        # Pottting
                        PlotPoints(
                            *Fig,
                            QuickObject,
                            alpha=alpha,
                            names=Names,
                            cursor=Cursor_Points,
                            cursor_data=cursor_data,
                            color=color,
                            legend=LegendString,
                            Symbol=marker,
                            Info=Info,
                            fontsize=fontsize,
                            Size=str(size),
                            selectList=selectList,
                            parameter=parameter
                        )

    # Plotting Nodes last

    for key in PlotList:
        if len(keys) > 0:
            if (len(Netz.__dict__[key])) > 0:
                if key not in linekeys:
                    color = Comp_Style(line_size_default,size_default,small).get(key, {}).get("color", next(colors))
                    marker = Comp_Style(line_size_default,size_default,small).get(key, {}).get("marker", next(markers))
                    size = Comp_Style(line_size_default,size_default,small).get(key, {}).get("size", size_default)
                    QuickObject = PO.Nodes2Points(
                        Netz.__dict__[key],
                        tagstyle=tagstyle,
                        parameter=parameter,
                        dictionary=dictionary,
                    )
                    color = SingleColor if SingleColor != "" else color
                    key = SingleLabel if SingleLabel != "" else key
                    marker = SingleMarker if SingleMarker != "" else marker
                    size = SingleSize if SingleSize != "" else size
                    alpha = SingleAlpha if SingleAlpha != "" else alpha
                    linestyle = SingleLineStyle if SingleLineStyle != "" else linestyle

                    if len(selectList) == 0:
                        LegendString = getLegendStr(Legend,
                            LegendStyle, key, len(Netz.__dict__[key]))

                    else:

                        LegendString = getLegendStr(Legend,
                            LegendStyle, key, len(selectList)
                        )

                    PlotPoints(
                        *Fig,
                        QuickObject,
                        names=Names,
                        cursor_data=cursor_data,
                        cursor=Cursor_Points,
                        color=color,
                        alpha=alpha,
                        legend=LegendString,
                        Symbol=marker,
                        Info=Info,
                        fontsize=fontsize,
                        Size=str(size),
                        selectList=selectList,
                        parameter=parameter
                    )

                else:

                    if key in linekeys:
                        color = Comp_Style(line_size_default,size_default,small).get(key, {}).get("color", next(colors))
                        marker = Comp_Style(line_size_default,size_default,small).get(key, {}).get("marker", next(markers))
                        size = Comp_Style(line_size_default,size_default,small).get(key, {}).get("size", size_default)
                        SingleLineWidth = Comp_Style(line_size_default,size_default,small).get(str(key), {}).get(
                            "size", size_default
                        )
                        QuickObject = PO.Ways2Lines(
                            Netz.__dict__[key],
                            tagstyle=tagstyle,
                            parameter=parameter,
                            orig_path=orig_path,
                            pipelinethickness=thicklines,
                            dictionary=dictionary,
                        )
                        color = SingleColor if SingleColor != "" else color
                        key = SingleLabel if SingleLabel != "" else key
                        marker = SingleMarker if SingleMarker != "" else marker
                        size = SingleSize if SingleSize != "" else size
                        alpha = SingleAlpha if SingleAlpha != "" else alpha
                        linestyle = (
                            SingleLineStyle if SingleLineStyle != "" else linestyle
                        )
                        if len(selectList) == 0:

                            LegendString = getLegendStr(Legend,
                                LegendStyle, key, len(Netz.__dict__[key]))

                        else:
                            LegendString = getLegendStr(Legend,
                                LegendStyle, key, len(selectList))
                         
                        PlotLines(
                            *Fig,
                            QuickObject,
                            cursor_data=cursor_data,
                            Cursor_Lines=Cursor_Lines,
                            linewidth=int(SingleLineWidth),
                            linestyle=SingleLineStyle,
                            alpha=alpha,
                            loops=loops,
                            color=color,
                            legend=LegendString,
                            Info=Info,
                            selectList=selectList,
                            parameter=parameter,
                            thicklines=thicklines
                        )
    
    def onpick(event):
        thisline = event.artist
        url = thisline.url
        print(url)

        pass
    #if Fig!=False:
        fig=Fig[0]

    if hold==False and Fig!=False:
        fig=Fig[0] 
        fig.canvas.mpl_connect("pick_event", onpick)
    #elif hold==True and Fig==False:
        
    
    if not Frame:
        plt.axis("off")

    if not Axis:
        # fig.axis('off')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    if LegendStyle == "":
        ax.legend()

    if GridOn:
        plt.grid()

    if Save == True:
        fig.savefig(savefile, dpi=save_dpi)
        print("\nFile saved to: " + Cyan + savefile + End)

    if Cursor_Points == True:
        PlotCursor(cursor_data,"point", multiple=False, hover=False)
    if Cursor_Lines == True:
        PlotCursor(cursor_data,"line", multiple=False, hover=False)

    if hold==False:
        plt.show()

    return Fig



