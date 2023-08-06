import itertools
import pandas as pd
import faker
from .deployment import providers
from dataclasses import dataclass


@dataclass
class Deployment_level:
    name: str
    num_items: int
    level_type: faker.providers.BaseProvider


class deployment_generator:
    def __init__(self):
        """Creates a deployment factory"""
        self.faker = faker.Faker("en_US")

        self.faker.add_provider(providers.LocationProvider)

        self.configuration: list = list()
        self.temp_location_configuration: dict = dict()

    def generate_deployment(self, configuration: dict = dict()) -> pd.DataFrame:
        """Generates a deployment

        Parameters
        ----------
        configuration : list, optional
            A deployment configuration, if not provided assumes `self.add_levels()` was used
            beforehand to create a levels configuration

        Returns
        -------
        pd.DataFrame
            Generated deployment
        """

        # Gather deployment configurations
        deployment_configuration = self._get_or_create_configuration(configuration)

        # Populate levels with data
        tmp_generation = self._add_column_to_sample([], deployment_configuration.copy())
        columns = self._extract_columns_from_configuration(deployment_configuration)

        # Create deployment DF
        df = pd.DataFrame(data=tmp_generation, columns=columns)

        if not self.temp_location_configuration:
            return df
        else:
            return self._add_location_to_df(df)

    def get_faker(self):
        """Returns the currently configured faker instance"""
        return self.faker

    def add_location(self, location_level: str, location_bounds: dict):
        """Add a location parameter to the deployment (as the last level)

        Parameters
        ----------
        location_level : str
            The deployment level to add the location to
        location_bounds : dict
            The box bounds of the location, as a dict containing the `nw` (north-west)
            and the `se` (south-east) boundary points.
        """
        self.temp_location_configuration = {
            "level": location_level,
            "nw": location_bounds["nw"],
            "se": location_bounds["se"],
        }

    def _get_or_create_configuration(self, configuration: dict = dict()) -> dict:
        # Do we need to create levels from ad-hoc configuration?
        if configuration:
            # Need to parse the current configuration and add the levels accordingly
            deployment_configuration = self._get_deployment_config(configuration)

            # Create levels according to configuration
            for level, level_configs in deployment_configuration.items():
                devices_to_generate = level_configs.get("num_items", 1)
                level_type = level_configs.get("faker", "msisdn")
                self.add_level(
                    level,
                    number=devices_to_generate,
                    level_type=getattr(self.faker, level_type),
                )
        deployment_configuration = self.configuration
        return deployment_configuration

    @staticmethod
    def _get_deployment_config(config: dict) -> dict:
        """Returns the  static data part from the config.
        if there is no `static` entry in the provided config
        it will assume the entire provided config is a static data config
        config.

        Parameters
        ----------
        config : dict
            A static data configuration, or a configuration containing `static` entry
            for a static data featuers configuration

        Returns
        -------
        dict
            static data features configuration
        """
        return config.get("static", config)

    @staticmethod
    def _get_deployment_config(config: dict) -> dict:
        """Returns the  deployment part from the config.
        if there is no `deployment` entry in the provided config
        it will assume the entire provided config is a deployment
        config.

        Parameters
        ----------
        config : dict
            A Deployment configuration, or a configuration containing `deployment` entry
            for a deployment configuration

        Returns
        -------
        dict
            deployment configuration
        """
        return config.get("deployment", config)

    def _add_location_to_df(self, df: pd.DataFrame):
        level = self._get_location_level()
        bounding_box = self._get_location_bounding_box()
        unique_level_values = df[level].unique()
        locations = {
            current_value: str(self.faker.location(bounding_box))
            for current_value in unique_level_values
        }
        df["location"] = df[level].apply(lambda val: locations[val])
        return df

    def _get_location_level(self):
        return self.temp_location_configuration["level"]

    def _get_location_bounding_box(self):
        return {
            "nw": self.temp_location_configuration["nw"],
            "se": self.temp_location_configuration["se"],
        }

    def add_level(self, name: str, number: int, level_type):
        """Adds a deployment level to the deployment generator.
        Deployment levels allows us to have hierarchy such as:
        Data Center -> Device,
        For each level, `number` of instances will be created.

        So for a 2 data_centers, 2 devices deployment, 4 devices will be
        created, 2 devices in each of the 2 data centers.

        Parameters
        ----------
        name : str
            Level name
        number : int
            Number of instances to create (This `number` will be created for
            each instance of the previous levels)
        level_type : str
            Name of the faker generator to be used for generating the
            level's instances
        """
        self.configuration.append(Deployment_level(name, number, level_type))

    def _add_config_name(self, name: str):
        return 0

    def _add_config_number(self, num: int):
        return 0

    def _is_data_generation_needed(self, level_tuple: tuple):
        if type(level_tuple[1]) == int:
            return True
        return False

    def _extract_columns_from_configuration(self, configuration: list):
        return list(map(lambda levels: levels.name, configuration))

    def _add_column_to_sample(self, current: list, left: list):
        """Generates the data for each column as defined in the list

        Parameters
        ----------
        current : list
            [description]
        left : list
            [description]

        Returns
        -------
        [type]
            [description]
        """
        current_level: Deployment_level = left.pop(0)
        current_generator = current_level.level_type
        num_possibilities_to_generate = current_level.num_items
        to_append = [
            current_generator().replace(",", "_").replace(" ", "_")
            for _ in range(num_possibilities_to_generate)
        ]
        if not left:
            generated = [[*current, elem] for elem in to_append]
            return generated

        generated = [
            self._add_column_to_sample([*current, elem], left.copy())
            for elem in to_append
        ]
        return list(itertools.chain.from_iterable(generated))
