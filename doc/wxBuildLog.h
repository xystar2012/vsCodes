


// /etc/profile

LD_LIBRARY_PATH=/opt/sdk:$LD_LIBRARY_PATH
PKG_CONFIG_PATH=/opt/ffmpeg/lib/pkgconfig:/opt/zlib-1.2.11/lib/pkgconfig:/opt/opencv_2.4.12/lib/pkgconfig:/opt/SDL2-2.0.5/lib/pkgconfig:/opt/qt5.6.2_static/lib/pkgconfig:$PKG_CONFIG_PATH
export LD_LIBRARY_PATH PKG_CONFIG_PATH


// .bashrc
TERM=xterm
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/Devel
        source /usr/local/bin/virtualenvwrapper.sh
fi




## visualGdb  添加编译选项时 如果 LinuxGdb 设置为 vsGdb 会存在编译问题

sudo apt-get install freeglut3 freeglut3-dev
sudo apt-get install mesa-common-dev mesa-utils
//  Libs:
DEBUG=1 _FILE_OFFSET_BITS=64 __WXGTK__ NDEBUG linux __LINUX__

/opt/wxWidgets_3.0.2/lib/wx/include/gtk2-unicode-static-3.0 /opt/wxWidgets_3.0.2/include/wx-3.0 /opt/boost_1.55/include /opt/gltools/include /opt/3dLibs /opt/opencv_2.4.12/include /usr/lib/x86_64-linux-gnu/gtk-2.0/include /usr/include/gtk-2.0 /usr/include/atk-1.0 /usr/include/cairo /usr/include/gdk-pixbuf-2.0 /usr/include/pango-1.0 /usr/include/gio-unix-2.0/ /usr/include/freetype2 /usr/include/glib-2.0 /usr/lib/x86_64-linux-gnu/glib-2.0/include /usr/include/pixman-1 /usr/include/libpng12 /usr/include/harfbuzz /opt/linux/EagleSDKTrunk/include ../LibCommon /opt/ffmpeg3.0/include

/opt/boost_1.55/lib /opt/gltools/lib /opt/opencv_2.4.12/lib

wx_gtk2u_gl-3.0 boost_filesystem boost_system gltools glut GL GLU opencv_core opencv_features2d opencv_flann opencv_imgproc opencv_highgui

-L/opt/wxWidgets_3.0.2/lib -pthread /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_xrc-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_qa-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_baseu_net-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_html-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_adv-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_core-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_baseu_xml-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_baseu-3.0.a -pthread -lgthread-2.0 -lX11 -lXxf86vm -lSM -lgtk-x11-2.0 -lgdk-x11-2.0 -latk-1.0 -lgio-2.0 -lpangoft2-1.0 -lpangocairo-1.0 -lgdk_pixbuf-2.0 -lcairo -lpango-1.0 -lfontconfig -lgobject-2.0 -lglib-2.0 -lfreetype -lpng -lexpat -lwxregexu-3.0 -lwxtiff-3.0 -lwxjpeg-3.0 -lz -ldl -lm


-ggdb -ffunction-sections -O0  -std=c++11

// MainFrame

Preprocessor:

DEBUG=1 _FILE_OFFSET_BITS=64 __WXGTK__ NDEBUG linux __LINUX__

/opt/wxWidgets_3.0.2/lib/wx/include/gtk2-unicode-static-3.0 /opt/wxWidgets_3.0.2/include/wx-3.0 /opt/boost_1.55/include /opt/gltools/include /opt/3dLibs /opt/opencv_2.4.12/include /usr/lib/x86_64-linux-gnu/gtk-2.0/include /usr/include/gtk-2.0 /usr/include/atk-1.0 /usr/include/cairo /usr/include/gdk-pixbuf-2.0 /usr/include/pango-1.0 /usr/include/gio-unix-2.0/ /usr/include/freetype2 /usr/include/glib-2.0 /usr/lib/x86_64-linux-gnu/glib-2.0/include /usr/include/pixman-1 /usr/include/libpng12 /usr/include/harfbuzz /opt/linux/EagleSDKTrunk/include ../../Libs/LibCommon /opt/ffmpeg3.0/include ../MainFrame

/opt/boost_1.55/lib /opt/gltools/lib /opt/opencv_2.4.12/lib /opt/sdk /opt/ffmpeg3.0/lib

TestGui CameraPluginMgr CamSerial Libs sdk wx_gtk2u_gl-3.0 boost_filesystem boost_system gltools glut GL GLU boost_date_time boost_system boost_regex boost_filesystem avformat avcodec swscale avutil avfilter swresample avdevice opencv_core opencv_features2d opencv_flann opencv_imgproc opencv_highgui rt


Addition linksInputs:
-L/opt/wxWidgets_3.0.2/lib -pthread /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_xrc-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_qa-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_baseu_net-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_html-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_adv-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_gtk2u_core-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_baseu_xml-3.0.a /opt/wxWidgets_3.0.2/lib/libwx_baseu-3.0.a -pthread -lgthread-2.0 -lX11 -lXxf86vm -lSM -lgtk-x11-2.0 -lgdk-x11-2.0 -latk-1.0 -lgio-2.0 -lpangoft2-1.0 -lpangocairo-1.0 -lgdk_pixbuf-2.0 -lcairo -lpango-1.0 -lfontconfig -lgobject-2.0 -lglib-2.0 -lfreetype -lpng -lexpat -lwxregexu-3.0 -lwxtiff-3.0 -lwxjpeg-3.0 -lz -ldl -lm

cFlags:
-ggdb -ffunction-sections -O0 -std=c++11


// CameraPluginMgr

 -Wl,-Bsymbolic     -Wl,--as-needed
 dlopen(plname, RTLD_NOW | /*RTLD_GLOBAL*/ RTLD_DEEPBIND or RTLD_LOCAL);


//cameras   LinuxDebug   

Preprocessor macros:
 __LINUX__
 

 INCLUDE:
 /opt/boost_1.55/include /opt/linux/EagleSDKTrunk/include
 
 
 LibPath& LibName
 /opt/sdk
 CamSerial
 
 CFLags:
 -std=c++11
 
 
 
 
 //Qt  build
 
 
 __STDC_FORMAT_MACROS _DEBUG __LINUX__
 
 /opt/ffmpeg3.0/include /opt/boost_1.55/include /opt/linux/EagleSDKTrunk/include . LinuxDebug LibCommon /opt/opencv_2.4.12_static/include
 
 /opt/ffmpeg3.0/lib /opt/boost_1.55/lib /opt/sdk /opt/opencv_2.4.12_static/lib
 
 camerasCtrl CamSerial sdk dl qcustomplot boost_date_time boost_system boost_regex boost_filesystem avformat avcodec swscale avutil avfilter swresample avdevice opencv_imgproc opencv_core pthread z
 
  CamSerial 
 
 
 
 // kugou
 
 avdevice avfilter swscale avformat avcodec xcb-shm xcb-xfixes xcb-render xcb-shape xcb X11 z swresample avutil m SDL2 SDL2main z dl X11 pthread
