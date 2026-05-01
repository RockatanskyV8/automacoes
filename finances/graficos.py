import matplotlib.pyplot as plt

class Barras():
    def __init__(self, dataframe, eixo_x, eixo_y, Titulo):
        self.dataframe = dataframe
        self.x = eixo_x
        self.y = eixo_y
        self.Titulo = Titulo
        
        plt.figure(figsize=(10, 6))

    def grafico(self):
        # Criar lista de cores baseada nos valores
        cores = ['blue' if valor >= 0 else 'red' for valor in self.dataframe[self.y]]
        bars = plt.bar(self.dataframe[self.x], self.dataframe[self.y], color=cores, edgecolor='black', alpha=0.8)
    
        # Adicionar valores em cima das barras (opcional)
        for bar in bars:
            height = bar.get_height()
            va = 'bottom' if height >= 0 else 'top'  # Posicionamento do texto
            color = 'darkblue' if height >= 0 else 'darkred'
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va=va, fontweight='bold', color=color)

        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()


    def plots(self):
        plt.title(self.Titulo, fontsize=12, fontweight='bold')
        plt.xlabel(self.x, fontsize=12)
        plt.ylabel(self.y, fontsize=12)
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.show()


class Linhas():
    def __init__(self, dataframe, x, y, Titulo):
        self.dataframe = dataframe
        self.x = x
        self.y = y
        self.Titulo = Titulo

        plt.figure(figsize=(10, 6))
    
    def grafico(self):
        # Paleta de cores para positivos e negativos
        cores_positivas = ['blue', 'green', 'teal', 'navy', 'darkblue']
        cores_negativas = ['red', 'orange', 'coral', 'darkred', 'maroon']
    
        for i, y in enumerate(self.y):
            if self.dataframe[y].max() > 0 :
                cor = cores_positivas[i % len(cores_positivas)]
            else:
                cor = cores_negativas[i % len(cores_negativas)]
    
            plt.plot(self.dataframe[self.x], self.dataframe[y], 'b-', linewidth=2, label=y, color=cor)

    def plots(self):
        plt.title(self.Titulo, fontsize=14, fontweight='bold')
        plt.xlabel(self.x, fontsize=12)
        plt.ylabel(self.y, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


# top=0.938,
# bottom=0.111,
# left=0.095,
# right=0.985,
# hspace=0.2,
# wspace=0.2
