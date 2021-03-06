import functools
import json
import random
import operator

random.seed(0)
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=False, type=int, default=0)
    ap.add_argument("--end", required=False, type=int, default=64)
    ap.add_argument("--gpus", required=False, type=int, default=2)
    args = vars(ap.parse_args())
    val_options = {
        "lr": [0.001],
        "seed": [0],
        "epoch_num": [200],
        "dropout": [0, 0.1],
        "n_head": [2, 4, 6], #, 8],
        "proj_dim_a": [20, 40],
        "proj_dim_v": [20, 40, 80],
        "conv_dims": [[40, 40], [10, 10], [20, 20],
                      [8, 20, 10], [10, 5, 10], [10, 10, 5], [10, 5], [20, 20, 10], [10, 5, 10], [2], [5, 10]],
        # [20, 50, 50, 20], [10, 20, 40, 80, 40, 20, 10],

        "ff_dim_final": [128, 256, 320, 512],

        "n_layers": [6, 7, 8],

        "dim_total_proj": [512, 800, 1024],
        "gru_lr": [0.001]  # , 0.0001, 0.00001],
    }
    option_lens = [len(options) for options in val_options.values()]
    num_comb = functools.reduce(operator.mul, option_lens, 1)
    start = int(args["start"])
    end = int(args["end"])
    gpus = int(args["gpus"])
    for i, id in enumerate(random.sample(range(num_comb), end)[start:end]):
        cuda = i % gpus
        file_name = '../configs/' + 'conf_b0_cuda%d_%d.json' % (cuda, i + start)
        new_config = {'cuda': cuda}
        for key, options in val_options.items():
            choice = id % len(options)
            new_config[key] = options[choice]
            id //= len(options)
        with open(file_name, 'w') as outfile:
            json.dump(new_config, outfile)
