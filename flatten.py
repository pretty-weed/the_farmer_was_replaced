from __builtins__ import Callable, dig, get_pos_z
from movement import go_to, weave
from tasks import do_dig

heightmap = {}
def measure(x, y):
    global heightmap
    z = get_pos_z()
    if not z in heightmap:
        heightmap[z] = []
    heightmap[z].append((x, y))


def main(cont=True):
    flatten(cont)

def flatten(continue_scrape: bool | Callable[[int,], bool] = True):
    companions = []
    
    global heightmap
    iteration = -1
    while True:
        iteration += 1
        if len(heightmap) > 1 or iteration == 0:
            heightmap = {}
            weave([
                (1.0, [], measure),
            ], False)

            while len(heightmap) > 1:
                this_z = max(heightmap)
                here = heightmap[this_z].pop()
                go_to(here)
                if not heightmap[this_z]:
                    heightmap.pop(this_z)
                dig()
                if this_z -1 not in heightmap:
                    heightmap[this_z-1] = [here]
                else:
                    heightmap[this_z-1].append(here)
        elif continue_scrape == False:
            break
        elif continue_scrape == True or continue_scrape(iteration):
            weave(
                [(1.0, [], do_dig)]
            )
        else:
            break
            

if __name__ == "__main__":
    layers = 1
    def do_n(i):
        return i <= layers
    main(do_n)