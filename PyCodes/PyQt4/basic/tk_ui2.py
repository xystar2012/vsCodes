from tkinter import *  
  
import time  
import random   
import sys
   
def main():  
  
  # print sys.path
  ###******回调函数定义******###  
    
  def sendMsg():                  #发送消息  
    strMsg = 'i_chaoren:' + time.strftime("%Y-%m-%d %H:%M:%S",  
                                  time.localtime()) + '\n '  
    txtMsgList.insert(END, strMsg, 'greencolor')   #插入到tag位置  
    txtMsgList.insert(END, txtMsg.get('0.0', END))  
    txtMsg.delete('0.0', END)  
       
  def cancelMsg():                #取消消息  
    txtMsg.delete('0.0', END)  
   
  def sendMsgEvent(event):        #发送消息事件  
    if event.keysym == "Return":  #按回车键可发送  
      sendMsg()  
  
  def red():                      #Canvas背景色控制  
    imgCanvas.config(bg='red')  
  def green():  
    imgCanvas.config(bg='green')  
  def blue():  
    imgCanvas.config(bg='blue')  
  def color1():  
    names = ['red', 'green', 'blue','yellow','white','SlateGray','SpringGreen','LightSteelBlue','Cyan','BlueViolet','GhostWhite']  
    for i in names:  
      imgCanvas.config(bg=i)  
      time.sleep(0.4)  
      imgCanvas.update()  
      
  def Oval():                     #Canvas绘制几何图案  
    imgCanvas.create_oval(110, 20, 170, 120)  
  def Polygon():  
    imgCanvas.create_polygon(20, 20, 110, 50,100,110,40,120)  
  
  def fontSize(ev=None):          #字体缩放  
    timeText2.config(font='Helvetica -%d bold' % sizeScale.get())  
    sizeLabel.config(text='字号：%d'% sizeScale.get())  
  
  def txtlist():                  #字典实现--书名与内容的对应  
    book={'NO.1 《平凡的世界》  路遥':'1.一个平平常常的日子，细蒙蒙的雨丝夹着一星半点的雪花，正纷纷淋淋的向大地飘洒着，时令已快到惊蛰，雪当然再不会存留，往往还没等落地，就消失的无踪无影了，黄土高原严寒而漫长的冬天看来就要过去，但那真正温暖的春天还远远没有到来。\n2、这时候，他也体验到了类似孙少平的那种感觉：只有繁重的体力劳动才使精神上的痛苦变为某种麻木，以致思维局限在机械性活动中。\n3、哭，笑，都是因为欢乐，哭的人知道而笑的人不知道，这欢乐是多少痛苦所换来的。',  
          'NO.2 《看见》  柴静':'1.写本身也是一种发现自己的过程，你不写永远都知道自己身上发生了什么。\n2.保持对不同论述的警惕，才能保持自己的独立性。\n3.灵魂变得沉重，是因为爱，因为所爱的东西，眼睁睁在失去，却无能为力。\n4.我可能做不到更好了，但还是要像朱光潜说的那样，此时，此地，此身，此时我能做的事情绝不推诿到下一时刻，此地我能做的事情绝不换另一种境地再去做，此身我能做的事绝不妄想与他人来替代。\n5.如果带着强烈的预设和反感，你就没有办法真的认识这个人。',  
          'NO.3 《亲爱的安德烈》龙应台':'1.我也要求你读书用功，不是因为我要你跟别人比较成就，而是因为，我希望你将来会拥有会选择的权利，选择有意义、有时间的工作，而不是被迫谋生。 当你的工作在你的心中有意义，你就有成就感。当你的工作给你时间，不剥夺你的生活，你就有尊严。成就感和尊严，给你快乐。\n2.农村中长大的孩子，会接触更真实的社会，接触更丰富的生活，会感受到人间的各种悲欢离合。所以更能形成那种原始的，正面的价值观—那“愚昧无知”的渔村，确实没有给我知识，但是给了我一种能力，悲悯同情的能力，使得我在日后面对权利的傲慢、欲望的嚣张和种种时代的虚假时，仍旧得以穿透，看见文明的核心关怀所在。'}  
    txtText.delete(0.0,END)  
    txtText.insert(END,book[txtSpinbox.get()])  
  def message():                  #弹出窗口  
    messagebox.showinfo("联系人搜索","这是一个假的功能！！")  
      
  ###******回调函数定义******###  
      
      
    
  #创建窗口   
  t = Tk()  
  t.title('超级聊天窗口')     # 窗口名称  
  t.resizable(0, 0)           # 禁止调整窗口大小  
         
  
  ###******创建frame容器******###  
    
  #第一列  
  frmA1 = Frame(width=180, height=30)  
  frmA2 = Frame(width=180, height=290)  
  frmA3 = Frame(width=180, height=140)   
  frmA4 = Frame(width=180, height=30)   
  #第二列  
  frmB1 = Frame(width=350, height=320)  
  frmB2 = Frame(width=350, height=150)  
  frmB3 = Frame(width=350, height=30)  
  #第三列  
  frmC1 = Frame(width=200, height=30)  
  frmC11= Frame(width=200, height=290)  
  frmC2 = Frame(width=200, height=150)  
  frmC3 = Frame(width=200, height=30)  
  
  ###******创建frame容器******###  
  
    
  ###******创建控件******###  
  
  #1.Text控件  
  txtMsgList = Text(frmB1)                          #frmB1表示父窗口  
  #创建并配置标签tag属性  
  txtMsgList.tag_config('greencolor',               #标签tag名称  
                        foreground='#008C00')       #标签tag前景色，背景色为默认白色  
  
  txtMsg = Text(frmB2);  
  txtMsg.bind("<KeyPress-Return>", sendMsgEvent)    #事件绑定，定义快捷键  
  
  timeText=Text(frmC2,font=("Times", "28", "bold italic"),height=1,bg="PowderBlue")  
  timeText2=Text(frmC2,fg="blue",font=("Times", "12","bold italic"))  
  
  txtText=Text(frmC11,font=("Times", "11",'bold'),  #字体控制  
               width=24,height=15,                  #文本框的宽（in characters ）和高(in lines) (not pixels!)  
               spacing2=5,                          #文本的行间距  
               bd=2,                                #边框宽度  
               padx=5,pady=5,                       #距离文本框四边的距离  
               selectbackground='blue',             #选中文本的颜色  
               state=NORMAL)                        #文本框是否启用 NORMAL/DISABLED  
  txtText.insert(END,'1.一个平平常常的日子，细蒙蒙的雨丝夹着一星半点的雪花，正纷纷淋淋的向大地飘洒着，时令已快到惊蛰，雪当然再不会存留，往往还没等落地，就消失的无踪无影了，黄土高原严寒而漫长的冬天看来就要过去，但那真正温暖的春天还远远没有到来。\n2、这时候，他也体验到了类似孙少平的那种感觉：只有繁重的体力劳动才使精神上的痛苦变为某种麻木，以致思维局限在机械性活动中。\n3、哭，笑，都是因为欢乐，哭的人知道而笑的人不知道，这欢乐是多少痛苦所换来的。')  
                                                    # insert(插入位置，插入内容)  
  #2.Button控件  
  btnSend = Button(frmB3, text='发 送', width = 8,cursor='heart', command=sendMsg)  
  btnCancel = Button(frmB3, text='取消', width = 8,cursor='shuttle', command=cancelMsg)  
  btnSerch=Button(frmA1, text='搜索联系人',         #button的显示内容  
                  width = 9,height=1,               #宽和高  
                  cursor='man',                     #光标样式       
                  command =message)                 #回调函数  
    
  #3.Entry控件  
  entrySerch=Entry(frmA1, bd =3,width=14,  
                   show='*')                        #输入值以掩码显示      
    
  #4.Scrollbar控件  
  scroLianxi = Scrollbar(frmA2,width=22,cursor='pirate',troughcolor="blue")   
  
  #5.Listbox控件  
  listLianxi = Listbox(frmA2, width=22,height=16,  
                       yscrollcommand = scroLianxi.set )  #连接listbox 到 vertical scrollbar  
  Linkman=['曹操','刘备','孙权','关羽','张飞','赵云','马超','黄忠','张郃','姜维','夏侯惇','魏延','张辽','周瑜','贾诩','典韦','吕布','袁绍','袁术','貂蝉','董卓','华佗','诸葛亮','郭嘉','孙策','孙坚','太史慈','鲁肃','黄盖','程普','程昱','司马懿','曹丕','曹植','曹睿']  
  for line in Linkman:  
      listLianxi.insert(END, "  联系人   ------   " + str(line))  
  scroLianxi.config( command = listLianxi.yview )   #scrollbar滚动时listbox同时滚动  
  
  #6.Canvas控件  
  imgCanvas=Canvas(frmA3,bg='ivory')  
  
  #7.Radiobutton控件  
  var = IntVar()                                    #设置variable和value可以保证只有一个按钮被按下  
  R1 = Radiobutton(frmA4, text="多边形", variable=var, value=1,command=Polygon)  
  R2 = Radiobutton(frmA4, text="椭圆", variable=var, value=2,command=Oval)  
    
  #8.Menubutton控件  
  colorMenubt =  Menubutton (frmA4, text="画板颜色", relief=RAISED )  
  
  #9.Menu控件  
  colorMenubt.menu  =  Menu ( colorMenubt, tearoff = 0 )  
  colorMenubt["menu"]  =  colorMenubt.menu  
  
  colorMenubt.menu.add_checkbutton ( label="红色",command=red)  
  colorMenubt.menu.add_checkbutton ( label="绿色",command=green)  
  colorMenubt.menu.add_checkbutton ( label="蓝色",command=blue)  
  colorMenubt.menu.add_separator()       #添加菜单分隔符  
  colorMenubt.menu.add_checkbutton ( label="连续色",command=color1)  
  
  #10.Scale控件  
  sizeScale = Scale(frmC3,length=135,width=18,from_=10, to=35,orient=HORIZONTAL,command=fontSize,cursor='star',  
                    showvalue=0,         #不显示数值  
                    sliderlength=30,     #滑块的长度               
                    troughcolor='ivory') #滑动条底色  
  sizeScale.set(20)                      #设置滑块的初始值  
  
  #11.Label控件  
  sizeLabel = Label(frmC3,width=8,height=1,bd=1, relief=RIDGE)  
  nameLabel = Label(frmC1, text='   Favorite Book List',font="Times 16 bold italic")  
  
  #12.Spinbox控件  
  txtSpinbox = Spinbox(frmC11,width=24,command=txtlist)  
  txtSpinbox.config(values=['NO.1 《平凡的世界》  路遥','NO.2 《看见》  柴静','NO.3 《亲爱的安德烈》龙应台'])  
    
  ###******创建控件******###  
  
  
  ###******窗口布局******###  
    
  frmA1.grid(row=0, column=0, padx=10, pady=3)  
  frmA2.grid(row=1, column=0, padx=10)  
  frmA3.grid(row=2, column=0, rowspan=1)  
  frmA4.grid(row=3, column=0, rowspan=1)  
    
  frmB1.grid(row=0, column=1, columnspan=1, rowspan=2, padx=1, pady=3)  
  frmB2.grid(row=2, column=1, columnspan=1, padx=1, pady=1)  
  frmB3.grid(row=3, column=1, columnspan=1, padx=1)  
    
  frmC1.grid(row=0, column=2, rowspan=1, padx=1, pady=1)  
  frmC11.grid(row=1, column=2, rowspan=1, padx=1, pady=1)    
  frmC2.grid(row=2, column=2, rowspan=1, padx=1, pady=1)  
  frmC3.grid(row=3, column=2, padx=1)  
   
  ###******窗口布局******###  
    
  
  #固定大小  
  frmA1.grid_propagate(0)  
  frmA2.grid_propagate(0)  
  frmA3.grid_propagate(0)  
  #frmA4.grid_propagate(0)  
    
  frmB1.grid_propagate(0)  
  frmB2.grid_propagate(0)  
  frmB3.grid_propagate(0)  
    
  frmC1.grid_propagate(0)  
  frmC11.grid_propagate(0)    
  frmC2.grid_propagate(0)  
  frmC3.grid_propagate(0)  
  
  
  ###******控件布局******###   
  
  btnSend.grid(row=0, column=0)  
  btnCancel.grid(row=0, column=1)  
  btnSerch.grid(row=0,column=1)  
  
  nameLabel.grid()  
  sizeLabel.grid(row=0,column=0)  
    
  txtMsgList.grid()  
  txtMsg.grid()  
  
  entrySerch.grid(row=0,column=0)  
   
  scroLianxi.grid(row=0,column=1,ipady=120)  
  
  listLianxi.grid(row=0,column=0)  
  
  imgCanvas.grid(row=0,column=0,sticky=N)  
  
  colorMenubt.grid(row=0,column=0)  
  
  R1.grid(row=0,column=1)   
  R2.grid(row=0,column=2)  
    
  timeText.grid(row=0,column=0)  
  timeText2.grid(row=1,column=0,sticky=E+W)  
  txtText.grid(row=1,column=0,pady=5)  
    
  sizeScale.grid(row=0,column=1)  
  txtSpinbox.grid(row=0,column=0)  
    
  ###******控件布局******###   
  
  
  #时间模块，开启之后会影响运行速度  
  '''''  
  while 1: 
      Time1 = time.strftime("   %H:%M:%S",time.localtime()) + '\n ' 
      Time2 = time.strftime("  %Y/%m/%d",time.localtime()) + '\n ' 
      Time3 = time.strftime("   %A",time.localtime()) + '\n ' 
                             
      timeText.insert(END, Time1) 
      timeText2.insert(END, Time2) 
      timeText2.insert(END, Time3) 
                             
      time.sleep(1) 
      timeText.update() 
      timeText.delete(1.0,END) 
      timeText2.delete(1.0,END) 
  '''  
  #主事件循环  
  t.mainloop()  
   
if __name__ == '__main__':  
    main()  