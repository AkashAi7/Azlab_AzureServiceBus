# Azure Service Bus and AKS Lab

This lab script allows you to set up a lab environment for testing Azure Service Bus integration with Azure Kubernetes Service (AKS). You can perform various tasks such as creating a Service Bus namespace, creating an AKS cluster, sending messages to a Service Bus queue manually, and deploying a cronjob in AKS to send messages automatically.

## Requirements

- Python 3.x
- Azure CLI (installed and logged in)
- Azure subscription with the necessary permissions

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your_username/azure-service-bus-aks-lab.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script `main.py`:

    ```bash
    python main.py
    ```

2. Follow the on-screen instructions to perform various actions such as setting up the lab environment, sending messages manually, deploying a cronjob in AKS, etc.

## Functions

- **Setup Lab Environment**: Sets up the lab environment by creating a resource group, AKS cluster, and Azure Service Bus namespace.
- **Get Azure Service Bus Connection URI**: Retrieves the connection URI for the Azure Service Bus namespace.
- **Send Message Manually**: Manually sends a message to the Azure Service Bus queue.
- **Send Message through AKS Cronjob**: Deploys a cronjob in AKS to send messages automatically at scheduled intervals.
- **Teardown Lab Setup**: Deletes the entire lab setup from the Azure subscription.

## Configuration

Make sure to configure the necessary variables such as `resource_group`, `cluster_name`, `location`, etc., within the script before running it.
