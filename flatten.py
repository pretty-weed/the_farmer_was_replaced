from __builtins__ import Callable, get_pos_z, get_world_size
from movement import weave
from tasks import do_dig

base_max_z = get_world_size() * -100
base_min_z = -base_max_z
max_z = base_max_z
min_z = base_min_z
def measure(x, y):
    global max_z
    global min_z
    z = get_pos_z()
    max_z = max(z, max_z)
    min_z = min(z, min_z)


def do_dig_cond():
    return  get_pos_z() >= max_z

def main():
    flatten()

def flatten(continue_scrape: bool | Callable[[int,], bool] = True):
    companions = []
    
    global max_z
    global min_z
    iteration = 1
    while True:
        iteration += 1
        if max_z != min_z:
            max_z = base_max_z
            min_z = base_min_z

            weave([
                (1.0, [], measure),
            ], False)

            print("max z is "+ str(max_z) + "\nmin z is " + str(min_z))
            weave(
                [
                    (1.0, [do_dig_cond], do_dig)
                ]
            )
        elif continue_scrape == False:
            break
        elif continue_scrape == True or continue_scrape(iteration):
            weave(
                [(1.0, [], do_dig)]
            )
        else:
            break
            

if __name__ == "__main__":
    main()