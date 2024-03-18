import os
import subprocess
import json
import yaml
import time
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import subprocess

def setup():
    """Setup the lab environment."""
    # Azure login and set subscription
    # subscription_id = az_login()
    # az_set_subscription(subscription_id)

    # AKS cluster details
    global resource_group, cluster_name, location
    resource_group = "myResourceGroup"
    cluster_name = "myAKSCluster"
    location = "eastus"

    # Azure Service Bus details
    global sb_namespace, sb_queue
    sb_namespace = "samplenamespaceakstest" + str(os.environ.get("RAND"))
    sb_queue = "samplequeueaks"
    create_resource_group(resource_group, location)

        # Create AKS Cluster
    print("creating cluster  ")
    create_aks_cluster(resource_group, cluster_name, location)

        # Connect to the AKS Cluster
    connect_to_aks_cluster(resource_group, cluster_name)

    """" resource groups exist, create if not
    if not check_resource_exists(resource_group, cluster_name):
        create_resource_group(resource_group, location)

        # Create AKS Cluster
        print("creating cluster  ")
        create_aks_cluster(resource_group, cluster_name, location)

        # Connect to the AKS Cluster
        connect_to_aks_cluster(resource_group, cluster_name)

    """

    # Create Azure Service Bus namespace and queue
    create_service_bus_namespace(resource_group, sb_namespace, location)
    create_service_bus_queue(resource_group, sb_namespace, sb_queue)

    # Retrieve Azure Service Bus connection string
    global conn_str 
    conn_str = retrieve_service_bus_connection_string(resource_group, sb_namespace)

    print("Setup complete!")

def create_aks_cluster(resource_group, cluster_name, location):
    print(f"Creating AKS Cluster '{cluster_name}'...")
    os.system(f"az aks create --resource-group {resource_group} --name {cluster_name} --location {location} --enable-managed-identity --node-count 1 --generate-ssh-keys")

def connect_to_aks_cluster(resource_group, cluster_name):
    print(f"Connecting to AKS Cluster '{cluster_name}'...")
    # Example command to connect to AKS cluster
    subprocess.run(f"az aks get-credentials --resource-group {resource_group} --name {cluster_name}", shell=True)

# Other functions remain unchanged


def test_connection():
    """Test the AKS cluster and Azure Service Bus connection."""
    print("Testing AKS cluster and Azure Service Bus connection...")
    # Add your testing code here

def teardown():
    """Delete the entire lab setup from the Azure subscription."""
    print(f"Deleting AKS Cluster '{cluster_name}'...")
    os.system(f"az aks delete --resource-group {resource_group} --name {cluster_name} --yes")
    
    print(f"Deleting Service Bus Queue '{sb_queue}'...")
    os.system(f"az servicebus queue delete --resource-group {resource_group} --namespace-name {sb_namespace} --name {sb_queue}")
    
    print(f"Deleting Service Bus Namespace '{sb_namespace}'...")
    os.system(f"az servicebus namespace delete --resource-group {resource_group} --name {sb_namespace} --yes")
    
    print(f"Deleting resource group '{resource_group}'...")
    os.system(f"az group delete --name {resource_group} --yes")
    print("Deleting lab setup...")
    # Add your teardown code here
    

def az_login():
    print("Logging into Azure CLI...")
    subprocess.run("az login", shell=True)
    # Retrieve subscription ID after login
    subscription_id = subprocess.check_output("az account show --query id -o tsv", shell=True, text=True).strip()
    print(f"Logged in to subscription: {subscription_id}")
    return subscription_id

def az_set_subscription(subscription_id):
    print(f"Setting subscription to {subscription_id}...")
    subprocess.run(f"az account set --subscription {subscription_id}", shell=True)

