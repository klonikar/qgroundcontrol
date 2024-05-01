'''
# Execute the commands as below:
C:/Qt/6.6.1/msvc2019_64/bin/qtenv2.bat
"C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Auxiliary/Build/vcvarsall.bat" amd64
cd %HOMEPATH%/projects/qgroundcontrol
path=C:/ProgramData/anaconda3;%path%;
python make_win64.py --build newbuild

'''
import os
import sys
import glob
import time
import tempfile
from datetime import datetime
import argparse
import re

def compileSources(sourceFiles, compilationCmd, ignoreFiles, ignorePatterns):
	if len(sourceFiles) == 0:
		return
	tmpFile, tmpFileName = tempfile.mkstemp(text=True)
	print(f'using tmpFile {tmpFileName} to compile {sourceFiles}')
	modifiedSourceFiles = []
	for s in sourceFiles:
		ignoreSource = False
		if os.path.basename(s) in ignoreFiles:
			ignoreSource = True
		for p in ignorePatterns:
			if re.search(p, s):
				ignoreSource = True
				break
		if ignoreSource:
			print(f'Skipping {s}')
			continue
		objFileName = os.path.basename(s).split('.')[0] + '.obj'
		if not os.path.exists(objFileName) or os.path.getmtime(s) >= os.path.getmtime(objFileName):
			modifiedSourceFiles.append(s)
		else:
			print(f'Skipping {s}: {objFileName} more recent.')
	if len(modifiedSourceFiles):
		os.write(tmpFile, str.encode('\n'.join(modifiedSourceFiles)))
		os.close(tmpFile)
		os.system(compilationCmd + tmpFileName)

def compileAllSources(dirName, cppCompilationCmd, cCompilationCmd, ignoreFiles, ignorePatterns):
	cppFiles = glob.glob(dirName + '/*.cpp')
	compileSources(cppFiles, cppCompilationCmd, ignoreFiles, ignorePatterns)
	ccFiles = glob.glob(dirName + '/*.cc')
	compileSources(ccFiles, cppCompilationCmd, ignoreFiles, ignorePatterns)
	cxxFiles = glob.glob(dirName + '/*.cxx')
	compileSources(cxxFiles, cppCompilationCmd, ignoreFiles, ignorePatterns)
	cFiles = glob.glob(dirName + '/*.c')
	compileSources(cFiles, cCompilationCmd, ignoreFiles, ignorePatterns)

def fast_scandir(dirname, ignoreDirs):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir() and os.path.basename(f.path) not in ignoreDirs]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname, ignoreDirs))
    return subfolders

