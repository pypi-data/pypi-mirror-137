
import generate


if __name__ == "__main__":

    generate.rate_laws(kinetics=['mass_action', 'loguniform', ['kf', 'kr', 'kc', 'deg'], [[0.01, 100], [0.01, 100], [0.01, 100], [0.01, 100]]])

