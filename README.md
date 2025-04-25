导入 cx_Freeze 模块，用于将 Python 脚本打包成可执行文件
import cx_Freeze

execf=[cx_Freeze.Executable("surface2.py")]

cx_Freeze.setup(
    name="Jerk off",
    配置打包选项
    options={"build_exe":
    配置 build_exe 子选项
    {"packages":["pygame"],"include_files":
        [r'D:\Python\打飞机\image\fei.png',
         r'D:\Python\打飞机\image\cai.png',
         r'D:\Python\打飞机\image\caibu.jpg',
         r'D:\Python\打飞机\music\haha.mp3',
         r'D:\Python\打飞机\music\及.mp3',
         r'D:\Python\打飞机\music\起床了.mp3']}},

    executables=execf
)

