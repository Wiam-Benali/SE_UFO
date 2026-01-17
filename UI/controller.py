import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._model.get_all_years()
        for anno in self._model.years:
            self._view.dd_year.options.append(ft.dropdown.Option(key=anno, text=anno))

        self._model.get_all_shapes()
        for shape in self._model.shapes:
            self._view.dd_shape.options.append(ft.dropdown.Option(key=shape, text=shape))

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        try:
            year = int(self._view.dd_year.value)
            shape = str(self._view.dd_shape.value)
        except ValueError:
            self._view.show_alert('Devi inserire un valore in entrambe le tendine')
        self._model.build_graph(year,shape)
        nodi = len(self._model.G.nodes())
        archi = len(self._model.G.edges())
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero di vertici: {nodi}, Numero di archi: {archi}'))

        pesi_adiacenti = self._model.pesi_adiacenti()
        for nodo in pesi_adiacenti:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Nodo: {nodo}, somma pesi su archi {pesi_adiacenti[nodo]}'))

        self._view.update()
    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        cammino,d,peso = self._model.ricerca_percorso_max()

        for (i,arco) in enumerate(cammino):
            id1 = arco[0].id
            id2 = arco[1].id
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Peso cammino massimo {sum(d)}'))
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'{id1} -> {id2} weight: {peso[i]} distance: {d[i]} '))
        self._view.update()
