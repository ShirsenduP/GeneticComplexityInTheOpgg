"""
Standalone script to run a basic setup of the GOPGAR simulations with all default values.
"""

from gopgar import Configuration, Population
from argparse import ArgumentParser
import logging

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = ArgumentParser(
        description="Launch a simulation with a single parameter name and value."
    )
    parser.add_argument("index", help="Job index", type=int)
    parser.add_argument(
        "zeta",
        help="Proportion of the population to replace each timestep.",
        type=float,
    )
    parser.add_argument("norm", help="The social norm of the population", type=str)
    args = parser.parse_args()

    config = Configuration(
        N=100,
        n=5,
        t=2e5,
        p=8,
        c=1,
        r=3,
        sigma=1,
        social_norm=args.norm,
        omega=10 / 11,
        epsilon1=0.1,
        epsilon2=1.0,
        zeta=args.zeta,
    )

    P = Population(config=config)
    P.modify(batch_size=50000, job_id=args.index)
    P.simulate()
