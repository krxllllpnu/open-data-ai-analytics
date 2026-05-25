#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
USER_HOME="${HOME:-/root}"
KUBECONFIG="${KUBECONFIG:-$USER_HOME/.kube/config}"
export KUBECONFIG

echo "Using kubeconfig: $KUBECONFIG"
echo "Installing or updating Argo CD..."
echo "Creating or verifying Argo CD namespace..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
echo "Applying Argo CD manifests with server-side apply..."
kubectl apply --server-side -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "Waiting for Argo CD deployments..."
kubectl -n argocd rollout status deployment/argocd-server --timeout=300s
kubectl -n argocd rollout status deployment/argocd-repo-server --timeout=300s
kubectl -n argocd rollout status deployment/argocd-applicationset-controller --timeout=300s
kubectl -n argocd rollout status statefulset/argocd-application-controller --timeout=300s

APPLICATION_FILE="${PROJECT_DIR}/gitops/argocd/application.yaml"
if [ -f "$APPLICATION_FILE" ]; then
  echo "Applying Argo CD Application from ${APPLICATION_FILE}..."
  kubectl apply -f "$APPLICATION_FILE"
  echo "Argo CD Application applied successfully."
else
  echo "Argo CD Application file not found at ${APPLICATION_FILE}."
  echo "Manual step: run kubectl apply -f gitops/argocd/application.yaml after cloning the repository."
fi
