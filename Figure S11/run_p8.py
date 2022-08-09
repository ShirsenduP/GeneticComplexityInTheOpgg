"""
Standalone script to run a basic setup of the GOPGAR simulations with all default values.
"""

from gopgar import Configuration, Population
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Launch a simulation with a single parameter name and value."
    )
    parser.add_argument("index", help="Job index", type=int)
    parser.add_argument("beta", help="Reputation assignment error.", type=float)
    parser.add_argument("norm", help="Social norm.", type=str)
    args = parser.parse_args()

    config = Configuration(
        N=100,
        n=5,
        t=2e5,
        p=8,
        c=1,
        r=3,
        sigma=1,
        social_norm=args.norm.strip(),
        omega=10 / 11,
        epsilon1=0.1,
        epsilon2=1.0,
        zeta=0.1,
        alpha=0,
        beta=args.beta
    )

    config.export(args.index)
    
    print(config, end="\n\n")
    P = Population(config=config)
    P.modify(use_tqdm_bar=True, batch_size=50000, job_id=args.index)
    print(P.get_settings())
    P.simulate()

    P.export_chromosomes()
