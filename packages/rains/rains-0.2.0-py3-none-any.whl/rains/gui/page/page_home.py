import PySimpleGUI as Sg


def page_home_show():
    """

    """

    layout = [
        [Sg.Text('创建项目模板')],
        [Sg.Text('存放路径 :'), Sg.Input(), Sg.FolderBrowse('选择', size=(10, 0))],
        [Sg.Text('项目命名 :'), Sg.Input()],
        [Sg.Text('')],
        [Sg.Button('创建项目', size=(150, 0))]
    ]

    window = Sg.Window('Rains Project Handler - v 0.0.1', layout, size=(500, 150))

    return window
