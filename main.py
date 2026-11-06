from movement import weave
from tasks import do_harvest, do_plant, do_replace_rotten

DURT_ME = False

def main():
    companions = []
    while True:
        weave([
            (1.0, [], do_harvest),
            (1.0, [], do_plant),
            (1.0, [], do_replace_rotten),
#			(0.5, [not_on_border, ], do_observe),
        ])
            


if __name__ == "__main__":
    main()