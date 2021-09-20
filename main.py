# https://github.com/facebook/prophet/issues/1691
# https://blog.amedama.jp/entry/kivy-matplotlib

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
import numpy as np
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

kv_def = '''
<RootWidget>:
    orientation: 'vertical'

    Label:
        text: 'The following is a graph of Matplotlib'
        size_hint_y: 0.2

    GraphView:

<GraphView>:
'''
Builder.load_string(kv_def)

class GraphView(BoxLayout):
    """MatplotLibのグラフを表示するためのウィジェット"""

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # 初期化に用いるデータ
        x = np.linspace(-np.pi, np.pi, 100)
        y = np.sin(x)

        # 描画状態を保存するためのカウンタ
        self.counter = 0

        # Figure, Axisを保存しておく
        self.fig, self.ax = plt.subplots()
        # 最初に描画したときのLineも保存しておく
        self.line,  = self.ax.plot(x, y)

        # ウィジェットとしてグラフを追加する
        widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(widget)

        # 1秒ごとに表示を更新するタイマーを仕掛ける
        Clock.schedule_interval(self.update_view, 0.01)

    def update_view(self, *args, **kwargs):
        # データを更新する
        self.counter += np.pi/100 # 10分のpiずらす
        # ずらした値を使ってデータを作る
        x = np.linspace(-np.pi+self.counter, np.pi+self.counter, 100)
        y = np.sin(x)
        # lineにデータを設定する
        self.line.set_data(x, y)
        # グラフの見栄えを調整する
        self.ax.relim()
        self.ax.autoscale_view()
        # 再描画する
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

class RootWidget(BoxLayout):
    """子を追加していくためのウィジェットを用意しておく"""


class GraphApp(App):
    """Matplotlibのグラフを表示するアプリケーション"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = 'Matplotlib graph on kivy'

    def build(self):
        return RootWidget()

def main():
    # アプリケーションを開始する
    app = GraphApp()
    app.run()

if __name__ == '__main__':
    main()



