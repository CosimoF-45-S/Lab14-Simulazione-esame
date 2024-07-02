import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        result = self._model.creaGrafo1()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {result[0]}, Numero di archi: {result[1]}"))
        self._view.txt_result.controls.append(ft.Text(f"Arco a peso minimo: {result[2]}, Arco a peso massimo: {result[3]}"))
        self._view.update_page()


    def handle_countedges(self, e):
        soglia = int(self._view.txt_name.value)
        result = self._model.handle_count(soglia)
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi a peso minore di soglia:"
                f" {result[0]}, Numero di archi a peso maggiore di soglia: {result[1]}"))
        self._view.update_page()


    def handle_search(self, e):
        soglia = int(self._view.txt_name.value)
        result = self._model.handlepath(soglia)
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Peso totale del cammino toccato: {result[0]}"))
        for s in result[1]:
            self._view.txt_result3.controls.append(ft.Text(s))
        self._view.update_page()
