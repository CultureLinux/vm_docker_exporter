# ya_docker_exporter

<p align="center">
  <img src="https://github.com/CultureLinux/vm_docker_exporter/blob/main/images/vm_docker_exporter.png" alt="gh-otify"/>
</p>

## Description 

This project provides a **Docker exporter** for **VictoriaMetrics** and **Prometheus**, allowing real-time collection of metrics related to Docker container resource usage, including **CPU**, **memory**, and **network** usage. These metrics are exposed over an HTTP port to be scraped by Prometheus, providing deep visibility into the state of your Docker containers.

## Features

- **CPU Usage**: Collects CPU usage per Docker container.
- **Memory Usage**: Monitors memory usage of Docker containers.
- **Network Usage**: Monitors network input and output per Docker container.
- **Prometheus Support**: Exposes metrics in a format compatible with VictoriaMetrics / Prometheus.

## Prerequisites

- **Docker**: Docker must be installed and running.
- **Prometheus**: To collect and store the metrics.
- **Python 3.x**: The exporter script is written in Python 3.
- **pip**: Python package manager.

## Install
    git clone https://github.com/CultureLinux/vm_docker_exporter.git
    cd ya_docker_exporter
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Systemctl


    cat <<EOF >> /etc/systemd/system/vm_docker_exporter.service
    [Unit]
    Description=Docker Exporter for VictoriaMetrics / Prometheus
    After=network.target

    [Service]
    Type=simple
    ExecStart=/home/docky/vm_docker_exporter/venv/bin/python /home/docky/vm_docker_exporter/main.py
    Restart=always
    User=docky
    Group=docky
    WorkingDirectory=/usr/local/bin

    [Install]
    WantedBy=multi-user.target
    EOF

    systemctl daemon-reload
    systemctl enable vm_docker_exporter --now
    systemctl status vm_docker_exporter
    
## Access 
    http://localhost:9417

## VictoriaMetrics/Prometheus
    scrape_configs:
    - job_name: 'docker_exporter'
        static_configs:
        - targets: ['<votre_ip>:9417']

## Grafana dashboard

You can import a prebuild dashboard with the file `grafana_dashboard.json`