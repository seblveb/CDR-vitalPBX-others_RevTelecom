# native
from math import ceil, log

#imported
from matplotlib import pyplot as plt

# Retourne la puissance de 2 la plus proche pour que le graph soit bien alligné
def power_log(x):
    return 2**(ceil(log(x, 2)))

def make_graph(title, horodating, data_daily, data_total, save_path):

    # Crée un subplot pour pouvoir instancier deux mesures sur l'axe Y
    fig, ax1 = plt.subplots(figsize=((len(data_daily) / 5) + 10, 12))
    plt.title(title)

    # Premier label vertical | axe Y
    color = '#ff5b0c'
    ax1.bar(horodating, data_daily, color=color, width=0.5)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylabel('Consommation par heure (Mo)', color=color)
    # Etabli la hauteur maximale de l'échelle
    ax1.set_ylim(top=2000)
    # Ajoute une grille sur l'axe horizontal
    ax1.grid(axis='x')

    # Label horizontal | axe X
    ax1.set_xlabel('Horodatage')
    ax1.set_xticks(horodating)
    ax1.set_xticklabels(horodating, rotation=90)

    # Instantie un deuxième graph partageant le même axe X
    ax2 = ax1.twinx()

    # Second label vertical | axe Y
    color = '#0097ff'
    coeff = power_log(data_total[-1]/ 2000) * 2000
    ax2.set_ylim(top=coeff if coeff >= 2000 else 2000)
    ax2.set_ylabel('Consommation totale (Mo)', color=color)  # we already handled the x-label with ax1
    ax2.plot(horodating, data_total, color=color, linewidth=1)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(axis='y')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig("{}/{}".format(save_path, title))
    plt.close()
