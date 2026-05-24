# Changelog

## v0.5.0

Monitoring and observability lab release.

- Added a Prometheus and Grafana monitoring stack under `monitoring`.
- Added a separate Docker Compose file for monitoring services: Prometheus, Grafana, Node Exporter, and cAdvisor.
- Configured Prometheus to scrape metrics from Prometheus, Node Exporter, and cAdvisor.
- Added Grafana provisioning for the Prometheus data source.
- Added Azure Network Security Group rules for Grafana on port `3000` and Prometheus on port `9090`.
- Updated cloud-init automation to start the monitoring stack on VM provisioning.
- Added VM and container monitoring dashboards in Grafana for CPU, memory, disk usage, running containers, and active Prometheus targets.
- Updated README with monitoring startup, access, and verification instructions.

## v0.4.0

Azure Terraform deployment lab release.

- Added Terraform configuration under `infra/terraform` for Azure infrastructure provisioning.
- Added Azure resources for the deployment: resource group, virtual network, subnet, public IP, network security group, network interface, and Linux virtual machine.
- Configured cloud-init to install Docker, clone the GitHub repository, and start the project with Docker Compose.
- Updated deployment defaults for Azure for Students: `swedencentral` region and `Standard_B2s_v2` VM size.
- Configured the deployment to use the existing `compose.yaml` file and expose the web interface on port `8080`.
- Added Terraform outputs for `public_ip`, `web_url`, and `ssh_command`.
- Updated `.gitignore` rules for Terraform state, plans, lock files, and provider cache directories.
- Updated README with Azure Cloud Shell, Terraform apply, verification, and destroy instructions.

## v0.3.0

Docker containerization lab release.

- Added Dockerfiles for data loading, data quality analysis, data research, visualization, and web services.
- Added `compose.yaml` for running the full project with Docker Compose.
- Configured shared volumes for data, database, reports, and plots.
- Added SQLite database support for storing imported dataset records.
- Updated data quality analysis and data research modules to generate JSON reports.
- Added Flask web dashboard for viewing reports and generated plots.
- Added `.env.example` with Docker-related environment variables.
- Updated `.gitignore` for generated database, report, and plot artifacts.
- Updated README with Docker Compose run instructions and lab documentation.

## v0.2.0

CI/CD lab release.

- Added GitHub Actions CI workflow in `.github/workflows/ci.yml`.
- Configured CI triggers for `push`, `pull_request`, and manual `workflow_dispatch`.
- Added matrix-based execution for existing project scripts.
- Added artifact upload for generated reports, logs, and figures.
- Added self-hosted runner workflow in `.github/workflows/ci-selfhosted.yml`.
- Tested CI execution on both GitHub-hosted and self-hosted runners.
- Updated visualization script to use `matplotlib`.
- Updated `requirements.txt` with required Python dependencies.

## v0.1.0

Initial university Git/GitHub lab release.

- Initialized repository structure and `.gitignore`.
- Added project README with open data source and research questions.
- Added data loading script for the Iris open dataset.
- Added data quality analysis script.
- Added research analysis script.
- Practiced GitHub Pull Request merges for analysis branches.
- Created and resolved a README merge conflict.
- Added visualization script that generates two SVG charts.