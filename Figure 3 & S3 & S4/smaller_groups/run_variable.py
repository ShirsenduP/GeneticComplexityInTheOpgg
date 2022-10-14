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
    parser.add_argument("n", help="Group size", type=int)
    parser.add_argument("p", help="Behavioural strategy complexity", type=int)
    parser.add_argument("norm", help="Social norm", type=str)
    args = parser.parse_args()

    config = Configuration(
        N=int(args.n * 20),
        n=args.n,
        t=2e5,
        p=args.p,
        c=1,
        r=3,
        sigma=1,
        social_norm=args.norm.strip(),
        omega=10 / 11,
        epsilon1=0.1,
        epsilon2=1.0,
        zeta=0.1,
    )

    P = Population(config=config)
    P.modify(job_id=args.index, batch_size=50000)
    P.simulate(nofitness=True, nodistribution=True, nochromosomes=True)
