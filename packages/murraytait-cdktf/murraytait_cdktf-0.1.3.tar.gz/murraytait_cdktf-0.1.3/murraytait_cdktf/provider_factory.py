from cdktf_cdktf_provider_aws import AwsProvider, AwsProviderAssumeRole

from .config import Config


class ProviderFactory():
    def __init__(self, stack, config: Config, aws_role_arn, aws_profile):
        self._stack = stack
        self._config = config

        self._profile = None
        self._assume_role = None
        if config.use_role_arn:
            self._assume_role = AwsProviderAssumeRole(
                stack, role_arn=aws_role_arn)
        else:
            self._profile = aws_profile

    def build(self, aws_region, id="aws", alias=None, profile=None):
        if not profile:
            profile = self._profile

        return AwsProvider(
            self._stack, id=id, region=aws_region, profile=profile, assume_role=self._assume_role, alias=alias
        )
