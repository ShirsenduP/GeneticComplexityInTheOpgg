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
        "omega", help="Likelihood of further rounds in a single timestep.", type=float
    )
    parser.add_argument("norm", help="The social norm of the population", type=str)
    args = parser.parse_args()

    config = Configuration(
        N=100,
        n=5,
        t=2e5,
        p=2,
        c=1,
        r=3,
        sigma=1,
        social_norm=args.norm.strip(),
        omega=args.omega,
        epsilon1=0.1,
        epsilon2=1.0,
        zeta=0.1,
    )

    P = Population(config=config)
    P.modify(batch_size=50000, job_id=args.index)
    P.simulate(nochromosomes=True, nodistribution=True, nofitness=True)
