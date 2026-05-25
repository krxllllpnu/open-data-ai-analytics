#!/usr/bin/env bash
set -euo pipefail

echo "Installing or verifying k3s..."

if ! command -v k3s >/dev/null 2>&1; then
  curl -sfL https://get.k3s.io | sh -
else
  echo "k3s is already installed."
fi

sudo systemctl enable k3s
sudo systemctl start k3s

USER_HOME="${HOME:-/root}"

echo "Preparing kubeconfig..."
mkdir -p "$USER_HOME/.kube"
sudo cp /etc/rancher/k3s/k3s.yaml "$USER_HOME/.kube/config"
sudo chown "$(id -u):$(id -g)" "$USER_HOME/.kube/config"
chmod 600 "$USER_HOME/.kube/config"
export KUBECONFIG="$USER_HOME/.kube/config"

echo "Waiting for k3s node to become Ready..."
for attempt in $(seq 1 30); do
  if kubectl get nodes >/dev/null 2>&1 && kubectl wait --for=condition=Ready node --all --timeout=20s; then
    echo "k3s node is Ready."
    exit 0
  fi
  echo "k3s is not ready yet. Attempt ${attempt}/30..."
  sleep 10
done

echo "k3s node did not become Ready in time."
kubectl get nodes || true
exit 1