if __name__ == '__main__':
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("--build", default='build',
                    help="build dir")
	args = parser.parse_args()

	qtLibPath = 'C:/Qt/6.6.1/msvc2019_64/'
	gstreamerPath = 'C:/gstreamer/1.0/msvc_x86_64/'
	cxxFlags = f'-nologo -Zc:wchar_t -FS -Zc:rvalueCast -Zc:inline -Zc:throwingNew -permissive- -Zc:__cplusplus -Zc:externConstexpr -MP -O2 -Zi -MD /Gy /Zo -std:c++17 -utf-8 -GL -W3 -w34100 -w34189 -w44996 -w44456 -w44457 -w44458 -wd4577 -wd4467 /WX /W3 /wd4005 /wd4290 /wd4267 /wd4100 -EHsc /FdQGroundControl.vc.pdb -DUNICODE -D_UNICODE -DWIN32 -DQGC_GST_STREAMING -DHAVE_QT_QPA_HEADER -DQT_QUICK3D_LIB -DQT_QUICK3DUTILS_LIB -DHAVE_QT_WIN32 -DQT_SHADERTOOLS_LIB -DQT_QUICK3DRUNTIMERENDER_LIB -D_ENABLE_EXTENDED_ALIGNED_STORAGE -DWIN64 -DQGC_GST_TAISYNC_DISABLED -DQGC_GST_MICROHARD_DISABLED -D__STDC_LIMIT_MACROS -D__STDC_CONSTANT_MACROS -DDAILY_BUILD -DAPP_VERSION_STR="\\\"vUnknown\\\"" -DEIGEN_MPL2_ONLY -D_TTY_NOWARN_ -DQT_NO_DEBUG -DQT_MESSAGELOGCONTEXT -DQGC_DISABLE_PAIRING -DQGC_USE_ALL_MESSAGES -DNOMINMAX -DXZ_DEC_ANY_CHECK -DXZ_USE_CRC64 -DQGC_APPLICATION_NAME="\\"QGroundControl\\"" -DQGC_ORG_NAME="\\"QGroundControl.org\\"" -DQGC_ORG_DOMAIN="\\"org.qgroundcontrol\\"" -DNDEBUG -DQT_NO_DEBUG -DQT_LOCATION_LIB -DQT_POSITIONINGQUICK_LIB -DQT_QUICKSHAPES_LIB -DQT_QUICKCONTROLS2_LIB -DQT_QUICKWIDGETS_LIB -DQT_QUICK_LIB -DQT_CHARTS_LIB -DQT_OPENGLWIDGETS_LIB -DQT_OPENGL_LIB -DQT_WIDGETS_LIB -DQT_SVG_LIB -DQT_TEXTTOSPEECH_LIB -DQT_MULTIMEDIA_LIB -DQT_GUI_LIB -DQT_CONCURRENT_LIB -DQT_POSITIONING_LIB -DQT_QMLMODELS_LIB -DQT_QML_LIB -DQT_QMLINTEGRATION_LIB -DQT_NETWORK_LIB -DQT_SQL_LIB -DQT_XML_LIB -DQT_CORE5COMPAT_LIB -DQT_SERIALPORT_LIB -DQT_TESTLIB_LIB -DQT_CORE_LIB -DQT_TESTCASE_BUILDDIR="\\"C:/Users/Kiran Lonikar/projects/qgroundcontrol/{args.build}\\""'
	cFlags = f'-nologo -Zc:wchar_t -FS -O2 -Zi -MD /Gy /Zo -utf-8 -GL -W3 -w44456 -w44457 -w44458 /FdQGroundControl.vc.pdb -DUNICODE -D_UNICODE -DWIN32 -D_ENABLE_EXTENDED_ALIGNED_STORAGE -DWIN64 -DQGC_GST_TAISYNC_DISABLED -DQGC_GST_MICROHARD_DISABLED -D__STDC_LIMIT_MACROS -D__STDC_CONSTANT_MACROS -DDAILY_BUILD -DAPP_VERSION_STR="\\"vUnknown\\"" -DEIGEN_MPL2_ONLY -D_TTY_NOWARN_ -DQT_NO_DEBUG -DQGC_GST_STREAMING -DHAVE_QT_QPA_HEADER -DQT_QUICK3D_LIB -DQT_QUICK3DUTILS_LIB -DHAVE_QT_WIN32 -DQT_SHADERTOOLS_LIB -DQT_QUICK3DRUNTIMERENDER_LIB -DQT_MESSAGELOGCONTEXT -DQGC_DISABLE_PAIRING -DQGC_USE_ALL_MESSAGES -DNOMINMAX -DXZ_DEC_ANY_CHECK -DXZ_USE_CRC64 -DQGC_APPLICATION_NAME="\\"QGroundControl\\"" -DQGC_ORG_NAME="\\"QGroundControl.org\\"" -DQGC_ORG_DOMAIN="\\"org.qgroundcontrol\\"" -DNDEBUG -DQT_NO_DEBUG -DQT_LOCATION_LIB -DQT_POSITIONINGQUICK_LIB -DQT_QUICKSHAPES_LIB -DQT_QUICKCONTROLS2_LIB -DQT_QUICKWIDGETS_LIB -DQT_QUICK_LIB -DQT_CHARTS_LIB -DQT_OPENGLWIDGETS_LIB -DQT_OPENGL_LIB -DQT_WIDGETS_LIB -DQT_SVG_LIB -DQT_TEXTTOSPEECH_LIB -DQT_MULTIMEDIA_LIB -DQT_GUI_LIB -DQT_CONCURRENT_LIB -DQT_POSITIONING_LIB -DQT_QMLMODELS_LIB -DQT_QML_LIB -DQT_QMLINTEGRATION_LIB -DQT_NETWORK_LIB -DQT_SQL_LIB -DQT_XML_LIB -DQT_CORE5COMPAT_LIB -DQT_SERIALPORT_LIB -DQT_TESTLIB_LIB -DQT_CORE_LIB -DQT_TESTCASE_BUILDDIR="\\"C:/Users/Kiran Lonikar/projects/qgroundcontrol/{args.build}\\""'
	incPath = f'-I".." -I. -I{qtLibPath}include -I{qtLibPath}include/QtLocation -I{qtLibPath}include/QtQuick3D -I{gstreamerPath}include -I{gstreamerPath}include/gstreamer-1.0 -I{gstreamerPath}include/glib-2.0 -I{gstreamerPath}lib/glib-2.0/include -I{gstreamerPath}lib/gstreamer-1.0/include -I"../libs/msinttypes" -I"../libs/mavlink/include/mavlink/v2.0" -I"../libs/mavlink/include/mavlink/v2.0/all" -I"../libs/eigen" -I"../libs/libevents" -I"../libs/libevents/libevents/libs/cpp" -Ilibs/libevents/libs/cpp/parse -I"../libs/shapelib" -I"../libs/zlib/windows/include" -I"../libs/xz-embedded/userspace" -I"../libs/xz-embedded/linux/include/linux" -I"../libs" -I"../libs/qmdnsengine/src/include" -I"../libs/qmdnsengine/src/src" -I"../libs/sdl2/msvc/include" -I"../libs/OpenSSL/Windows/x64/include" -I".." -Iinclude/ui -I"../src" -I"../src/ADSB" -I"../src/api" -I"../src/AnalyzeView" -I"../src/Camera" -I"../src/Compression" -I"../src/AutoPilotPlugins" -I"../src/FlightDisplay" -I"../src/FlightMap" -I"../src/FlightMap/Widgets" -I"../src/FollowMe" -I"../src/Geo" -I"../src/GPS" -I"../src/Joystick" -I"../src/PlanView" -I"../src/MissionManager" -I"../src/PositionManager" -I"../src/QmlControls" -I"../src/QtLocationPlugin" -I"../src/QtLocationPlugin/QMLControl" -I"../src/Settings" -I"../src/Terrain" -I"../src/Vehicle" -I"../src/Audio" -I"../src/comm" -Isrc/input -Isrc/lib/qmapcontrol -I"../src/uas" -I"../src/ui" -Isrc/ui/linechart -Isrc/ui/map -Isrc/ui/mapdisplay -Isrc/ui/mission -Isrc/ui/px4_configuration -I"../src/ui/toolbar" -Isrc/ui/uas -I"../src/AutoPilotPlugins/Common" -I"../src/FirmwarePlugin" -I"../src/VehicleSetup" -I"../src/AutoPilotPlugins/APM" -I"../src/FirmwarePlugin/APM" -I"../src/AutoPilotPlugins/PX4" -I"../src/FirmwarePlugin/PX4" -I"../src/FactSystem" -I"../src/FactSystem/FactControls" -I"../src/VideoManager" -I"../src/VideoReceiver" -I"../src/Utilities" -I"../src/Vehicle/LibEvents" -I"../src/Vehicle/Actuators" -I"../src/AirLink" -I"../src/Viewer3D" -I"../src/GPS/Drivers/src" -I{qtLibPath}include/QtLocation/6.6.1 -I{qtLibPath}include/QtLocation/6.6.1/QtLocation -I{qtLibPath}include/QtPositioningQuick/6.6.1 -I{qtLibPath}include/QtPositioningQuick/6.6.1/QtPositioningQuick -I{qtLibPath}include/QtPositioningQuick -I{qtLibPath}include/QtQuickShapes -I{qtLibPath}include/QtQuickShapes/6.6.1 -I{qtLibPath}include/QtQuickShapes/6.6.1/QtQuickShapes -I{qtLibPath}include/QtQuick/6.6.1 -I{qtLibPath}include/QtQuick/6.6.1/QtQuick -I{qtLibPath}include/QtQuickControls2 -I{qtLibPath}include/QtQuickWidgets -I{qtLibPath}include/QtQuick -I{qtLibPath}include/QtCharts -I{qtLibPath}include/QtOpenGLWidgets -I{qtLibPath}include/QtOpenGL -I{qtLibPath}include/QtGui/6.6.1 -I{qtLibPath}include/QtGui/6.6.1/QtGui -I{qtLibPath}include/QtWidgets -I{qtLibPath}include/QtSvg -I{qtLibPath}include/QtTextToSpeech -I{qtLibPath}include/QtMultimedia -I{qtLibPath}include/QtGui -I{qtLibPath}include/QtConcurrent -I{qtLibPath}include/QtPositioning/6.6.1 -I{qtLibPath}include/QtPositioning/6.6.1/QtPositioning -I{qtLibPath}include/QtPositioning -I{qtLibPath}include/QtQmlModels/6.6.1 -I{qtLibPath}include/QtQmlModels/6.6.1/QtQmlModels -I{qtLibPath}include/QtQmlModels -I{qtLibPath}include/QtQml/6.6.1 -I{qtLibPath}include/QtQml/6.6.1/QtQml -I{qtLibPath}include/QtQml -I{qtLibPath}include/QtQmlIntegration -I{qtLibPath}include/QtNetwork -I{qtLibPath}include/QtCore/6.6.1 -I{qtLibPath}include/QtCore/6.6.1/QtCore -I{qtLibPath}include/QtSql -I{qtLibPath}include/QtXml -I{qtLibPath}include/QtCore5Compat -I{qtLibPath}include/QtSerialPort -I{qtLibPath}include/QtTest -I{qtLibPath}include/QtCore -I. -I/include -I{qtLibPath}mkspecs/win32-msvc'
	cppCompilationCmd = f'cl -c -FIsrc/stable_headers.h -Yusrc/stable_headers.h -FpQGroundControl_pch.pch {cxxFlags} {incPath} -Fo @'
	cCompilationCmd = f'cl -c {cFlags} {incPath} -Fo @'

	os.makedirs(args.build, exist_ok=True)
	os.chdir(args.build)
	print(f'Current directory now {os.getcwd()}')
	os.system('qmake ../') # This invokes qmake on Qt 5.15 and not 6.6.x as python conda shell changes Qt settings
	os.system('nmake') # This results in linker error

	ignoreDirs = ['.github', '.git', 'gst', 'qgcunittest', 'eigen', 'gst-plugins-good', 
				  'nlohmann_json', 'tests', 'examples', 'UTMSP']
	ignoreFiles = ['MockLink.cc', 'BluetoothLink.cc', 'MockLinkMissionItemHandler.cc', 
				   'FactSystemTestBase.cc', 'FactSystemTestGeneric.cc',
				   'FactSystemTestPX4.cc', 'MockLinkFTP.cc',
				   'PairingManager.cc', 'QtNFC.cc',
				   'TransectStyleComplexItemTestBase.cc', 'QGCPluginHost.cc',
				   'aes.cpp', 'xz_dec_syms.c',
				   'TestBrowser.cpp', 'qserialport_android.cpp',
				   'qserialportinfo_android.cpp', 'csv2shp.c', 'decompress_unxz.c', 'xz_dec_test.c',
				   'qserialport.cpp', 'MobileScreenMgr.cc',
				   #'GStreamer.cc', 'GstVideoReceiver.cc', 'gstqgc.c', 'gstqgcvideosinkbin.c', 
				  ]
	ignorePatterns = [r'.*Test\..*', r'.*Android\..*']
	subfolders = []
	for srcDir in ['../src', '../libs']:
		subfolders.append(srcDir)
		subfolders.extend(fast_scandir(srcDir, ignoreDirs))
	print(f'subfolders: {subfolders}')
	for dirName in subfolders:
		compileAllSources(dirName, cppCompilationCmd, cCompilationCmd, ignoreFiles, ignorePatterns)

	os.system('nmake') # The linker error gets resolved here

