### Setting up terraform-aws connection (WSL2)

1.  Configure AWS CLI with Your Credentials:\
Once AWS CLI is installed, configure it with your AWS credentials. These credentials should correspond to an IAM user with the necessary permissions for the Redshift Data API.
Run the following command:

```cmd
aws configure
```
You'll be prompted to enter:\
• AWS Access Key ID\
• AWS Secret Access Key\
• Default region name\
• Default output format (can be left blank)

2. Set Up Terraform to Use AWS Credentials:\
Using Environment Variables:\
Airflow can use AWS credentials set as environment variables.\
Set these in your shell:

```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=your_aws_region
```

Add these lines to your .bashrc, .bash_profile, or .zshrc file to make the configuration persistent across terminal sessions.

