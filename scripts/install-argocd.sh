#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"
export KUBECONFIG

echo "Installing or updating Argo CD..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
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
