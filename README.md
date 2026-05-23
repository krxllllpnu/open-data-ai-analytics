# Open Data AI Analytics

This repository contains a small university Git/GitHub lab project for working with open data, Python analysis scripts, branches, pull requests, merge conflicts, and release tagging.

The analytical purpose of the project is to explore the classic Iris flower dataset and use simple data analysis techniques to understand how flower measurements differ between species.

## Open Data Source

Dataset: [Iris Species CSV from the public seaborn-data repository](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv)

The dataset contains sepal and petal measurements for three Iris species: setosa, versicolor, and virginica.

## Research Questions and Hypotheses

1. Virginica is expected to have the largest average petal length and petal width.
2. The dataset is expected to have no missing values and very few duplicate records.
3. How strongly are petal length and petal width related across all observations?

## CI/CD Pipeline

This project uses GitHub Actions for a simple Python CI/CD lab pipeline.

The main workflow is defined in `.github/workflows/ci.yml`. It runs on pushes to `main`, pull requests targeting `main`, and manual `workflow_dispatch` runs. The workflow uses `ubuntu-latest`, installs dependencies from `requirements.txt`, and runs a matrix mapped to the existing project scripts:

- `data_load/app.py`
- `data_quality_analysis/app.py`
- `data_research/app.py`
- `visualization/app.py`

The source dataset for the Docker lab is stored in `data/dataset.csv`. The data loading module imports it into SQLite at `db/project.db`. Reports are saved in `reports/`, charts are saved in `plots/`, and the `artifacts/` directory is used by GitHub Actions for CI logs and copied final outputs uploaded with `actions/upload-artifact`.

To run the workflow manually, open the repository on GitHub, go to **Actions**, select **CI**, and click **Run workflow**.

Produced artifacts include:

- CI log files for each matrix module
- copied processed outputs, reports, and plots

The self-hosted runner workflow is defined in `.github/workflows/ci-selfhosted.yml`. It runs only manually and is intended to demonstrate how the same project can be executed on a configured self-hosted GitHub Actions runner. It runs `data_load/app.py` and `data_quality_analysis/app.py`, then uploads logs and generated reports as artifacts.

## Docker Images and Containers

This lab containerizes the project as a small multi-service analytics system. Docker Compose builds and runs separate containers for data loading, data quality analysis, data research, visualization, and a Flask web interface.

## Docker Services

- `data_load` reads `data/dataset.csv`, creates `db/project.db`, imports the dataset into SQLite, and writes `reports/data_load_report.json`.
- `data_quality_analysis` reads SQLite data, checks missing values, duplicates, numeric values, and species values, then writes `reports/data_quality_report.json`.
- `data_research` reads SQLite data, calculates descriptive statistics and correlation, then writes `reports/data_research_report.json`.
- `visualization` reads SQLite data, creates two matplotlib PNG charts, and writes `reports/visualization_report.json`.
- `web` runs a Flask dashboard that displays reports and generated charts.

## Running with Docker Compose

Run the full project from the repository root:

```powershell
docker compose up --build
```

Open the web interface:

```text
http://localhost:8080
```

The web service uses port `8080` by default. You can copy `.env.example` to `.env` and change `WEB_PORT` if needed.

Generated files are stored in:

- SQLite database: `db/project.db`
- JSON reports: `reports/*.json`
- PNG plots: `plots/*.png`

Useful checks:

```powershell
docker compose config
docker compose ps
docker compose down
```

## Azure Deployment with Terraform

This project can also be deployed to Azure with Terraform from Azure Cloud Shell. Terraform creates the Azure infrastructure, and cloud-init prepares the VM by installing Docker, cloning the GitHub repository, and starting the Docker Compose project with `compose.yaml`.

Terraform creates:

- resource group
- virtual network and subnet
- public IP address
- network security group
- network interface
- Linux virtual machine

Default project values:

- region: `swedencentral`
- VM size: `Standard_B2s_v2`
- app port: `8080`
- compose file: `compose.yaml`

### Open Azure Cloud Shell

1. Open the Azure Portal.
2. Click the Cloud Shell icon.
3. Choose **Bash**.
4. Select subscription (**Azure for Students** for example).
5. Use ephemeral Cloud Shell if persistent storage is not required.

### Apply Infrastructure

Go to the Terraform directory:

```bash
cd infra/terraform
```

Initialize, format, and validate Terraform:

```bash
terraform init
terraform fmt
terraform validate
```

Generate an SSH key if needed:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

Apply the infrastructure:

```bash
terraform apply -var="ssh_public_key_path=$HOME/.ssh/id_rsa.pub"
```

Confirm the apply step with `yes`.

### Check the Deployment

Use Terraform outputs to find:

- `public_ip`
- `web_url`
- `ssh_command`

Open `web_url` in a browser. You can also check the web service from Cloud Shell:

```bash
curl http://<PUBLIC_IP>:8080
```

Optionally SSH into the VM:

```bash
ssh azureuser@<PUBLIC_IP>
```

Check Docker containers on the VM:

```bash
sudo docker ps
cd /opt/app/project
sudo docker compose -f compose.yaml ps
```

### Destroy Infrastructure

To remove the Azure resources, go back to the Terraform directory:

```bash
cd infra/terraform
terraform destroy -var="ssh_public_key_path=$HOME/.ssh/id_rsa.pub"
```

Confirm with `yes`. Destroying the infrastructure is important to avoid consuming Azure credits.
