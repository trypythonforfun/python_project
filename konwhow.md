
##### pygal.i18n
在《Python编程：从入门到实践》书中的一个项目用到pygal.i18n获取国别码，然而，现在pygal已经没有i18n模块，
要改用pygal_maps_world.i18n，解决方法如下：

在终端中运行下面语句（注意pip3/pip）
pip3 install pygal_maps_world

在代码文件中添加下面语句：
from pygal_maps_world.i18n import COUNTRIES

##### pygal.Worldmap()报错
语句相应地更改模块名称：
import pygal.maps.world
wm = pygal.maps.world.World()
