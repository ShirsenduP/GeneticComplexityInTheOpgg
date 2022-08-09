from numpy import linspace
from argparse import ArgumentParser
from os import getcwd

NORMS = ["Defector", "Loner", "Neither", "Both"]

if __name__ == "__main__":

    parser = ArgumentParser(
        description="Command line app to generate a parameter file for a number of simulations."
    )
    parser.add_argument(
        "experiment", help="Experiment identifier (e.g. A, B, etc.)", type=str
    )
    parser.add_argument(
        "variable", help="Name of variable to examine (e.g. 'r')", type=str
    )
    parser.add_argument(
        "repeat",
        help="Number of times a single parameterisation is repeated (e.g. 20)",
        type=int,
    )
    parser.add_argument(
        "--min-value",
        help="Minimum value of variable to examine (e.g. 1)",
        type=float or int,
        default=None,
    )
    parser.add_argument(
        "--max-value",
        help="Maximum value of variable to examine (e.g. 4.5)",
        type=float or int,
        default=None,
    )
    parser.add_argument(
        "--interval",
        help="Size of interval between consecutive values (e.g. 0.1)",
        type=float or int,
        default=None,
    )
    parser.add_argument(
        "--norms",
        help="Flag to iterate through each social norm",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--directory",
        help="Path to output directory (Defaults to current working directory)",
        type=str,
        default=getcwd(),
    )
    parser.add_argument(
        "--dry-run", help="Output to screen instead of file", action="store_true"
    )
    args = parser.parse_args()

    experiment_name = args.experiment
    variable = args.variable
    number_of_steps = (
        None
        if args.variable == "norm"
        else int((args.max_value - args.min_value) / args.interval + 1)
    )
    values = (
        NORMS
        if args.variable == "norm"
        else linspace(args.min_value, args.max_value, number_of_steps)
    )
    parameter_list_as_string = ""

    index = 1
    if args.norms:
        for _ in range(args.repeat):
            for value in values:
                for norm in NORMS:
                    parameter_list_as_string += f"{index:04d} {round(value, 8)} {norm}\n"
                    index += 1
    else:
        for _ in range(args.repeat):
            for value in values:
                parameter_list_as_string += f"{index:04d} {round(value, 8)}\n"
                index += 1

    if args.variable == "norm":
        print(
            f"Generated {len(values)} job parameters over the norms={NORMS} with {args.repeat} runs each."
        )
    else:
        print(
            f"Generated {len(values)} job parameters "
            f"for {variable} in [{args.min_value:.1f},{args.max_value:.1f}] "
            f"in increments of {args.interval:.2f} with {args.repeat} runs."
        )

    if args.dry_run:
        print(parameter_list_as_string)
    else:
        filename = f"{args.directory}/scripts/{experiment_name}_parameters.txt"
        with open(filename, "w") as f:
            f.write(parameter_list_as_string)
        print(f"Exported to {filename}")
