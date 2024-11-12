from visualisation import ChessBoardGUI

tabla = []
for i in range(0, 8):
    red = []
    for j in range(0, 8):
        red.append(0)
    tabla.append(red)

for red in tabla:
    print(red)
print('\n')

for i in range(0, len(tabla)):
    for j in range(0, len(tabla)):
        if i == j:
            tabla[j][i] = 1
        
for red in tabla:
    print(red)
    
if __name__ == "__main__":

    gui = ChessBoardGUI()
    gui.mainloop()