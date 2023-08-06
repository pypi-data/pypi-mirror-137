from metrics_gen.deployment_generator import deployment_generator
import yaml


class TestDeployment:
    metrics_configuration: dict = yaml.safe_load(
        open(
            "./tests/test_configuration.yaml",
            "r",
        )
    )
    deployment_configuration: dict = metrics_configuration.get("deployment", {})

    @staticmethod
    def _get_deployment(configuration: dict = metrics_configuration):
        dep_gen = deployment_generator()
        deployment = dep_gen.generate_deployment(configuration=configuration)
        return deployment

    def test_deploy_with_add_levels(self):
        dep_gen = deployment_generator()
        faker = dep_gen.get_faker()

        for level, level_configs in self.deployment_configuration.items():
            devices_to_generate = level_configs.get("num_items", 1)
            level_type = level_configs.get("faker", "msisdn")
            dep_gen.add_level(
                level,
                number=devices_to_generate,
                level_type=getattr(faker, level_type),
            )
        deployment = dep_gen.generate_deployment()
        assert (deployment is not None, "Deployment should have values")

    def test_deploy_with_configuration_file(self):
        deployment = self._get_deployment()
        assert (deployment is not None, "Deployment should have values")

    def test_deploy_with_dep_configuration_only(self):
        deployment = self._get_deployment(self.deployment_configuration)
        assert (deployment is not None, "Deployment should have values")

    def test_deployment_get_faker(self):
        deployment = deployment_generator()
        faker = deployment.get_faker()

        assert (faker, "Faker not created")

    def test_all_columns_are_created(self):
        deployment = self._get_deployment()
        generated_levels = deployment.shape[1]

        num_levels = len(self.deployment_configuration.keys())
        assert (
            generated_levels == num_levels,
            f"Only {generated_levels} were created although {num_levels} were specified",
        )

    def test_number_of_generated_devices(self):
        deployment = self._get_deployment()
        generated_devices = deployment.shape[0]

        num_devices = 1
        for _, level_configs in self.deployment_configuration.items():
            num_devices = num_devices * level_configs.get("num_items", 1)
        assert (
            generated_devices == num_devices,
            f"Not enough devices created, {num_devices} should have been created while only {generated_devices} devices were created",
        )
