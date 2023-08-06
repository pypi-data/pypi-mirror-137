import py2D

win = py2D.Screen_([400,400])
run = True


sli = py2D.Widgets_.Sliders(
    win.screen,
    [100,100],100,10,0,100,1
)


while(run):
    run = win.close()
    win.Update().BG_col('white')

    sli.Update()
    print(sli.Get_selected())