import docker
from prometheus_client import start_http_server, Gauge
import time

# Connexion au client Docker
client = docker.from_env()

# Définir les métriques Prometheus
cpu_usage = Gauge('docker_container_cpu_usage', 'CPU usage of Docker containers', ['container_name'])
memory_usage = Gauge('docker_container_memory_usage', 'Memory usage of Docker containers (in bytes)', ['container_name'])
network_rx = Gauge('docker_container_network_rx', 'Network received (in bytes)', ['container_name'])
network_tx = Gauge('docker_container_network_tx', 'Network transmitted (in bytes)', ['container_name'])

def collect_metrics():
    for container in client.containers.list():
        try:
            stats = container.stats(stream=False)
            name = container.name
            
            # Extraire les métriques CPU
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
            num_cpus = len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', []))
            cpu_percent = (cpu_delta / system_delta) * num_cpus if system_delta > 0 else 0
            cpu_usage.labels(container_name=name).set(cpu_percent)

            # Extraire les métriques mémoire
            memory_usage.labels(container_name=name).set(stats['memory_stats']['usage'])

            # Extraire les métriques réseau
            network_stats = stats['networks']
            total_rx = sum(interface['rx_bytes'] for interface in network_stats.values())
            total_tx = sum(interface['tx_bytes'] for interface in network_stats.values())
            network_rx.labels(container_name=name).set(total_rx)
            network_tx.labels(container_name=name).set(total_tx)

        except Exception as e:
            print(f"Error while collecting metrics for the container {container.name}: {e}")

if __name__ == "__main__":
    # Démarrer le serveur HTTP Prometheus sur le port 9417
    start_http_server(9417)
    print("vm_docker_exporter start listening on 9417/tcp")

    while True:
        collect_metrics()
        time.sleep(10)  # Collecte toutes les 10 secondes