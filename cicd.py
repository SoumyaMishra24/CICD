from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_codebuild as codebuild

class MyCDKStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "MyVpc", cidr="10.0.0.0/16")

        # Jenkins EC2 instance
        jenkins_instance = ec2.Instance(self, "JenkinsInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc
        )

        # SonarQube EC2 instance
        sonarqube_instance = ec2.Instance(self, "SonarQubeInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc
        )

        # AWS CodeBuild project
        codebuild_project = codebuild.Project(self, "MyCodeBuildProject",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yaml")
        )

        # Add environment variables to the CodeBuild project
        codebuild_project.add_environment_variable(
            key="CODEBUILD_INITIATOR",
            value="jenkins",
            type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
        )
        codebuild_project.add_environment_variable(
            key="CODEBUILD_INITIATOR",
            value="sonarqube",
            type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
        )

app = core.App()
MyCDKStack(app, "MyCDKStack")
app.synth()