def check_resource_exists(resource_group, resource_name):
    print(f"Checking if resource {resource_name} exists...")
    try:
        subprocess.run(f"az resource show --resource-group {resource_group} --name {resource_name} --resource-type Microsoft.Resources/resourceGroups", shell=True, check=True)
        print(f"Resource {resource_name} already exists.")
        return True
    except subprocess.CalledProcessError:
        print(f"Resource {resource_name} does not exist.")
        return False

def create_resource_group(resource_group, location):
    print(f"Creating resource group {resource_group}...")
    subprocess.run(f"az group create --name {resource_group} --location {location}", shell=True)

def create_service_bus_namespace(resource_group, namespace_name, location):
    print("Creating Azure Service Bus namespace...")
    subprocess.run(f"az servicebus namespace create -n {namespace_name} -g {resource_group} -l {location}", shell=True)

def create_service_bus_queue(resource_group, namespace_name, queue_name):
    print("Creating Azure Service Bus queue...")
    subprocess.run(f"az servicebus queue create -n {queue_name} -g {resource_group} --namespace-name {namespace_name} -g {resource_group}", shell=True)

def retrieve_service_bus_connection_string(resource_group, namespace_name):
    print("Retrieving Azure Service Bus connection string...")
    conn_str_cmd = f"az servicebus namespace authorization-rule keys list --namespace-name {namespace_name} --resource-group {resource_group} --name RootManageSharedAccessKey"
    conn_str_output = subprocess.check_output(conn_str_cmd, shell=True)
    conn_str_json = json.loads(conn_str_output)
    print(conn_str_json)
    return conn_str_json["primaryConnectionString"]


def send_messages_to_queue():
    # Create a ServiceBusClient object
    # conn_str="Endpoint=sb://sb-store-demo-none.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=jIGQ1ycyqhka7qQPsXuQXv0tgZn/hIIEm+ASbLu0B7g=""
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=conn_str)

    sender = servicebus_client.get_queue_sender(queue_name=sb_queue)

            # Create a message
    message = ServiceBusMessage("Hello from AKS test session!")

            # Send the message
    sender.send_messages(message)
    print("Message sent successfully!")

            # Close the sender
    sender.close()

            # Wait for 1 second before sending the next message
    time.sleep(1)

    # Close the ServiceBusClient
    servicebus_client.close()





def update():
    """
    Update the SERVICE_BUS_CONNECTION_STRING variable in the specified YAML file.

    Args:
    - yaml_file (str): Path to the YAML file.
    - new_connection_string (str): New value for SERVICE_BUS_CONNECTION_STRING.
    """
    yaml_file = r".\cronjob.yaml"
    # conn_str="Endpoint=sb://sb-store-demo-none.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=jIGQ1ycyqhka7qQPsXuQXv0tgZn/hIIEm+ASbLu0B7g="
    new_connection_string = conn_str
     # Load the YAML content
    print("inside the update ")
    with open(yaml_file, 'r') as file:
        yaml_content = yaml.safe_load(file)

    # Update the value of SERVICE_BUS_CONNECTION_STRING
    yaml_content["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["env"][0]["value"] = new_connection_string
    # Write the updated YAML content back to the file
    with open(yaml_file, 'w') as file:
        yaml.dump(yaml_content, file)
    print("YAML file updated successfully")

    # Apply the YAML configuration using kubectl
    subprocess.run(f"kubectl apply -f {yaml_file} --validate=false", shell=True)

    yaml_file = r".\configmap.yaml"
    subprocess.run(f"kubectl apply -f {yaml_file} --validate=false", shell=True)

def getconnectionstr():
    print(conn_str)


def main():
    while True:
        print("Select an action:")
        print("1. Setup lab environment")
        print("2. Get Azure Service Bus connection uri ")
        print("3. Send message manually ")
        print("4. Send message through cronjob deployed in AKS  ")
        print("5. Teardown lab setup")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            setup()
        elif choice == "2":
            getconnectionstr()
        elif choice == "3":
            send_messages_to_queue()
        elif choice == "4":
            update()
        elif choice == "5":
            teardown()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
