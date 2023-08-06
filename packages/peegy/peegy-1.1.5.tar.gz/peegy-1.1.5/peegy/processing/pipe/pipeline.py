from peegy.processing.pipe.definitions import InputOutputProcess
import matplotlib.pyplot as plt
import os
import graphviz
import PIL as pil
import pydot
import tempfile
from PyQt5.QtCore import QLibraryInfo
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class PipeItem:
    def __init__(self, name='', process: InputOutputProcess = None):
        self.name = name
        self.process = process
        self.process.name = name
        self.ready = False
        self.figure_handle = None


class PipePool(list):
    """This class manages InputOutputProcess appended to it.
    When InputOutputProcess are appended, to the PipePool, they can be called by calling the run function of the
    PipePool. If an element has been already run, this won't be called again.
    """

    def __init__(self):
        super(PipePool, self).__init__()

    def append(self, item: object, name=None):
        if name is None:
            name = type(item).__name__
        super(PipePool, self).append(PipeItem(**{'name': name,
                                                 'process': item}))

    def __getitem__(self, key):
        return super(PipePool, self).__getitem__(key)

    def get_process(self, value):
        out = None
        for _i, _item in enumerate(self):
            if _item.name == value:
                out = _item.process
                break
        return out

    def run(self):
        for _pipe_item in self:
            if _pipe_item.ready:
                continue
            _pipe_item.process.run()
            _pipe_item.ready = True

    def diagram(self,
                file_name: str = '',
                return_figure=False,
                dpi=300,
                ):
        """
        This function generates a flow diagram with the available connections in the pipeline
        :param file_name: string indicating the file name to save pipeline diagram
        :param return_figure: boolean indicating if figure should be returned

        """
        _file, file_extension = os.path.splitext(file_name)
        _temp_file = tempfile.mkdtemp() + os.sep + 'diagram'
        gviz = graphviz.Digraph("Pipeline",
                                filename=_temp_file,
                                node_attr={'color': 'lightblue2', 'style': 'filled'},
                                format=file_extension.replace('.', ''))
        gviz.attr(rankdir='TB', size='7,14')
        items = list(self)
        for _idx_1 in list(range(len(self))):
            _current_list = []
            _assigned = False
            for _idx_2 in list(range(len(self))):
                if _idx_1 == _idx_2:
                    continue
                if items[_idx_1].process is not None and items[_idx_2].process is not None:
                    if items[_idx_1].process == items[_idx_2].process.input_process:
                        _current_list.append(items[_idx_2].name)
                        gviz.edge(items[_idx_1].name, items[_idx_2].name)
                        _assigned = True
            if not _assigned:
                gviz.node(items[_idx_1].name)
        gviz.render(_file)
        # use numpy to construct an array from the bytes
        gviz.save(_temp_file)
        (graph,) = pydot.graph_from_dot_file(_temp_file)
        graph.write_png(_temp_file + '.png', prog=['dot', '-Gdpi={:}'.format(dpi)])
        fig_out = None

        if return_figure:
            img = pil.Image.open(_temp_file + '.png')
            fig_out = plt.figure()
            ax = fig_out.add_subplot(111)
            ax.imshow(img, aspect=1)
            ax.axis('off')
            fig_out.tight_layout()
        return fig_out
