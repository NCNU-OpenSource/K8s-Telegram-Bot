local ksm = import 'kube-state-metrics/kube-state-metrics.libsonnet';
local version = std.extVar('version');

ksm {
  name:: 'kube-state-metrics',
  namespace:: 'kube-system',
  version:: version,
  image:: 'registry.k8s.io/kube-state-metrics/kube-state-metrics:v' + version,
}
