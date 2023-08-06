import mplcursors
def plotLinesWithCursor(Netz, countrycode="EU", figureNum=1):

    import configparser
    from pathlib import Path

    BackGroundAlpha = 0
    MapAlpha = 1
    SupTitleStr = ""
    MapColor = True

    Setup_Visuell = Path(os.getcwd() + "/Setup/Setup_Visuell.ini")
    InfoVisuell = configparser.ConfigParser()
    InfoVisuell.read(Setup_Visuell)

    fig, ax = PlotMap(
        countrycode=countrycode,
        figureNum=figureNum,
        MapColor=MapColor,
        SupTitleStr=SupTitleStr,
        MapAlpha=MapAlpha,
        BackGroundAlpha=BackGroundAlpha,
    )

    for pipe in Netz.PipeSegments:
        (line,) = ax.plot(pipe.long, pipe.lat, "-", picker=5)  # 5 points tolerance
        line.url = dict()

        line.url.update({"id": pipe.id})
        if "diameter_mm" in pipe.param:
            line.url.update({"diam": pipe.param["diameter_mm"]})
        else:
            line.url.update({"diam": "missing"})
        if "max_cap_M_m3_per_d" in pipe.param:
            line.url.update({"cap": pipe.param["max_cap_M_m3_per_d"]})
        else:
            line.url.update({"cap": "missing"})
        if "max_pressure_bar" in pipe.param:
            line.url.update({"press": pipe.param["max_pressure_bar"]})
        else:
            line.url.update({"press": "missing"})

    def onpick(event):
        thisline = event.artist
        url = thisline.url
        print("id   :", url["id"])
        print("diam :", url["diam"])
        print("cap  :", url["cap"])
        print("press:", url["press"])
        print(" ")

    fig.canvas.mpl_connect("pick_event", onpick)

    plt.show()

def PlotCursor(cursor_data,typ, multiple, hover):
    """
    Allows to show underlying data by clicking on the map, currently works only for node objects
    and only for a very small set of Pipelines.

    Parameters
    ----------
    cursor_data : Data you wish to hover
    multiple : If false only one hover at the same time
    hover : Boolean

    Returns
    -------
    None.
    """

    pointlist = list(cursor_data["point"].keys())
    linelist = list(cursor_data["line"].keys())
    #cursorlist = pointlist + linelist
    cursorlist= list(cursor_data[typ].keys())
    cursor = mplcursors.cursor(cursorlist, multiple=False, hover=False)

    @cursor.connect("add")
    def on_add(sel):
        if sel.artist in pointlist:
            text = cursor_data["point"][sel.artist][sel.target.index]
        elif sel.artist in linelist:
            text = cursor_data["line"][sel.artist]

        sel.annotation.set_text(text)
        sel.annotation.get_bbox_patch().set(fc="white")
        sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=0.5)

    return
    
